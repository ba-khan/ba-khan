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
	chapter = Chapter_Mineduc.objects.all()
	#topic = Topic_Mineduc.objects.all()
	mision=[]
	for chap in chapter:
		capitulo={}
		capitulo["id"]=chap.id_chapter_mineduc
		capitulo["nombre"]=chap.name
		unidad=[]
		topic = Topic_Mineduc.objects.filter(id_chapter_id=chap.id_chapter_mineduc)
		for top in topic:
			topico={}
			topico["id"]=top.id_topic_mineduc
			topico["nombre"]=top.name
			aprendizaje=[]
			subtopic = Subtopic_Mineduc.objects.filter(id_topic_id=top.id_topic_mineduc)
			for sub in subtopic:
				subtopico={}
				subtopico["id"]=sub.id_subtopic_mineduc
				subtopico["nombre"]=sub.name
				aprendizaje.append(subtopico)
			topico["subtopico"]=aprendizaje
			unidad.append(topico)
		capitulo["topico"]=unidad
		mision.append(capitulo)
	json_dict={"capitulos":mision}
	json_data = json.dumps(json_dict)
	return render_to_response('curriculum.html', { 'json_data':json_data} ,context_instance=RequestContext(request))

@permission_required('bakhanapp.isSuper', login_url="/")
def newChapter(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			Chapter_Mineduc.objects.create(name=args['name'])
			return HttpResponse('Chapter guardado correctamente')

		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def newTopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			#topico = args['nombre']
			#curso = formulario.split('nameTopic=')
			#topico = curso[1].replace('+', ' ')
			Topic_Mineduc.objects.create(name=args['nombre'], id_chapter_id=args['curso'])
			return HttpResponse('Topic guardado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def newSubtopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			#formulario = args['form']
			#curso = formulario.split('nameSubtopic=')
			#topico = curso[1].replace('+', ' ')
			Subtopic_Mineduc.objects.create(name=args['nombre'], id_topic_id=args['curso'])
			return HttpResponse('Subtopic guardado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")