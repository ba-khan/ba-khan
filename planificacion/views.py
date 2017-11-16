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
from bakhanapp.models import Assesment_Skill, Administrator, Teacher, Class_Subject, Class_Schedule, Class, Student_Class, Student, Institution, Chapter_Mineduc, Topic_Mineduc, Subtopic_Mineduc, Subtopic_Skill_Mineduc, Subtopic_Video_Mineduc, Subtopic_Video, Chapter, Topic, Subtopic, Subtopic_Skill, Skill, Video, Subject, Planning, Planning_Log, Skill_Planning, Video_Planning, Institutional_Plan, Skill_Institution_Plan, Video_Institution_Plan, Student_Skill
from django.db import connection, IntegrityError

register = template.Library()
from configs import timeSleep

import json
from datetime import datetime, timedelta, date

from functools import wraps
import sys, os, traceback


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

	N = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']

	isAdmin = False
	isTeacher = False

	inst_id = Teacher.objects.get(kaid_teacher=request.user.user_profile.kaid).id_institution

	#Si es admin, obtiene todos los curriculos
	if(request.user.has_perm('bakhanapp.isAdmin')):
		teacher = Teacher.objects.filter(class_subject__curriculum_id__isnull=False, id_institution=inst_id).distinct("kaid_teacher").values("kaid_teacher","name").exclude(kaid_teacher=request.user.user_profile.kaid)

		isTeacher = True
		curriculums = Chapter_Mineduc.objects.all().values('id_chapter_mineduc','level','year').order_by('-year','level')

		for i in range(len(curriculums)):
			curriculums[i]['level'] = N[int(curriculums[i]['level'])]

			if (Institutional_Plan.objects.filter(curriculum=curriculums[i]['id_chapter_mineduc'], share_class=True)):
				curriculums[i]['share'] = "On"
			elif (Institutional_Plan.objects.filter(curriculum=curriculums[i]['id_chapter_mineduc'], share_class=False)):
				curriculums[i]['share'] = "Off"
			else:
				curriculums[i]['share'] = "Null"

		return render_to_response('planinstituto.html', { 'isTeacher':isTeacher, 'curriculums':curriculums, 'teachers':teacher, 'institucion':inst_id} ,context_instance=RequestContext(request))

	#Si solo es profesor, obtiene sus cursos
	elif (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		teacher = Teacher.objects.filter(class_subject__planning__share_class=True, id_institution=inst_id).distinct("kaid_teacher").values("kaid_teacher","name").exclude(kaid_teacher=request.user.user_profile.kaid)

		isTeacher = True
		classes = Class.objects.filter(class_subject__kaid_teacher=request.user.user_profile.kaid).values('level', 'letter', 'year', 'additional', 'class_subject__id_class_subject', 'class_subject__curriculum').order_by('-year','level','letter')

		instHasPlan = False;
		if (Institutional_Plan.objects.filter(share_class=True)):
			instHasPlan = True;

		for i in range(len(classes)):
			classes[i]['level'] = N[int(classes[i]['level'])]

			if (Planning.objects.filter(class_subject_id=classes[i]['class_subject__id_class_subject'], share_class=True)):
				classes[i]['share'] = "On"
			elif (Planning.objects.filter(class_subject_id=classes[i]['class_subject__id_class_subject'], share_class=False)):
				classes[i]['share'] = "Off"
			else:
				classes[i]['share'] = "Null"

		return render_to_response('planificacion.html', { 'isTeacher':isTeacher, 'classes':classes, 'teachers':teacher, 'institucion':inst_id, 'planExist':instHasPlan} ,context_instance=RequestContext(request))

@login_required()
def saveShareConfig(request):
	if request.method == "POST":
		try:
			args = request.POST.getlist('data[]')

			if(request.user.has_perm('bakhanapp.isAdmin')):
				for value in args:
					plan_list = Institutional_Plan.objects.filter(curriculum=value, share_class=False)
					if (plan_list):
						plan_list.update(share_class=True)
					else:
						plan_list = Institutional_Plan.objects.filter(curriculum=value).update(share_class=False)

			else:
				for value in args:
					plan_list = Planning.objects.filter(class_subject_id=value, share_class=False)
					if (plan_list):
						plan_list.update(share_class=True)
					else:
						plan_list = Planning.objects.filter(class_subject_id=value).update(share_class=False)

			return HttpResponse('Configuración guardada correctamente')

		except Exception as e:
			print "Error en la modificacion de la configuración de planes: planificacion/view.py:saveShareConfig"
			print traceback.print_exc()
			return HttpResponse('La configuración no se puede guardar')

@login_required()
def getSharedClassList(request):
	request.session.set_expiry(timeSleep)
	if request.method == "GET":
		try:
			teacher = request.GET.get("id", None)
			inst_id = Teacher.objects.get(kaid_teacher=request.user.user_profile.kaid).id_institution

			N = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']

			#El instituto tiene acceso a todos los cursos, independiente de la configuración de compartir que tengan los profesores en sus cursos.
			if(request.user.has_perm('bakhanapp.isAdmin')):
				classes = Class.objects.filter(class_subject__curriculum_id__isnull=False, class_subject__kaid_teacher=teacher, id_institution=inst_id).values('level', 'letter', 'year', 'additional', 'class_subject__id_class_subject', 'class_subject__curriculum', 'class_subject__kaid_teacher__name').order_by('-year','level','letter', 'class_subject__id_class_subject').distinct()

			else:
				#El valor 0 esta asignado a las clases sugeridas por la institución.
				if teacher == "0":
					classes = Chapter_Mineduc.objects.filter(institutional_plan__share_class=True, institutional_plan__institution=inst_id).values('level', 'year', 'additional', 'id_chapter_mineduc').order_by('-year','level').distinct()
					
				else:
					classes = Class.objects.filter(class_subject__planning__share_class=True, class_subject__kaid_teacher=teacher, id_institution=inst_id).values('level', 'letter', 'year', 'additional', 'class_subject__id_class_subject', 'class_subject__curriculum', 'class_subject__kaid_teacher__name').order_by('-year','level','letter', 'class_subject__id_class_subject').distinct()

			for i in range(len(classes)):
				classes[i]['level'] = N[int(classes[i]['level'])]

			json_class = json.dumps(list(classes))

			return HttpResponse(json_class, content_type="application/json")
		except Exception as e:
			print "Error en la obtencion de las clases compartidas: planificacion/view.py:getSharedClassList"
			print traceback.print_exc()
			return HttpResponse('No se pudo obtener la información.')

@login_required()
def getPlan(request, class_subj_id):
	request.session.set_expiry(timeSleep)
	current_time = date.today()

	isAdmin = False
	isTeacher = False

	level_names = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']

	if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True

	try:
		#Si el usuario es Institución.
		if request.user.has_perm('bakhanapp.isAdmin'):
			isAdmin = True
			#Iteración para un Instituto accediendo a una clase compartida.
			if "compartido" in request.path:
				print "Correcto"
				plan_list = Planning.objects.filter(class_subject_id=class_subj_id).order_by('class_date')
				id_chapter_mineduc = Class_Subject.objects.filter(id_class_subject=class_subj_id).values('curriculum_id')
				teacher_name = Teacher.objects.filter(class_subject__id_class_subject=class_subj_id).values('name')
			#Si no, esta accediendo al plan institucional.
			else:
				plan_list = Institutional_Plan.objects.filter(curriculum=class_subj_id).order_by('class_date')
				id_chapter_mineduc = [{'curriculum_id':class_subj_id}]
		#Si es un profesor accediendo.
		else:
			#Iteración para un profesor accediendo a un plan institucional.
			if ("inst" in request.path) and ("compartido" in request.path):
				plan_list = Institutional_Plan.objects.filter(curriculum=class_subj_id).order_by('class_date')
				id_chapter_mineduc = [{'curriculum_id':class_subj_id}]
				teacher_name = [{"name":"Institución"}]
			#Si no, esta accediendo al algun plan de profesor (Suyo o compartido).
			else:
				plan_list = Planning.objects.filter(class_subject_id=class_subj_id).order_by('class_date')
				id_chapter_mineduc = Class_Subject.objects.filter(id_class_subject=class_subj_id).values('curriculum_id')
				
		selected_topic = Topic_Mineduc.objects.filter(id_chapter_id=id_chapter_mineduc[0]['curriculum_id']).order_by('index')
		current_curriculum = Chapter_Mineduc.objects.filter(id_chapter_mineduc = id_chapter_mineduc[0]['curriculum_id']).values('level','year')
		current_subject = Subject.objects.filter(chapter_mineduc__id_chapter_mineduc = id_chapter_mineduc[0]['curriculum_id']).values()

		planes = []
		for plan in plan_list:
			clase = {}
			clase["id"] = plan.id_planning
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
			clase["late"] = False
			if plan.class_date < current_time:
				clase["late"] = True
			plan_skills = []

			#Si "inst" esta en la URL, implica que se esta accediendo al curriculo instituciónal.
			if("inst" in request.path):
				#El plan institucional no se realiza por lo que no puede estar "atrasado".
				clase.pop("late", None)
				clase.pop("status", None)
				skillplanning = Skill_Institution_Plan.objects.filter(id_planning=plan.id_planning)
				videoplanning = Video_Institution_Plan.objects.filter(id_planning=plan.id_planning)
			else:
				skillplanning = Skill_Planning.objects.filter(id_planning=plan.id_planning)
				videoplanning = Video_Planning.objects.filter(id_planning=plan.id_planning)

			for skill in skillplanning:
				skilldict = {}
				skilldict["id"] = skill.id_skill.id_skill_name
				skilldict["nombre"] = skill.id_skill.name_spanish
				skilldict["url"] = skill.id_skill.url_skill
				skilldict["tree"] = skill.id_subtopic.id_subtopic_skill
				plan_skills.append(skilldict)
			clase["skills"] = plan_skills

			plan_videos =[]

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
			topico["horas"]= top.suggested_time
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

		#Revisa si la redirección es hacia un plan compartido.
		if "compartido" in request.path:
			classes = Class.objects.filter(class_subject__curriculum_id=id_chapter_mineduc[0]['curriculum_id'], class_subject__kaid_teacher=request.user.user_profile.kaid).values('level', 'letter', 'year', 'additional', 'class_subject__id_class_subject').order_by('-year','level','letter')
			class_name = Class.objects.filter(class_subject__id_class_subject=class_subj_id).values('level','letter','year','additional')

			for i in range(len(class_name)):
				class_name[i]['level'] = level_names[int(class_name[i]['level'])]

			for i in range(len(classes)):
				classes[i]['level'] = level_names[int(classes[i]['level'])]

			#Si es institución, accede al plan con acceso al Resumen.
			if request.user.has_perm('bakhanapp.isAdmin'):
				log_data = []
				for plan in plan_list:
					logs = Planning_Log.objects.filter(id_planning=plan).values("id_planning", "field", "old_value", "new_value", "date").order_by("date")
					if (logs):
						for log in logs:
							log["date"] = str(log["date"].year) + "-" +  str(log["date"].month) + "-" + str(log["date"].day)
							log_data.append(log)

				log_dict = {"info":log_data}
				log_dump = json.dumps(log_dict)

				return render_to_response('plancompartirnivelinst.html', {
					'id': class_subj_id,												#ID del Class Suject
					'plan':plan_dump,													#Diccionario de planificaciones
					'log': log_dump,															#Historial de cambios
					'autor':teacher_name,												#Nombre del dueño del curriculo
					'clase':class_name,													#Datos del curso compartido.
					'cursos_usuario':classes,											#Lista de los cursos del usuario que coinsiden con el curriculo actual.
					'curriculo_id':id_chapter_mineduc, 									#ID del Curriculo actual
					'lista_topicos':selected_topic,										#Lista de unidades/topicos en el curriculo
					'nivel_curriculo': level_names[current_curriculum[0]['level']],		#Nivel del curriculo
					'anno_curriculo': current_curriculum[0]['year'],					#Año del curriculo
					'asignatura': current_subject[0]['name_spanish'],					#Asignatura del curriculo
					'json_data':json_data,												#Dump del diccionario de datos Mineduc
					'isTeacher': isTeacher
				}, context_instance=RequestContext(request))

			#Si es profesor, solo se accede al listado de clases.
			else:
				return render_to_response('plancompartirnivel.html', {
					'id': class_subj_id,												#ID del Class Suject
					'plan':plan_dump,													#Diccionario de planificaciones
					'autor':teacher_name,												#Nombre del dueño del curriculo
					'clase':class_name,													#Datos del curso compartido.
					'cursos_usuario':classes,											#Lista de los cursos del usuario que coinsiden con el curriculo actual.
					'curriculo_id':id_chapter_mineduc, 									#ID del Curriculo actual
					'lista_topicos':selected_topic,										#Lista de unidades/topicos en el curriculo
					'nivel_curriculo': level_names[current_curriculum[0]['level']],		#Nivel del curriculo
					'anno_curriculo': current_curriculum[0]['year'],					#Año del curriculo
					'asignatura': current_subject[0]['name_spanish'],					#Asignatura del curriculo
					'json_data':json_data,												#Dump del diccionario de datos Mineduc
					'isTeacher': isTeacher
				}, context_instance=RequestContext(request))

		#Si no es compartido, primero obtiene los datos para el arbol de habilidades/videos de khan.
		else:		
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
				'class_subject':class_subj_id,	 									#ID del Class Subject (Curriculo en caso de ser Institucion)
				'lista_topicos':selected_topic,										#Lista de unidades/topicos en el curriculo
				'nivel_curriculo': level_names[current_curriculum[0]['level']],		#Nivel del curriculo
				'anno_curriculo': current_curriculum[0]['year'],					#Año del curriculo
				'anno': current_time.year,											#Año actual
				'asignatura': current_subject[0]['name_spanish'],					#Asignatura del curriculo
				'json_data':json_data,												#Dump del diccionario de datos Mineduc
				'json_khan_tree':topictree_json_string, 							#Dump del diccionario de habilidades Khan
				'isTeacher': isTeacher,
				'isAdmin':isAdmin,
			}, context_instance=RequestContext(request))
	except Exception as e:
		print "Error en la apertura del plan: planificacion/view.py:getPlan"
		print traceback.print_exc()
		return HttpResponseRedirect("/inicio")

