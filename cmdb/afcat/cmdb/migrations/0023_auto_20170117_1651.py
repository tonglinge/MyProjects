# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-17 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0022_auto_20170117_1643'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ipdesign',
            options={'permissions': (('view_ipdesign', 'Can View IPDesign'),), 'verbose_name': 'IP地址规划', 'verbose_name_plural': 'IP地址规划'},
        ),
        migrations.AddField(
            model_name='ipdesign',
            name='counts',
            field=models.IntegerField(null=True, verbose_name='子网/IP数量'),
        ),
        migrations.AddField(
            model_name='ipdesign',
            name='datacenter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.BaseDataCenter', verbose_name='数据中心'),
        ),
        migrations.AddField(
            model_name='ipdesign',
            name='netarea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.BaseNetArea', verbose_name='网络区域'),
        ),
        migrations.AddField(
            model_name='ipdesign',
            name='parentip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.IPDesign', verbose_name='子网归属'),
        ),
        migrations.AddField(
            model_name='ipdesign',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='备注'),
        ),
    ]