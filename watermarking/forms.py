# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-
from django import forms
from .models import Watermarking, CoverImage, WatermarkImage, Metric

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
        fields = ['name', 'created_at', 'paper', 'source_code']


class CoverImageForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = CoverImage
        fields = ['name', 'cover_image']


class WatermarkImageForm(forms.ModelForm):
    class Meta:
        model = WatermarkImage
        fields = ['watermark_image']


class MetricForm(BtnsSubmitCancelMixing, forms.ModelForm):
    class Meta:
        model = Metric
        fields = ['name', 'source_code']
