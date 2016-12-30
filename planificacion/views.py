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
from bakhanapp.models import Chapter_Mineduc, Topic_Mineduc, Subtopic_Mineduc, Subtopic_Skill_Mineduc, Subtopic_Video_Mineduc
from bakhanapp.models import Subtopic_Video, Chapter, Topic, Subtopic, Subtopic_Skill, Skill, Video, Subject, Planning, Skill_Planning, Video_Planning
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
@login_required()
def getCurriculumProposed(request):
	request.session.set_expiry(timeSleep)
	if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True
	else:
		isTeacher = False

	if (request.user.has_perm('bakhanapp.isAdmin')):
		classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).values('level').distinct().order_by('level')
	N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
	for i in range(len(classes)):
		#print classes[i]['level']
		classes[i]['nivel'] = N[int(classes[i]['level'])] 
		#x.add(classes[i].level)

	#uniq = x

	#print list(uniq)
	'''
	miplanificacion = Planning.objects.filter(teacher=request.user.user_profile.kaid)
	vkhn = ''
	ekhn = ''
	for miplan in miplanificacion:
		nombrecurso = Chapter_Mineduc.objects.filter(id_chapter_mineduc=miplan.curso).values('name')
		miplan.nombrecurso = nombrecurso[0]['name']
		nombreoa = Subtopic_Mineduc.objects.filter(name=miplan.oa).values('AE_OE')
		miplan.nombreoa = nombreoa[0]['AE_OE']

		miplan.ejerciciokhan = Skill_Planning.objects.filter(id_planning_id=miplan.id_planning).values('id_skill_id')
		for i in range(len(miplan.ejerciciokhan)):
			queryskill = Skill.objects.filter(id_skill_name=miplan.ejerciciokhan[i]['id_skill_id']).values('name_spanish', 'url_skill')
			miplan.ejerciciokhan[i]['namespanish']=queryskill[0]['name_spanish']
			miplan.ejerciciokhan[i]['urlskill']=queryskill[0]['url_skill']

		miplan.videokhan = Video_Planning.objects.filter(id_planning_id=miplan.id_planning).values('id_video_id')
		for j in range(len(miplan.videokhan)):
			queryvideo = Video.objects.filter(id_video_name=miplan.videokhan[j]['id_video_id']).values('name_spanish', 'url_video')
			miplan.videokhan[j]['namespanish']=queryvideo[0]['name_spanish']
			miplan.videokhan[j]['urlvideo']=queryvideo[0]['url_video']

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
				subtopico["aeoa"]=sub.AE_OE
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
		video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "index":video.id_video_name.index}
		sorted(video_obj, key=video_obj.get)
		topictree.append(video_obj)
	topictree_json['core']={'data':topictree}
	topictree_json_string=json.dumps(topictree_json)
	'''
	return render_to_response('planificacion.html', { 'isTeacher':isTeacher, 'classes':classes} ,context_instance=RequestContext(request))


@login_required()
def getCurriculumPropuesto(request, level):
	request.session.set_expiry(timeSleep)
	try:
		N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
		nivel = N[int(level)]

		tpmin = Topic_Mineduc.objects.filter(id_chapter_id=Chapter_Mineduc.objects.filter(name__iexact=nivel))

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
		topictree_json['core']={'data':topictree}
		topictree_json_string_exercise=json.dumps(topictree_json)

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

		topictree_json_vid['core']={'data':topictree_vid}
		topictree_json_string_video=json.dumps(topictree_json_vid)

		return render_to_response('planificacionnivel.html',{'nivel':nivel, 'topic_mineduc':tpmin, 'json_data':json_data, 'topictree_exercise':topictree_json_string_exercise, 'topictree_video':topictree_json_string_video},  context_instance=RequestContext(request))
	except Exception as e:
		print e
		return HttpResponseRedirect("/inicio")

@login_required()
def savePlanning(request):
	if request.method=="POST":
		try:
			teacher = request.user.user_profile.kaid
			args = request.POST
			Planning.objects.create(curso=args['nombre'], oa=args['oa'], clase=args['clase'], objetivo=args['objetivo'], inicio=args['inicio'], descripcion=args['descripcion'], cierre=args['cierre'], teacher_id=teacher)
			idplanning = Planning.objects.filter(curso=args['nombre'], oa=args['oa']).values('id_planning')
			ejerciciokhan=args['ejercicio']
			ejerkhan = ejerciciokhan.split('**')
			videokhan=args['video']
			vidkhan = videokhan.split('**')
			for i in range(1,len(ejerkhan)):
				Skill_Planning.objects.create(id_planning_id=idplanning[0]['id_planning'], id_skill_id=ejerkhan[i])
			for j in range(1,len(vidkhan)):
				Video_Planning.objects.create(id_planning_id=idplanning[0]['id_planning'], id_video_id=vidkhan[j])
			return HttpResponse('Planificacion guardada correctamente')
		except Exception as e:
			print e
			return HttpResponse('La planificacion no se puede guardar')

@login_required()
def deletePlanning(request):
	if request.method=="POST":
		try:
			args = request.POST
			cursoeliminar = args['curso']
			oaeliminar = args['oa']
			idplanning = Planning.objects.filter(curso=args['curso'], oa=args['oa']).values('id_planning')
			Video_Planning.objects.filter(id_planning_id=idplanning).delete()
			Skill_Planning.objects.filter(id_planning_id=idplanning).delete()
			Planning.objects.filter(curso=cursoeliminar, oa=oaeliminar).delete()
			return HttpResponse('Planificacion borrada correctamente')
		except Exception as e:
			print e
			return HttpResponse('no guardando')