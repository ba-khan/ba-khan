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
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule, Class, Student_Class, Skill_Attempt, Student, Video_Playing, Student_Skill
from bakhanapp.models import Schedule, Chapter, Skill_Progress, Topic, Subtopic, Subtopic_Skill, Skill
from django.db import connection
from django.db.models import Max

register = template.Library()
from configs import timeSleep

import json
from datetime import datetime, timedelta
import collections


##
## @brief      Gets the schedules.
##
## @param      request  The request
##
## @return     The schedules.
##
@login_required()
def getStatistics(request):
	request.session.set_expiry(timeSleep)
	try:
		teacher = Teacher.objects.get(email=request.user.email)
	except:
		return render_to_response('statistics.html', context_instance=RequestContext(request))
	if (Administrator.objects.filter(kaid_administrator=request.user.user_profile.kaid) or Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
		isTeacher = True
	else:
		isTeacher = False
	if(request.user.has_perm('bakhanapp.isAdmin')):
		classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).order_by('level','letter')
		class_schedule = Class_Schedule.objects.filter(id_class_id__in=classes).exclude(id_class_id__isnull=True)
	else:
		classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class')).order_by('level','letter')
		class_schedule = Class_Schedule.objects.filter(kaid_teacher_id=request.user.user_profile.kaid).exclude(id_class_id__isnull=True)
	N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
	for i in range(len(classes)):
		classes[i].nivel = N[int(classes[i].level)] 
	schedules = Schedule.objects.filter(id_institution_id=teacher.id_institution_id).order_by('start_time')
	start = "00:00"
	end = "00:00"
	otrahora = []
	largo = len(schedules)
	j=0
	for sched in schedules:
		j=j+1
		if sched.end_time!=start:
			horaini = datetime.strptime(start, "%H:%M")
			start = horaini.strftime('%H:%M')
			horafn= datetime.strptime(sched.start_time,"%H:%M")
			horafn = horafn.strftime('%H:%M')
			if (start!=horafn):
				otrahora.append(start +" - "+ horafn)
			start = sched.end_time
		if j==largo:
			horaini = datetime.strptime(sched.end_time, "%H:%M")
			horaini = horaini.strftime('%H:%M')
			otrahora.append(horaini +" - "+end)
	#print otrahora
	return render_to_response('statistics.html', {'isTeacher': isTeacher, 'classes':classes, 'schedules':schedules, 'class_schedule':class_schedule, 'otrahora':otrahora} ,context_instance=RequestContext(request))


