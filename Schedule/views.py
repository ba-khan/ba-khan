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
from bakhanapp.models import Class,Class_Subject, Class_Schedule, Teacher, Schedule
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
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except:
        return render_to_response('schedules.html', context_instance=RequestContext(request))
    schedules = Schedule.objects.filter(id_institution_id=teacher.id_institution_id).order_by('start_time')
    teachers = Teacher.objects.filter(id_institution_id=teacher.id_institution_id)
    class_schedule = Class_Schedule.objects.filter(kaid_teacher_id__in=teachers)
    return render_to_response('schedules.html', {'schedules': schedules, 'teachers': teachers, 'class_schedule': class_schedule}, context_instance=RequestContext(request))
