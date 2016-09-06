""" """
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule, Class
from bakhanapp.models import Schedule
from django.db import connection

register = template.Library()
from configs import timeSleep

import json


##
## @brief      Gets the schedules.
##
## @param      request  The request
##
## @return     The schedules.
##
@login_required()
def getStatistics(request):
	request.session.set_expiry(timeSleep)
	try:
		teacher = Teacher.objects.get(email=request.user.email)
	except:
		return render_to_response('statistics.html', context_instance=RequestContext(request))
	if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True
	else:
		isTeacher = False
	if(request.user.has_perm('bakhanapp.isAdmin')):
		classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).order_by('level','letter')
	else:
		classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class')).order_by('level','letter')
	schedules = Schedule.objects.filter(id_institution_id=teacher.id_institution_id).order_by('start_time')
	return render_to_response('statistics.html', {'isTeacher': isTeacher, 'classes':classes, 'schedules':schedules} ,context_instance=RequestContext(request))
