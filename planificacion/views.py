#!usr/bin/env python
# -*- coding: utf-8 -*-
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
from datetime import datetime, timedelta, date

import sys, os


##
## @brief      Gets the schedules.
##
## @param      request  The request
##
## @return     The schedules.
##
@login_required()
def getClassList(request):
	request.session.set_expiry(timeSleep)
	if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True
		classes = Class.objects.filter(class_subject__kaid_teacher=request.user.user_profile.kaid).values('level', 'letter', 'year', 'additional', 'class_subject__id_class_subject', 'class_subject__curriculum').order_by('-year','level','letter')
	else:
		isTeacher = False
		##classes = Class.objects.filter(INSTITUCION)

	
	N = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']
	for i in range(len(classes)):
		classes[i]['level'] = N[int(classes[i]['level'])]		 

	return render_to_response('planificacion.html', { 'isTeacher':isTeacher, 'classes':classes} ,context_instance=RequestContext(request))


@login_required()
def getPlan(request, class_subj_id):
	request.session.set_expiry(timeSleep)
	current_year = date.today().year

	if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True
	else:
		isTeacher = False

	try:
		plan_list = Planning.objects.filter(class_subject_id=class_subj_id).order_by('class_date')

		id_chapter_mineduc = Class_Subject.objects.filter(id_class_subject=class_subj_id, kaid_teacher=request.user.user_profile.kaid).values('curriculum_id')
		selected_topic = Topic_Mineduc.objects.filter(id_chapter_id=id_chapter_mineduc[0]['curriculum_id']).order_by('index')
		
		level_names = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']
		current_curriculum = Chapter_Mineduc.objects.filter(id_chapter_mineduc = id_chapter_mineduc).values('level','year')
		current_subject = Subject.objects.filter(chapter_mineduc__id_chapter_mineduc = id_chapter_mineduc).values()

		planes = []
		for plan in plan_list:
			clase = {}
			clase["id"] = plan.id_planning
			clase["class_subject"] = plan.class_subject.id_class_subject
			clase["class_subtopic"] = plan.class_subtopic.id_subtopic_mineduc
			clase["class_date"] = []
			clase["class_date"].append(plan.class_date.year)
			clase["class_date"].append(plan.class_date.month)
			clase["class_date"].append(plan.class_date.day)
			clase["minutes"] = plan.minutes
			clase["status"] = plan.status
			clase["desc_inicio"] = plan.desc_inicio
			clase["desc_cierre"] = plan.desc_cierre
			clase["share_class"] = plan.share_class
			clase["class_name"] = plan.class_name
			plan_skills = []
			skillplanning = Skill_Planning.objects.filter(id_planning=plan.id_planning)
			for skill in skillplanning:
				skilldict = {}
				skilldict["id"] = skill.id_skill.id_skill_name
				skilldict["nombre"] = skill.id_skill.name_spanish
				skilldict["url"] = skill.id_skill.url_skill
				skilldict["tree"] = skill.id_subtopic.id_subtopic_skill
				plan_skills.append(skilldict)
			clase["skills"] = plan_skills
			plan_videos =[]
			videoplanning = Video_Planning.objects.filter(id_planning=plan.id_planning)
			for video in videoplanning:
				videodict = {}
				videodict["id"] = video.id_video.id_video_name
				videodict["nombre"] = video.id_video.name_spanish
				videodict["url"] = video.id_video.url_video
				videodict["tree"] = video.id_subtopic.id_subtopic_video
				plan_videos.append(videodict)
			clase["videos"] = plan_videos
			planes.append(clase)
		plan_dict = {"plan":planes}
		plan_dump = json.dumps(plan_dict)

		unidad = []
		for top in selected_topic:
			topico = {}
			topico["id"] = top.id_topic_mineduc
			topico["index"] = top.index
			topico["desc"] = top.descripcion_topic
			aprendizaje = []
			subtopic = Subtopic_Mineduc.objects.filter(id_topic_id=top.id_topic_mineduc).order_by('index')
			for sub in subtopic:
				subtopico = {}
				subtopico["id"] = sub.id_subtopic_mineduc
				subtopico["index"] = sub.index
				subtopico["desc"] = sub.description
				subtopico["resumen"] = sub.summary
				skills = []
				videos = []
				subtopicskill = Subtopic_Skill_Mineduc.objects.filter(id_subtopic_mineduc_id=subtopico["id"])
				for subskill in subtopicskill:
					subtskillmin={}
					subtskillmin["skill"]=subskill.id_skill_name.id_skill_name
					subtskillmin["nombre"]=subskill.id_skill_name.name_spanish
					subtskillmin["url"]=subskill.id_skill_name.url_skill
					subtskillmin["idtree"]=subskill.id_tree
					skills.append(subtskillmin)
				subtopico["skills"]=skills
				subtopicvideo = Subtopic_Video_Mineduc.objects.filter(id_subtopic_name_mineduc_id=subtopico["id"])
				for subvideo in subtopicvideo:
					subtvideomin={}
					subtvideomin["video"]=subvideo.id_video_name.id_video_name
					subtvideomin["nombre"]=subvideo.id_video_name.name_spanish
					subtvideomin["url"]=subvideo.id_video_name.url_video
					subtvideomin["idtree"]=subvideo.id_tree
					videos.append(subtvideomin)
				subtopico["videos"]=videos
				aprendizaje.append(subtopico)
			topico["subtopico"]=aprendizaje
			unidad.append(topico)

		json_dict = {"topicos":unidad}
		json_data = json.dumps(json_dict)

		topictree_json={}
		topictree_json['checkbox']={'keep_selected_style':False, 'cascade_to_hidden':False, 'cascade_to_disabled':False}
		topictree_json['plugins']=['checkbox','search']
		topictree=[]
		
		subject_obj={"id": current_subject[0]['id_subject_name'], "parent":"#", "text": current_subject[0]['name_spanish'], "state": {"opened":"true"}, "icon":"false"}
		topictree.append(subject_obj)
		
		subject_chapter = Chapter.objects.filter(id_subject_name=current_subject[0]['id_subject_name']).exclude(index=None).order_by('index')
		for chapter in subject_chapter:
			chapter_obj = {"id":chapter.id_chapter_name, "parent": chapter.id_subject_name_id, "text":chapter.name_spanish, "type":chapter.type_chapter,"icon":"false"}
			topictree.append(chapter_obj)
		chapter_topic=Topic.objects.filter(id_chapter_name_id__in=subject_chapter).exclude(index=None).order_by('index')
		for topic in chapter_topic:
			topic_obj={"id":topic.id_topic_name, "parent": topic.id_chapter_name_id, "text":topic.name_spanish, "icon":"false"}
			topictree.append(topic_obj)
		topic_subtopic=Subtopic.objects.filter(id_topic_name_id__in=chapter_topic).exclude(index=None).order_by('index')
		for subtopic in topic_subtopic:
			subtopic_obj={"id":subtopic.id_subtopic_name, "parent": subtopic.id_topic_name_id, "text":subtopic.name_spanish, "icon":"false"}
			topictree.append(subtopic_obj)
		subtopic_skill=Subtopic_Skill.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_skill_name')
		subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
		for video in subtopic_video:
			video_obj={"id":video.id_subtopic_video, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "index":video.id_video_name.index}
			sorted(video_obj, key=video_obj.get)
			topictree.append(video_obj)
		for skill in subtopic_skill:
			skill_obj={"id":skill.id_subtopic_skill, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "index":skill.id_skill_name.index, "icon":"false"}
			sorted(skill_obj, key=skill_obj.get)
			topictree.append(skill_obj)

		topictree_json['core']={'data':topictree}
		topictree_json_string=json.dumps(topictree_json)
		
		return render_to_response('planificacionnivel.html', {
								'plan':plan_dump,													#Diccionario de planificaciones
								'class_subject':class_subj_id,	 									#ID del Class Subject
								'curriculo_id':id_chapter_mineduc, 									#ID del Curriculo actual
								'lista_topicos':selected_topic,										#Lista de topicos en el curriculo
								'nivel_curriculo': level_names[current_curriculum[0]['level']],		#Nivel del curriculo
								'anno_curriculo': current_curriculum[0]['year'],					#Año del curriculo
								'anno': current_year,												#Año actual
								'asignatura': current_subject[0]['name_spanish'],					#Asignatura del curriculo
								'json_data':json_data,												#Dump del diccionario de datos Mineduc
								'json_khan_tree':topictree_json_string, 							#Dump del diccionario de habilidades Khan
							}, context_instance=RequestContext(request))
	except Exception as e:
		print "Error en la apertura del plan: planificacion/view.py:getPlan"
		print repr(e)
		return HttpResponseRedirect("/inicio")

