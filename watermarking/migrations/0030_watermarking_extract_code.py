# Generated by Django 2.0 on 2018-11-13 15:22

import django.core.validators
from django.db import migrations, models
import watermarking.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('watermarking', '0029_auto_20181113_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='watermarking',
            name='extract_code',
            field=models.FileField(default='', upload_to=watermarking.helpers.random_source_code_name, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['py'], message="Please upload '.py' files only.")]),
            preserve_default=False,
        ),
    ]