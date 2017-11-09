# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0012_topic_mineduc_suggested_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtopic_mineduc',
            name='id_topic',
            field=models.ForeignKey(related_name='topic_mineduc', to='bakhanapp.Topic_Mineduc'),
        ),
        migrations.AlterField(
            model_name='subtopic_skill_mineduc',
            name='id_subtopic_mineduc',
            field=models.ForeignKey(related_name='subtopic_mineduc', blank=True, to='bakhanapp.Subtopic_Mineduc', null=True),
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='id_chapter',
            field=models.ForeignKey(related_name='topic_mineduc', to='bakhanapp.Chapter_Mineduc'),
        ),
    ]
