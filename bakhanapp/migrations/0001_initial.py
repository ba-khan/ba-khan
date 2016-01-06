# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('kaid', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Configuracion_Evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentaje_exigencia', models.IntegerField()),
                ('puntaje_max', models.IntegerField()),
                ('id_asignatura', models.ForeignKey(to='bakhanapp.Asignatura')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nivel', models.CharField(max_length=50)),
                ('letra', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Curso_Asignatura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_asignatura', models.ForeignKey(to='bakhanapp.Asignatura')),
                ('id_curso', models.ForeignKey(to='bakhanapp.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('ciudad', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('kaid', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=50)),
                ('nombreApoderado', models.CharField(max_length=50)),
                ('mailApoderado', models.EmailField(max_length=254)),
                ('observacion', models.CharField(max_length=300)),
                ('puntos', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante_Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_curso', models.ForeignKey(to='bakhanapp.Curso')),
                ('id_estudiante', models.ForeignKey(to='bakhanapp.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante_Habilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_done', models.IntegerField()),
                ('total_correct', models.IntegerField()),
                ('streak', models.IntegerField()),
                ('longest_streak', models.IntegerField()),
                ('exercises_states', models.CharField(max_length=30)),
                ('exercise_progress', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante_Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seconds_watched', models.IntegerField()),
                ('points_earned', models.IntegerField()),
                ('last_second_watched', models.IntegerField()),
                ('is_video_complete', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_termino', models.DateField()),
                ('id_conf_ev', models.ForeignKey(to='bakhanapp.Configuracion_Evaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluacion_habilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_conf_ev', models.ForeignKey(to='bakhanapp.Configuracion_Evaluacion')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('kaid_est_tutor', models.ForeignKey(to='bakhanapp.Estudiante', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo_Estudiante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_grupo', models.ForeignKey(to='bakhanapp.Grupo')),
                ('kaid_est', models.ForeignKey(to='bakhanapp.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Habilidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kaid_est', models.CharField(max_length=30)),
                ('id_evaluacion', models.CharField(max_length=30)),
                ('nota', models.IntegerField()),
                ('puntos_desempeno', models.IntegerField()),
                ('puntos_empeno', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('kaid', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subtema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('id_unidad', models.ForeignKey(to='bakhanapp.Asignatura')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='tema',
            name='id_unidad',
            field=models.ForeignKey(to='bakhanapp.Unidad'),
        ),
        migrations.AddField(
            model_name='subtema',
            name='id_tema',
            field=models.ForeignKey(to='bakhanapp.Tema'),
        ),
        migrations.AddField(
            model_name='evaluacion_habilidad',
            name='id_habilidad',
            field=models.ForeignKey(to='bakhanapp.Habilidad'),
        ),
        migrations.AddField(
            model_name='estudiante_video',
            name='id_video',
            field=models.ForeignKey(to='bakhanapp.Video'),
        ),
        migrations.AddField(
            model_name='estudiante_video',
            name='kaid_est',
            field=models.ForeignKey(to='bakhanapp.Estudiante'),
        ),
        migrations.AddField(
            model_name='estudiante_habilidad',
            name='id_habilidad',
            field=models.ForeignKey(to='bakhanapp.Habilidad'),
        ),
        migrations.AddField(
            model_name='estudiante_habilidad',
            name='id_mision',
            field=models.ForeignKey(to='bakhanapp.Mision', null=True),
        ),
        migrations.AddField(
            model_name='estudiante_habilidad',
            name='kaid_est',
            field=models.ForeignKey(to='bakhanapp.Estudiante'),
        ),
        migrations.AddField(
            model_name='curso_asignatura',
            name='id_profesor',
            field=models.ForeignKey(to='bakhanapp.Profesor'),
        ),
        migrations.AddField(
            model_name='curso',
            name='establecimiento',
            field=models.ForeignKey(to='bakhanapp.Establecimiento'),
        ),
        migrations.AddField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(to='bakhanapp.Profesor'),
        ),
        migrations.AddField(
            model_name='configuracion_evaluacion',
            name='id_profesor',
            field=models.ForeignKey(to='bakhanapp.Profesor'),
        ),
    ]
