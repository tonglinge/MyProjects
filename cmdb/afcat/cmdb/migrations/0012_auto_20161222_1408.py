# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-22 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0011_auto_20161222_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecustomerinfo',
            name='id',
            field=models.BigIntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='basecustomerinfo',
            name='idcode',
            field=models.IntegerField(unique=True, verbose_name='唯一序号'),
        ),
    ]