@login_required()
def savePlanning(request):
	if request.method=="POST":
		try:
			teacher = request.user.user_profile.kaid
			args = request.POST
			
			oa = Subtopic_Mineduc.objects.get(id_subtopic_mineduc=args['oa'])

			habilidades = request.POST.getlist('lista_hab[]')
			videos = request.POST.getlist('lista_vid[]')

			if (args['estado'] == "False"):
				status = False
			else:
				status = True

			class_date = date(int(args['anno']), int(args['mes']), int(args['dia']))

			#Si el usuario es Admin, guarda el plan en Institutional_Plan
			if(request.user.has_perm('bakhanapp.isAdmin')):
				#En este caso, id_tema_clase' es el PK del curriculo en Chapter_Mineduc
				curriculum = Chapter_Mineduc.objects.get(id_chapter_mineduc=args['id_tema_clase'])
				institution = Teacher.objects.get(kaid_teacher=teacher).id_institution

				p = Institutional_Plan.objects.create(class_name=args['nombre'], desc_inicio=args['desc_inicio'],desc_cierre=args['desc_cierre'],class_date=class_date, curriculum=curriculum,class_subtopic=oa, minutes=args['duracion'],share_class=False,status=status, institution=institution)

				for habilidad in habilidades:
					arr = habilidad.split(',')
					try:
						Skill_Institution_Plan.objects.create(id_planning=p, id_subtopic=Subtopic_Skill.objects.get(id_subtopic_skill=arr[1]), id_skill=Skill.objects.get(id_skill_name=arr[0]))
					except IntegrityError as e:
						pass

				for video in videos:
					arr = video.split(',')
					try:
						Video_Institution_Plan.objects.create(id_planning=p, id_subtopic=Subtopic_Video.objects.get(id_subtopic_video=arr[1]), id_video=Video.objects.get(id_video_name=arr[0]))
					except IntegrityError as e:
						pass

			#Caso contrario, el usuario es solamente profesor.
			else:
				#'id_tema_clase' es el PK de Class_Subject en este caso.
				class_sub = Class_Subject.objects.get(id_class_subject=args['id_tema_clase'])

				p = Planning.objects.create(class_name=args['nombre'], desc_inicio=args['desc_inicio'],desc_cierre=args['desc_cierre'],class_date=class_date,class_subject=class_sub,class_subtopic=oa,minutes=args['duracion'],share_class=False,status=status)

				for habilidad in habilidades:
					arr = habilidad.split(',')
					try:
						Skill_Planning.objects.create(id_planning=p, id_subtopic=Subtopic_Skill.objects.get(id_subtopic_skill=arr[1]), id_skill=Skill.objects.get(id_skill_name=arr[0]))
					except IntegrityError as e:
						pass

				for video in videos:
					arr = video.split(',')
					try:
						Video_Planning.objects.create(id_planning=p, id_subtopic=Subtopic_Video.objects.get(id_subtopic_video=arr[1]), id_video=Video.objects.get(id_video_name=arr[0]))
					except IntegrityError as e:
						pass

			return HttpResponse('Planificación guardada correctamente')
		except Exception as e:
			if "duplicate key value violates unique constraint" in e:
				return HttpResponse('La planificacion no se puede editar. El nombre de la clase ya existe.')
			print "Error en la modificacion de un plan: planificacion/view.py:savePlanning"
			print traceback.print_exc()
			return HttpResponse('La planificacion no se puede editar, favor revisar los campos ingresados.')

