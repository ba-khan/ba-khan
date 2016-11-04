# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('kaid_administrator', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('phone', models.IntegerField(null=True)),
            ],
            options={
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
                ('max_grade', models.IntegerField()),
                ('min_grade', models.IntegerField()),
                ('approval_grade', models.IntegerField()),
                ('max_effort_bonus', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Assesment_Config',
            fields=[
                ('id_assesment_config', models.AutoField(serialize=False, primary_key=True)),
                ('approval_percentage', models.IntegerField()),
                ('top_score', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('importance_skill_level', models.IntegerField()),
                ('importance_completed_rec', models.IntegerField()),
                ('applied', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Assesment_Skill',
            fields=[
                ('id_assesment_skill', models.AutoField(serialize=False, primary_key=True)),
                ('id_assesment_config', models.ForeignKey(to='bakhanapp.Assesment_Config')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id_chapter_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150)),
                ('index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Chapter_Mineduc',
            fields=[
                ('id_chapter_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('index', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id_class', models.AutoField(serialize=False, primary_key=True)),
                ('level', models.IntegerField()),
                ('letter', models.CharField(max_length=2)),
                ('year', models.IntegerField()),
                ('additional', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Class_Schedule',
            fields=[
                ('id_class_schedule', models.AutoField(serialize=False, primary_key=True)),
                ('day', models.CharField(max_length=20)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Class_Subject',
            fields=[
                ('id_class_subject', models.AutoField(serialize=False, primary_key=True)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id_grade', models.AutoField(serialize=False, primary_key=True)),
                ('grade', models.FloatField()),
                ('teacher_grade', models.FloatField(null=True)),
                ('performance_points', models.FloatField()),
                ('effort_points', models.FloatField()),
                ('recomended_complete', models.IntegerField(null=True)),
                ('excercice_time', models.IntegerField(default=0, null=True)),
                ('video_time', models.IntegerField(default=0, null=True)),
                ('correct', models.IntegerField(default=0, null=True)),
                ('incorrect', models.IntegerField(default=0, null=True)),
                ('hints', models.IntegerField(default=0, null=True)),
                ('videos', models.IntegerField(default=0, null=True)),
                ('nothing', models.IntegerField(default=0, null=True)),
                ('struggling', models.IntegerField(default=0, null=True)),
                ('practiced', models.IntegerField(default=0, null=True)),
                ('mastery1', models.IntegerField(default=0, null=True)),
                ('mastery2', models.IntegerField(default=0, null=True)),
                ('mastery3', models.IntegerField(default=0, null=True)),
                ('comment', models.CharField(max_length=300, null=True)),
                ('evaluated', models.BooleanField(default=False)),
                ('bonus_grade', models.FloatField(default=0.0, null=True)),
                ('unstarted', models.IntegerField(default=0, null=True)),
                ('total_recomended', models.IntegerField(default=0, null=True)),
                ('id_assesment', models.ForeignKey(to='bakhanapp.Assesment')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id_group', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('master', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Group_Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_group', models.ForeignKey(to='bakhanapp.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id_institution', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('last_load', models.CharField(max_length=25)),
                ('key', models.CharField(max_length=20)),
                ('secret', models.CharField(max_length=20)),
                ('identifier', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id_schedule', models.AutoField(serialize=False, primary_key=True)),
                ('start_time', models.CharField(max_length=10)),
                ('end_time', models.CharField(max_length=10)),
                ('name_block', models.CharField(max_length=50)),
                ('id_institution', models.ForeignKey(to='bakhanapp.Institution')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id_skill_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150, null=True)),
                ('name', models.CharField(max_length=150, null=True)),
                ('index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Attempt',
            fields=[
                ('id_skill_attempt', models.AutoField(serialize=False, primary_key=True)),
                ('problem_number', models.IntegerField()),
                ('count_attempts', models.IntegerField()),
                ('mission', models.CharField(max_length=150, null=True)),
                ('time_taken', models.IntegerField()),
                ('count_hints', models.IntegerField()),
                ('skipped', models.BooleanField()),
                ('points_earned', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('correct', models.BooleanField()),
                ('video', models.BooleanField(default=False)),
                ('task_type', models.CharField(max_length=150, null=True)),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Log',
            fields=[
                ('id_skill_log', models.AutoField(serialize=False, primary_key=True)),
                ('correct', models.IntegerField(null=True)),
                ('incorrect', models.IntegerField(null=True)),
                ('skill_progress', models.CharField(max_length=20)),
                ('id_grade', models.ForeignKey(to='bakhanapp.Grade')),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
            ],
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
                ('email', models.EmailField(max_length=50, null=True)),
                ('phone', models.IntegerField(null=True)),
                ('points', models.IntegerField()),
                ('nickname', models.CharField(max_length=100)),
                ('last_update', models.DateField()),
                ('new_student', models.BooleanField()),
                ('id_institution', models.ForeignKey(to='bakhanapp.Institution')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Class',
            fields=[
                ('id_student_class', models.AutoField(serialize=False, primary_key=True)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
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
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id_subject_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id_subtopic_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150)),
                ('index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic_Mineduc',
            fields=[
                ('id_subtopic_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('AE_OE', models.CharField(max_length=200)),
                ('index', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic_Skill',
            fields=[
                ('id_subtopic_skill', models.AutoField(serialize=False, primary_key=True)),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
                ('id_subtopic_name', models.ForeignKey(to='bakhanapp.Subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic_Skill_Mineduc',
            fields=[
                ('id_subtopic_skill_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
                ('id_subtopic_mineduc', models.ForeignKey(to='bakhanapp.Subtopic_Mineduc')),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic_Video',
            fields=[
                ('id_subtopic_video', models.AutoField(serialize=False, primary_key=True)),
                ('id_subtopic_name', models.ForeignKey(to='bakhanapp.Subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic_Video_Mineduc',
            fields=[
                ('id_subtopic_video_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('id_subtopic_name_mineduc', models.ForeignKey(to='bakhanapp.Subtopic_Mineduc')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('kaid_teacher', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('id_institution', models.ForeignKey(to='bakhanapp.Institution')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id_topic_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150)),
                ('index', models.IntegerField()),
                ('id_chapter_name', models.ForeignKey(to='bakhanapp.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Topic_Mineduc',
            fields=[
                ('id_topic_mineduc', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('index', models.IntegerField()),
                ('id_chapter', models.ForeignKey(to='bakhanapp.Chapter_Mineduc')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id_tutor', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('phone', models.IntegerField(null=True)),
                ('kaid_student_child', models.ForeignKey(to='bakhanapp.Student')),
            ],
        ),
        migrations.CreateModel(
            name='User_Profile',
            fields=[
                ('kaid', models.CharField(max_length=40)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id_video_name', models.CharField(max_length=150, serialize=False, primary_key=True)),
                ('name_spanish', models.CharField(max_length=150, null=True)),
                ('index', models.IntegerField()),
                ('related_skill', models.CharField(max_length=150, null=True)),
            ],
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
        ),
        migrations.AddField(
            model_name='subtopic_video_mineduc',
            name='id_video_name',
            field=models.ForeignKey(to='bakhanapp.Video'),
        ),
        migrations.AddField(
            model_name='subtopic_video',
            name='id_video_name',
            field=models.ForeignKey(to='bakhanapp.Video'),
        ),
        migrations.AddField(
            model_name='subtopic_mineduc',
            name='id_topic',
            field=models.ForeignKey(to='bakhanapp.Topic_Mineduc'),
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
            model_name='skill_attempt',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='group_student',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='group',
            name='kaid_student_tutor',
            field=models.ForeignKey(to='bakhanapp.Student', null=True),
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
            field=models.ForeignKey(to='bakhanapp.Schedule'),
        ),
        migrations.AddField(
            model_name='class_schedule',
            name='kaid_teacher',
            field=models.ForeignKey(to='bakhanapp.Teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='id_institution',
            field=models.ForeignKey(related_name='id_institution_class', to='bakhanapp.Institution'),
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
            field=models.ForeignKey(to='bakhanapp.Subtopic_Skill'),
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
            field=models.ForeignKey(to='bakhanapp.Class'),
        ),
        migrations.AddField(
            model_name='administrator',
            name='id_institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_video_mineduc',
            unique_together=set([('id_video_name', 'id_subtopic_name_mineduc')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_video',
            unique_together=set([('id_video_name', 'id_subtopic_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_skill_mineduc',
            unique_together=set([('id_skill_name', 'id_subtopic_mineduc')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_skill',
            unique_together=set([('id_skill_name', 'id_subtopic_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='student_video',
            unique_together=set([('id_video_name', 'kaid_student')]),
        ),
        migrations.AlterUniqueTogether(
            name='student_skill',
            unique_together=set([('id_skill_name', 'kaid_student')]),
        ),
        migrations.AlterUniqueTogether(
            name='student_class',
            unique_together=set([('id_class', 'kaid_student')]),
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
            unique_together=set([('id_institution', 'level', 'letter', 'year', 'additional')]),
        ),
        migrations.AlterUniqueTogether(
            name='assesment_skill',
            unique_together=set([('id_assesment_config', 'id_skill_name')]),
        ),
    ]
