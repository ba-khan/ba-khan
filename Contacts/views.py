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
from bakhanapp.models import Student

register = template.Library()

import json

@login_required()
def getContacts(request, id_class):#url configuraciones
    #Esta funcion entrega todas las configuraciones de evaluaciones realizadas por un profesor
    
    return render_to_response('contacts.html', context_instance=RequestContext(request))