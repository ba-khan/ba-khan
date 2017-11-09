# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config_Skill',
            fields=[
                ('id_assesment_config_id', models.IntegerField(null=True, blank=True)),
                ('id_subtopic_skill_id', models.IntegerField(null=True, blank=True)),
                ('id_config_skill', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'db_table': 'bakhanapp_config_skill',
            },
        ),
        migrations.RemoveField(
            model_name='group',
            name='kaid_student_tutor',
        ),
        migrations.RemoveField(
            model_name='subtopic_mineduc',
            name='AE_OE',
        ),
        migrations.AddField(
            model_name='group',
            name='kaid_student_tutor_id',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='student_skill',
            name='kaid_student_id',
            field=models.CharField(default=0, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subtopic_mineduc',
            name='ae_oe',
            field=models.CharField(max_length=500, null=True, db_column=b'AE_OE', blank=True),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='email',
            field=models.CharField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='kaid_administrator',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='phone',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment',
            name='approval_grade',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment',
            name='id_class',
            field=models.ForeignKey(blank=True, to='bakhanapp.Class', null=True),
        ),
        migrations.AlterField(
            model_name='assesment',
            name='max_effort_bonus',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment',
            name='max_grade',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment',
            name='min_grade',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment_config',
            name='applied',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='assesment_config',
            name='importance_skill_level',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment_config',
            name='top_score',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='assesment_skill',
            name='id_subtopic_skill',
            field=models.ForeignKey(blank=True, to='bakhanapp.Subtopic_Skill', null=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='type_chapter',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chapter_mineduc',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chapter_mineduc',
            name='name',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='additional',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='id_institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
        migrations.AlterField(
            model_name='class_schedule',
            name='day',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='class_schedule',
            name='id_class',
            field=models.ForeignKey(blank=True, to='bakhanapp.Class', null=True),
        ),
        migrations.AlterField(
            model_name='class_schedule',
            name='id_schedule',
            field=models.ForeignKey(blank=True, to='bakhanapp.Schedule', null=True),
        ),
        migrations.AlterField(
            model_name='class_schedule',
            name='kaid_teacher',
            field=models.ForeignKey(blank=True, to='bakhanapp.Teacher', null=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='bonus_grade',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='comment',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='correct',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='effort_points',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='evaluated',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='grade',
            name='excercice_time',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='hints',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='incorrect',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='mastery1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='mastery2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='mastery3',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='nothing',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='performance_points',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='practiced',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='recomended_complete',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='struggling',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='teacher_grade',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='total_recomended',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='unstarted',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='video_time',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='videos',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='master',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='address',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='identifier',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='key',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='last_load',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='password',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='secret',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='cierre',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='clase',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='curso',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='descripcion',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='ejerciciokhan',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='inicio',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='oa',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='objetivo',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='teacher',
            field=models.ForeignKey(blank=True, to='bakhanapp.Teacher', null=True),
        ),
        migrations.AlterField(
            model_name='planning',
            name='videokhan',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='related_video_exercise',
            name='id_exercise',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='related_video_exercise',
            name='id_video',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_time',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='id_institution',
            field=models.ForeignKey(blank=True, to='bakhanapp.Institution', null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='name_block',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_time',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name_spanish',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='url_skill',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill_attempt',
            name='mission',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill_attempt',
            name='task_type',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill_attempt',
            name='video',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='skill_log',
            name='correct',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill_log',
            name='id_grade',
            field=models.ForeignKey(blank=True, to='bakhanapp.Grade', null=True),
        ),
        migrations.AlterField(
            model_name='skill_log',
            name='id_skill_name',
            field=models.ForeignKey(blank=True, to='bakhanapp.Skill', null=True),
        ),
        migrations.AlterField(
            model_name='skill_log',
            name='incorrect',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill_log',
            name='skill_progress',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skill_planning',
            name='id_planning',
            field=models.ForeignKey(blank=True, to='bakhanapp.Planning', null=True),
        ),
        migrations.AlterField(
            model_name='skill_planning',
            name='id_skill',
            field=models.ForeignKey(blank=True, to='bakhanapp.Skill', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='id_institution',
            field=models.ForeignKey(blank=True, to='bakhanapp.Institution', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_update',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='new_student',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='nickname',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='points',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic_mineduc',
            name='id_topic',
            field=models.ForeignKey(blank=True, to='bakhanapp.Topic_Mineduc', null=True),
        ),
        migrations.AlterField(
            model_name='subtopic_mineduc',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic_mineduc',
            name='name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic_skill_mineduc',
            name='id_skill_name',
            field=models.ForeignKey(blank=True, to='bakhanapp.Skill', null=True),
        ),
        migrations.AlterField(
            model_name='subtopic_skill_mineduc',
            name='id_subtopic_mineduc',
            field=models.ForeignKey(blank=True, to='bakhanapp.Subtopic_Mineduc', null=True),
        ),
        migrations.AlterField(
            model_name='subtopic_skill_mineduc',
            name='id_tree',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic_video_mineduc',
            name='id_subtopic_name_mineduc',
            field=models.ForeignKey(blank=True, to='bakhanapp.Subtopic_Mineduc', null=True),
        ),
        migrations.AlterField(
            model_name='subtopic_video_mineduc',
            name='id_tree',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic_video_mineduc',
            name='id_video_name',
            field=models.ForeignKey(blank=True, to='bakhanapp.Video', null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='topic',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='descripcion_topic',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='id_chapter',
            field=models.ForeignKey(blank=True, to='bakhanapp.Chapter_Mineduc', null=True),
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='email',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='phone',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='kaid',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='index',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='name_spanish',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='url_video',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video_planning',
            name='id_planning',
            field=models.ForeignKey(blank=True, to='bakhanapp.Planning', null=True),
        ),
        migrations.AlterField(
            model_name='video_planning',
            name='id_video',
            field=models.ForeignKey(blank=True, to='bakhanapp.Video', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together=set([('id_institution', 'level', 'letter', 'additional')]),
        ),
        migrations.AlterUniqueTogether(
            name='student_skill',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_skill_mineduc',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_video_mineduc',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='video_playing',
            unique_together=set([('date', 'id_video_name', 'kaid_student')]),
        ),
        migrations.AlterModelTable(
            name='administrator',
            table='bakhanapp_administrator',
        ),
        migrations.AlterModelTable(
            name='assesment',
            table='bakhanapp_assesment',
        ),
        migrations.AlterModelTable(
            name='assesment_config',
            table='bakhanapp_assesment_config',
        ),
        migrations.AlterModelTable(
            name='assesment_skill',
            table='bakhanapp_assesment_skill',
        ),
        migrations.AlterModelTable(
            name='chapter',
            table='bakhanapp_chapter',
        ),
        migrations.AlterModelTable(
            name='chapter_mineduc',
            table='bakhanapp_chapter_mineduc',
        ),
        migrations.AlterModelTable(
            name='class',
            table='bakhanapp_class',
        ),
        migrations.AlterModelTable(
            name='class_schedule',
            table='bakhanapp_class_schedule',
        ),
        migrations.AlterModelTable(
            name='class_subject',
            table='bakhanapp_class_subject',
        ),
        migrations.AlterModelTable(
            name='grade',
            table='bakhanapp_grade',
        ),
        migrations.AlterModelTable(
            name='group',
            table='bakhanapp_group',
        ),
        migrations.AlterModelTable(
            name='group_student',
            table='bakhanapp_group_student',
        ),
        migrations.AlterModelTable(
            name='institution',
            table='bakhanapp_institution',
        ),
        migrations.AlterModelTable(
            name='planning',
            table='bakhanapp_planning',
        ),
        migrations.AlterModelTable(
            name='related_video_exercise',
            table='bakhanapp_related_video_exercise',
        ),
        migrations.AlterModelTable(
            name='schedule',
            table='bakhanapp_schedule',
        ),
        migrations.AlterModelTable(
            name='skill',
            table='bakhanapp_skill',
        ),
        migrations.AlterModelTable(
            name='skill_attempt',
            table='bakhanapp_skill_attempt',
        ),
        migrations.AlterModelTable(
            name='skill_log',
            table='bakhanapp_skill_log',
        ),
        migrations.AlterModelTable(
            name='skill_planning',
            table='bakhanapp_skill_planning',
        ),
        migrations.AlterModelTable(
            name='student',
            table='bakhanapp_student',
        ),
        migrations.AlterModelTable(
            name='student_class',
            table='bakhanapp_student_class',
        ),
        migrations.AlterModelTable(
            name='student_skill',
            table='bakhanapp_student_skill',
        ),
        migrations.AlterModelTable(
            name='student_video',
            table='bakhanapp_student_video',
        ),
        migrations.AlterModelTable(
            name='subject',
            table='bakhanapp_subject',
        ),
        migrations.AlterModelTable(
            name='subtopic',
            table='bakhanapp_subtopic',
        ),
        migrations.AlterModelTable(
            name='subtopic_mineduc',
            table='bakhanapp_subtopic_mineduc',
        ),
        migrations.AlterModelTable(
            name='subtopic_skill',
            table='bakhanapp_subtopic_skill',
        ),
        migrations.AlterModelTable(
            name='subtopic_skill_mineduc',
            table='bakhanapp_subtopic_skill_mineduc',
        ),
        migrations.AlterModelTable(
            name='subtopic_video',
            table='bakhanapp_subtopic_video',
        ),
        migrations.AlterModelTable(
            name='subtopic_video_mineduc',
            table='bakhanapp_subtopic_video_mineduc',
        ),
        migrations.AlterModelTable(
            name='teacher',
            table='bakhanapp_teacher',
        ),
        migrations.AlterModelTable(
            name='topic',
            table='bakhanapp_topic',
        ),
        migrations.AlterModelTable(
            name='topic_mineduc',
            table='bakhanapp_topic_mineduc',
        ),
        migrations.AlterModelTable(
            name='tutor',
            table='bakhanapp_tutor',
        ),
        migrations.AlterModelTable(
            name='user_profile',
            table='bakhanapp_user_profile',
        ),
        migrations.AlterModelTable(
            name='video',
            table='bakhanapp_video',
        ),
        migrations.AlterModelTable(
            name='video_planning',
            table='bakhanapp_video_planning',
        ),
        migrations.AlterModelTable(
            name='video_playing',
            table='bakhanapp_video_playing',
        ),
        migrations.RemoveField(
            model_name='student_skill',
            name='kaid_student',
        ),
    ]
