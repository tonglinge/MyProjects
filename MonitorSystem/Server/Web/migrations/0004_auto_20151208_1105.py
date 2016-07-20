# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0003_auto_20151203_1752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host_CPU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CheckTime', models.DateTimeField()),
                ('CPU_Idle', models.FloatField()),
                ('CPU_User', models.FloatField()),
                ('CPU_Sys', models.FloatField()),
                ('Hosts', models.ForeignKey(to='Web.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Host_Disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CheckTime', models.DateTimeField()),
                ('DISK_Mountpoint', models.CharField(max_length=50)),
                ('DISK_TotalSize', models.FloatField()),
                ('DISK_Used', models.FloatField()),
                ('DISK_Free', models.FloatField()),
                ('DISK_Precent', models.FloatField()),
                ('Hosts', models.ForeignKey(to='Web.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Host_Memory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CheckTime', models.DateTimeField()),
                ('Mem_TotalSize', models.FloatField()),
                ('Mem_Used', models.FloatField()),
                ('Mem_Free', models.FloatField()),
                ('Mem_Precent', models.FloatField()),
                ('Hosts', models.ForeignKey(to='Web.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Host_Swap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CheckTime', models.DateTimeField()),
                ('Swap_TotalSize', models.FloatField()),
                ('Swap_Used', models.FloatField()),
                ('Swap_Free', models.FloatField()),
                ('Swap_Precent', models.FloatField()),
                ('Hosts', models.ForeignKey(to='Web.Host')),
            ],
        ),
        migrations.AddField(
            model_name='monitormodels',
            name='ModelPlubName',
            field=models.CharField(default=datetime.datetime(2015, 12, 8, 3, 5, 10, 901000, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
