# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.db.models import Count

from django import template
from bakhanapp.models import Assesment_Skill
register = template.Library()

from bakhanapp.models import Class,User_Profile
from bakhanapp.models import Skill
from bakhanapp.models import Skill_Progress
from bakhanapp.models import Student
from bakhanapp.models import Student_Class
from bakhanapp.models import Student_Video
from bakhanapp.models import Student_Skill
from bakhanapp.models import Video_Playing
from bakhanapp.models import Skill_Attempt
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Class_Subject
from bakhanapp.models import Assesment
from bakhanapp.models import Assesment_Config
from bakhanapp.models import Subtopic_Skill
from bakhanapp.models import Subtopic_Video
from bakhanapp.models import Grade,Skill,Student_Skill,Skill_Progress
from bakhanapp.models import Subject,Chapter,Topic,Subtopic,Subtopic_Skill,Group_Student
from groups.models import Group_Skill,Master_Group

from configs import timeSleep

import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser
import psycopg2

import json
import sys
from pprint import pprint
import codecs
from lib2to3.fixer_util import String
from django.core import serializers
from django.db import connection

from bakhanapp.models import Group,Group_Student
from django.utils import timezone
from bakhanapp.views import getTopictree
import time
import datetime

def getLastGroup(request,id_class):
    try:
        g = Master_Group.objects.filter(id_class=id_class)
        l = g.latest('date')
        data = serializers.serialize('json', [l])
        struct = json.loads(data)
        last = json.dumps(struct)
    except Exception as e:
        last = False
    return HttpResponse(last)

def getSkillGroup(request,id_class):
    #funcion que devuelve un json con los skills de un grupo
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        id_master_group = args['id_master_group']
        s = Group_Skill.objects.filter(id_group=id_master_group).values('id_skill_id')
        n = Skill.objects.filter(id_skill_name__in=s)
        data = serializers.serialize('json', n)
        struct = json.loads(data)
        skills = json.dumps(struct)
    return HttpResponse(skills)

def getStudentGroup(request,id_class):
    #funcion que devuelve un json con los datos de grupos y alumnos
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        kaid_teacher = request.user.user_profile.kaid
        id_master_group = args['id_master_group']
        g = Group.objects.filter(master=id_master_group).values('id_group')
        g_e = Group_Student.objects.filter(id_group__in=g)
        data = serializers.serialize('json', g_e)
        struct = json.loads(data)
        students_groups = json.dumps(struct)
    return HttpResponse(students_groups)

def getMakedGroup(request,id_class):
    #funcion que devuelve un json con los datos de grupos y alumnos ya realizaados cuando se selecciona una agrupacion.
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        id_master_group = args['id_master_group']
        g = Group.objects.filter(master=id_master_group).values('id_group')
        g_e = Group_Student.objects.filter(id_group__in=g)
        data = serializers.serialize('json', g_e)
        struct = json.loads(data)
        students_groups = json.dumps(struct)
        g_c = Group.objects.filter(master=id_master_group)
        data2 = serializers.serialize('json', g_c)
        struct2 = json.loads(data2)
        groups_data = json.dumps(struct2)
    return HttpResponse(groups_data)


