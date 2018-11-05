import os
import uuid

from django.db import models
# Work with datetime
from django.utils import timezone
# Reverse
from django.urls import reverse
# File validators
from django.core.validators import FileExtensionValidator


def random_paper_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('papers/', filename)


def random_source_code_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('source_codes/', filename)


def random_cover_image_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('cover_images/', filename)


def random_watermark_image_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('watermark_images/', filename)


def random_noise_code_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('noise_codes/', filename)


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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('watermarking:methods')


class CoverImage(models.Model):
    uuid = models.CharField(max_length=64, unique=True, default=uuid.uuid4())
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(
        upload_to=random_cover_image_name,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg'],
            message="Please upload '.jpg' files only.")])

    def __str__(self):
        return self.uuid

    def get_absolute_url(self):
        return reverse('watermarking:coverImage')


class WatermarkImage(models.Model):
    uuid = models.CharField(max_length=64, unique=True, default=uuid.uuid4())
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
