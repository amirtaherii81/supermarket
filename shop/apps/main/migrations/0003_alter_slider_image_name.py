# Generated by Django 5.0.6 on 2024-09-27 14:09

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_slider_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر اسلایدر'),
        ),
    ]