@login_required
def selectStatistics(request):
	request.session.set_expiry(timeSleep)
	try:
		if request.method=="POST":
			args=request.POST
			desde = args['desde']
			hasta = args['hasta']
			cursos = args.getlist('selclase[]')
			horarios = args.getlist('selhora[]')
			radio = args['radioselect']
			tipochapter = args['typechapter']
			fechadesde = datetime.strptime(desde, '%Y-%m-%d')
			fechahasta = datetime.strptime(hasta, '%Y-%m-%d')+timedelta(days=1)-timedelta(seconds=1)
			if len(cursos)>1:
				j=0
				json_array = []
				for curso in cursos:
					classes = Class.objects.filter(id_class=curso).order_by('level','letter')
					N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
					for i in range(len(classes)):
						classes[i].nivel = N[int(classes[i].level)] 
					sclass = Student_Class.objects.filter(id_class_id=curso).values('kaid_student_id')
					students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
					if radio=="radio1":
						contador_est=0
						contador_vid=0
						time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_time=Sum('time_taken'))
						time_video = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_seconds=Sum('seconds_watched'))
						total_exercise = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_total=Count('kaid_student_id'))
						try:
							queryradiothree = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
							delta = timedelta(days=1)
							total_out=[]
							time_video_out=[]
							for qthree in queryradiothree:
								horas = Schedule.objects.filter(id_schedule=qthree['id_schedule_id']).values('start_time', 'end_time')
								inicio = horas[0]['start_time']
								final = horas[0]['end_time']
								d = fechadesde
								while d <= fechahasta:
									if d.strftime("%A")==qthree['day']:
										newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
										newend = d.strftime("%Y-%m-%d")+" "+final+":00"
										if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
											newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
											newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										else:
											newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
											newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
											time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
											total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
									d+=delta
							for total2 in total_exercise:
								for outt in total_out:
									if total2['kaid_student_id']==outt['kaid_student_id']:
										total2['total_total']= total2['total_total']-outt['total']
							
							for video2 in time_video:
								for out_video in time_video_out:
									if video2['kaid_student_id']==out_video['kaid_student_id']:
										video2['total_seconds']= video2['total_seconds']-out_video['seconds']
							

							for total3 in total_exercise:
								if total3['total_total']>0:
									contador_est+=1

							for video3 in time_video:
								if video3['total_seconds']>0:			
									contador_vid+=1

						except Exception as e:
							print e
					if radio=="radio2":
						queryradiotwo = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
						delta = timedelta(days=1)
						time_exercise=[]
						time_video=[]
						total_exercise=[]
						for qtwo in queryradiotwo:
							horas = Schedule.objects.filter(id_schedule=qtwo['id_schedule_id']).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==qtwo['day']:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta

						for student in students:
							timee = 0
							timev = 0
							totalt =0
							for time in time_exercise:
								if time['kaid_student_id']==student.kaid_student:
									timee=timee+time['time']
									time['total_time']=timee
							for video in time_video:
								if video['kaid_student_id']==student.kaid_student:
									timev=timev+video['seconds']
									video['total_seconds']=timev
							for total in total_exercise:
								if total['kaid_student_id']==student.kaid_student:
									totalt=totalt+total['total']
									total['total_total']=totalt

					if radio=="radio3":
						time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
						time_video = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
						total_exercise = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
						queryradiothree = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
						delta = timedelta(days=1)
						time_out=[]
						time_video_out=[]
						total_out=[]
						for qthree in queryradiothree:
							horas = Schedule.objects.filter(id_schedule=qthree['id_schedule_id']).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==qthree['day']:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
						for time in time_exercise:
							for out in time_out:
								if time['kaid_student_id']==out['kaid_student_id']:
									time['time']= time['time']-out['time']
							time['total_time']=time['time']
						for video in time_video:
							for out_video in time_video_out:
								if video['kaid_student_id']==out_video['kaid_student_id']:
									video['seconds']= video['seconds']-out_video['seconds']
							video['total_seconds']=video['seconds']
						for total in total_exercise:
							for outt in total_out:
								if total['kaid_student_id']==outt['kaid_student_id']:
									total['total']= total['total']-outt['total']
							total['total_total']=total['total']

					if radio=="radio4":
						time_exercise=[]
						time_video=[]
						total_exercise=[]
						for horario in horarios:
							newhorario=horario.split('_')
							largo = len(newhorario)
							delta = timedelta(days=1)
							if newhorario[2]=="OTRO":
								hours = newhorario[1].split(' - ')
								inicio = hours[0]
								final = hours[1]
								if final=="00:00":
									final = "23:59"
								d = fechadesde
								while d <= fechahasta:
									if d.strftime("%A")==newhorario[0]:
										newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
										newend = d.strftime("%Y-%m-%d")+" "+final+":00"
										if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
											newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
											newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										else:
											newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
											newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
										time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
										time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
										total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
									d+=delta
							else:
								horas = Schedule.objects.filter(id_schedule=newhorario[1]).values('start_time', 'end_time')
								inicio = horas[0]['start_time']
								final = horas[0]['end_time']
								d = fechadesde
								while d <= fechahasta:
									if d.strftime("%A")==newhorario[0]:
										newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
										newend = d.strftime("%Y-%m-%d")+" "+final+":00"
										if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
											newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
											newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										else:
											newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
											newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
										time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
										time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
										total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
									d+=delta
						for student in students:
							timee = 0
							timev = 0
							totalt= 0
							for time in time_exercise:
								if time['kaid_student_id']==student.kaid_student:
									timee=timee+time['time']
									time['total_time']=timee
							for video in time_video:
								if video['kaid_student_id']==student.kaid_student:
									timev=timev+video['seconds']
									video['total_seconds']=timev
							for total in total_exercise:
								if total['kaid_student_id']==student.kaid_student:
									totalt=totalt+total['total']
									total['total_total']=totalt
					
					delta = timedelta(days=1)
					cantidadclase=0
					diferencia=0
					queryclass = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
					d=fechadesde
					while d<= fechahasta:
						for qclass in queryclass:
							if d.strftime("%A")==qclass['day']:
								cantidadclase+=1
								horas = Schedule.objects.filter(id_schedule=qclass['id_schedule_id']).values('start_time', 'end_time')
								inicio = horas[0]['start_time']
								final = horas[0]['end_time']
								date_inicio = datetime.strptime(inicio, '%H:%M')
								date_final = datetime.strptime(final, '%H:%M')
								diferencia = diferencia+abs((date_final-date_inicio).seconds)
								#print abs((date_final-date_inicio).seconds)
						d+=delta
					
					dictTime = {}
					dictVideo = {}
					dictTotal = {}
					
					
					class_json={}
					class_json["id"] = j
					class_json["tiempo_ejercicios_clase"] = 0
					class_json["tiempo_videos_clase"] = 0
					class_json["total_ejercicios_clase"] = 0
					class_json["curso"] = curso
					class_json["cantidad_clases"]=cantidadclase
					class_json["tiempo_esperado"]=diferencia #tiempo esperado de trabajo para 1 estudiante
					try:
						class_json["estudiantes_out"]=contador_est
					except:
						class_json["estudiantes_out"]=0
					
					try:
						class_json["estudiantes_out_vid"]=contador_vid
					except:
						class_json["estudiantes_out_vid"]=0
					
					try:
						for clase in classes:
							if clase.additional:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)+" "+str(clase.additional)
							else:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)
					except Exception as e:
						print e
					
					#misiones = Chapter.objects.exclude(index=None).values('name_spanish', 'id_chapter_name')
					misiones = Chapter.objects.filter(type_chapter=tipochapter).values('name_spanish', 'id_chapter_name')
					dictChapter=[]
					
					dictHab={}
					chapts=[]

					for mision in misiones:
						dictSkill={}
						skills_mis={}
						skills_array=[]
						dictSkill["mision"]=mision['name_spanish']
						seleccion = Subtopic_Skill.objects.filter(id_subtopic_name_id__id_topic_name_id__id_chapter_name_id=mision['id_chapter_name']).values('id_skill_name_id')
						spanish_name = Skill.objects.filter(id_skill_name__in=seleccion)
						for selec in spanish_name:
							#spanish_name = Skill.objects.filter(id_skill_name=selec['id_skill_name_id']).values('name_spanish')
							skills_mis={'id': selec.id_skill_name, 'nombre_skill':selec.name_spanish,'nivel': {'mastery3':0, 'mastery2':0, 'mastery1':0, 'practiced':0, 'unstarted':0, 'struggling':0}}
							skills_array.append(skills_mis)
						dictSkill["habilidades"]=skills_array
						dictChapter.append(dictSkill)
					class_json["misiones"]=dictChapter

					cursor = connection.cursor()
					cursor.callproc("niveles", [int(curso), fechadesde, fechahasta])
					query = cursor.fetchall()

					for q in query:
						longitud=len(class_json["misiones"])
						for x in range(0, longitud-1):
							longskill=len(class_json["misiones"][x]["habilidades"])
							for y in range(0,longskill-1):
								if class_json["misiones"][x]["habilidades"][y]["id"]==q[2]:
									if q[3]==True:
										class_json["misiones"][x]["habilidades"][y]["nivel"]["struggling"]=q[1]
									else:
										class_json["misiones"][x]["habilidades"][y]["nivel"][q[0]]=q[1]
				
					
					for time in time_exercise:
						dictTime[time['kaid_student_id']] = time['total_time']
					for video in time_video:
						dictVideo[video['kaid_student_id']] = video['total_seconds']
					for total in total_exercise:
						dictTotal[total['kaid_student_id']] = total['total_total']

					i=0
					
					student_array=[]
					for student in students:
						student_json={}
						try:
							class_json["tiempo_ejercicios_clase"] = class_json["tiempo_ejercicios_clase"] + dictTime[student.kaid_student]
						except:
							class_json["tiempo_ejercicios_clase"] = class_json["tiempo_ejercicios_clase"] + 0
						try:
							class_json["tiempo_videos_clase"] = class_json["tiempo_videos_clase"] + dictVideo[student.kaid_student]
						except:
							class_json["tiempo_videos_clase"] = class_json["tiempo_videos_clase"] + 0
						try:
							class_json["total_ejercicios_clase"] = class_json["total_ejercicios_clase"] + dictTotal[student.kaid_student]
						except:
							class_json["total_ejercicios_clase"] = class_json["total_ejercicios_clase"] + 0
						try:
							student_json["kaid"]=student.kaid_student
						except:
							student_json["kaid"]="ninguno"
						try:
							student_json["name"] = student.nickname
						except:
							student_json["name"] = "ninguno"
						try:
							student_json["tiempo_ejercicios"] = dictTime[student.kaid_student]
						except:
							student_json["tiempo_ejercicios"] =  0
						try:
							student_json["tiempo_videos"] = dictVideo[student.kaid_student]
						except:
							student_json["tiempo_videos"] = 0
						try:
							student_json["total_ejercicios"] = dictTotal[student.kaid_student]
						except:
							student_json["total_ejercicios"] = 0
						
						i+=1
						student_array.append(student_json)
					class_json["students"]=student_array
					j+=1
					json_array.append(class_json)
				json_dict={"clases":json_array}
				json_data = json.dumps(json_dict)

			else:
				sclass = Student_Class.objects.filter(id_class_id=cursos[0]).values('kaid_student_id')
				students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
				if radio=="radio1":
					time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_time=Sum('time_taken'))
					time_video = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_seconds=Sum('seconds_watched'))
					total_exercise = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_total=Count('kaid_student_id'))
				if radio=="radio2":
					queryradiotwo = Class_Schedule.objects.filter(id_class_id=cursos[0]).values('day', 'id_schedule_id')
					delta = timedelta(days=1)
					time_exercise=[]
					time_video=[]
					total_exercise=[]
					for qtwo in queryradiotwo:
						horas = Schedule.objects.filter(id_schedule=qtwo['id_schedule_id']).values('start_time', 'end_time')
						inicio = horas[0]['start_time']
						final = horas[0]['end_time']
						d = fechadesde
						while d <= fechahasta:
							if d.strftime("%A")==qtwo['day']:
								newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
								newend = d.strftime("%Y-%m-%d")+" "+final+":00"
								if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								else:
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
								time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta
							
					for student in students:
						timee = 0
						timev = 0
						totalt =0
						for time in time_exercise:
							if time['kaid_student_id']==student.kaid_student:
								timee=timee+time['time']
								time['total_time']=timee
						for video in time_video:
							if video['kaid_student_id']==student.kaid_student:
								timev=timev+video['seconds']
								video['total_seconds']=timev
						for total in total_exercise:
							if total['kaid_student_id']==student.kaid_student:
								totalt=totalt+total['total']
								total['total_total']=totalt

	
				if radio=="radio3":
					time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
					time_video = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
					total_exercise = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
					queryradiothree = Class_Schedule.objects.filter(id_class_id=cursos[0]).values('day', 'id_schedule_id')
					delta = timedelta(days=1)
					time_out=[]
					time_video_out=[]
					total_out=[]
					for qthree in queryradiothree:
						horas = Schedule.objects.filter(id_schedule=qthree['id_schedule_id']).values('start_time', 'end_time')
						inicio = horas[0]['start_time']
						final = horas[0]['end_time']
						d = fechadesde
						while d <= fechahasta:
							if d.strftime("%A")==qthree['day']:
								newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
								newend = d.strftime("%Y-%m-%d")+" "+final+":00"
								if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								else:
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
								time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta

					for time in time_exercise:
						for out in time_out:
							if time['kaid_student_id']==out['kaid_student_id']:
								time['time']= time['time']-out['time']
						time['total_time']=time['time']
					for video in time_video:
						for out_video in time_video_out:
							if video['kaid_student_id']==out_video['kaid_student_id']:
								video['seconds']= video['seconds']-out_video['seconds']
						video['total_seconds']=video['seconds']
					for total in total_exercise:
						for outt in total_out:
							if total['kaid_student_id']==outt['kaid_student_id']:
								total['total']= total['total']-outt['total']
						total['total_total']=total['total']

				if radio=="radio4":
					time_exercise=[]
					time_video=[]
					total_exercise=[]
					for horario in horarios:
						newhorario=horario.split('_')
						largo = len(newhorario)
						delta = timedelta(days=1)
						if newhorario[2]=="OTRO":
							hours = newhorario[1].split(' - ')
							inicio = hours[0]
							final = hours[1]
							if final=="00:00":
								final="23:59"
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==newhorario[0]:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
						else:
							horas = Schedule.objects.filter(id_schedule=newhorario[1]).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==newhorario[0]:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
					for student in students:
						timee = 0
						timev = 0
						totalt= 0
						for time in time_exercise:
							if time['kaid_student_id']==student.kaid_student:
								timee=timee+time['time']
								time['total_time']=timee
						for video in time_video:
							if video['kaid_student_id']==student.kaid_student:
								timev=timev+video['seconds']
								video['total_seconds']=timev
						for total in total_exercise:
							if total['kaid_student_id']==student.kaid_student:
								totalt=totalt+total['total']
								total['total_total']=totalt


				dictTime = {}
				dictVideo = {}
				dictTotal = {}
				for time in time_exercise:
					dictTime[time['kaid_student_id']] = time['total_time']
				for video in time_video:
					dictVideo[video['kaid_student_id']] = video['total_seconds']
				for total in total_exercise:
					dictTotal[total['kaid_student_id']] = total['total_total']

				i=0
				json_array = []
				for student in students:
					student_json = {}
					student_json["id"] = i
					try:
						student_json["kaid"] = student.kaid_student
					except:
						student_json["kaid"] = "ninguno"
					try:
						student_json["name"] = student.nickname
					except:
						student_json["name"] = "ninguno"
					try:
						student_json["tiempo_ejercicios"] = dictTime[student.kaid_student]
					except:
						student_json["tiempo_ejercicios"] =  0
					try:
						student_json["tiempo_videos"] = dictVideo[student.kaid_student]
					except:
						student_json["tiempo_videos"] = 0
					try:
						student_json["total_ejercicios"] = dictTotal[student.kaid_student]
					except:
						student_json["total_ejercicios"] = 0
 					i+=1
					json_array.append(student_json)
				j+=1
				json_dict={"students":json_array}
				json_data = json.dumps(json_dict)

			return HttpResponse(json_data)
	except Exception as e:
		print e

