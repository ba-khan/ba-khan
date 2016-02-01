# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count

from django import template
from bakhanapp.models import Assesment_Skill
register = template.Library()

from bakhanapp.models import Class
from bakhanapp.models import Teacher
from bakhanapp.models import Skill
from bakhanapp.models import Skill_Progress
from bakhanapp.models import Student
from bakhanapp.models import Student_Class
from bakhanapp.models import Student_Video
from bakhanapp.models import Student_Skill
from bakhanapp.models import Video
from bakhanapp.models import Video_Playing
from bakhanapp.models import Skill_Attempt
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Class_Subject
from bakhanapp.models import Assesment
from bakhanapp.models import Assesment_Config
from bakhanapp.models import Subtopic_Skill
from bakhanapp.models import Subtopic_Video
from bakhanapp.models import Grade,Skill
from bakhanapp.models import Student_Skill
from bakhanapp.models import Skill_Progress
from bakhanapp.models import Subject
from bakhanapp.models import Chapter
from bakhanapp.models import Topic
from bakhanapp.models import Subtopic
from bakhanapp.models import Subtopic_Skill

import datetime

import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser
import psycopg2

import json
import simplejson
import sys
from pprint import pprint
import codecs
from lib2to3.fixer_util import String
from django.core import serializers
from django.db import connection

import random


def newAssesment3(request):
    if request.method == 'POST':
        args = request.POST
        fecha1=args['fecha_inicio']
        fecha2=args['fecha_termino']
        nota1=eval(args['nota_minima'])
        nota2=eval(args['nota_maxima'])
        id_config=(args['input_id_config'])
        nombre_config=args['input_nombre']
        students=eval(args['input_kaid'])
        id_class=eval(args['input_id_class'])

        new_assesment = Assesment(start_date=fecha1,
                               end_date=fecha2,
                               id_assesment_conf_id=id_config,
                               min_grade=nota1,
                               max_grade=nota2,
                               name=nombre_config,
                               id_class_id=id_class
                               )
        new_assesment.save()
        id_new_assesment=new_assesment.pk
        for s in students:
            #s['kaid_student']
            #id_new_assesment
            new_grade = Grade(grade=0,
                               teacher_grade=0,
                               performance_points=0,
                               effort_points=0,
                               id_assesment_id=id_new_assesment,
                               kaid_student_id=s['kaid_student']
                               )
            new_grade.save()
            update_assesment_configs = Assesment_Config.objects.get(pk=id_config)
            update_assesment_configs.applied = True
            update_assesment_configs.save() 
    return HttpResponse()