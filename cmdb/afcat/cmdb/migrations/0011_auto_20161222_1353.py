# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-22 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0010_auto_20161222_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecustomerinfo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]