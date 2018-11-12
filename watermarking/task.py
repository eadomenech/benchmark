# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
from django.conf import settings
from django.shortcuts import get_object_or_404

import uuid

from celery import shared_task
from .models import *

from subprocess import Popen, PIPE
import subprocess


@shared_task
def mainTask():
    list_dir = ['media/watermarked_images/', 'media/noised_images/']
    for i in list_dir:
        try:
            os.stat(i)
        except:
            os.mkdir(i)
    for cover in CoverImage.objects.all():
        for watermark in WatermarkImage.objects.all():
            for watermarking in Watermarking.objects.all():
                if not SprintWatermarking.objects.filter(
                        watermarking=watermarking.id, coverImage=cover,
                        watermark=watermark).exists():
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
                    SprintWatermarking.objects.create(
                        watermarking=watermarking, coverImage=cover,
                        watermark=watermark,
                        watermarked_image=watermarked_image
                    )
                    # process = Popen(
                    #     [
                    #         'python', 'media/'+str(
                    #             watermarking.source_code),
                    #         '-i', 'media/'+str(cover.cover_image),
                    #         '-w', 'media/'+str(
                    #             watermark.watermark_image),
                    #         '-o', watermarked_image],
                    #     shell=True, stdout=PIPE, stderr=PIPE
                    # )
                    # stdout, stderr = process.communicate()
                    # if stderr:
                    #     for line in stderr.strip().split("\n"):
                    #         print(line)
                    # else:
                    #     sprint = SprintWatermarking.objects.create(
                    #         watermarking=watermarking, coverImage=cover,
                    #         watermark=watermark
                    #     )
                sprint = get_object_or_404(
                    SprintWatermarking, watermarking=watermarking.id,
                    coverImage=cover, watermark=watermark)
                for noise in Noise.objects.all():
                    if not NoiseSprintWatermarking.objects.filter(
                            noise=noise, sprintWatermarking=sprint).exists():
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
                        NoiseSprintWatermarking.objects.create(
                            noise=noise, sprintWatermarking=sprint,
                            watermarked_image_with_noise=noised_image)
    return 'Success!'
