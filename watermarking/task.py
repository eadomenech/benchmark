# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

import uuid

from celery import shared_task
from .models import *

from subprocess import Popen, PIPE
import subprocess

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def mainTask():
    media = "media/"
    list_dir = [
        'media/watermarked_images/', 'media/noised_images/',
        'media/watermarks_with_noise/', 'media/source_codes/']
    for i in list_dir:
        try:
            os.stat(i)
        except:
            logger.info('Creating %s' % (i))
            os.mkdir(i)
    for cover in CoverImage.objects.all():
        cover_types = ImageType.objects.filter(coverimage=cover)
        for watermark in WatermarkImage.objects.all():
            watermark_types = ImageType.objects.filter(watermarkimage=watermark)
            for watermarking in Watermarking.objects.filter(
                    cover_type__in=cover_types,
                    watermark_type__in=watermark_types):
                if not SprintWatermarking.objects.filter(
                        watermarking=watermarking.id, cover_image=cover,
                        watermark=watermark).exists():
                    try:
                        s = SprintWatermarking.objects.create(
                            watermarking=watermarking, cover_image=cover,
                            watermark=watermark)
                        logger.info('Creating SprintWatermarking: %s' % (s))
                        # subprocess
                        ext = str(cover.cover_image).split('.')[-1]
                        filename = "%s.%s" % (uuid.uuid4(), ext)
                        watermarked_image = 'watermarked_images/'+filename
                        process = subprocess.Popen(
                            [
                                "python", media + str(watermarking.source_code),
                                "-i", media + str(cover.cover_image),
                                "-w", media + str(watermark.watermark_image),
                                "-o", media + watermarked_image],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE
                        )
                        (stdout, stderr) = process.communicate()
                        if process.returncode == 0:
                            s.watermarked_image = watermarked_image
                            s.save()
                            logger.info(
                                'Updating watermarked_image of SprintWatermarking: %s' % (s.watermarked_image))
                        else:
                            logger.error('Error: %s' % (stderr))
                    except IntegrityError:
                        pass
                sprint = get_object_or_404(
                    SprintWatermarking, watermarking=watermarking.id,
                    cover_image=cover, watermark=watermark)
                # Aplicando los distintos tipos de ruidos
                for noise in Noise.objects.all():
                    if not NoiseSprintWatermarking.objects.filter(
                            noise=noise, sprintWatermarking=sprint).exists():
                        if sprint.watermarked_image:
                            try:
                                n = NoiseSprintWatermarking.objects.create(
                                    noise=noise, sprintWatermarking=sprint)
                                logger.info(
                                    'Creating NoiseSprintWatermarking: %s' % (n))
                                # subprocess
                                ext = str(cover.cover_image).split('.')[-1]
                                filename = "%s.%s" % (uuid.uuid4(), ext)
                                noised_image = 'noised_images/'+filename
                                process = subprocess.Popen(
                                    [
                                        "python", media + str(noise.source_code),
                                        "-i", media + str(sprint.watermarked_image),
                                        "-o", media + noised_image],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                                )
                                (stdout, stderr) = process.communicate()
                                if process.returncode == 0:
                                    n.watermarked_image_with_noise = noised_image
                                    n.save()
                                    logger.info(
                                        'Updating watermarked_image_with_noise of NoiseSprintWatermarking(%s): %s' % (n, n.watermarked_image_with_noise))
                                else:
                                    logger.error('Error: %s' % (stderr))

                                ext = str(
                                    n.sprintWatermarking.watermark.watermark_image
                                ).split('.')[-1]
                                filename = "%s.%s" % (uuid.uuid4(), ext)
                                watermark_with_noise = 'watermarks_with_noise/'+filename
                                process = subprocess.Popen(
                                    [
                                        "python", media + str(n.sprintWatermarking.watermarking.extract_code),
                                        "-i", media + str(n.watermarked_image_with_noise),
                                        "-w", media + str(n.sprintWatermarking.watermark.watermark_image),
                                        "-o", media + watermark_with_noise],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                                )
                                (stdout, stderr) = process.communicate()
                                if process.returncode == 0:
                                    n.watermark_image_with_noise = watermark_with_noise
                                    n.save()
                                    logger.info(
                                        'Updating watermark_image_with_noise of NoiseSprintWatermarking(%s): %s' % (n, n.watermark_image_with_noise))
                                else:
                                    logger.error('Error: %s' % (stderr))
                            except IntegrityError:
                                pass
                # Calculando metricas a las watermarked images
                for metric in Metric.objects.filter(
                        metric_type='1', image_type__in=cover_types):
                    if not MetricSprintWatermarking.objects.filter(
                            metric=metric, sprintWatermarking=sprint).exists():
                        if sprint.watermarked_image:
                            try:
                                me = MetricSprintWatermarking.objects.create(
                                    metric=metric, sprintWatermarking=sprint)
                                logger.info(
                                    'Creating MetricSprintWatermarking: %s' % (me))
                                # subprocess
                                process = subprocess.Popen(
                                    [
                                        "python", media + str(metric.source_code),
                                        "-i", media + str(sprint.cover_image.cover_image),
                                        "-w", media + str(sprint.watermarked_image)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                                )
                                (stdout, stderr) = process.communicate()
                                if process.returncode == 0:
                                    me.value = float(stdout)
                                    me.save()
                                    logger.info(
                                        'Updating value of MetricSprintWatermarking(%s): %s' % (me, me.value))
                                else:
                                    logger.error('Error: %s' % (stderr))
                            except:
                                pass

    # Calculando metricas a las watermark images
    for noiseSprint in NoiseSprintWatermarking.objects.all():
        for metric in Metric.objects.filter(
                metric_type='2', image_type__in=watermark_types):
            if noiseSprint.watermarked_image_with_noise and noiseSprint.watermark_image_with_noise:
                if not MetricNoiseSprintWatermarking.objects.filter(
                        metric=metric,
                        noiseSprintWatermarking=noiseSprint).exists():
                    try:
                        m = MetricNoiseSprintWatermarking.objects.create(
                            metric=metric, noiseSprintWatermarking=noiseSprint)
                        # subprocess
                        process = subprocess.Popen(
                            [
                                "python", media + str(metric.source_code),
                                "-i", media + str(noiseSprint.sprintWatermarking.watermark.watermark_image),
                                "-w", media + str(noiseSprint.watermark_image_with_noise)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE
                        )
                        (stdout, stderr) = process.communicate()
                        if process.returncode == 0:
                            m.value = float(stdout)
                            m.save()
                            logger.info(
                                'Updating value of MetricNoiseSprintWatermarking(%s): %s' % (m, m.value))
                        else:
                            logger.error('Error: %s' % (stderr))
                    except IntegrityError:
                        pass
    return 'Success!'
