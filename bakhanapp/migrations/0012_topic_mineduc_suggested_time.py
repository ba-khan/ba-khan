# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0011_auto_20170917_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic_mineduc',
            name='suggested_time',
            field=models.IntegerField(default=48),
            preserve_default=False,
        ),
    ]
