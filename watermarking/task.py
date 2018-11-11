# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django.conf import settings

import uuid

from celery import shared_task
from .models import *

from subprocess import Popen, PIPE
import subprocess


@shared_task
def mainTask():
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
    return 'Success!'
