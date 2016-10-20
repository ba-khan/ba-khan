""" """
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count

from django import template
from bakhanapp.models import Class,Class_Subject, Class_Schedule, Teacher, Schedule, Administrator
from bakhanapp.models import Student_Class
from bakhanapp.models import Tutor
from configs import timeSleep
register = template.Library()

import json


##
## @brief      Gets the contacts.
##
## @param      request   The request
## @param      id_class  The identifier class
##
## @return     The contacts.
##
@login_required()
def getSchedules(request, id_class):
	request.session.set_expiry(timeSleep)
	classroom = Class.objects.filter(id_class=id_class)
	N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
	spanish_classroom = N[int(classroom[0].level)] +' '+ classroom[0].letter
	if (Administrator.objects.filter(kaid_administrator=request.user.user_profile.kaid) or Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True
	else:
		isTeacher = False
	try:
		teacher = Teacher.objects.get(email=request.user.email)
	except:
		return render_to_response('schedules.html', context_instance=RequestContext(request))
	schedules = Schedule.objects.filter(id_institution_id=teacher.id_institution_id).order_by('start_time')
	teacher = Class_Subject.objects.filter(id_class_id=id_class).values('kaid_teacher_id')
	class_schedule = Class_Schedule.objects.filter(kaid_teacher_id=teacher[0]['kaid_teacher_id'])
	if(request.user.has_perm('bakhanapp.isAdmin')):
		classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).order_by('level','letter')
	else:
		classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class')).order_by('level','letter')
	N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
	for i in range(len(classes)):
		classes[i].nivel = N[int(classes[i].level)] 
	return render_to_response('schedules.html', {'spanish_classroom':spanish_classroom, 'schedules': schedules, 'class_schedule': class_schedule, 'id_class':id_class, 'teacher':teacher, 'isTeacher':isTeacher, 'classes':classes}, context_instance=RequestContext(request))

@login_required()
def saveScheduleClass(request, id_class):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		try:
			args = request.POST
			dias = args.getlist('values[]')
			teacher = Class_Subject.objects.filter(id_class_id=id_class).values('kaid_teacher_id')
			class_schedule = Class_Schedule.objects.filter(kaid_teacher_id=teacher[0]['kaid_teacher_id'], id_class_id=id_class).update(id_class_id=None)
			for dia in dias:
				diasplit = dia.split('_')
				class_schedule = Class_Schedule.objects.filter(kaid_teacher_id=teacher[0]['kaid_teacher_id'], day=diasplit[0], id_schedule_id=int(diasplit[1])).update(id_class_id=id_class)
				#print "class schedule esta abajo"
				#print class_schedule[0]['id_class_schedule']
				#Class_Schedule.objects.filter(pk=class_schedule[0]['id_class_schedule']).update(id_class_id=id_class)
				#print update_schedule_class
				#update_schedule_class.id_class_id=id_class
			return HttpResponse('Horario para el profesor guardado')
		except Exception as e:
			print e

	return HttpResponse('Error al guardar')