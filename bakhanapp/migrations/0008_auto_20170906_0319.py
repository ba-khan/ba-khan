# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0007_auto_20170906_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_skill',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
    ]
