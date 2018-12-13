# -*- encoding:utf-8 -*-
# -*- coding:utf-8 -*-

from django import template
from watermarking.models import (
    Metric, MetricNoiseSprintWatermarking, MetricSprintWatermarking)

register = template.Library()


@register.simple_tag(takes_context=True)
def metrics_watermarked(context):
    return Metric.objects.filter(metric_type="1")


@register.simple_tag(takes_context=True)
def metrics_watermark(context):
    return Metric.objects.filter(metric_type="2")


@register.simple_tag(takes_context=True)
def metrics_watermarked_of_noised(context, sprint_id):
    metrics = Metric.objects.filter(metric_type="1")
    lista = []
    for m in metrics:
        try:
            lista.append(MetricSprintWatermarking.objects.get(
                metric=m, sprintWatermarking=sprint_id
            ).value)
        except:
            lista.append(-3)
    return lista


@register.simple_tag(takes_context=True)
def metrics_watermark_of_noised(context, noise_id):
    metrics = Metric.objects.filter(metric_type="2")
    lista = []
    for m in metrics:
        try:
            lista.append(
                MetricNoiseSprintWatermarking.objects.get(
                    metric=m, noiseSprintWatermarking=noise_id
                ).value)
        except:
            lista.append(-3)
    return lista
