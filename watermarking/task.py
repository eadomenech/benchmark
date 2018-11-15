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


@shared_task
def mainTask():
    list_dir = [
        'media/watermarked_images/', 'media/noised_images/',
        'media/watermarks_with_noise/']
    for i in list_dir:
        try:
            os.stat(i)
        except:
            os.mkdir(i)
    for cover in CoverImage.objects.all():
        for watermark in WatermarkImage.objects.all():
            for watermarking in Watermarking.objects.all():
                if not SprintWatermarking.objects.filter(
                        watermarking=watermarking.id, cover_image=cover,
                        watermark=watermark).exists():
                    try:
                        s = SprintWatermarking.objects.create(
                            watermarking=watermarking, cover_image=cover,
                            watermark=watermark)
                        # subprocess
                        ext = str(cover.cover_image).split('.')[-1]
                        filename = "%s.%s" % (uuid.uuid4(), ext)
                        watermarked_image = 'watermarked_images/'+filename
                        subprocess.call(
                            [
                                'python media/' + str(watermarking.source_code) +
                                ' -i media/' + str(cover.cover_image) +
                                ' -w media/' + str(watermark.watermark_image) +
                                ' -o media/' + watermarked_image],
                            shell=True
                        )
                        s.watermarked_image = watermarked_image
                        s.save()
                    except IntegrityError:
                        pass
                sprint = get_object_or_404(
                    SprintWatermarking, watermarking=watermarking.id,
                    cover_image=cover, watermark=watermark)
                # Aplicando los distintos tipos de ruidos
                for noise in Noise.objects.all():
                    if not NoiseSprintWatermarking.objects.filter(
                            noise=noise, sprintWatermarking=sprint).exists():
                        try:
                            n = NoiseSprintWatermarking.objects.create(
                                noise=noise, sprintWatermarking=sprint)
                            # subprocess
                            ext = str(cover.cover_image).split('.')[-1]
                            filename = "%s.%s" % (uuid.uuid4(), ext)
                            noised_image = 'noised_images/'+filename
                            subprocess.call(
                                [
                                    'python media/' + str(noise.source_code) +
                                    ' -i media/' + str(sprint.watermarked_image) +
                                    ' -o media/' + noised_image],
                                shell=True
                            )
                            n.watermarked_image_with_noise = noised_image
                            n.save()
                        except IntegrityError:
                            pass
                # Calculando metricas a las watermarked images
                for metric in Metric.objects.filter(metric_type='1'):
                    if not MetricSprintWatermarking.objects.filter(
                            metric=metric, sprintWatermarking=sprint).exists():
                        try:
                            me = MetricSprintWatermarking.objects.create(
                                metric=metric, sprintWatermarking=sprint)
                            # subprocess
                            p = subprocess.run(
                                [
                                    'python media/' + str(metric.source_code) +
                                    ' -i media/' + str(sprint.cover_image.cover_image) +
                                    ' -w media/' + str(sprint.watermarked_image)],
                                stdout=subprocess.PIPE, shell=True
                            )
                            me.value = float(p.stdout)
                            me.save()
                        except:
                            pass

    # Calculando metricas a las watermark images
    for noiseSprint in NoiseSprintWatermarking.objects.all():
        for metric in Metric.objects.filter(metric_type='2'):
            if not MetricNoiseSprintWatermarking.objects.filter(
                    metric=metric,
                    noiseSprintWatermarking=noiseSprint).exists():
                try:
                    m = MetricNoiseSprintWatermarking.objects.create(
                        metric=metric, noiseSprintWatermarking=noiseSprint)
                    # subprocess
                    ext = str(
                        noiseSprint.sprintWatermarking.watermark.watermark_image
                    ).split('.')[-1]
                    filename = "%s.%s" % (uuid.uuid4(), ext)
                    watermark_with_noise = 'watermarks_with_noise/'+filename
                    subprocess.run(
                        [
                            'python media/' + str(noiseSprint.sprintWatermarking.watermarking.extract_code) +
                            ' -i media/' + str(
                                noiseSprint.watermarked_image_with_noise) +
                            ' -w media/' + str(
                                noiseSprint.sprintWatermarking.watermark.watermark_image) +
                            ' -o media/' + watermark_with_noise],
                        shell=True
                    )
                    p = subprocess.run(
                        [
                            'python media/' + str(metric.source_code) +
                            ' -i media/' + str(
                                noiseSprint.sprintWatermarking.watermark.watermark_image) +
                            ' -w media/' + watermark_with_noise],
                        stdout=subprocess.PIPE, shell=True
                    )
                    m.value = float(p.stdout)
                    m.save()
                except IntegrityError:
                    pass
    return 'Success!'
