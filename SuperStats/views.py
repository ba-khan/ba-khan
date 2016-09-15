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
from bakhanapp.models import Schedule
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
def getSuperStats(request):
	request.session.set_expiry(timeSleep)
	institutions = Institution.objects.all().order_by('id_institution')

	return render_to_response('superstats.html', { 'institutions':institutions} ,context_instance=RequestContext(request))

@permission_required('bakhanapp.isSuper', login_url="/")
def selectClass(request):
	request.session.set_expiry(timeSleep)
	if request.method=="POST":
		args=request.POST
		instituciones = args.getlist('sel[]')
		for institucion in instituciones:
			clases = Class.objects.filter(id_institution_id=institucion).order_by('level','letter')
			N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
			for i in range(len(classes)):
				classes[i].level = N[int(classes[i].level)] 
		return HttpResponse("hola")


@permission_required('bakhanapp.isSuper', login_url="/")
def selectSuperStats(request):
	request.session.set_expiry(timeSleep)
	try:
		if request.method=="POST":
			args=request.POST
			desde = args['desde']
			hasta = args['hasta']
			cursos = args.getlist('selclase[]')
			horarios = args.getlist('selhora[]')
			radio = args['radioselect']
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
						time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
						time_video = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
						total_exercise = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
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
									newend = d.strftime("%Y-%m-%d")+" "+final+":59"
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
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
									newend = d.strftime("%Y-%m-%d")+" "+final+":59"
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta
						for time in time_exercise:
							for out in time_out:
								if time['kaid_student_id']==out['kaid_student_id']:
									time['time']= time['time']-out['time']
						for video in time_video:
							for out_video in time_video_out:
								if video['kaid_student_id']==out_video['kaid_student_id']:
									video['seconds']= video['seconds']-out_video['seconds']
						for total in total_exercise:
							for outt in total_out:
								if total['kaid_student_id']==outt['kaid_student_id']:
									total['total']= total['total']-outt['total']

					if radio=="radio4":
						time_exercise=[]
						time_video=[]
						total_exercise=[]
						for horario in horarios:
							newhorario=horario.split('_')
							largo = len(newhorario)
							delta = timedelta(days=1)
							if largo==3:
								hours = newhorario[1].split(' - ')
								inicio = hours[0]
								final = hours[1]
								d = fechadesde
								while d <= fechahasta:
									if d.strftime("%A")==newhorario[0]:
										newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
										newend = d.strftime("%Y-%m-%d")+" "+final+":59"
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
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
										newend = d.strftime("%Y-%m-%d")+" "+final+":59"
										newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
										time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
										time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
										total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
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
					try:
						for clase in classes:
							if clase.additional:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)+" "+str(clase.additional)
							else:
								class_json["nombre"]=str(clase.nivel)+" "+str(clase.letter)+" "+str(clase.year)
					except Exception as e:
						print e

					
					for time in time_exercise:
						dictTime[time['kaid_student_id']] = time['time']
					for video in time_video:
						dictVideo[video['kaid_student_id']] = video['seconds']
					for total in total_exercise:
						dictTotal[total['kaid_student_id']] = total['total']
					i=0
					for student in students:
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
						i+=1
					
					j+=1
					json_array.append(class_json)
				json_dict={"clases":json_array}
				json_data = json.dumps(json_dict)

			else:
				sclass = Student_Class.objects.filter(id_class_id=cursos[0]).values('kaid_student_id')
				students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
				if radio=="radio1":
					time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(time=Sum('time_taken'))
					time_video = Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))
					total_exercise = Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[fechadesde, fechahasta]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))
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
								newend = d.strftime("%Y-%m-%d")+" "+final+":59"
								newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta
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
								newend = d.strftime("%Y-%m-%d")+" "+final+":59"
								newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
								time_out.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
								time_video_out.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
								total_out.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
							d+=delta
					for time in time_exercise:
						for out in time_out:
							if time['kaid_student_id']==out['kaid_student_id']:
								time['time']= time['time']-out['time']
					for video in time_video:
						for out_video in time_video_out:
							if video['kaid_student_id']==out_video['kaid_student_id']:
								video['seconds']= video['seconds']-out_video['seconds']
					for total in total_exercise:
						for outt in total_out:
							if total['kaid_student_id']==outt['kaid_student_id']:
								total['total']= total['total']-outt['total']

				if radio=="radio4":
					time_exercise=[]
					time_video=[]
					total_exercise=[]
					for horario in horarios:
						newhorario=horario.split('_')
						largo = len(newhorario)
						delta = timedelta(days=1)
						if largo==3:
							hours = newhorario[1].split(' - ')
							inicio = hours[0]
							final = hours[1]
							d = fechadesde
							while d <= fechahasta:
								if d.strftime("%A")==newhorario[0]:
									newstart = d.strftime("%Y-%m-%d")+" "+inicio +":00"
									newend = d.strftime("%Y-%m-%d")+" "+final+":59"
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
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
									newend = d.strftime("%Y-%m-%d")+" "+final+":59"
									newstart = datetime.strptime(newstart, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									newend = datetime.strptime(newend, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1)
									time_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student_id__in=students,date__range=[newstart, newend]).values('kaid_student_id').annotate(time=Sum('time_taken'))))
									time_video.extend(list(Video_Playing.objects.filter(kaid_student_id__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(seconds=Sum('seconds_watched'))))
									total_exercise.extend(list(Skill_Attempt.objects.filter(kaid_student__in=students, date__range=[newstart, newend]).values('kaid_student_id').annotate(total=Count('kaid_student_id'))))
								d+=delta

				dictTime = {}
				dictVideo = {}
				dictTotal = {}
				for time in time_exercise:
					dictTime[time['kaid_student_id']] = time['time']
				for video in time_video:
					dictVideo[video['kaid_student_id']] = video['seconds']
				for total in total_exercise:
					dictTotal[total['kaid_student_id']] = total['total']
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
				json_dict={"students":json_array}
				json_data = json.dumps(json_dict)

			return HttpResponse(json_data)
	except Exception as e:
		print e