@login_required
def selectChapter(request):
	request.session.set_expiry(timeSleep)
	try:
		if request.method=="POST":
			args=request.POST
			desde = args['desde']
			hasta = args['hasta']
			cursos = args.getlist('selclase[]')
			tipochapter = args['typechapter']
			fechadesde = datetime.strptime(desde, '%Y-%m-%d')
			fechahasta = datetime.strptime(hasta, '%Y-%m-%d')+timedelta(days=1)-timedelta(seconds=1)
			if len(cursos)>1:
				j=0
				json_array = []
				for curso in cursos:
					classes = Class.objects.filter(id_class=curso).order_by('level','letter')
					N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
					for i in range(len(classes)):
						classes[i].nivel = N[int(classes[i].level)] 
					sclass = Student_Class.objects.filter(id_class_id=curso).values('kaid_student_id')
					students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
					class_json={}
					class_json["id"] = j
					class_json["curso"] = curso
					try:
						for clase in classes:
							if clase.additional:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)+" "+str(clase.additional)
							else:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)
					except Exception as e:
						print e

					#misiones = Chapter.objects.exclude(index=None).values('name_spanish', 'id_chapter_name')
					misiones = Chapter.objects.filter(type_chapter=tipochapter).values('name_spanish', 'id_chapter_name')
					dictChapter=[]
					
					dictHab={}
					chapts=[]

					for mision in misiones:
						dictSkill={}
						skills_mis={}
						skills_array=[]
						dictSkill["mision"]=mision['name_spanish']
						seleccion = Subtopic_Skill.objects.filter(id_subtopic_name_id__id_topic_name_id__id_chapter_name_id=mision['id_chapter_name']).values('id_skill_name_id')
						spanish_name = Skill.objects.filter(id_skill_name__in=seleccion)
						for selec in spanish_name:
							#spanish_name = Skill.objects.filter(id_skill_name=selec['id_skill_name_id']).values('name_spanish')
							skills_mis={'id': selec.id_skill_name, 'nombre_skill':selec.name_spanish,'nivel': {'mastery3':0, 'mastery2':0, 'mastery1':0, 'practiced':0, 'unstarted':0, 'struggling':0}}
							skills_array.append(skills_mis)
						dictSkill["habilidades"]=skills_array
						dictChapter.append(dictSkill)
					class_json["misiones"]=dictChapter

					cursor = connection.cursor()
					cursor.callproc("niveles", [int(curso), fechadesde, fechahasta])
					query = cursor.fetchall()
					class_json["students"]=len(students)
					for q in query:
						longitud=len(class_json["misiones"])
						for x in range(0, longitud-1):
							longskill=len(class_json["misiones"][x]["habilidades"])
							for y in range(0,longskill-1):
								if class_json["misiones"][x]["habilidades"][y]["id"]==q[2]:
									if q[3]==True:
										class_json["misiones"][x]["habilidades"][y]["nivel"]["struggling"]=q[1]
									else:
										class_json["misiones"][x]["habilidades"][y]["nivel"][q[0]]=q[1]
					json_array.append(class_json)
					j+=1
				json_dict={"clases":json_array}
				json_data = json.dumps(json_dict)
		return HttpResponse(json_data)
	except Exception as e:
		print e