@login_required()
def copyPlanning(request):
	if request.method=="POST":
		try:
			teacher = request.user.user_profile.kaid
			args = request.POST

			Planning.objects.filter(class_subject=args['owner_class_id']).delete()
			#Si existe "inst" en el URL, esta copiando desde un plan institucional, se hace la Query en la tabla relacionada.
			if args["is_institution"] == "True":
				plan_list = Institutional_Plan.objects.filter(curriculum=args['copied_class_id'])
			else:
				plan_list = Planning.objects.filter(class_subject=args['copied_class_id'])

			for plan in plan_list:
				new = Planning.objects.create(class_name=plan.class_name, desc_inicio=plan.desc_inicio, desc_cierre=plan.desc_cierre, class_date=plan.class_date, class_subject=Class_Subject.objects.get(id_class_subject=args['owner_class_id']), class_subtopic=plan.class_subtopic, minutes=plan.minutes, share_class=False, status=plan.status)

				if args["is_institution"] == "True":
					habilidades = Skill_Institution_Plan.objects.filter(id_planning=plan)
				else:
					habilidades = Skill_Planning.objects.filter(id_planning=plan)
				for habilidad in habilidades:
					Skill_Planning.objects.create(id_planning=new, id_subtopic=habilidad.id_subtopic, id_skill=habilidad.id_skill)

				if args["is_institution"] == "True":
					videos = Video_Institution_Plan.objects.filter(id_planning=plan)
				else:
					videos = Video_Planning.objects.filter(id_planning=plan)
				for video in videos:
					Video_Planning.objects.create(id_planning=new, id_subtopic=video.id_subtopic, id_video=video.id_video)

			return HttpResponse('Planificación copiada correctamente')
		except Exception as e:
			print "Error en el copiado de un plan: planificacion/view.py:copyPlanning"
			print traceback.print_exc()
			return HttpResponse('La planificacion no se puede copiar')

