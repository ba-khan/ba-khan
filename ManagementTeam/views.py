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
from bakhanapp.models import Assesment_Skill

register = template.Library()

# Create your views here.
@login_required()
def getAdministrators(request):
    
    return render_to_response('administrators.html', context_instance=RequestContext(request))

@login_required()
def newAdministrator(request):
    return HttpResponse("Pauta Eliminada")

@login_required()
def editAdministrator(request):
    
    return HttpResponse("Pauta Eliminada")

@login_required()
def deleteAdministrator(request):
    
    return HttpResponse("Pauta Eliminada")