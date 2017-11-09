# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0013_auto_20171003_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planning_log',
            name='old_value',
            field=models.TextField(null=True),
        ),
    ]
