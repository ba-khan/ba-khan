# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0009_auto_20170908_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutional_plan',
            name='share_class',
            field=models.NullBooleanField(default=False),
        ),
    ]
