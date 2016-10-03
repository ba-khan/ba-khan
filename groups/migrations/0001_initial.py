# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_Group',
            fields=[
                ('id_group', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('date_int', models.IntegerField()),
                ('kaid_teacher', models.CharField(max_length=40)),
                ('id_class', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student_Sub_Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_group', models.ForeignKey(to='bakhanapp.Group')),
            ],
        ),
        migrations.AddField(
            model_name='student_sub_group',
            name='id_sub_group',
            field=models.ForeignKey(to='groups.Sub_Group'),
        ),
        migrations.AddField(
            model_name='student_sub_group',
            name='kaid_student',
            field=models.ForeignKey(to='bakhanapp.Student'),
        ),
        migrations.AddField(
            model_name='group_skill',
            name='id_group',
            field=models.ForeignKey(to='groups.Master_Group'),
        ),
        migrations.AddField(
            model_name='group_skill',
            name='id_skill',
            field=models.ForeignKey(to='bakhanapp.Skill'),
        ),
    ]