@login_required()
def getGroups(request, id_class):
    request.session.set_expiry(timeSleep)
    topictree=getTopictree('math')
    g = Master_Group.objects.filter(id_class=id_class)
    data = serializers.serialize('json', g)
    struct = json.loads(data)
    groups = json.dumps(struct)#arreglo en json con los master de las agrupaciones.
    if request.method == 'POST':
        args = request.POST
        skills_selected = eval(args['skills'])
        if args["student_groups"]:#si se ha seleccionado la opcion guardar agrupacion.
            tutors = eval(args['tutors'])
            #provisorio: si no ha escogido un alumno tutor, se asigna uno arbitrario. finalmente se debe asignar el kaid profesor
            if tutors[0]['kaid_tutor_reforzamiento'] == '3':
                tutors[0]['kaid_tutor_reforzamiento'] = request.user.user_profile.kaid
            if tutors[0]['kaid_tutor_intermedios'] =='2':
                tutors[0]['kaid_tutor_intermedios'] = request.user.user_profile.kaid
            tutors[0]['kaid_tutor_avanzados'] = request.user.user_profile.kaid 
            master = Master_Group()
            master.name = 'test'
            #master.date = timezone.now()
            #print master.date
            fecha = time.time()
            print fecha
            hoy= datetime.datetime.fromtimestamp(fecha).strftime('%Y-%m-%d %H:%M:%S')
            print hoy
            #t = time.mktime(time.strptime(hoy, "%Y-%m-%d %H:%M:%S"))
            master.date_int = int(fecha)
            master.kaid_teacher = request.user.user_profile.kaid
            master.id_class = id_class
            master.date = hoy

            master.save()
            print master.date_int
            new_Avanzados = Group()
            new_Avanzados.type = 'Avanzados'
            new_Avanzados.kaid_student_tutor_id = tutors[0]['kaid_tutor_avanzados']
            new_Avanzados.master = master.id
            new_Avanzados.save()
            new_Intermedios = Group()
            new_Intermedios.type = 'Intermedios'
            new_Intermedios.kaid_student_tutor_id = tutors[0]['kaid_tutor_intermedios']
            new_Intermedios.master = master.id
            new_Intermedios.save()
            new_Reforzamiento = Group()
            new_Reforzamiento.type = 'Reforzamiento'
            new_Reforzamiento.kaid_student_tutor_id = tutors[0]['kaid_tutor_reforzamiento']
            new_Reforzamiento.master = master.id
            new_Reforzamiento.save()
            new_SinGrupo = Group()
            new_SinGrupo.type = 'SinGrupo'
            new_SinGrupo.kaid_student_tutor_id = tutors[0]['kaid_tutor_reforzamiento']
            new_SinGrupo.master = master.id
            new_SinGrupo.save()
            for skills in skills_selected:
                Group_Skill(id_group_id=master.id,
                    id_skill_id=skills).save()
            groups = eval(args['student_groups'])

            subGroups = eval(args['subGroups'])

            dicSub = {
                'SinGrupo' : new_SinGrupo.id_group,
                'Avanzados' : new_Avanzados.id_group,
                'Intermedios' : new_Intermedios.id_group,
                'Reforzamiento' : new_Reforzamiento.id_group
            }

            #print dicSub
            for sub in subGroups:
                if "kaid_" not in sub['tutor']: 
                    new_group = Group(type=sub['name'],master=master.id,kaid_student_tutor_id=request.user.user_profile.kaid)
                else:
                    new_group = Group(type=sub['name'],master=master.id,kaid_student_tutor_id=sub['tutor'])
                new_group.save()
                dicSub[sub['name']] = new_group.id_group

            

            for g in groups:#guarda el estududiante el en respectivo grupo avanzados, intermedio o reforzamiento.
                #print 
                #print dicSub[str(g['group'])]
                Group_Student(id_group_id=dicSub[str(g['group'])],
                                  kaid_student_id=g['kaid_student']).save()
                
            students = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
            for s in students:
                s.type = 'SinGrupo'
        students = makeGroups(id_class,skills_selected)
        return HttpResponse(students)
    else:
        students = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
        for s in students:
            s.type = 'SinGrupo'
    classroom = Class.objects.filter(id_class=id_class)
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    spanish_classroom = N[int(classroom[0].level)] +' '+ classroom[0].letter
    if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid,id_class_id=id_class)):
        isTeacher = True
    else:
        isTeacher = False
    kaid_teacher_object=Class_Subject.objects.filter(id_class_id=id_class).values('kaid_teacher')
    kaid_teacher = kaid_teacher_object[0]['kaid_teacher']
    return render_to_response('groups.html',{'students': students,'topictree':topictree,'id_class':id_class,'groups':groups,'spanish_classroom':spanish_classroom,'isTeacher':isTeacher,'kaid_teacher':kaid_teacher},context_instance=RequestContext(request))

def makeGroups(id_class,skills_selected):
    #Funcion que entrega un arreglo con los estudiantes y su nivel de agrupamiento.
    #print skills_selected                                                         #aqui llegan bien las habilidades seleccionadas
    students = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#retorna todos los estudiantes de un curso
    data = []  
    for s in students:
        #Por cada estudiante en id_class, se obtiene su agrupacion.
        s.type = getTypeStudent(s.kaid_student,skills_selected) #args debe contener todas las id de las skill seleccionadas para el agrupamiento.
        student={}
        student["kaid_student"] = s.kaid_student
        student["name"] = s.name
        student["type"] = s.type
        data.append(student)
        
    json_data = json.dumps(data)
    return json_data

def getTypeStudent(kaid_student,args):
    #Funcion que entrega en que nivel grupo debe ser organizado un estudiante
    #de acuerdo a su nivel en las skills seleccionadas por el profesor.
    #skills = Group_Skill.objects.filter(id_group_id=id_group)
    Reforzamiento = 0
    Intermedios = 0
    Avanzados = 0
    total = len(args)
    for skill in args:
        student_progress = Student_Skill.objects.filter(kaid_student_id=kaid_student,id_skill_name_id=skill).values('last_skill_progress')
        #el problema esta con la variable student_progress
        if student_progress:
            if student_progress[0]["last_skill_progress"] == 'struggling' or student_progress[0]["last_skill_progress"] == 'unstarted':
                Reforzamiento += 1
            if student_progress[0]["last_skill_progress"] == 'mastery1' or student_progress[0]["last_skill_progress"] == 'mastery2' or student_progress[0]["last_skill_progress"] == 'practiced':
                Intermedios += 1
            if student_progress[0]["last_skill_progress"] == 'mastery3':
                Avanzados += 1
    if Reforzamiento > 0:
        return 'Reforzamiento'
    elif Intermedios > 0:
        return 'Intermedios'
    elif Avanzados == total:
        if total == 0:
            return 'SinGrupo'
        else:
            return 'Avanzados'
    else:
        return 'Reforzamiento'
            