@login_required
def compareStatistics(request):
	request.session.set_expiry(timeSleep)
	try:
		if request.method=="POST":
			args=request.POST
			desde = args['desde']
			hasta = args['hasta']
			cursos = args.getlist('selclase[]')
			radio = args['radioselect']
			fechadesde = datetime.strptime(desde, '%Y-%m-%d')
			fechahasta = datetime.strptime(hasta, '%Y-%m-%d')+timedelta(days=1)-timedelta(seconds=1)
			if len(cursos)>1:
				j=0
				json_array = []
				for curso in cursos:
					class_json={}
					classes = Class.objects.filter(id_class=curso).order_by('level','letter')
					N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
					for i in range(len(classes)):
						classes[i].nivel = N[int(classes[i].level)] 
					sclass = Student_Class.objects.filter(id_class_id=curso).values('kaid_student_id')
					students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
					if radio=="radio5":
						time_exercise_1 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_time=Sum('time_taken'))
						time_video_1 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_seconds=Sum('seconds_watched'))
						total_exercise_1 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_total=Count('kaid_student_id'))

						queryradiofive = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
						delta = timedelta(days=1)
						time_exercise_2=[]
						time_video_2=[]
						total_exercise_2=[]
						for qfive in queryradiofive:
							horas = Schedule.objects.filter(id_schedule=qfive['id_schedule_id']).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==qfive['day']:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_exercise_2.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video_2.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise_2.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
						class_json["tipo1"] = "Todos"
						class_json["tipo2"] = "Horario de clases"

						for student in students:
							timee = 0
							timev = 0
							totalt =0
							for time in time_exercise_2:
								if time['kaid_student_id']==student.kaid_student:
									timee=timee+time['time']
									time['total_time']=timee
							for video in time_video_2:
								if video['kaid_student_id']==student.kaid_student:
									timev=timev+video['seconds']
									video['total_seconds']=timev
							for total in total_exercise_2:
								if total['kaid_student_id']==student.kaid_student:
									totalt=totalt+total['total']
									total['total_total']=totalt

					if radio=="radio6":
						time_exercise_1 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_time=Sum('time_taken'))
						time_video_1 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_seconds=Sum('seconds_watched'))
						total_exercise_1 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_total=Count('kaid_student_id'))

						time_exercise_2 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
						time_video_2 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
						total_exercise_2 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
						queryradiosix = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
						delta = timedelta(days=1)
						time_out=[]
						time_video_out=[]
						total_out=[]
						for qsix in queryradiosix:
							horas = Schedule.objects.filter(id_schedule=qsix['id_schedule_id']).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==qsix['day']:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
						for time in time_exercise_2:
							for out in time_out:
								if time['kaid_student_id']==out['kaid_student_id']:
									time['time']= time['time']-out['time']
							time['total_time']=time['time']
						for video in time_video_2:
							for out_video in time_video_out:
								if video['kaid_student_id']==out_video['kaid_student_id']:
									video['seconds']= video['seconds']-out_video['seconds']
							video['total_seconds']=video['seconds']
						for total in total_exercise_2:
							for outt in total_out:
								if total['kaid_student_id']==outt['kaid_student_id']:
									total['total']= total['total']-outt['total']
							total['total_total']=total['total']
						class_json["tipo1"] = "Todos"
						class_json["tipo2"] = "Fuera horario de clases"

					if radio=="radio7":
						queryradiofive = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
						delta = timedelta(days=1)
						time_exercise_1=[]
						time_video_1=[]
						total_exercise_1=[]
						for qfive in queryradiofive:
							horas = Schedule.objects.filter(id_schedule=qfive['id_schedule_id']).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==qfive['day']:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_exercise_1.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video_1.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise_1.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta

						for student in students:
							timee = 0
							timev = 0
							totalt =0
							for time in time_exercise_1:
								if time['kaid_student_id']==student.kaid_student:
									timee=timee+time['time']
									time['total_time']=timee
							for video in time_video_1:
								if video['kaid_student_id']==student.kaid_student:
									timev=timev+video['seconds']
									video['total_seconds']=timev
							for total in total_exercise_1:
								if total['kaid_student_id']==student.kaid_student:
									totalt=totalt+total['total']
									total['total_total']=totalt

						time_exercise_2 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
						time_video_2 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
						total_exercise_2 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
						queryradiosix = Class_Schedule.objects.filter(id_class_id=curso).values('day', 'id_schedule_id')
						delta = timedelta(days=1)
						time_out=[]
						time_video_out=[]
						total_out=[]
						for qsix in queryradiosix:
							horas = Schedule.objects.filter(id_schedule=qsix['id_schedule_id']).values('start_time', 'end_time')
							inicio = horas[0]['start_time']
							final = horas[0]['end_time']
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==qsix['day']:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":00"
									if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									else:
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
									time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
						for time in time_exercise_2:
							for out in time_out:
								if time['kaid_student_id']==out['kaid_student_id']:
									time['time']= time['time']-out['time']
							time['total_time']=time['time']
						for video in time_video_2:
							for out_video in time_video_out:
								if video['kaid_student_id']==out_video['kaid_student_id']:
									video['seconds']= video['seconds']-out_video['seconds']
							video['total_seconds']=video['seconds']
						for total in total_exercise_2:
							for outt in total_out:
								if total['kaid_student_id']==outt['kaid_student_id']:
									total['total']= total['total']-outt['total']
							total['total_total']=total['total']
						class_json["tipo1"] = "Horario de clases"
						class_json["tipo2"] = "Fuera horario de clases"


					dictTime_1 = {}
					dictVideo_1 = {}
					dictTotal_1 = {}
					dictTime_2 = {}
					dictVideo_2 = {}
					dictTotal_2 = {}
					
					#class_json={}
					class_json["id"] = j
					class_json["tiempo_ejercicios_clase_1"] = 0
					class_json["tiempo_videos_clase_1"] = 0
					class_json["total_ejercicios_clase_1"] = 0
					class_json["tiempo_ejercicios_clase_2"] = 0
					class_json["tiempo_videos_clase_2"] = 0
					class_json["total_ejercicios_clase_2"] = 0
					class_json["curso"] = curso

					try:
						for clase in classes:
							if clase.additional:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)+" "+str(clase.additional)
							else:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)
					except Exception as e:
						print e

					
					for time_1 in time_exercise_1:
						dictTime_1[time_1['kaid_student_id']] = time_1['total_time']
					for video_1 in time_video_1:
						dictVideo_1[video_1['kaid_student_id']] = video_1['total_seconds']
					for total_1 in total_exercise_1:
						dictTotal_1[total_1['kaid_student_id']] = total_1['total_total']

					for time_2 in time_exercise_2:
						dictTime_2[time_2['kaid_student_id']] = time_2['total_time']
					for video_2 in time_video_2:
						dictVideo_2[video_2['kaid_student_id']] = video_2['total_seconds']
					for total_2 in total_exercise_2:
						dictTotal_2[total_2['kaid_student_id']] = total_2['total_total']

					student_array=[]
					i=0
					for student in students:
						try:
							class_json["tiempo_ejercicios_clase_1"] = class_json["tiempo_ejercicios_clase_1"] + dictTime_1[student.kaid_student]
						except:
							class_json["tiempo_ejercicios_clase_1"] = class_json["tiempo_ejercicios_clase_1"] + 0
						try:
							class_json["tiempo_videos_clase_1"] = class_json["tiempo_videos_clase_1"] + dictVideo_1[student.kaid_student]
						except:
							class_json["tiempo_videos_clase_1"] = class_json["tiempo_videos_clase_1"] + 0
						try:
							class_json["total_ejercicios_clase_1"] = class_json["total_ejercicios_clase_1"] + dictTotal_1[student.kaid_student]
						except:
							class_json["total_ejercicios_clase_1"] = class_json["total_ejercicios_clase_1"] + 0
						try:
							class_json["tiempo_ejercicios_clase_2"] = class_json["tiempo_ejercicios_clase_2"] + dictTime_2[student.kaid_student]
						except:
							class_json["tiempo_ejercicios_clase_2"] = class_json["tiempo_ejercicios_clase_2"] + 0
						try:
							class_json["tiempo_videos_clase_2"] = class_json["tiempo_videos_clase_2"] + dictVideo_2[student.kaid_student]
						except:
							class_json["tiempo_videos_clase_2"] = class_json["tiempo_videos_clase_2"] + 0
						try:
							class_json["total_ejercicios_clase_2"] = class_json["total_ejercicios_clase_2"] + dictTotal_2[student.kaid_student]
						except:
							class_json["total_ejercicios_clase_2"] = class_json["total_ejercicios_clase_2"] + 0
						
						student_json = {}
						student_json["id"] = i
						try:
							student_json["kaid"] = student.kaid_student
						except:
							student_json["kaid"] = "ninguno"
						
						try:
							student_json["name"] = student.nickname
						except:
							student_json["name"] = "ninguno"
						try:
							student_json["tiempo_ejercicios_1"] = dictTime_1[student.kaid_student]
						except:
							student_json["tiempo_ejercicios_1"] =  0
						try:
							student_json["tiempo_videos_1"] = dictVideo_1[student.kaid_student]
						except:
							student_json["tiempo_videos_1"] = 0
						try:
							student_json["total_ejercicios_1"] = dictTotal_1[student.kaid_student]
						except:
							student_json["total_ejercicios_1"] = 0
						try:
							student_json["tiempo_ejercicios_2"] = dictTime_2[student.kaid_student]
						except:
							student_json["tiempo_ejercicios_2"] =  0
						try:
							student_json["tiempo_videos_2"] = dictVideo_2[student.kaid_student]
						except:
							student_json["tiempo_videos_2"] = 0
						try:
							student_json["total_ejercicios_2"] = dictTotal_2[student.kaid_student]
						except:
							student_json["total_ejercicios_2"] = 0
						#student_json["tipo1"] = tipo1
						#student_json["tipo2"] = tipo2
	 					#i+=1
	 					
						#json_array.append(student_json)
						i+=1
						student_array.append(student_json)
					class_json["students"]=student_array
					j+=1
					json_array.append(class_json)
				json_dict={"clases":json_array}
				json_data = json.dumps(json_dict)
			
			else:
				sclass = Student_Class.objects.filter(id_class_id=cursos[0]).values('kaid_student_id')
				students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
				if radio=="radio5":
					tipo1 = "Todo"
					tipo2 = "Horario de clases"
					time_exercise_1 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_time=Sum('time_taken'))
					time_video_1 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_seconds=Sum('seconds_watched'))
					total_exercise_1 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_total=Count('kaid_student_id'))

					queryradiofive = Class_Schedule.objects.filter(id_class_id=cursos[0]).values('day', 'id_schedule_id')
					delta = timedelta(days=1)
					time_exercise_2=[]
					time_video_2=[]
					total_exercise_2=[]
					for qfive in queryradiofive:
						horas = Schedule.objects.filter(id_schedule=qfive['id_schedule_id']).values('start_time', 'end_time')
						inicio = horas[0]['start_time']
						final = horas[0]['end_time']
						d = fechadesde
						while d <= fechahasta:
							if d.strftime("%A")==qfive['day']:
								newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
								newend = d.strftime("%Y-%m-%d")+" "+final+":00"
								if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								else:
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
								time_exercise_2.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video_2.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_exercise_2.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta
					for student in students:
						timee = 0
						timev = 0
						totalt =0
						for time in time_exercise_2:
							if time['kaid_student_id']==student.kaid_student:
								timee=timee+time['time']
								time['total_time']=timee
						for video in time_video_2:
							if video['kaid_student_id']==student.kaid_student:
								timev=timev+video['seconds']
								video['total_seconds']=timev
						for total in total_exercise_2:
							if total['kaid_student_id']==student.kaid_student:
								totalt=totalt+total['total']
								total['total_total']=totalt

				if radio=="radio6":
					tipo1 = "Todo"
					tipo2 = "Fuera horario de clases"
					time_exercise_1 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_time=Sum('time_taken'))
					time_video_1 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_seconds=Sum('seconds_watched'))
					total_exercise_1 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total_total=Count('kaid_student_id'))

					time_exercise_2 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
					time_video_2 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
					total_exercise_2 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
					queryradiosix = Class_Schedule.objects.filter(id_class_id=cursos[0]).values('day', 'id_schedule_id')
					delta = timedelta(days=1)
					time_out=[]
					time_video_out=[]
					total_out=[]
					for qsix in queryradiosix:
						horas = Schedule.objects.filter(id_schedule=qsix['id_schedule_id']).values('start_time', 'end_time')
						inicio = horas[0]['start_time']
						final = horas[0]['end_time']
						d = fechadesde
						while d <= fechahasta:
							if d.strftime("%A")==qsix['day']:
								newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
								newend = d.strftime("%Y-%m-%d")+" "+final+":00"
								if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								else:
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
								time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta

					for time in time_exercise_2:
						for out in time_out:
							if time['kaid_student_id']==out['kaid_student_id']:
								time['time']= time['time']-out['time']
						time['total_time']=time['time']
					for video in time_video_2:
						for out_video in time_video_out:
							if video['kaid_student_id']==out_video['kaid_student_id']:
								video['seconds']= video['seconds']-out_video['seconds']
						video['total_seconds']=video['seconds']
					for total in total_exercise_2:
						for outt in total_out:
							if total['kaid_student_id']==outt['kaid_student_id']:
								total['total']= total['total']-outt['total']
						total['total_total']=total['total']

				if radio=="radio7":
					tipo1 = "Horario de clases"
					tipo2 = "Fuera horario de clases"
					queryradiofive = Class_Schedule.objects.filter(id_class_id=cursos[0]).values('day', 'id_schedule_id')
					delta = timedelta(days=1)
					time_exercise_1=[]
					time_video_1=[]
					total_exercise_1=[]
					for qfive in queryradiofive:
						horas = Schedule.objects.filter(id_schedule=qfive['id_schedule_id']).values('start_time', 'end_time')
						inicio = horas[0]['start_time']
						final = horas[0]['end_time']
						d = fechadesde
						while d <= fechahasta:
							if d.strftime("%A")==qfive['day']:
								newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
								newend = d.strftime("%Y-%m-%d")+" "+final+":00"
								if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								else:
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
								time_exercise_1.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video_1.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_exercise_1.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta
					for student in students:
						timee = 0
						timev = 0
						totalt =0
						for time in time_exercise_1:
							if time['kaid_student_id']==student.kaid_student:
								timee=timee+time['time']
								time['total_time']=timee
						for video in time_video_1:
							if video['kaid_student_id']==student.kaid_student:
								timev=timev+video['seconds']
								video['total_seconds']=timev
						for total in total_exercise_1:
							if total['kaid_student_id']==student.kaid_student:
								totalt=totalt+total['total']
								total['total_total']=totalt

					time_exercise_2 = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
					time_video_2 = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
					total_exercise_2 = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
					queryradiosix = Class_Schedule.objects.filter(id_class_id=cursos[0]).values('day', 'id_schedule_id')
					delta = timedelta(days=1)
					time_out=[]
					time_video_out=[]
					total_out=[]
					for qsix in queryradiosix:
						horas = Schedule.objects.filter(id_schedule=qsix['id_schedule_id']).values('start_time', 'end_time')
						inicio = horas[0]['start_time']
						final = horas[0]['end_time']
						d = fechadesde
						while d <= fechahasta:
							if d.strftime("%A")==qsix['day']:
								newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
								newend = d.strftime("%Y-%m-%d")+" "+final+":00"
								if d.strftime("%Y-%m-%d")>'2016-05-14' and d.strftime("%Y-%m-%d")<'2016-08-14':
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								else:
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')
								time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta

					for time in time_exercise_2:
						for out in time_out:
							if time['kaid_student_id']==out['kaid_student_id']:
								time['time']= time['time']-out['time']
						time['total_time']=time['time']
					for video in time_video_2:
						for out_video in time_video_out:
							if video['kaid_student_id']==out_video['kaid_student_id']:
								video['seconds']= video['seconds']-out_video['seconds']
						video['total_seconds']=video['seconds']
					for total in total_exercise_2:
						for outt in total_out:
							if total['kaid_student_id']==outt['kaid_student_id']:
								total['total']= total['total']-outt['total']
						total['total_total']=total['total']

				

				dictTime_1 = {}
				dictVideo_1 = {}
				dictTotal_1 = {}
				dictTime_2 = {}
				dictVideo_2 = {}
				dictTotal_2 = {}
				for time in time_exercise_1:
					dictTime_1[time['kaid_student_id']] = time['total_time']
				for video in time_video_1:
					dictVideo_1[video['kaid_student_id']] = video['total_seconds']
				for total in total_exercise_1:
					dictTotal_1[total['kaid_student_id']] = total['total_total']

				for time in time_exercise_2:
					dictTime_2[time['kaid_student_id']] = time['total_time']
				for video in time_video_2:
					dictVideo_2[video['kaid_student_id']] = video['total_seconds']
				for total in total_exercise_2:
					dictTotal_2[total['kaid_student_id']] = total['total_total']
				i=0
				json_array = []
				for student in students:
					student_json = {}
					student_json["id"] = i
					try:
						student_json["kaid"] = student.kaid_student
					except:
						student_json["kaid"] = "ninguno"
					try:
						student_json["name"] = student.nickname
					except:
						student_json["name"] = "ninguno"
					try:
						student_json["tiempo_ejercicios_1"] = dictTime_1[student.kaid_student]
					except:
						student_json["tiempo_ejercicios_1"] =  0
					try:
						student_json["tiempo_videos_1"] = dictVideo_1[student.kaid_student]
					except:
						student_json["tiempo_videos_1"] = 0
					try:
						student_json["total_ejercicios_1"] = dictTotal_1[student.kaid_student]
					except:
						student_json["total_ejercicios_1"] = 0
					try:
						student_json["tiempo_ejercicios_2"] = dictTime_2[student.kaid_student]
					except:
						student_json["tiempo_ejercicios_2"] =  0
					try:
						student_json["tiempo_videos_2"] = dictVideo_2[student.kaid_student]
					except:
						student_json["tiempo_videos_2"] = 0
					try:
						student_json["total_ejercicios_2"] = dictTotal_2[student.kaid_student]
					except:
						student_json["total_ejercicios_2"] = 0
					student_json["tipo1"] = tipo1
					student_json["tipo2"] = tipo2
 					i+=1
					json_array.append(student_json)
				json_dict={"students":json_array}
				json_data = json.dumps(json_dict)

			return HttpResponse(json_data)
		
		return HttpResponse(json_data)
	except Exception as e:
		print e