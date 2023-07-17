# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-28 19:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("storage", "0003_auto_20170424_2002"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="label",
            name="revision",
        ),
        migrations.AddField(
            model_name="label",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="label",
            name="style",
            field=models.CharField(
                choices=[("basic_99012_v1", "Basic Dymo 89x36mm label")],
                default="basic_99012_v1",
                max_length=32,
            ),
        ),
    ]
