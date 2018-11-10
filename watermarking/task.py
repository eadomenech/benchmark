from celery import shared_task
from .models import *


@shared_task
def mainTask():
    for cover in CoverImage.objects.all():
        for watermark in WatermarkImage.objects.all():
            for watermarking in Watermarking.objects.all():
                if not SprintWatermarking.objects.filter(
                        watermarking=watermarking.id, coverImage=cover,
                        watermark=watermark).exists():
                    sprint = SprintWatermarking.objects.create(
                        watermarking=watermarking, coverImage=cover,
                        watermark=watermark
                    )
                    print(sprint)
    return 'Success!'
