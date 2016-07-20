# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('HostName', models.CharField(max_length=30)),
                ('HostNetIpAddr', models.IPAddressField()),
                ('HostPriIpAddr', models.IPAddressField()),
                ('CpuCount', models.IntegerField(null=True)),
                ('DiskCount', models.IntegerField(null=True)),
                ('OSType', models.CharField(max_length=10, null=True)),
                ('OSVerision', models.CharField(max_length=10, null=True)),
                ('Producter', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host_Group_Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('GroupName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Model_Group_Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Interval', models.IntegerField()),
                ('Gid', models.ForeignKey(to='Web.HostGroups')),
            ],
        ),
        migrations.CreateModel(
            name='MonitorModels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('MonitorName', models.CharField(max_length=50)),
                ('ModelName', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='model_group_relation',
            name='Mid',
            field=models.ForeignKey(to='Web.MonitorModels'),
        ),
        migrations.AddField(
            model_name='host_group_relation',
            name='Gid',
            field=models.ForeignKey(to='Web.HostGroups'),
        ),
        migrations.AddField(
            model_name='host_group_relation',
            name='Hid',
            field=models.ForeignKey(to='Web.Host'),
        ),
    ]
