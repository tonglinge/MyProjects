# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-27 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0018_auto_20161226_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='cabinet',
            field=models.CharField(max_length=100, null=True, verbose_name='机柜'),
        ),
    ]