@login_required()
def editPlanning(request):
	if request.method=="POST":
		try:
			teacher = request.user.user_profile.kaid
			args = request.POST

			oa = Subtopic_Mineduc.objects.get(id_subtopic_mineduc=args['oa'])

			class_date = date(int(args['anno']), int(args['mes']), int(args['dia']))

			habilidades = request.POST.getlist('lista_hab[]')
			videos = request.POST.getlist('lista_vid[]')

			if (args['estado'] == "False"):
				status = False
			else:
				status = True

			if(request.user.has_perm('bakhanapp.isAdmin')):
				Institutional_Plan.objects.filter(id_planning=args['id']).update(class_name=args['nombre'], desc_inicio=args['desc_inicio'],desc_cierre=args['desc_cierre'],class_date=class_date,class_subtopic=oa,minutes=args['duracion'],share_class=False,status=status)

				Skill_Institution_Plan.objects.filter(id_planning=args['id']).delete();
				Video_Institution_Plan.objects.filter(id_planning=args['id']).delete();

				for habilidad in habilidades:
					arr = habilidad.split(',')
					try:
						Skill_Institution_Plan.objects.create(id_planning=Institutional_Plan.objects.get(id_planning=args['id']), id_subtopic=Subtopic_Skill.objects.get(id_subtopic_skill=arr[1]), id_skill=Skill.objects.get(id_skill_name=arr[0]))
					except IntegrityError as e:
						pass

				for video in videos:
					arr = video.split(',')
					try:
						Video_Institution_Plan.objects.create(id_planning=Institutional_Plan.objects.get(id_planning=args['id']), id_subtopic=Subtopic_Video.objects.get(id_subtopic_video=arr[1]), id_video=Video.objects.get(id_video_name=arr[0]))
					except IntegrityError as e:
						pass

			else:
				current_plan = Planning.objects.get(id_planning=args['id'])
				current_time = datetime.now()

				if (current_plan.class_name != args["nombre"]):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Nombre", old_value=current_plan.class_name, new_value=args["nombre"])
				if (current_plan.desc_inicio != args['desc_inicio']):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Descripción de inicio", old_value=current_plan.desc_inicio, new_value=args["desc_inicio"])
				if (current_plan.desc_cierre != args['desc_cierre']):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Descripción de cierre", old_value=current_plan.desc_cierre, new_value=args["desc_cierre"])
				if (current_plan.class_date != class_date):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Fecha", old_value=str(current_plan.class_date), new_value=str(class_date))
				if (current_plan.class_subtopic != oa):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Objetivo de Aprendizaje", old_value=str(current_plan.class_subtopic.index), new_value=str(oa.index))
				if (int(current_plan.minutes) != int(args['duracion'])):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Duración", old_value=str(current_plan.minutes) + "minutos", new_value=str(args["duracion"]) + "minutos")
				if (current_plan.status != status):
					Planning_Log.objects.create(id_planning=current_plan, date=current_time, field="Estado", old_value=str(current_plan.status), new_value=str(args["estado"]))

				Planning.objects.filter(id_planning=args['id']).update(class_name=args['nombre'], desc_inicio=args['desc_inicio'],desc_cierre=args['desc_cierre'],class_date=class_date,class_subtopic=oa,minutes=args['duracion'],share_class=False,status=status)

				Skill_Planning.objects.filter(id_planning=args['id']).delete();
				Video_Planning.objects.filter(id_planning=args['id']).delete();

				for habilidad in habilidades:
					arr = habilidad.split(',')
					try:
						Skill_Planning.objects.create(id_planning=Planning.objects.get(id_planning=args['id']), id_subtopic=Subtopic_Skill.objects.get(id_subtopic_skill=arr[1]), id_skill=Skill.objects.get(id_skill_name=arr[0]))
					except IntegrityError as e:
						pass

				for video in videos:
					arr = video.split(',')
					try:
						Video_Planning.objects.create(id_planning=Planning.objects.get(id_planning=args['id']), id_subtopic=Subtopic_Video.objects.get(id_subtopic_video=arr[1]), id_video=Video.objects.get(id_video_name=arr[0]))
					except IntegrityError as e:
						pass

			return HttpResponse('Planificación guardada correctamente')
		except Exception as e:
			if "duplicate key" in str(e):
				return HttpResponse('La planificacion no se puede editar. El nombre de la clase ya existe.')
			else:
				print "Error en la modificacion de un plan: planificacion/view.py:editPlanning"
				print traceback.print_exc()
				return HttpResponse('La planificacion no se puede editar, favor revisar los campos ingresados.')

