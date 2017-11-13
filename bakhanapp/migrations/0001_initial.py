# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('kaid_administrator', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=254, null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_administrator',
                'permissions': (('isAdmin', 'Is Admin'),),
            },
        ),
        migrations.CreateModel(
            name='Assesment',
            fields=[
                ('id_assesment', models.AutoField(serialize=False, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('name', models.CharField(max_length=150)),
                ('max_grade', models.IntegerField(null=True, blank=True)),
                ('min_grade', models.IntegerField(null=True, blank=True)),
                ('approval_grade', models.IntegerField(null=True, blank=True)),
                ('max_effort_bonus', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_assesment',
            },
        ),
        migrations.CreateModel(
            name='Assesment_Config',
            fields=[
                ('id_assesment_config', models.AutoField(serialize=False, primary_key=True)),
                ('approval_percentage', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('importance_skill_level', models.IntegerField(null=True, blank=True)),
                ('importance_completed_rec', models.IntegerField()),
                ('applied', models.NullBooleanField()),
                ('top_score', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_assesment_config',
            },
        ),
        migrations.CreateModel(
            name='Assesment_Skill',
            fields=[
                ('id_assesment_skill', models.AutoField(serialize=False, primary_key=True)),
                ('id_assesment_config', models.ForeignKey(to='bakhanapp.Assesment_Config')),
            ],
            options={
                'db_table': 'bakhanapp_assesment_skill',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id_chapter_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150)),
                ('index', models.IntegerField(null=True, blank=True)),
                ('type_chapter', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_chapter',
            },
        ),
        migrations.CreateModel(
            name='Chapter_Mineduc',
            fields=[
                ('id_chapter_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('level', models.IntegerField()),
                ('year', models.IntegerField()),
                ('additional', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_chapter_mineduc',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id_class', models.AutoField(serialize=False, primary_key=True)),
                ('level', models.IntegerField()),
                ('letter', models.CharField(max_length=2)),
                ('year', models.IntegerField()),
                ('additional', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_class',
            },
        ),
        migrations.CreateModel(
            name='Class_Schedule',
            fields=[
                ('id_class_schedule', models.AutoField(serialize=False, primary_key=True)),
                ('day', models.CharField(max_length=20, null=True, blank=True)),
                ('id_class', models.ForeignKey(blank=True, to='bakhanapp.Class', null=True)),
            ],
            options={
                'db_table': 'bakhanapp_class_schedule',
            },
        ),
        migrations.CreateModel(
            name='Class_Subject',
            fields=[
                ('id_class_subject', models.AutoField(serialize=False, primary_key=True)),
                ('curriculum', models.ForeignKey(blank=True, to='bakhanapp.Chapter_Mineduc', null=True)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
            ],
            options={
                'db_table': 'bakhanapp_class_subject',
            },
        ),
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
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id_grade', models.AutoField(serialize=False, primary_key=True)),
                ('grade', models.FloatField()),
                ('teacher_grade', models.FloatField(null=True, blank=True)),
                ('performance_points', models.FloatField(null=True, blank=True)),
                ('effort_points', models.FloatField(null=True, blank=True)),
                ('comment', models.CharField(max_length=300, null=True, blank=True)),
                ('evaluated', models.NullBooleanField()),
                ('recomended_complete', models.IntegerField(null=True, blank=True)),
                ('excercice_time', models.IntegerField(null=True, blank=True)),
                ('video_time', models.IntegerField(null=True, blank=True)),
                ('correct', models.IntegerField(null=True, blank=True)),
                ('incorrect', models.IntegerField(null=True, blank=True)),
                ('struggling', models.IntegerField(null=True, blank=True)),
                ('practiced', models.IntegerField(null=True, blank=True)),
                ('mastery1', models.IntegerField(null=True, blank=True)),
                ('mastery2', models.IntegerField(null=True, blank=True)),
                ('mastery3', models.IntegerField(null=True, blank=True)),
                ('hints', models.IntegerField(null=True, blank=True)),
                ('videos', models.IntegerField(null=True, blank=True)),
                ('nothing', models.IntegerField(null=True, blank=True)),
                ('bonus_grade', models.FloatField(null=True, blank=True)),
                ('unstarted', models.IntegerField(null=True, blank=True)),
                ('total_recomended', models.IntegerField(null=True, blank=True)),
                ('id_assesment', models.ForeignKey(to='bakhanapp.Assesment')),
            ],
            options={
                'db_table': 'bakhanapp_grade',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id_group', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('kaid_student_tutor_id', models.CharField(max_length=40, null=True, blank=True)),
                ('master', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_group',
            },
        ),
        migrations.CreateModel(
            name='Group_Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_group', models.ForeignKey(to='bakhanapp.Group')),
            ],
            options={
                'db_table': 'bakhanapp_group_student',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id_institution', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('last_load', models.CharField(max_length=50, null=True, blank=True)),
                ('key', models.CharField(max_length=20, null=True, blank=True)),
                ('secret', models.CharField(max_length=20, null=True, blank=True)),
                ('identifier', models.CharField(max_length=50, null=True, blank=True)),
                ('password', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_institution',
            },
        ),
        migrations.CreateModel(
            name='Institutional_Plan',
            fields=[
                ('id_planning', models.AutoField(serialize=False, primary_key=True)),
                ('class_date', models.DateField(null=True, blank=True)),
                ('minutes', models.IntegerField(null=True, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('desc_inicio', models.TextField(null=True, blank=True)),
                ('desc_cierre', models.TextField(null=True, blank=True)),
                ('share_class', models.NullBooleanField(default=False)),
                ('class_name', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'bakhanapp_institutional_plan',
            },
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id_planning', models.AutoField(serialize=False, primary_key=True)),
                ('class_date', models.DateField(null=True, blank=True)),
                ('minutes', models.IntegerField(null=True, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('desc_inicio', models.TextField(null=True, blank=True)),
                ('desc_cierre', models.TextField(null=True, blank=True)),
                ('share_class', models.NullBooleanField(default=False)),
                ('class_name', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('class_subject', models.ForeignKey(to='bakhanapp.Class_Subject')),
            ],
            options={
                'db_table': 'bakhanapp_planning',
            },
        ),
        migrations.CreateModel(
            name='Planning_Log',
            fields=[
                ('id_log', models.AutoField(serialize=False, primary_key=True)),
                ('field', models.TextField()),
                ('old_value', models.TextField(null=True)),
                ('new_value', models.TextField()),
                ('date', models.DateField()),
                ('id_planning', models.ForeignKey(to='bakhanapp.Planning')),
            ],
            options={
                'db_table': 'bakhanapp_planning_log',
            },
        ),
        migrations.CreateModel(
            name='Related_Video_Exercise',
            fields=[
                ('id_related', models.AutoField(serialize=False, primary_key=True)),
                ('id_video', models.CharField(max_length=150, null=True, blank=True)),
                ('id_exercise', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_related_video_exercise',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id_schedule', models.AutoField(serialize=False, primary_key=True)),
                ('start_time', models.CharField(max_length=10, null=True, blank=True)),
                ('end_time', models.CharField(max_length=10, null=True, blank=True)),
                ('name_block', models.CharField(max_length=50, null=True, blank=True)),
                ('id_institution', models.ForeignKey(blank=True, to='bakhanapp.Institution', null=True)),
            ],
            options={
                'db_table': 'bakhanapp_schedule',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id_skill_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150, null=True, blank=True)),
                ('name', models.CharField(max_length=150, null=True, blank=True)),
                ('index', models.IntegerField(null=True, blank=True)),
                ('url_skill', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_skill',
            },
        ),
        migrations.CreateModel(
            name='Skill_Attempt',
            fields=[
                ('id_skill_attempt', models.AutoField(serialize=False, primary_key=True)),
                ('count_attempts', models.IntegerField()),
                ('mission', models.CharField(max_length=150, null=True, blank=True)),
                ('time_taken', models.IntegerField()),
                ('count_hints', models.IntegerField()),
                ('skipped', models.BooleanField()),
                ('points_earned', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('correct', models.BooleanField()),
                ('problem_number', models.IntegerField()),
                ('video', models.NullBooleanField()),
                ('task_type', models.CharField(max_length=150, null=True, blank=True)),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
            ],
            options={
                'db_table': 'bakhanapp_skill_attempt',
            },
        ),
        migrations.CreateModel(
            name='Skill_Institution_Plan',
            fields=[
                ('id_skill_planning', models.AutoField(serialize=False, primary_key=True)),
                ('id_planning', models.ForeignKey(to='bakhanapp.Institutional_Plan')),
                ('id_skill', models.ForeignKey(to='bakhanapp.Skill')),
            ],
            options={
                'db_table': 'bakhanapp_skill_institution_plan',
            },
        ),
        migrations.CreateModel(
            name='Skill_Log',
            fields=[
                ('id_skill_log', models.AutoField(serialize=False, primary_key=True)),
                ('correct', models.IntegerField(null=True, blank=True)),
                ('incorrect', models.IntegerField(null=True, blank=True)),
                ('skill_progress', models.CharField(max_length=20, null=True, blank=True)),
                ('id_grade', models.ForeignKey(blank=True, to='bakhanapp.Grade', null=True)),
                ('id_skill_name', models.ForeignKey(blank=True, to='bakhanapp.Skill', null=True)),
            ],
            options={
                'db_table': 'bakhanapp_skill_log',
            },
        ),
        migrations.CreateModel(
            name='Skill_Planning',
            fields=[
                ('id_skill_planning', models.AutoField(serialize=False, primary_key=True)),
                ('id_planning', models.ForeignKey(to='bakhanapp.Planning')),
                ('id_skill', models.ForeignKey(to='bakhanapp.Skill')),
            ],
            options={
                'db_table': 'bakhanapp_skill_planning',
            },
        ),
        migrations.CreateModel(
            name='Skill_Progress',
            fields=[
                ('id_skill_progress', models.AutoField(serialize=False, primary_key=True)),
                ('to_level', models.CharField(max_length=50)),
                ('from_level', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('kaid_student', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, null=True, blank=True)),
                ('points', models.IntegerField(null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
                ('nickname', models.CharField(max_length=100, null=True, blank=True)),
                ('last_update', models.DateField(null=True, blank=True)),
                ('new_student', models.NullBooleanField()),
                ('id_institution', models.ForeignKey(blank=True, to='bakhanapp.Institution', null=True)),
            ],
            options={
                'db_table': 'bakhanapp_student',
            },
        ),
        migrations.CreateModel(
            name='Student_Class',
            fields=[
                ('id_student_class', models.AutoField(serialize=False, primary_key=True)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
            options={
                'db_table': 'bakhanapp_student_class',
            },
        ),
        migrations.CreateModel(
            name='Student_Skill',
            fields=[
                ('id_student_skill', models.AutoField(serialize=False, primary_key=True)),
                ('total_done', models.IntegerField()),
                ('total_correct', models.IntegerField()),
                ('streak', models.IntegerField()),
                ('longest_streak', models.IntegerField()),
                ('last_skill_progress', models.CharField(max_length=50)),
                ('total_hints', models.IntegerField()),
                ('struggling', models.BooleanField()),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
            options={
                'db_table': 'bakhanapp_student_skill',
            },
        ),
        migrations.CreateModel(
            name='Student_Video',
            fields=[
                ('id_student_video', models.AutoField(serialize=False, primary_key=True)),
                ('total_seconds_watched', models.IntegerField()),
                ('total_points_earned', models.IntegerField()),
                ('last_second_watched', models.IntegerField()),
                ('is_video_complete', models.BooleanField()),
                ('youtube_id', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'bakhanapp_student_video',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id_subject_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'bakhanapp_subject',
            },
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id_subtopic_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150)),
                ('index', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_subtopic',
            },
        ),
        migrations.CreateModel(
            name='Subtopic_Mineduc',
            fields=[
                ('id_subtopic_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('index', models.IntegerField()),
                ('description', models.TextField(null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_subtopic_mineduc',
            },
        ),
        migrations.CreateModel(
            name='Subtopic_Skill',
            fields=[
                ('id_subtopic_skill', models.AutoField(serialize=False, primary_key=True)),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
                ('id_subtopic_name', models.ForeignKey(to='bakhanapp.Subtopic')),
            ],
            options={
                'db_table': 'bakhanapp_subtopic_skill',
            },
        ),
        migrations.CreateModel(
            name='Subtopic_Skill_Mineduc',
            fields=[
                ('id_subtopic_skill_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('id_tree', models.CharField(max_length=50, null=True, blank=True)),
                ('id_skill_name', models.ForeignKey(blank=True, to='bakhanapp.Skill', null=True)),
                ('id_subtopic_mineduc', models.ForeignKey(related_name='subtopic_mineduc', blank=True, to='bakhanapp.Subtopic_Mineduc', null=True)),
            ],
            options={
                'db_table': 'bakhanapp_subtopic_skill_mineduc',
            },
        ),
        migrations.CreateModel(
            name='Subtopic_Video',
            fields=[
                ('id_subtopic_video', models.AutoField(serialize=False, primary_key=True)),
                ('id_subtopic_name', models.ForeignKey(to='bakhanapp.Subtopic')),
            ],
            options={
                'db_table': 'bakhanapp_subtopic_video',
            },
        ),
        migrations.CreateModel(
            name='Subtopic_Video_Mineduc',
            fields=[
                ('id_subtopic_video_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('id_tree', models.CharField(max_length=50, null=True, blank=True)),
                ('id_subtopic_name_mineduc', models.ForeignKey(blank=True, to='bakhanapp.Subtopic_Mineduc', null=True)),
            ],
            options={
                'db_table': 'bakhanapp_subtopic_video_mineduc',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('kaid_teacher', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('id_institution', models.ForeignKey(to='bakhanapp.Institution')),
            ],
            options={
                'db_table': 'bakhanapp_teacher',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id_topic_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150)),
                ('index', models.IntegerField(null=True, blank=True)),
                ('id_chapter_name', models.ForeignKey(to='bakhanapp.Chapter')),
            ],
            options={
                'db_table': 'bakhanapp_topic',
            },
        ),
        migrations.CreateModel(
            name='Topic_Mineduc',
            fields=[
                ('id_topic_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('index', models.IntegerField()),
                ('descripcion_topic', models.TextField(null=True, blank=True)),
                ('suggested_time', models.IntegerField()),
                ('id_chapter', models.ForeignKey(related_name='topic_mineduc', to='bakhanapp.Chapter_Mineduc')),
            ],
            options={
                'db_table': 'bakhanapp_topic_mineduc',
            },
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id_tutor', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150, null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
                ('kaid_student_child', models.ForeignKey(to='bakhanapp.Student')),
            ],
            options={
                'db_table': 'bakhanapp_tutor',
            },
        ),
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('kaid', models.CharField(max_length=40, null=True, blank=True)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bakhanapp_user_profile',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id_video_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150, null=True, blank=True)),
                ('index', models.IntegerField(null=True, blank=True)),
                ('url_video', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'bakhanapp_video',
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
        migrations.CreateModel(
            name='Video_Planning',
            fields=[
                ('id_video_planning', models.AutoField(serialize=False, primary_key=True)),
                ('id_planning', models.ForeignKey(to='bakhanapp.Planning')),
                ('id_subtopic', models.ForeignKey(to='bakhanapp.Subtopic_Video')),
                ('id_video', models.ForeignKey(to='bakhanapp.Video')),
            ],
            options={
                'db_table': 'bakhanapp_video_planning',
            },
        ),
        migrations.CreateModel(
            name='Video_Playing',
            fields=[
                ('id_video_playing', models.AutoField(serialize=False, primary_key=True)),
                ('seconds_watched', models.IntegerField()),
                ('points_earned', models.IntegerField()),
                ('last_second_watched', models.IntegerField()),
                ('is_video_complete', models.BooleanField()),
                ('date', models.DateTimeField()),
                ('id_video_name', models.ForeignKey(to='bakhanapp.Video')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
            options={
                'db_table': 'bakhanapp_video_playing',
            },
        ),
        migrations.AddField(
            model_name='subtopic_video_mineduc',
            name='id_video_name',
            field=models.ForeignKey(blank=True, to='bakhanapp.Video', null=True),
        ),
        migrations.AddField(
            model_name='subtopic_video',
            name='id_video_name',
            field=models.ForeignKey(to='bakhanapp.Video'),
        ),
        migrations.AddField(
            model_name='subtopic_mineduc',
            name='id_topic',
            field=models.ForeignKey(related_name='topic_mineduc', to='bakhanapp.Topic_Mineduc'),
        ),
        migrations.AddField(
            model_name='subtopic',
            name='id_topic_name',
            field=models.ForeignKey(to='bakhanapp.Topic'),
        ),
        migrations.AddField(
            model_name='student_video',
            name='id_video_name',
            field=models.ForeignKey(to='bakhanapp.Video'),
        ),
        migrations.AddField(
            model_name='student_video',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='skill_progress',
            name='id_student_skill',
            field=models.ForeignKey(to='bakhanapp.Student_Skill'),
        ),
        migrations.AddField(
            model_name='skill_planning',
            name='id_subtopic',
            field=models.ForeignKey(to='bakhanapp.Subtopic_Skill'),
        ),
        migrations.AddField(
            model_name='skill_institution_plan',
            name='id_subtopic',
            field=models.ForeignKey(to='bakhanapp.Subtopic_Skill'),
        ),
        migrations.AddField(
            model_name='skill_attempt',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='planning',
            name='class_subtopic',
            field=models.ForeignKey(to='bakhanapp.Subtopic_Mineduc'),
        ),
        migrations.AddField(
            model_name='institutional_plan',
            name='class_subtopic',
            field=models.ForeignKey(to='bakhanapp.Subtopic_Mineduc'),
        ),
        migrations.AddField(
            model_name='institutional_plan',
            name='curriculum',
            field=models.ForeignKey(to='bakhanapp.Chapter_Mineduc'),
        ),
        migrations.AddField(
            model_name='institutional_plan',
            name='institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
        migrations.AddField(
            model_name='group_student',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='grade',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='class_subject',
            name='id_subject_name',
            field=models.ForeignKey(to='bakhanapp.Subject'),
        ),
        migrations.AddField(
            model_name='class_subject',
            name='kaid_teacher',
            field=models.ForeignKey(to='bakhanapp.Teacher'),
        ),
        migrations.AddField(
            model_name='class_schedule',
            name='id_schedule',
            field=models.ForeignKey(blank=True, to='bakhanapp.Schedule', null=True),
        ),
        migrations.AddField(
            model_name='class_schedule',
            name='kaid_teacher',
            field=models.ForeignKey(blank=True, to='bakhanapp.Teacher', null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='id_institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
        migrations.AddField(
            model_name='chapter_mineduc',
            name='id_subject',
            field=models.ForeignKey(to='bakhanapp.Subject'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='id_subject_name',
            field=models.ForeignKey(to='bakhanapp.Subject'),
        ),
        migrations.AddField(
            model_name='assesment_skill',
            name='id_skill_name',
            field=models.ForeignKey(to='bakhanapp.Skill'),
        ),
        migrations.AddField(
            model_name='assesment_skill',
            name='id_subtopic_skill',
            field=models.ForeignKey(blank=True, to='bakhanapp.Subtopic_Skill', null=True),
        ),
        migrations.AddField(
            model_name='assesment_config',
            name='id_subject_name',
            field=models.ForeignKey(to='bakhanapp.Subject'),
        ),
        migrations.AddField(
            model_name='assesment_config',
            name='kaid_teacher',
            field=models.ForeignKey(to='bakhanapp.Teacher'),
        ),
        migrations.AddField(
            model_name='assesment',
            name='id_assesment_conf',
            field=models.ForeignKey(to='bakhanapp.Assesment_Config'),
        ),
        migrations.AddField(
            model_name='assesment',
            name='id_class',
            field=models.ForeignKey(blank=True, to='bakhanapp.Class', null=True),
        ),
        migrations.AddField(
            model_name='administrator',
            name='id_institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
        migrations.AlterUniqueTogether(
            name='video_playing',
            unique_together=set([('date', 'id_video_name', 'kaid_student')]),
        ),
        migrations.AlterUniqueTogether(
            name='video_planning',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_video')]),
        ),
        migrations.AlterUniqueTogether(
            name='video_institution_plan',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_video')]),
        ),
        migrations.AlterUniqueTogether(
            name='topic_mineduc',
            unique_together=set([('index', 'id_chapter')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_video',
            unique_together=set([('id_video_name', 'id_subtopic_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_skill',
            unique_together=set([('id_skill_name', 'id_subtopic_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_mineduc',
            unique_together=set([('index', 'id_topic')]),
        ),
        migrations.AlterUniqueTogether(
            name='student_video',
            unique_together=set([('id_video_name', 'kaid_student')]),
        ),
        migrations.AlterUniqueTogether(
            name='student_class',
            unique_together=set([('id_class', 'kaid_student')]),
        ),
        migrations.AlterUniqueTogether(
            name='skill_planning',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='skill_institution_plan',
            unique_together=set([('id_planning', 'id_subtopic'), ('id_planning', 'id_skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='skill_attempt',
            unique_together=set([('id_skill_name', 'kaid_student', 'problem_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together=set([('start_time', 'end_time', 'id_institution')]),
        ),
        migrations.AlterUniqueTogether(
            name='planning',
            unique_together=set([('class_name', 'class_subject')]),
        ),
        migrations.AlterUniqueTogether(
            name='institutional_plan',
            unique_together=set([('class_name', 'curriculum')]),
        ),
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together=set([('kaid_student', 'id_assesment')]),
        ),
        migrations.AlterUniqueTogether(
            name='class_subject',
            unique_together=set([('id_class', 'id_subject_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='class_schedule',
            unique_together=set([('id_schedule', 'day', 'kaid_teacher')]),
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together=set([('id_institution', 'level', 'letter', 'additional')]),
        ),
        migrations.AlterUniqueTogether(
            name='chapter_mineduc',
            unique_together=set([('level', 'year', 'id_subject')]),
        ),
        migrations.AlterUniqueTogether(
            name='assesment_skill',
            unique_together=set([('id_assesment_config', 'id_skill_name', 'id_subtopic_skill')]),
        ),
    ]
