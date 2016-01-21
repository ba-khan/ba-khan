# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect
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
from bakhanapp.models import Skill
from bakhanapp.models import Skill_Progress
from bakhanapp.models import Student
from bakhanapp.models import Student_Class
from bakhanapp.models import Student_Video
from bakhanapp.models import Student_Skill
from bakhanapp.models import Video_Playing
from bakhanapp.models import Skill_Attempt
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Class_Subject
from bakhanapp.models import Assesment
from bakhanapp.models import Assesment_Config
from bakhanapp.models import Subtopic_Skill
from bakhanapp.models import Subtopic_Video
from bakhanapp.models import Grade,Skill,Student_Skill,Skill_Progress
from bakhanapp.models import Subject,Chapter,Topic,Subtopic,Subtopic_Skill

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

from bakhanapp.models import Group
from django.utils import timezone


# Create your views here.
@login_required()
def getGroups(request, id_class):

    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))

    return render_to_response('groups.html',{'students': students},context_instance=RequestContext(request))

def save_groups(request,id_class):
	#Funcion de prueba que crea un nuevo grupo con datos de prueba
	g = Group()
	g.name = 'test'
	g.type = 'avanzado'
	g.start_date = timezone.now()
	g.end_date = timezone.now()
	g.kaid_student_tutor_id = 'kaid_1097501097555535353578558'
	g.save()
	return render (request,'groups.html')

def make_groups(request,id_class):
	#Funcion que entrega un arreglo con los estudiantes y su nivel de agrupamiento.
	students = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#retorna todos los estudiantes de un curso
	if request.method == 'POST':
		args = request.POST
		for s in students:
			#Por cada estudiante en id_class, se obtiene su agrupacion.
			s.type = getTypeStudent(s.kaid_student,args) #args debe contener todas las id de las skill seleccionadas para el agrupamiento.
			return s

def getTypeStudent(request,kaid_student,args):
	#Funcion que entrega en que nivel grupo debe ser organizado un estudiante
	#de acuerdo a su nivel en las skills seleccionadas por el profesor.
	#skills = Group_Skill.objects.filter(id_group_id=id_group)
	for skill in args:
		student_progress = Student_Skill.objects.filter(id_skill_name_id=skill['id_skill_id']).values('last_skill_progress')
		if student_progress == 'struggling' or student_progress == 'unstarted':
			return 'reinforcement'
		if student_progress == 'mastery1' or student_progress == 'mastery2':
			return 'intermediate'
		else:
			return 'advanced'
