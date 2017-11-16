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
import unicodedata


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule, Class, Student_Class, Skill_Attempt, Student, Video_Playing, Institution
from bakhanapp.models import Chapter_Mineduc, Topic_Mineduc, Subtopic_Mineduc, Subtopic_Skill_Mineduc, Subtopic_Video_Mineduc
from bakhanapp.models import Subtopic_Video, Chapter, Topic, Subtopic, Subtopic_Skill, Video, Skill, Subject
from django.db import connection

register = template.Library()
from configs import timeSleep

import json
import xlrd
from datetime import datetime, timedelta

import sys, os, traceback


##
## @brief	  Gets the schedules.
##
## @param	  request  The request
##
## @return	 The schedules.
##

@permission_required('bakhanapp.isSuper', login_url="/")
def getCurriculum(request):
	request.session.set_expiry(timeSleep)
	current_year = datetime.today().year
	chapter = Chapter_Mineduc.objects.all().values('id_chapter_mineduc','level','year','additional').order_by('-year','level')
	N = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']
	for i in range(len(chapter)):
		chapter[i]['level'] = N[int(chapter[i]['level'])] 

	subject = Subject.objects.all();
	return render_to_response('curriculum.html', {'capitulos':chapter, 'a_actual':current_year, 'lista_asign': subject}, context_instance=RequestContext(request))

@permission_required('bakhanapp.isSuper', login_url="/")
def getCurriculumInfo(request, id_chapter_mineduc):
	request.session.set_expiry(timeSleep)
	try:
		selected_topic = Topic_Mineduc.objects.filter(id_chapter_id=id_chapter_mineduc).order_by('index')
		
		level_names = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']
		current_curriculum = Chapter_Mineduc.objects.filter(id_chapter_mineduc = id_chapter_mineduc).values('level','year')
		current_subject = Subject.objects.filter(chapter_mineduc__id_chapter_mineduc = id_chapter_mineduc).values('name_spanish')
		last_missing_topic = 1

		unidad = []
		for top in selected_topic:
			topico = {}
			topico["id"] = top.id_topic_mineduc
			topico["index"] = top.index
			topico["desc"] = top.descripcion_topic
			topico["time"] = top.suggested_time
			if last_missing_topic == topico["index"]:
				last_missing_topic = last_missing_topic + 1
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

		json_dict = {"topicos":unidad}
		json_data = json.dumps(json_dict)

		topictree_json={}
		topictree_json['checkbox']={'keep_selected_style':False}
		topictree_json['plugins']=['checkbox','search']
		topictree=[]

		topictree_json_vid={}
		topictree_json_vid['checkbox']={'keep_selected_style':False}
		topictree_json_vid['plugins']=['checkbox','search']
		
		selected_subject = Subject.objects.filter(chapter_mineduc__id_chapter_mineduc=id_chapter_mineduc)
		subject_obj={"id": selected_subject[0].id_subject_name, "parent":"#", "text": selected_subject[0].name_spanish, "state": {"opened":"true"}, "icon":"false"}
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
		subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
		for skill in subtopic_skill:
			skill_id=skill.id_subtopic_skill
			skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
			sorted(skill_obj, key=skill_obj.get)
			topictree.append(skill_obj)
		subtopic_video=Subtopic_Video.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_video_name')
		for video in subtopic_video:
			video_id=video.id_subtopic_video
			video_obj={"id":video_id, "parent":video.id_subtopic_name_id, "text": video.id_video_name.name_spanish, "data":{"video_id":video.id_video_name.id_video_name}, "index":video.id_video_name.index}
			sorted(video_obj, key=video_obj.get)
			topictree.append(video_obj)

		topictree_json['core']={'data':topictree}
		topictree_json_string=json.dumps(topictree_json)
		
		return render_to_response('curriculumnivel.html', {
								'curriculo_id':id_chapter_mineduc, 									#ID del Curriculo actual
								'lista_topicos':selected_topic,										#Lista de topicos en el curriculo
								'nivel_curriculo': level_names[current_curriculum[0]['level']],		#Nivel del curriculo
								'anno_curriculo': current_curriculum[0]['year'],					#Año del curriculo
								'asignatura': current_subject[0]['name_spanish'],					#Asignatura del curriculo
								'unidad_siguiente': last_missing_topic,								#La proxima Unidad que sigue por crear
								'json_data':json_data,												#Dump del diccionario de datos Mineduc
								'json_skill_tree':topictree_json_string, 							#Dump del diccionario de Khan
							}, context_instance=RequestContext(request))
	except Exception as e:
		print "Error en la apertura de curriculo: curriculum/view.py:getCurriculumInfo"
		print traceback.print_exc()
		return HttpResponseRedirect("/inicio")

