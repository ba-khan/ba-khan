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
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher

register = template.Library()
from configs import timeSleep

import json


@permission_required('bakhanapp.isAdmin', login_url="/")
def getRoster(request):
    request.session.set_expiry(timeSleep)
    #try:
    #    teacher = Teacher.objects.get(email=request.user.email)
    #except:
    #    return render_to_response('administrators.html', context_instance=RequestContext(request))
    #administrators = Administrator.objects.filter(id_institution=teacher.id_institution_id).order_by('name')
    #print administrators
    #return render_to_response('classRoster.html', {'administrators': administrators}, context_instance=RequestContext(request))
    return render_to_response('classRoster.html', context_instance=RequestContext(request))