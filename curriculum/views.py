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
import unicodedata


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule, Class, Student_Class, Skill_Attempt, Student, Video_Playing, Institution
from bakhanapp.models import Chapter_Mineduc, Topic_Mineduc, Subtopic_Mineduc, Subtopic_Skill_Mineduc, Subtopic_Video_Mineduc
from bakhanapp.models import Subtopic_Video, Chapter, Topic, Subtopic, Subtopic_Skill, Skill, Video, Subject
from django.db import connection

register = template.Library()
from configs import timeSleep

import json
from datetime import datetime, timedelta

import sys, os


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
			subtopic = Subtopic_Mineduc.objects.filter(id_topic_id=top.id_topic_mineduc).order_by('name')
			for sub in subtopic:
				subtopico={}
				subtopico["id"]=sub.id_subtopic_mineduc
				subtopico["nombre"]=sub.name
				subtopico["aeoe"]=sub.AE_OE
				skills=[]
				videos=[]
				subtopicskill = Subtopic_Skill_Mineduc.objects.filter(id_subtopic_mineduc_id=subtopico["id"])
				for subskill in subtopicskill:
					nameskill = Skill.objects.filter(id_skill_name=subskill.id_skill_name_id).values('name_spanish', 'url_skill')
					subtskillmin={}
					subtskillmin["skill"]=subskill.id_skill_name_id
					subtskillmin["nombre"]=nameskill[0]['name_spanish']
					subtskillmin["url"]=nameskill[0]['url_skill']
					subtskillmin["idtree"]=subskill.id_tree
					skills.append(subtskillmin)
				subtopico["skills"]=skills
				subtopicvideo = Subtopic_Video_Mineduc.objects.filter(id_subtopic_name_mineduc_id=subtopico["id"])
				for subvideo in subtopicvideo:
					namevideo=Video.objects.filter(id_video_name=subvideo.id_video_name_id).values('name_spanish', 'url_video')
					subtvideomin={}
					subtvideomin["video"]=subvideo.id_video_name_id
					subtvideomin["nombre"]=namevideo[0]['name_spanish']
					subtvideomin["url"]=namevideo[0]['url_video']
					subtvideomin["idtree"]=subvideo.id_tree
					videos.append(subtvideomin)
				subtopico["videos"]=videos
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

	topictree_json_vid={}
	topictree_json_vid['checkbox']={'keep_selected_style':False}
	topictree_json_vid['plugins']=['checkbox','search']
	topictree_vid=[]

	subjects=Subject.objects.all()
	for subject in subjects:
	    subject_obj={"id": subject.id_subject_name, "parent":"#", "text": subject.name_spanish, "state": {"opened":"true"}, "icon":"false"}
	    topictree.append(subject_obj)
	    topictree_vid.append(subject_obj)
	subject_chapter=Chapter.objects.exclude(index=None).order_by('index')
	for chapter in subject_chapter:
	    chapter_obj={"id":chapter.id_chapter_name, "parent": chapter.id_subject_name_id, "text":chapter.name_spanish, "icon":"false"}
	    topictree.append(chapter_obj)
	    topictree_vid.append(chapter_obj)
	chapter_topic=Topic.objects.exclude(index=None).order_by('index')
	for topic in chapter_topic:
	    topic_obj={"id":topic.id_topic_name, "parent": topic.id_chapter_name_id, "text":topic.name_spanish, "icon":"false"}
	    topictree.append(topic_obj)
	    topictree_vid.append(topic_obj)
	topic_subtopic=Subtopic.objects.exclude(index=None).order_by('index')
	for subtopic in topic_subtopic:
	    subtopic_obj={"id":subtopic.id_subtopic_name, "parent": subtopic.id_topic_name_id, "text":subtopic.name_spanish, "icon":"false"}
	    topictree.append(subtopic_obj)
	    topictree_vid.append(subtopic_obj)
	subtopic_skill=Subtopic_Skill.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_skill_name')
	#id=0
	subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
	for video in subtopic_video:
		video_id=video.id_subtopic_video
		video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "index":video.id_video_name.index}
		sorted(video_obj, key=video_obj.get)
		topictree_vid.append(video_obj)

	for skill in subtopic_skill:
	    skill_id=skill.id_subtopic_skill
	    skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
	    sorted(skill_obj, key=skill_obj.get)
	    topictree.append(skill_obj)
	    topictree_vid.append(skill_obj)
	    #id=id+1
	subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
	for video in subtopic_video:
		video_id=video.id_subtopic_video
		video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "index":video.id_video_name.index}
		sorted(video_obj, key=video_obj.get)
		topictree.append(video_obj)

	topictree_json_vid['core']={'data':topictree_vid}
	topictree_json_string_video=json.dumps(topictree_json_vid)

	topictree_json['core']={'data':topictree}
	topictree_json_string=json.dumps(topictree_json)
	return render_to_response('curriculum.html', { 'json_data':json_data, 'topictree_json_string':topictree_json_string, 'topictree_json_string_video':topictree_json_string_video} ,context_instance=RequestContext(request))