@login_required()
def deletePlanning(request):
	if request.method=="POST":
		try:
			args = request.POST
			plan_id = args['id']
			if(request.user.has_perm('bakhanapp.isAdmin')):
				#Borrado logico
				#Institutional_Plan.objects.filter(id_planning=plan_id).update(is_deleted=True)
				Institutional_Plan.objects.filter(id_planning=plan_id).delete()
			else:
				#Planning.objects.filter(id_planning=plan_id).update(is_deleted=True)
				Planning.objects.filter(id_planning=plan_id).delete()
			return HttpResponse('Planificacion borrada correctamente')
		except Exception as e:
			print "Error en el borrado de un plan: planificacion/view.py:deletePlanning"
			print traceback.print_exc()
			return HttpResponse('La planificacion no se pudo borrar.')

@login_required()
def getReport(request):
	if request.method=="GET":
		try:
			subj_id = request.GET.get("subj_class_id",None)
			class_subject = Class_Subject.objects.get(id_class_subject=subj_id)
			selected_class = Class.objects.get(id_class=class_subject.id_class.id_class)
			plan_list = Planning.objects.filter(class_subject=subj_id).order_by('class_date').values("class_date", "status", "class_subtopic__id_topic__index","id_planning")

			data = {}
			t0 = datetime(1,1,1)
			now = date.today()

			data['nStudents'] = Student.objects.filter(student_class__id_class_id=class_subject.id_class).count()
			data['nPlans'] = Planning.objects.filter(class_subject__id_class_subject=subj_id).count()
			data['teacher_name'] = Teacher.objects.get(class_subject__id_class_subject=subj_id).name
			data['start_date'] = [plan_list[0]["class_date"].day, plan_list[0]["class_date"].month, plan_list[0]["class_date"].year]
			data['end_date'] = [plan_list[len(plan_list)-1]["class_date"].day, plan_list[len(plan_list)-1]["class_date"].month, plan_list[len(plan_list)-1]["class_date"].year]

			unit_list = Topic_Mineduc.objects.filter(id_chapter=class_subject.curriculum_id).order_by("index","id_topic_mineduc")
			time_data = []
			
			skill_list = []
			for unit in unit_list:
				skill_sublist = []

				time_data.append({"label":"Unidad " + str(unit.index), "index":unit.index, "unit_id":unit.id_topic_mineduc, "times":[]})

				skills = Skill.objects.filter(skill_planning__id_planning=Planning.objects.filter(class_subtopic__id_topic=unit, class_subject=subj_id))
				skill_mastery = Student_Skill.objects.filter(kaid_student_id__student_class__id_class=selected_class, id_skill_name=skills).values('last_skill_progress','struggling','id_skill_name','kaid_student__name', 'id_skill_name__name_spanish')

				for skill in skills:
					found_skills = 0
					skill_data = {}
					skill_data["level"] = {"total": 0, "unstarted": 0, "practiced": 0, "mastery1": 0, "mastery2": 0, "mastery3": 0, "struggling": 0}
					skill_data["name"] = skill.name_spanish

					for mastery in skill_mastery:						
						if (mastery['id_skill_name'] == skill.id_skill_name):
							found_skills += 1
							if (mastery['struggling'] == True):
								skill_data["level"]["struggling"] += 1
							else:
								skill_data["level"][mastery['last_skill_progress']] += 1

					skill_data["level"]["unstarted"] += data['nStudents'] - found_skills

					skill_data["level"]["total"] = data['nStudents']
					skill_sublist.append(skill_data)
				skill_list.append(skill_sublist)
			data["skills"] = skill_list

			for plan in plan_list:
				#Obtain the planned class dates in Ticks format as required by Timeline.js d3 plugin.
				colortype = ""
				tx = datetime(1, plan["class_date"].month, plan["class_date"].day)
				tfx = (tx - t0).total_seconds() * 1000.0

				if (plan["status"] == True):
					colortype = "done"
				elif plan["class_date"] < now:
					colortype = "late"
				else:
					colortype = "not-done"

				for time in time_data:
					if time["index"] == plan["class_subtopic__id_topic__index"]:
						time["times"].append({"starting_time":tfx, "ending_time":tfx, "ctype":colortype, "plan_id":plan["id_planning"]})

			data["time"] = time_data
			json_data = json.dumps(data)

			return HttpResponse(json_data, content_type="application/json")
		except Exception as e:
			print "Error en la obtencion de los datos del resumen: planificacion/view.py:getReport"
			print traceback.print_exc()
			return HttpResponse('No se pudo obtener la información.')

