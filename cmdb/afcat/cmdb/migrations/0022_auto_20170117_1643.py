# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-17 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0021_auto_20161229_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPDesign',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ipaddr', models.GenericIPAddressField(verbose_name='IP地址')),
                ('maskbits', models.IntegerField(verbose_name='子网掩码位')),
            ],
            options={
                'permissions': (('view_ipsource', 'Can View IPSource'),),
                'verbose_name': 'IP地址规划',
                'verbose_name_plural': 'IP地址规划',
            },
        ),
        migrations.CreateModel(
            name='TemplsteVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=100, verbose_name='模板名称')),
                ('md5_value', models.CharField(max_length=100, verbose_name='校验码')),
            ],
            options={
                'verbose_name': '模板校验',
                'verbose_name_plural': '模板校验',
            },
        ),
        migrations.DeleteModel(
            name='IPAllocation',
        ),
        migrations.DeleteModel(
            name='IPSource',
        ),
    ]
