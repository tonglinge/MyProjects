# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-03 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0027_auto_20170119_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipdesign',
            name='createdate',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='创建日期'),
        ),
        migrations.AddField(
            model_name='ipdesign',
            name='createuser',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='创建人'),
        ),
    ]
