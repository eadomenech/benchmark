import uuid

from django.db import models
# Work with datetime
from django.utils import timezone
# Reverse
from django.urls import reverse
# File validators
from django.core.validators import FileExtensionValidator

from .helpers import (
    random_paper_name, random_source_code_name, random_cover_image_name,
    random_watermark_image_name, random_noise_code_name,
    random_metric_code_name)


class Watermarking(models.Model):
    name = models.CharField(max_length=300, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField(default=timezone.now)

    paper = models.FileField(
        upload_to=random_paper_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf'],
            message="Please upload '.pdf' files only.")])
    source_code = models.FileField(
        upload_to=random_source_code_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['py'],
            message="Please upload '.py' files only.")])
    extract_code = models.FileField(
        upload_to=random_source_code_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['py'],
            message="Please upload '.py' files only.")])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('watermarking:methods')


class CoverImage(models.Model):
    uuid = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(
        upload_to=random_cover_image_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'bmp', 'png'],
            message="Please upload '.jpg', '.png' or '.bmp' files only.")])

    def __str__(self):
        return self.uuid

    def get_absolute_url(self):
        return reverse('watermarking:coverImage')


class WatermarkImage(models.Model):
    uuid = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    watermark_image = models.ImageField(
        upload_to=random_watermark_image_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['png'],
            message="Please upload '.png' files only.")])

    def __str__(self):
        return self.uuid

    def get_absolute_url(self):
        return reverse('watermarking:watermarkImage')


class Noise(models.Model):
    name = models.CharField(max_length=300, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    source_code = models.FileField(
        upload_to=random_noise_code_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['py'],
            message="Please upload '.py' files only.")])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('watermarking:noises')


metric_types = (
    ('1', 'Watermarked'),
    ('2', 'Watermark'))


class Metric(models.Model):
    name = models.CharField(max_length=100, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    metric_type = models.CharField(max_length=10, choices=metric_types)
    source_code = models.FileField(
        upload_to=random_metric_code_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['py'],
            message="Please upload '.py' files only.")])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('watermarking:metrics')


class SprintWatermarking(models.Model):
    watermarking = models.ForeignKey(Watermarking, on_delete=models.CASCADE)
    cover_image = models.ForeignKey(CoverImage, on_delete=models.CASCADE)
    watermark = models.ForeignKey(WatermarkImage, on_delete=models.CASCADE)
    watermarked_image = models.ImageField()

    class Meta:
        unique_together = ("watermarking", "cover_image", "watermark")

    def __str__(self):
        return str(self.watermarking) + '_' + str(self.cover_image) + '_' + str(self.watermark)


class MetricSprintWatermarking(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    sprintWatermarking = models.ForeignKey(
        SprintWatermarking, on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        unique_together = ("metric", "sprintWatermarking")

    def __str__(self):
        return str(self.metric) + '_' + str(self.sprintWatermarking)


class NoiseSprintWatermarking(models.Model):
    noise = models.ForeignKey(Noise, on_delete=models.CASCADE)
    sprintWatermarking = models.ForeignKey(
        SprintWatermarking, on_delete=models.CASCADE)
    watermarked_image_with_noise = models.ImageField()

    class Meta:
        unique_together = ("noise", "sprintWatermarking")

    def __str__(self):
        return str(self.noise) + '_' + str(self.sprintWatermarking)


class MetricNoiseSprintWatermarking(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    noiseSprintWatermarking = models.ForeignKey(
        NoiseSprintWatermarking, on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        unique_together = ("metric", "noiseSprintWatermarking")

    def __str__(self):
        return str(self.metric) + '_' + str(self.noiseSprintWatermarking)
