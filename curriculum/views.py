""" """
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count, Sum
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core import serializers


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule, Class, Student_Class, Skill_Attempt, Student, Video_Playing, Institution
from bakhanapp.models import Chapter_Mineduc, Topic_Mineduc, Subtopic_Mineduc, Subtopic_Skill_Mineduc
from django.db import connection

register = template.Library()
from configs import timeSleep

import json
from datetime import datetime, timedelta


##
## @brief      Gets the schedules.
##
## @param      request  The request
##
## @return     The schedules.
##
@permission_required('bakhanapp.isSuper', login_url="/")
def getCurriculum(request):
	request.session.set_expiry(timeSleep)
	#chapter = Chapter_Mineduc.objects.all()
	return render_to_response('curriculum.html')

@permission_required('bakhanapp.isSuper', login_url="/")
def newChapter(request):
	#print "entro a newchapter"
	request.session.set_expiry(timeSleep)
	#user = Teacher.objects.get(email=request.user.email)
	if request.method == 'POST':
		args = request.POST
		try:
			#print args['name']
			Chapter_Mineduc.objects.create(name=args['name'])
			return HttpResponse('Chapter guardado correctamente')
			#falta validar que los bloques no se solapen
			'''
			result=validateTime(args['start'], args['end'], user.id_institution_id, args['block'])
			if not all(result):
			return HttpResponse("Los horarios no se pueden solapar, revise las horas")
			else:
			Schedule.objects.create(name_block=args['block'],
			start_time=args['start'],
			end_time=args['end'],
			id_institution_id=user.id_institution_id)
			return HttpResponse("Bloque guardado correctamente")    
			''' 
		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")