@permission_required('bakhanapp.isSuper', login_url="/")
def newChapter(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		try:
			args = request.POST
			Chapter_Mineduc.objects.create(name=args['chapter'])
			return HttpResponse('Nivel guardado correctamente')

		except Exception as e:
			print e
			return HttpResponse("Error al guardar, compruebe que no existe el nivel")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def newTopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			nombrecap = Chapter_Mineduc.objects.filter(name=args['curso']).values('id_chapter_mineduc')
			Topic_Mineduc.objects.create(name=args['nombre'], id_chapter_id=nombrecap[0]['id_chapter_mineduc'])
			return HttpResponse('Unidad guardada correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar, revise que no exista la unidad.")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def newSubtopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			Subtopic_Mineduc.objects.create(name=args['nombre'], id_topic_id=args['topico'], AE_OE=args['descripcion'])
			return HttpResponse('Objetivo de Aprendizaje guardado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar, compruebe que no existe el Objetivo de Aprendizaje")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def saveVideoExercise(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			subtopic_id = args['subtopic']
			Subtopic_Skill_Mineduc.objects.filter(id_subtopic_mineduc_id=subtopic_id).delete()
			Subtopic_Video_Mineduc.objects.filter(id_subtopic_name_mineduc_id=subtopic_id).delete()
			cantidad = (len(args)-1)/3
			#print args
			for x in range(0,cantidad):
				try:
					if args['infodata['+str(x)+'][icon]']=="false":
						Subtopic_Skill_Mineduc.objects.create(id_skill_name_id=args['infodata['+str(x)+'][id_sv]'], id_tree=args['infodata['+str(x)+'][id]'], id_subtopic_mineduc_id=subtopic_id)
					else:
						Subtopic_Video_Mineduc.objects.create(id_video_name_id=args['infodata['+str(x)+'][id_sv]'], id_tree=args['infodata['+str(x)+'][id]'], id_subtopic_name_mineduc_id=subtopic_id)
				except Exception as e:
					print e
					continue
			return HttpResponse('Ejercicios y/o Videos guardados correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def deleteVideoExercise(request):
	request.session.set_expiry(timeSleep)
	if request.method == "POST":
		args = request.POST
		try:
			Subtopic_Skill_Mineduc.objects.filter(id_subtopic_mineduc_id=args['idsubtopic']).delete()
			Subtopic_Video_Mineduc.objects.filter(id_subtopic_name_mineduc_id=args['idsubtopic']).delete()
		except Exception as e:
			print e
			return HttpResponse('No se ha podido borrar los videos y/o ejercicios')
		return HttpResponse('Videos y Ejercicios borrados correctamente')
	return HttpResponse("Error al eliminar")

@permission_required('bakhanapp.isSuper', login_url="/")
def deleteSubtopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == "POST":
		args = request.POST
		try:
			Subtopic_Mineduc.objects.filter(id_topic_id=args['idtopic']).delete()
		except Exception as e:
			print e
			return HttpResponse('No se ha podido borrar el objetivo de aprendizaje')
		return HttpResponse('Objetivo de Aprendizaje borrado correctamente')
	return HttpResponse('Error al eliminar')

@permission_required('bakhanapp.isSuper', login_url="/")
def deleteTopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == "POST":
		args = request.POST
		try:
			Topic_Mineduc.objects.filter(id_chapter_id=args['idchapter']).delete()
		except Exception as e:
			print e
			return HttpResponse('No se ha podido borrar la unidad')
		return HttpResponse('Unidad borrada correctamente')
	return HttpResponse('Error al eliminar')

@permission_required('bakhanapp.isSuper', login_url="/")
def deleteChapter(request):
	request.session.set_expiry(timeSleep)
	if request.method == "POST":
		args = request.POST
		try:
			Chapter_Mineduc.objects.filter(id_chapter_mineduc=args['idchapter']).delete()
		except Exception as e:
			print e
			return HttpResponse('No se ha podido borrar el nivel')
		return HttpResponse('Nivel borrado correctamente')
	return HttpResponse('Error al eliminar')


@permission_required('bakhanapp.isSuper', login_url="/")
def downloadCurriculum(request):
	print "download curriculum"
	request.session.set_expiry(timeSleep)
	if request.method == "GET":
		chapmineduc = Chapter_Mineduc.objects.all()
		arrayCurriculum={}
		for chapm in chapmineduc:
			name_sheet = strip_acent(chapm.name)
			if len(name_sheet)>30:
				words = name_sheet.split()
				length = 22/len(words)
                name_sheet=''
                for w in words:
                    name_sheet += w[:length]
			#name_sheet = name_sheet.replace(' ','')
			#arrayCurriculum=#algo

		return HttpResponse('entro al descarga excel')
	return HttpResponse('no entro en descarga excel')


def strip_acent(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

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
    #id=0
    subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
    for video in subtopic_video:
    	video_id=video.id_subtopic_video
    	video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "icon":"false", "index":video.id_video_name.index}
    	sorted(video_obj, key=video_obj.get)
    	topictree.append(video_obj)
    	
    for skill in subtopic_skill:
        skill_id=skill.id_subtopic_skill
        skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
        sorted(skill_obj, key=skill_obj.get)
        topictree.append(skill_obj)
        #id=id+1
        
    
    topictree_json['core']={'data':topictree}
    topictree_json_string=json.dumps(topictree_json)
    return topictree_json_string