@permission_required('bakhanapp.isSuper', login_url="/")
def newChapter(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		try:
			args = request.POST
			Chapter_Mineduc.objects.create(id_subject=Subject.objects.get(id_subject_name=args['subj']), year=args['year'], level=args['level'] ,additional=args['additional'])
			return HttpResponse('Nuevo curriculo guardado correctamente')

		except Exception as e:
			print e
			return HttpResponse("Error al guardar los datos. Revise si ya tiene creado el curriculo con ese mismo nivel y año.")
	return HttpResponse("Error al realizar la petición")

@permission_required('bakhanapp.isSuper', login_url="/")
def newTopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			Topic_Mineduc.objects.create(id_chapter=Chapter_Mineduc.objects.get(id_chapter_mineduc=args['curr_id']), index=args['indice'], suggested_time=args['horas'], descripcion_topic=args['descr'])
			return HttpResponse('Unidad guardada correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar, revise que no exista la unidad.")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def updateTopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			Topic_Mineduc.objects.filter(id_topic_mineduc=args['topic_id']).update(index=args['indice'], suggested_time=args['horas'], descripcion_topic=args['descr'])
			return HttpResponse('Unidad actualizada correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar, revise que no exista el indice de la unidad.")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def newSubtopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			Subtopic_Mineduc.objects.create(id_topic=Topic_Mineduc.objects.get(id_topic_mineduc=args['topic_id']), index=args['indice'], description=args['descr'], summary=args['resum'])
			return HttpResponse('Objetivo de Aprendizaje guardado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar, compruebe que no existe el objetivo de aprendizaje")
	return HttpResponse("Error al guardar")

@permission_required('bakhanapp.isSuper', login_url="/")
def updateSubtopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		try:
			Subtopic_Mineduc.objects.filter(id_subtopic_mineduc=args['subtopic_id']).update(index=args['indice'], description=args['descr'], summary=args['resum'])
			return HttpResponse('Objetivo de aprendizaje actualizado correctamente')
		except Exception as e:
			print e
			return HttpResponse("Error al guardar, compruebe que no este en uso el indice del Objetivo de aprendizaje")
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
			return HttpResponse('Ejercicios y videos guardados correctamente')
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
			return HttpResponse('No se ha podido borrar los videos o ejercicios')
		return HttpResponse('Videos y ejercicios borrados correctamente')
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
		return HttpResponse('Objetivo de aprendizaje borrado correctamente')
	return HttpResponse('Error al eliminar')

@permission_required('bakhanapp.isSuper', login_url="/")
def deleteTopic(request):
	request.session.set_expiry(timeSleep)
	if request.method == "POST":
		args = request.POST
		try:
			Topic_Mineduc.objects.filter(id_topic_mineduc=args['topic_id']).delete()
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

@permission_required('bakhanapp.isSuper', login_url="/")
def loadSpreadsheet(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		try:
			excel = request.FILES
			wb = xlrd.open_workbook(file_contents=excel['file-0'].read())

		except Exception as e:
			print "Error en la lectura de archivo XLS: curriculum/view.py:loadSpreadsheet."
			print traceback.print_exc()
			return HttpResponse("Error! El archivo cargado no es valido.")

		try:
			#Construye el diccionario
			curriculum_list = []

			for sheet in wb.sheets():
				row = sheet.row_values(0)

				curriculum = {}
				u_dict = {}
				oa_dict = {}

				video_list = []
				skill_list = []
				oa_list = []
				u_list = []

				curriculum["year"] = int(row[1])
				curriculum["subject"] = row[5]
				curriculum["level"] = int(row[3])

				for rownum in range(2, sheet.nrows):
					row = sheet.row_values(rownum)
					
					if row[0] != '':
						if "index" in u_dict:
							u_dict["oa"] = oa_list
							u_list.append(u_dict)

							oa_list = []
							u_dict = {}

						u_dict["index"] = int(row[0])
						u_dict["desc"] = row[1]
						u_dict["time"] = int(row[2])

					if row[3] != '':
						if "index" in oa_dict:
							oa_dict["videos"] = video_list
							oa_dict["skills"] = skill_list

							oa_list.append(oa_dict)

							video_list = []
							skill_list = []
							oa_dict = {}

						oa_dict["index"] = int(row[3])
						oa_dict["desc"] = row[4]

					if row[5] != '':
						video_list.append(row[5])

					if row[6] != '':
						skill_list.append(row[6])

				#Agrega a la lista OA el ultimo OA
				oa_dict["videos"] = video_list
				oa_dict["skills"] = skill_list
				oa_list.append(oa_dict)

				#Agrega a la lista Unidad la ultima Unidad
				u_dict["oa"] = oa_list
				u_list.append(u_dict)

				curriculum["unit"] = u_list
				curriculum_list.append(curriculum)
		except Exception as e:
			print "Error en la creación de la base de datos: curriculum/view.py:loadSpreadsheet."
			print traceback.print_exc()
			return HttpResponse("Error! Hubo un error en la lectura del archivo, asegurese que tenga el formato correcto.")

		hit = {}
		hit["v"] = 0
		hit["tv"] = 0
		hit["s"] = 0
		hit["ts"] = 0
		try:
			for curr in curriculum_list:
				Chapter_Mineduc.objects.filter(id_subject=Subject.objects.get(name_spanish=curr["subject"]), year=curr['year'], level=curr['level']).delete()
				new_curr = Chapter_Mineduc.objects.create(id_subject=Subject.objects.get(name_spanish=curr["subject"]), year=curr['year'], level=curr['level'])

				for unit in curr["unit"]:
					new_unit = Topic_Mineduc.objects.create(id_chapter=new_curr, index=unit['index'], suggested_time=unit['time'], descripcion_topic=unit['desc'])
					for oa in unit["oa"]:
						new_oa = Subtopic_Mineduc.objects.create(id_topic=new_unit, index=oa['index'], description=oa['desc'])
						for v in oa["videos"]:
							video = Video.objects.filter(name_spanish=v)
							hit["tv"] = hit["tv"] + 1
							if (video):
								idtree = Subtopic_Video.objects.filter(id_video_name=video[0]).values("id_subtopic_video")
								Subtopic_Video_Mineduc.objects.create(id_video_name=video[0], id_tree=int(idtree[0]["id_subtopic_video"]), id_subtopic_name_mineduc=new_oa)
								hit["v"] = hit["v"] + 1

						for s in oa["skills"]:
							skill = Skill.objects.filter(name_spanish=s)
							hit["ts"] = hit["ts"] + 1
							if (skill):
								idtree = Subtopic_Skill.objects.filter(id_skill_name=skill[0]).values("id_subtopic_skill")
								Subtopic_Skill_Mineduc.objects.create(id_skill_name=skill[0], id_tree=idtree[0]["id_subtopic_skill"], id_subtopic_mineduc=new_oa)
								hit["s"] = hit["s"] + 1
							#Por si coincide el nombre en Ingles.
							else:
								s = s.replace(" ","_")
								skill = Skill.objects.filter(name=s)
								if (skill):
									idtree = Subtopic_Skill.objects.filter(id_skill_name=skill[0]).values("id_subtopic_skill")
									Subtopic_Skill_Mineduc.objects.create(id_skill_name=skill[0], id_tree=idtree[0]["id_subtopic_skill"], id_subtopic_mineduc=new_oa)
									hit["s"] = hit["s"] + 1

		except Exception as e:
			print "Error en la creación de la base de datos: curriculum/view.py:loadSpreadsheet."
			print traceback.print_exc()
			return HttpResponse("Error! No se logro crear la base de datos. Favor contactar con el administrador.")

		print "done"
		response = "Se han cargado los datos con exito, de un total de " + str(hit["tv"]) + " videos, se reconocieron " + str(hit["v"]) +". De un total de " + str(hit["s"]) + " habilidades, se reconocieron " + str(hit["ts"]) + ". Si la cantidad es muy baja asegurese de que los nombres en las tablas coinsidan con el enunciado que se muestra en la pagina de Khan Academy."
		return HttpResponse(response)

