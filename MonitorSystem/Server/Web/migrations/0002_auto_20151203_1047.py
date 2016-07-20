# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('GroupName', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup_HostGroup_Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('HostGroupID', models.ForeignKey(to='Web.HostGroups')),
                ('UserGroupID', models.ForeignKey(to='Web.UserGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Username', models.CharField(max_length=20)),
                ('Password', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=20)),
                ('Email', models.EmailField(max_length=254)),
                ('Tel', models.IntegerField()),
                ('Mobile', models.IntegerField()),
                ('UserGroupID', models.ForeignKey(to='Web.UserGroup')),
            ],
        ),
        migrations.AlterField(
            model_name='host',
            name='HostNetIpAddr',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='host',
            name='HostPriIpAddr',
            field=models.CharField(max_length=15),
        ),
    ]
