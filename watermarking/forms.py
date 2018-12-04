# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django import forms
from .models import (
    Watermarking, CoverImage, WatermarkImage, Metric, Noise, ImageType)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class BtnsSubmitCancelMixing(object):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.add_input(Submit(
        'cancel', 'Cancel', css_class='btn-danger',
        formnovalidate='formnovalidate',))
    helper.form_method = 'POST'


class WatermarkingForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = Watermarking
        fields = '__all__'


class CoverImageForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = CoverImage
        fields = ['name', 'cover_image', 'image_type']


class WatermarkImageForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = WatermarkImage
        fields = ['name', 'watermark_image', 'image_type']


class MetricForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = Metric
        fields = '__all__'


class NoiseForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = Noise
        fields = ['name', 'source_code']


class ImageTypeForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = ImageType
        fields = "__all__"
