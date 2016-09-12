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
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule, Class, Student_Class, Skill_Attempt, Student
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
@login_required()
def getStatistics(request):
	request.session.set_expiry(timeSleep)
	try:
		teacher = Teacher.objects.get(email=request.user.email)
	except:
		return render_to_response('statistics.html', context_instance=RequestContext(request))
	if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
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
	start = "23:59"
	end = "23:59"
	otrahora = []
	largo = len(schedules)
	j=0
	for sched in schedules:
		j=j+1
		if sched.start_time!=start:
			horaini = datetime.strptime(start, "%H:%M") + timedelta(minutes=1)
			start = horaini.strftime('%H:%M')
			horafn= datetime.strptime(sched.start_time,"%H:%M") + timedelta(minutes=-1)
			horafn = horafn.strftime('%H:%M')
			otrahora.append(start +" - "+ horafn)
			start = sched.end_time
		if j==largo:
			horaini = datetime.strptime(sched.end_time, "%H:%M") + timedelta(minutes=1)
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
			if len(cursos)>1:
				for curso in cursos:
					for horario in horarios:
						fechadesde = datetime.strptime(desde, '%Y-%m-%d')
						#print fechadesde.isoweekday()
						sclass = Student_Class.objects.filter(id_class_id=curso).values('kaid_student_id')
						#print sclass
			else:
				sclass = Student_Class.objects.filter(id_class_id=cursos[0]).values('kaid_student_id')
				students=Student.objects.filter(kaid_student__in=sclass).order_by('nickname')
				time_exercise = Skill_Attempt.objects.filter(kaid_student_id__in=students).values('kaid_student_id').annotate(time=Sum('time_taken'))
				#for sc in sclass:
					#print sc['kaid_student_id']
				#	time_exercise = Skill_Attempt.objects.filter(kaid_student_id=sc['kaid_student_id']).values('kaid_student_id').annotate(time=Sum('time_taken'))
					#tiempo = [time_exercise]
				#	print time_exercise
				dictTime = {}
				for time in time_exercise:
					dictTime[time['kaid_student_id']] = time['time']
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
						student_json["stats"] = {"tiempo_ejecicios": dictTime[student.kaid_student]}
					except:
						student_json["stats"] = 0
					i+=1
					json_array.append(student_json)
				json_dict={"students":json_array}
				json_data = json.dumps(json_dict)
				print json_data

				
				fechadesde = datetime.strptime(desde, '%Y-%m-%d')
				#diacomienzo = fechadesde.isoweekday()
				fechahasta = datetime.strptime(hasta, '%Y-%m-%d')
				#fechahasta = fechahasta.isoweekday()
					#aqui va una consulta
		
					#print fechadesde.isoweekday()	
			return HttpResponse(json_data)
	except Exception as e:
		print e