# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-07 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0032_ipmanage_cust'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceMapping',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('vsname', models.TextField(max_length=150, verbose_name='vs名称')),
                ('vsaddr', models.GenericIPAddressField(blank=True, null=True, verbose_name='vs地址')),
                ('port', models.IntegerField(blank=True, null=True, verbose_name='服务端口')),
                ('dnsdomain', models.TextField(blank=True, max_length=100, null=True, verbose_name='DNS域名')),
                ('snataddr', models.TextField(blank=True, max_length=300, null=True, verbose_name='SNAT地址')),
                ('pooladdr', models.TextField(blank=True, max_length=300, null=True, verbose_name='地址池')),
                ('vlan', models.IntegerField(blank=True, null=True, verbose_name='VLAN')),
                ('business', models.TextField(blank=True, max_length=100, null=True, verbose_name='所属业务')),
                ('hostname', models.TextField(blank=True, max_length=300, null=True, verbose_name='主机名称')),
                ('remark', models.TextField(blank=True, max_length=200, null=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Equipment', verbose_name='所属设备')),
                ('netarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.BaseNetArea', verbose_name='所属区域')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Projects', verbose_name='所属系统')),
            ],
            options={
                'verbose_name_plural': 'F5映射',
                'verbose_name': 'F5映射',
                'permissions': (('view_balancemapping', 'can view F5 Mapping'),),
            },
        ),
    ]
