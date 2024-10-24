# Generated by Django 5.0.6 on 2024-09-15 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment_scoring_favorites', '0002_scoring'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='approving_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_user2', to=settings.AUTH_USER_MODEL, verbose_name='کاربر تایید کننده نظر'),
        ),
    ]
