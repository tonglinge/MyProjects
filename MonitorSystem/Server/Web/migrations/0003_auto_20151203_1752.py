# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web', '0002_auto_20151203_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host_group_relation',
            name='Gid',
        ),
        migrations.RemoveField(
            model_name='host_group_relation',
            name='Hid',
        ),
        migrations.AddField(
            model_name='host',
            name='HostGroup',
            field=models.ForeignKey(default=1, to='Web.HostGroups'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Host_Group_Relation',
        ),
    ]
