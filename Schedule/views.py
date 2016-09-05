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
from bakhanapp.models import Student, Class,Class_Subject
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
    return HttpResponse("hola")