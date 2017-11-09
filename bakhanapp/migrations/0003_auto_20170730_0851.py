# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakhanapp', '0002_auto_20170730_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter_mineduc',
            name='additional',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='chapter_mineduc',
            name='id_subject',
            field=models.ForeignKey(default=1, to='bakhanapp.Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapter_mineduc',
            name='level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapter_mineduc',
            name='year',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planning',
            name='class_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='planning',
            name='class_name',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planning',
            name='class_subject',
            field=models.ForeignKey(default=1, to='bakhanapp.Class_Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planning',
            name='class_subtopic',
            field=models.ForeignKey(default=1, to='bakhanapp.Subtopic_Mineduc'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planning',
            name='desc_cierre',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='planning',
            name='desc_inicio',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='planning',
            name='minutes',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='planning',
            name='share_class',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='planning',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subtopic_mineduc',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subtopic_mineduc',
            name='summary',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subtopic_mineduc',
            name='id_topic',
            field=models.ForeignKey(default=1, to='bakhanapp.Topic_Mineduc'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subtopic_mineduc',
            name='index',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='descripcion_topic',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='id_chapter',
            field=models.ForeignKey(default=1, to='bakhanapp.Chapter_Mineduc'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic_mineduc',
            name='index',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='chapter_mineduc',
            unique_together=set([('level', 'year', 'id_subject')]),
        ),
        migrations.AlterUniqueTogether(
            name='planning',
            unique_together=set([('class_name', 'class_subject')]),
        ),
        migrations.AlterUniqueTogether(
            name='subtopic_mineduc',
            unique_together=set([('index', 'id_topic')]),
        ),
        migrations.AlterUniqueTogether(
            name='topic_mineduc',
            unique_together=set([('index', 'id_chapter')]),
        ),
        migrations.RemoveField(
            model_name='chapter_mineduc',
            name='index',
        ),
        migrations.RemoveField(
            model_name='chapter_mineduc',
            name='name',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='cierre',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='clase',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='curso',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='ejerciciokhan',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='inicio',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='oa',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='objetivo',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='planning',
            name='videokhan',
        ),
        migrations.RemoveField(
            model_name='subtopic_mineduc',
            name='ae_oe',
        ),
        migrations.RemoveField(
            model_name='subtopic_mineduc',
            name='name',
        ),
        migrations.RemoveField(
            model_name='topic_mineduc',
            name='name',
        ),
    ]
