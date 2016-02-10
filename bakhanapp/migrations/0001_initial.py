# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('kaid_administrator', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Assesment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Assesment_Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approval_percentage', models.IntegerField()),
                ('top_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Assesment_skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_assesment_conf', models.ForeignKey(to='bakhanapp.Assesment_Config')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id_chapter_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name_esp', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=50)),
                ('letter', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Class_Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.IntegerField()),
                ('performance_point', models.IntegerField()),
                ('effort_points', models.IntegerField()),
                ('id_assesment', models.ForeignKey(to='bakhanapp.Assesment')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
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
                ('id_institution', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id_skill_name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('name_esp', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('errors', models.IntegerField()),
                ('mission', models.CharField(max_length=100)),
                ('time_taken', models.IntegerField()),
                ('count_hints', models.IntegerField()),
                ('skipped', models.BooleanField()),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('kaid_student', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=50)),
                ('tutor_name', models.CharField(max_length=50)),
                ('tutor_mail', models.EmailField(max_length=254)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student_Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_class', models.ForeignKey(to='bakhanapp.Class')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_done', models.IntegerField()),
                ('total_correct', models.IntegerField()),
                ('streak', models.IntegerField()),
                ('longest_streak', models.IntegerField()),
                ('exercises_states', models.CharField(max_length=30)),
                ('exercise_progress', models.CharField(max_length=30)),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_seconds_watched', models.IntegerField()),
                ('total_points_earned', models.IntegerField()),
                ('last_second_watched', models.IntegerField()),
                ('is_video_complete', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id_subject', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id_subtopic_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name_esp', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('kaid_teacher', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('id_institution', models.ForeignKey(to='bakhanapp.Institution')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id_topic_name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('name_esp', models.CharField(max_length=50)),
                ('id_chapter_name', models.ForeignKey(to='bakhanapp.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id_video_name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('name_esp', models.CharField(max_length=100)),
                ('id_subtopic_name', models.ForeignKey(to='bakhanapp.Subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='Video_Playing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seconds_watched', models.IntegerField()),
                ('points_earned', models.IntegerField()),
                ('last_second_watched', models.IntegerField()),
                ('is_video_complete', models.BooleanField()),
                ('id_skill_name', models.ForeignKey(to='bakhanapp.Skill')),
                ('kaid_student', models.ForeignKey(to='bakhanapp.Student')),
            ],
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
            model_name='skill_attempt',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='skill',
            name='id_subtopic_name',
            field=models.ForeignKey(to='bakhanapp.Subtopic'),
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
            name='id_subject',
            field=models.ForeignKey(to='bakhanapp.Subject'),
        ),
        migrations.AddField(
            model_name='class_subject',
            name='kaid_teacher',
            field=models.ForeignKey(to='bakhanapp.Teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='id_institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
        migrations.AddField(
            model_name='class',
            name='kaid_teacher',
            field=models.ForeignKey(to='bakhanapp.Teacher'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='id_subject',
            field=models.ForeignKey(to='bakhanapp.Subject'),
        ),
        migrations.AddField(
            model_name='assesment_skill',
            name='id_skill_name',
            field=models.ForeignKey(to='bakhanapp.Skill'),
        ),
        migrations.AddField(
            model_name='assesment_config',
            name='id_subject',
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
            model_name='administrator',
            name='id_institution',
            field=models.ForeignKey(to='bakhanapp.Institution'),
        ),
    ]