@login_required()
def savePlanning(request):
	if request.method=="POST":
		try:
			teacher = request.user.user_profile.kaid
			args = request.POST

			class_sub = Class_Subject.objects.get(id_class_subject=args['id_tema_clase'])
			oa = Subtopic_Mineduc.objects.get(id_subtopic_mineduc=args['oa'])

			habilidades = request.POST.getlist('lista_hab[]')
			videos = request.POST.getlist('lista_vid[]')

			if (args['estado'] == "False"):
				status = False
			else:
				status = True

			class_date = date(int(args['anno']), int(args['mes']), int(args['dia']))
			p = Planning.objects.create(class_name=args['nombre'], desc_inicio=args['desc_inicio'],desc_cierre=args['desc_cierre'],class_date=class_date,class_subject=class_sub,class_subtopic=oa,minutes=args['duracion'],share_class=False,status=status)

			for habilidad in habilidades:
				arr = habilidad.split(',')
				Skill_Planning.objects.create(id_planning=p, id_subtopic=Subtopic_Skill.objects.get(id_subtopic_skill=arr[1]), id_skill=Skill.objects.get(id_skill_name=arr[0]))

			for video in videos:
				arr = video.split(',')
				Video_Planning.objects.create(id_planning=p, id_subtopic=Subtopic_Video.objects.get(id_subtopic_video=arr[1]), id_video=Video.objects.get(id_video_name=arr[0]))

			return HttpResponse('Planificación guardada correctamente')
		except Exception as e:
			print "Error en el guardado de un plan: planificacion/view.py:savePlanning"
			print repr(e)
			return HttpResponse('La planificacion no se puede guardar')

