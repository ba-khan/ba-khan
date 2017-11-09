# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0005_auto_20170806_0411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planning_Log',
            fields=[
                ('id_log', models.AutoField(serialize=False, primary_key=True)),
                ('field', models.TextField()),
                ('old_value', models.TextField()),
                ('new_value', models.TextField()),
                ('date', models.DateField()),
                ('id_planning', models.ForeignKey(to='bakhanapp.Planning')),
            ],
            options={
                'db_table': 'bakhanapp_planning_log',
            },
        ),
    ]
