# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-15 14:43
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20161215_1327'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='assets',
            managers=[
                ('report', django.db.models.manager.Manager()),
            ],
        ),
    ]
