# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assesment_config',
            name='assesment_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
