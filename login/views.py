# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from .forms import loginForm
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
from random import randint

import time

from websocket_server import WebsocketServer


def login(request):
    return render_to_response('login.html', context_instance=RequestContext(request))

def rejected(request):
    return render(request, 'rejected.html')


def authenticateUser(request):
    authorized = False
    if request.method == 'POST':
        args = request.POST
        username = args["username"]
        email = args["email"]
        #print username+" "+email
        user = auth.authenticate(username=username, password=email)
        if user:
            auth.login(request, user)
            authorized = True
            return HttpResponse(authorized)
        else:
            autorized=True
            return HttpResponse(authorized)
            user = User.objects.create_user(username=username,email=email,password=email)
            user.save()
            #user2 = auth.authenticate(username=username, password=email)
            #if user2:
            auth.login(request, user)
            authorized = True
            return HttpResponse(authorized)
    return HttpResponse(authorized)