@login_required()
def generateClassExcel(request, id_plan):
    #funcion que genera el excel de un curso completo con todas sus evaluaciones
    request.session.set_expiry(timeSleep)
    if request.method == 'GET':
        #funcion que genera el excel de una evaluacion
        assesment = Assesment.objects.filter(id_class=id_class)
        rClass = Class.objects.get(id_class=id_class)
        
        nameClass= N[int(rClass.level)]  +' '+ rClass.letter
        #print nameClass
        try:#id1004
            #create multi-sheet book with array
            arrayAssesment={}
            arrayAssesment['General'] = getArrayClassDetail(id_class)
            for a in assesment:
                name_sheet = strip_acent(a.name)
                if len(name_sheet) > 22:
                    words = name_sheet.split()
                    #print len(words)
                    length = 22/len(words)
                    name_sheet=''
                    for w in words:
                        name_sheet += w[:length]
                name_sheet = name_sheet.replace(' ','')
                #print a.id_assesment
                arrayAssesment[name_sheet+'_detalle']=getArrayAssesmentDetail(a.id_assesment) 
                arrayAssesment[name_sheet+'_resumen'] = getArrayAssesmentResumen(a.id_assesment)   
            book = pe.Book(arrayAssesment)
        except Exception as e:
            print '***ERROR*** problemas al crear multiples hojas excel con dataTest try id1004'
            print e
        try:
            response = excel.make_response(book, 'xls', file_name=nameClass)
        except Exception as e:
            print '***ERROR*** no se ha podido generar la respuesta excel en generateClassExcel'
            print e
            response = False
        return response