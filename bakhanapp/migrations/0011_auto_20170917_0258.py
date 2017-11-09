# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0010_institutional_plan_share_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutional_plan',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='planning',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
