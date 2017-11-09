# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0006_planning_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_skill',
            old_name='kaid_student_id',
            new_name='kaid_student',
        ),
    ]
