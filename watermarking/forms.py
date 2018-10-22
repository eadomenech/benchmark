# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django import forms
from .models import Watermarking, CoverImage, WatermarkImage


class WatermarkingForm(forms.ModelForm):
    class Meta:
        model = Watermarking
        fields = ['name', 'created_at', 'paper', 'source_code']


class CoverImageForm(forms.ModelForm):
    class Meta:
        model = CoverImage
        fields = ['cover_image']


class WatermarkImageForm(forms.ModelForm):
    class Meta:
        model = WatermarkImage
        fields = ['watermark_image']
