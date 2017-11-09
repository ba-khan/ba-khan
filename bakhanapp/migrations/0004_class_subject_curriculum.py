# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0003_auto_20170730_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='class_subject',
            name='curriculum',
            field=models.ForeignKey(blank=True, to='bakhanapp.Chapter_Mineduc', null=True),
        ),
    ]
