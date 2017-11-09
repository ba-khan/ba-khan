# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0008_auto_20170906_0319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institutional_Plan',
            fields=[
                ('id_planning', models.AutoField(serialize=False, primary_key=True)),
                ('class_date', models.DateField(null=True, blank=True)),
                ('minutes', models.IntegerField(null=True, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('desc_inicio', models.TextField(null=True, blank=True)),
                ('desc_cierre', models.TextField(null=True, blank=True)),
                ('class_name', models.TextField()),
                ('class_subtopic', models.ForeignKey(to='bakhanapp.Subtopic_Mineduc')),
                ('curriculum', models.ForeignKey(to='bakhanapp.Chapter_Mineduc')),
                ('institution', models.ForeignKey(to='bakhanapp.Institution')),
            ],
            options={
                'db_table': 'bakhanapp_institutional_plan',
            },
        ),
        migrations.CreateModel(
            name='Skill_Institution_Plan',
            fields=[
                ('id_skill_planning', models.AutoField(serialize=False, primary_key=True)),
                ('id_planning', models.ForeignKey(to='bakhanapp.Institutional_Plan')),
                ('id_skill', models.ForeignKey(to='bakhanapp.Skill')),
                ('id_subtopic', models.ForeignKey(to='bakhanapp.Subtopic_Skill')),
            ],
            options={
                'db_table': 'bakhanapp_skill_institution_plan',
            },
        ),
        migrations.CreateModel(
            name='Video_Institution_Plan',
            fields=[
                ('id_video_planning', models.AutoField(serialize=False, primary_key=True)),
                ('id_planning', models.ForeignKey(to='bakhanapp.Institutional_Plan')),
                ('id_subtopic', models.ForeignKey(to='bakhanapp.Subtopic_Video')),
                ('id_video', models.ForeignKey(to='bakhanapp.Video')),
            ],
            options={
                'db_table': 'bakhanapp_video_institution_plan',
            },
        ),
        migrations.AlterUniqueTogether(
            name='video_institution_plan',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_video')]),
        ),
        migrations.AlterUniqueTogether(
            name='skill_institution_plan',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='institutional_plan',
            unique_together=set([('class_name', 'curriculum')]),
        ),
    ]
