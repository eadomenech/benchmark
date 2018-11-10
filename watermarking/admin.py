from django.contrib import admin

from .models import Watermarking, CoverImage, WatermarkImage, Noise, Metric

admin.site.register(Watermarking)
admin.site.register(CoverImage)
admin.site.register(WatermarkImage)
admin.site.register(Noise)
admin.site.register(Metric)
