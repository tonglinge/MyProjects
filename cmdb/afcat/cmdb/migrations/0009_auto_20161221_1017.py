# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-21 10:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0008_auto_20161217_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsSet',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('itemname', models.CharField(max_length=200, verbose_name='项目集名称')),
                ('cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.BaseCustomerInfo', to_field='idcode', verbose_name='所属客户')),
                ('staffs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Staffs', verbose_name='联系人')),
            ],
            options={
                'permissions': (('view_itemsset', 'Can View ItemsSet'),),
                'verbose_name': '项目集',
                'verbose_name_plural': '项目集',
            },
        ),
        migrations.AlterModelOptions(
            name='portlist',
            options={'ordering': ['portname'], 'verbose_name': '端口列表', 'verbose_name_plural': '端口列表'},
        ),
        migrations.AlterModelOptions(
            name='portmapping',
            options={'ordering': ['localport__portname'], 'verbose_name': '端口映射', 'verbose_name_plural': '端口映射'},
        ),
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['sysname', 'sysalias', 'company', 'syslevel'], 'permissions': (('view_projects', 'Can View Projects'),), 'verbose_name': '项目信息', 'verbose_name_plural': '项目信息'},
        ),
        migrations.RemoveField(
            model_name='projects',
            name='cust',
        ),
        migrations.AddField(
            model_name='projects',
            name='itemsset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.ItemsSet', verbose_name='所属项目集'),
        ),
    ]
