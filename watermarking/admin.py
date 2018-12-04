from django.contrib import admin

from .models import (
    Watermarking, CoverImage, WatermarkImage, Noise, Metric, SprintWatermarking,
    MetricSprintWatermarking, NoiseSprintWatermarking,
    MetricNoiseSprintWatermarking, ImageType)

admin.site.register(Watermarking)
admin.site.register(CoverImage)
admin.site.register(WatermarkImage)
admin.site.register(Noise)
admin.site.register(Metric)
admin.site.register(SprintWatermarking)
admin.site.register(MetricSprintWatermarking)
admin.site.register(NoiseSprintWatermarking)
admin.site.register(MetricNoiseSprintWatermarking)
admin.site.register(ImageType)