@login_required()
def editPlanning(request):
	if request.method=="POST":
		try:
			teacher = request.user.user_profile.kaid
			args = request.POST

			class_sub = Class_Subject.objects.get(id_class_subject=args['id_tema_clase'])
			oa = Subtopic_Mineduc.objects.get(id_subtopic_mineduc=args['oa'])

			class_date = date(int(args['anno']), int(args['mes']), int(args['dia']))

			if (args['estado'] == "False"):
				status = False
			else:
				status = True
			
			Planning.objects.filter(id_planning=args['id']).update(class_name=args['nombre'], desc_inicio=args['desc_inicio'],desc_cierre=args['desc_cierre'],class_date=class_date,class_subtopic=oa,minutes=args['duracion'],share_class=False,status=status)

			Skill_Planning.objects.filter(id_planning=args['id']).delete();
			Video_Planning.objects.filter(id_planning=args['id']).delete();

			habilidades = request.POST.getlist('lista_hab[]')
			videos = request.POST.getlist('lista_vid[]')

			print videos

			for habilidad in habilidades:
				arr = habilidad.split(',')
				Skill_Planning.objects.create(id_planning=Planning.objects.get(id_planning=args['id']), id_subtopic=Subtopic_Skill.objects.get(id_subtopic_skill=arr[1]), id_skill=Skill.objects.get(id_skill_name=arr[0]))

			for video in videos:
				arr = video.split(',')
				Video_Planning.objects.create(id_planning=Planning.objects.get(id_planning=args['id']), id_subtopic=Subtopic_Video.objects.get(id_subtopic_video=arr[1]), id_video=Video.objects.get(id_video_name=arr[0]))

			return HttpResponse('Planificación guardada correctamente')
		except Exception as e:
			print "Error en la modificacion de un plan: planificacion/view.py:editPlanning"
			print repr(e)
			return HttpResponse('La planificacion no se puede guardar')

@login_required()
def deletePlanning(request):
	if request.method=="POST":
		try:
			args = request.POST
			plan_id = args['id']
			Planning.objects.filter(id_planning=plan_id).delete()
			return HttpResponse('Planificacion borrada correctamente')
		except Exception as e:
			print "Error en el borrado de un plan: planificacion/view.py:deletePlanning"
			print repr(e)
			return HttpResponse('La planificacion no se pudo borrar.')