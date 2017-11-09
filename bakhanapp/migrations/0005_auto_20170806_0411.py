# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0004_class_subject_curriculum'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill_planning',
            name='id_subtopic',
            field=models.ForeignKey(default=0, to='bakhanapp.Subtopic_Skill'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video_planning',
            name='id_subtopic',
            field=models.ForeignKey(default=0, to='bakhanapp.Subtopic_Video'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='skill_planning',
            name='id_planning',
            field=models.ForeignKey(to='bakhanapp.Planning'),
        ),
        migrations.AlterField(
            model_name='skill_planning',
            name='id_skill',
            field=models.ForeignKey(to='bakhanapp.Skill'),
        ),
        migrations.AlterField(
            model_name='video_planning',
            name='id_planning',
            field=models.ForeignKey(to='bakhanapp.Planning'),
        ),
        migrations.AlterField(
            model_name='video_planning',
            name='id_video',
            field=models.ForeignKey(to='bakhanapp.Video'),
        ),
        migrations.AlterUniqueTogether(
            name='skill_planning',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='video_planning',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_video')]),
        ),
    ]
