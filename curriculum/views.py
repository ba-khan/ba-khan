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
from bakhanapp.models import Subtopic_Video, Chapter, Topic, Subtopic, Subtopic_Skill, Skill, Video, Subject
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

	topictree_json={}
	topictree_json['checkbox']={'keep_selected_style':False}
	topictree_json['plugins']=['checkbox','search']
	topictree=[]
	subjects=Subject.objects.all()
	for subject in subjects:
	    subject_obj={"id": subject.id_subject_name, "parent":"#", "text": subject.name_spanish, "state": {"opened":"true"}, "icon":"false"}
	    topictree.append(subject_obj)
	subject_chapter=Chapter.objects.exclude(index=None).order_by('index')
	for chapter in subject_chapter:
	    chapter_obj={"id":chapter.id_chapter_name, "parent": chapter.id_subject_name_id, "text":chapter.name_spanish, "icon":"false"}
	    topictree.append(chapter_obj)
	chapter_topic=Topic.objects.exclude(index=None).order_by('index')
	for topic in chapter_topic:
	    topic_obj={"id":topic.id_topic_name, "parent": topic.id_chapter_name_id, "text":topic.name_spanish, "icon":"false"}
	    topictree.append(topic_obj)
	topic_subtopic=Subtopic.objects.exclude(index=None).order_by('index')
	for subtopic in topic_subtopic:
	    subtopic_obj={"id":subtopic.id_subtopic_name, "parent": subtopic.id_topic_name_id, "text":subtopic.name_spanish, "icon":"false"}
	    topictree.append(subtopic_obj)
	subtopic_skill=Subtopic_Skill.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_skill_name')
	id=0
	for skill in subtopic_skill:
	    skill_id=skill.id_subtopic_skill
	    skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
	    sorted(skill_obj, key=skill_obj.get)
	    topictree.append(skill_obj)
	    id=id+1
	subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
	for video in subtopic_video:
		video_id=video.id_subtopic_video
		video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name},"index":video.id_video_name.index}
		sorted(video_obj, key=video_obj.get)
		topictree.append(video_obj)
	topictree_json['core']={'data':topictree}
	topictree_json_string=json.dumps(topictree_json)
	return render_to_response('curriculum.html', { 'json_data':json_data, 'topictree_json_string':topictree_json_string} ,context_instance=RequestContext(request))

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
			Subtopic_Mineduc.objects.create(name=args['nombre'], id_topic_id=args['curso'])
			return HttpResponse('Subtopic guardado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def saveVideoExercise(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			subtopic_id = args['subtopic'] #id del subtopic
			for arg in args:
				#print arg
				if arg=="subtopic":
					idsubtopic = arg
					#print idsubtopic
				else:
					idskill = arg
					if args[idskill]=="false":
						Subtopic_Skill_Mineduc.objects.create(id_skill_name_id=idskill[6:-1], id_subtopic_mineduc_id=subtopic_id)
					#print idskill[6:-1] #id del skill o video
					#print args[idskill] #booleano de skill/video, false es skill, true es video
			#print args
			#print args
			#for arg in args:
				#print args #id skill o video
				#print arg[1] #indica si es video o no, si es 1 es skill, si es 2 es video
				#if args[1]=="1":
					#Subtopic_Skill_Mineduc.objects.create()
			#Subtopic_Mineduc.objects.create(name=args['nombre'], id_topic_id=args['curso'])
			return HttpResponse('Skills guardado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")

def topicTree():
    topictree_json={}
    topictree_json['checkbox']={'keep_selected_style':False}
    topictree_json['plugins']=['checkbox','search']
    topictree=[]
    start_time=time.time()
    subjects=Subject.objects.all()
    for subject in subjects:
        subject_obj={"id": subject.id_subject_name, "parent":"#", "text": subject.name_spanish, "state": {"opened":"true"}, "icon":"false"}
        topictree.append(subject_obj)
    subject_chapter=Chapter.objects.exclude(index=None).order_by('index')
    for chapter in subject_chapter:
        chapter_obj={"id":chapter.id_chapter_name, "parent": chapter.id_subject_name_id, "text":chapter.name_spanish, "icon":"false"}
        topictree.append(chapter_obj)
    chapter_topic=Topic.objects.exclude(index=None).order_by('index')
    for topic in chapter_topic:
        topic_obj={"id":topic.id_topic_name, "parent": topic.id_chapter_name_id, "text":topic.name_spanish, "icon":"false"}
        topictree.append(topic_obj)
    topic_subtopic=Subtopic.objects.exclude(index=None).order_by('index')
    for subtopic in topic_subtopic:
        subtopic_obj={"id":subtopic.id_subtopic_name, "parent": subtopic.id_topic_name_id, "text":subtopic.name_spanish, "icon":"false"}
        topictree.append(subtopic_obj)
    subtopic_skill=Subtopic_Skill.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_skill_name')
    id=0
    for skill in subtopic_skill:
        skill_id=skill.id_subtopic_skill
        skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
        sorted(skill_obj, key=skill_obj.get)
        topictree.append(skill_obj)
        id=id+1
    subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
    for video in subtopic_video:
    	video_id=video.id_subtopic_video
    	video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "icon":"false", "index":video.id_video_name.index}
    	sorted(video_obj, key=video_obj.get)
    	topictree.append(video_obj)
    topictree_json['core']={'data':topictree}
    topictree_json_string=json.dumps(topictree_json)
    return topictree_json_string