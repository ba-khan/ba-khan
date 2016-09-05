""" """
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher,Class_Subject, Class_Schedule
from bakhanapp.models import Schedule
from django.db import connection

register = template.Library()
from configs import timeSleep

import json


##
## @brief      Gets the schedules.
##
## @param      request  The request
##
## @return     The schedules.
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def getSchedules(request):
    request.session.set_expiry(timeSleep)
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except:
        return render_to_response('horario.html', context_instance=RequestContext(request))
    schedules = Schedule.objects.filter(id_institution_id=teacher.id_institution_id).order_by('start_time')
    teachers = Teacher.objects.filter(id_institution_id=teacher.id_institution_id)
    class_schedule = Class_Schedule.objects.filter(kaid_teacher_id__in=teachers)
    return render_to_response('horario.html', {'schedules': schedules, 'teachers': teachers, 'class_schedule': class_schedule}, context_instance=RequestContext(request))


##
## @brief      Deletes a schedule.
##
## @param      request  The request
##
## @return     HttpResponse
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def deleteSchedule(request):
	try:
	    request.session.set_expiry(timeSleep)
	    user = Teacher.objects.get(email=request.user.email)
	    if request.is_ajax():
	        if request.method == 'POST':
	            json_str = json.loads(request.body)
	            sched = Schedule.objects.filter(name_block=json_str["schBlock"], start_time=json_str["schStart"], end_time=json_str["schEnd"],id_institution_id=user.id_institution_id).delete()
	            return HttpResponse("Bloque eliminado correctamente")

	    return HttpResponse("Error al eliminar")
	except Exception as e:
		print e


##
## @brief      Create a schedule
##
## @param      request  The request
##
## @return     HttpResponse
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def newSchedule(request):
    request.session.set_expiry(timeSleep)
    user = Teacher.objects.get(email=request.user.email)
    if request.method == 'POST':
        args = request.POST
        try:
            #falta validar que los bloques no se solapen

            result=validateTime(args['start'], args['end'], user.id_institution_id, args['block'])
            if not all(result):
                return HttpResponse("Los horarios no se pueden solapar, revise las horas")
            else:
                Schedule.objects.create(name_block=args['block'],
                start_time=args['start'],
                end_time=args['end'],
                id_institution_id=user.id_institution_id)
                return HttpResponse("Bloque guardado correctamente")     
        except Exception as e:
        	print e
        	return HttpResponse("Error al guardar")
    return HttpResponse("Error al guardar")


def validateTime(start_time, end_time, id_institution_id, name_block):
    cursor = connection.cursor()
    cursor.execute("select count(*) from (values (%s, %s, %s, %s)) as t(start_time, end_time, id_institution_id, name_block) where not exists (select 1 from bakhanapp_schedule as m where m.id_institution_id=t.id_institution_id and (t.start_time<m.end_time and t.end_time>m.start_time))", (start_time,  end_time, id_institution_id, name_block))
    query = cursor.fetchone()
    return query

@permission_required('bakhanapp.isAdmin', login_url="/")
def saveSchedule(request):
	request.session.set_expiry(timeSleep)
	if request.method == 'POST':
		args = request.POST
		dias = args.getlist("days[]")
		print args['teacher']
		Class_Schedule.objects.filter(kaid_teacher_id=args['teacher']).delete()
		for dia in dias:
			diasplit = dia.split('_')
			try:
				newScheduleTeacher = Class_Schedule(id_schedule_id=int(diasplit[1]), day=diasplit[0], kaid_teacher_id=args['teacher'])
				newScheduleTeacher.save()
			except:
				continue
		return HttpResponse('Horario para el profesor guardado')

	return HttpResponse('listo')