#!/usr/bin/end python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django import template
from bakhanapp.models import Assesment_Skill
register = template.Library()

from bakhanapp.models import Class
from bakhanapp.models import Teacher
from bakhanapp.models import Skill
from bakhanapp.models import Skill_Progress
from bakhanapp.models import Student
from bakhanapp.models import Student_Class
from bakhanapp.models import Student_Video
from bakhanapp.models import Student_Skill
from bakhanapp.models import Video
from bakhanapp.models import Video_Playing
from bakhanapp.models import Skill_Attempt
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Class_Subject
from bakhanapp.models import Assesment
from bakhanapp.models import Assesment_Config
from bakhanapp.models import Subtopic_Skill
from bakhanapp.models import Subtopic_Video
from bakhanapp.models import Grade,Skill
from bakhanapp.models import Student_Skill
from bakhanapp.models import Skill_Progress
from bakhanapp.models import Subject
from bakhanapp.models import Chapter
from bakhanapp.models import Topic
from bakhanapp.models import Subtopic
from bakhanapp.models import Subtopic_Skill
from bakhanapp.models import Tutor
from bakhanapp.models import Skill_Log

import datetime
import threading

from configs import timeSleep

import unicodedata
import os
import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser
import psycopg2

import json
import simplejson
import sys
from pprint import pprint
import codecs
from lib2to3.fixer_util import String
from django.core import serializers
from django.db import connection

import random

def updateGrade(request):
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        teacher_grade=eval(args['input_grade_teacher'])
        teacher_comment=args['input_comment']
        id_grade=eval(args['input_grade_id'])
        update_grade = Grade.objects.get(pk=id_grade)
        update_grade.teacher_grade = teacher_grade
        update_grade.comment = teacher_comment 
        update_grade.save()

    return HttpResponse()

def getAssesment(request): #entrega una evaluacion (con todos sus parametros)
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        id_assesment=args['assesment']
        get_assesment = Assesment.objects.filter(id_assesment=id_assesment)
        data = serializers.serialize('json', get_assesment)
        struct = json.loads(data)
        assesment_data = json.dumps(struct)
        
    return HttpResponse(assesment_data)

def updateAssesment(request): #modifica una evaluacion 
    request.session.set_expiry(timeSleep)
    if request.method =='POST':
        args = request.POST
        id_assesment=args['input_id_assesment']
        fecha1=args['fecha_inicio']
        fecha2=args['fecha_termino']
        nota1=eval(args['nota_minima'])
        nota2=eval(args['nota_maxima'])
        nota3=eval(args['nota_aprobacion'])
        id_config=(args['input_id_config'])
        nombre_config=args['input_nombre']
        students=eval(args['input_kaid'])
        id_class=eval(args['input_id_class'])

        update_Assesment = Assesment.objects.get(pk=id_assesment)
        update_Assesment.start_date=fecha1
        update_Assesment.end_date=fecha2
        update_Assesment.id_assesment_conf_id=id_config
        update_Assesment.min_grade=nota1
        update_Assesment.max_grade=nota2
        update_Assesment.approval_grade=nota3
        update_Assesment.name=nombre_config
        update_Assesment.id_class_id=id_class
        update_Assesment.save()

        delete_grades = Grade.objects.filter(id_assesment=id_assesment)
        delete_skill_log = Skill_Log.objects.filter(id_grade__in = delete_grades)

        delete_skill_log.delete()
        delete_grades.delete()
        
        skills = Assesment_Skill.objects.filter(id_assesment_config=id_config).values('id_skill_name_id')
        for s in students:
            new_grade = Grade(grade=0,
                               teacher_grade=0,
                               performance_points=0,
                               effort_points=0.1,
                               id_assesment_id=id_assesment,
                               kaid_student_id=s['kaid_student']
                               )
            new_grade.save()
            for skill in skills:
                new_skill_log = Skill_Log(id_skill_name_id = skill['id_skill_name_id'],
                        correct = 0,
                        incorrect =  0,
                        id_grade_id = new_grade.pk)
                new_skill_log.save()
        os.system('python /var/www/html/bakhanproyecto/manage.py calculateGrade')
    return HttpResponse()

def getStudentAssesment(request): #entrega a todos los alumnos a los que se le realiza una evaluacion
    request.session.set_expiry(timeSleep)
    if request.method =='POST':
        args = request.POST
        id_assesment=args['assesment']
        get_students = Grade.objects.filter(id_assesment_id=id_assesment)
        data2 = serializers.serialize('json', get_students)
        struct2 = json.loads(data2)
        student_data = json.dumps(struct2)
    return HttpResponse(student_data)

def newAssesment3(request): #recibe el post y crea una evaluacion en assesment y una tupla en grade para cada student, ademas envia mails a todos
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        fecha1=args['fecha_inicio']
        fecha2=args['fecha_termino']
        nota1=eval(args['nota_minima'])
        nota2=eval(args['nota_maxima'])
        nota3=eval(args['nota_aprobacion'])
        id_config=(args['input_id_config'])
        nombre_config=args['input_nombre']
        students=eval(args['input_kaid'])
        id_class=eval(args['input_id_class'])
        bono = eval(args['bono_esfuerzo'])
        recommendations = Assesment_Config.objects.filter(pk=id_config).values('importance_completed_rec')
        mastery = Assesment_Config.objects.filter(pk=id_config).values('importance_skill_level')
        recommendations = recommendations[0]['importance_completed_rec']
        mastery = mastery[0]['importance_skill_level']
        #recommendations = "recommendations"
        #mastery = "mastery"
        new_assesment = Assesment(start_date=fecha1,
                               end_date=fecha2,
                               id_assesment_conf_id=id_config,
                               min_grade=nota1,
                               max_grade=nota2,
                               approval_grade=nota3,
                               name=nombre_config,
                               id_class_id=id_class,
                               max_effort_bonus=bono
                               )
        new_assesment.save()
        id_new_assesment=new_assesment.pk
        skills = Assesment_Skill.objects.filter(id_assesment_config=id_config).values('id_skill_name_id')
        kaid = ''
        for s in students:
            kaid= kaid + ',' +str(s['kaid_student'])
            new_grade = Grade(grade=0,
                               teacher_grade=0,
                               performance_points=0,
                               effort_points=0.1,
                               id_assesment_id=id_new_assesment,
                               kaid_student_id=s['kaid_student']
                               )
            new_grade.save()
            for skill in skills:
                new_skill_log = Skill_Log(id_skill_name_id = skill['id_skill_name_id'],
                        correct = 0,
                        incorrect =  0,
                        id_grade_id = new_grade.pk)
                new_skill_log.save()
            update_assesment_configs = Assesment_Config.objects.get(pk=id_config)
            update_assesment_configs.applied = True
            update_assesment_configs.save()

        os.system('python /var/www/html/bakhanproyecto/manage.py calculateGrade')
        threads = []
        #envial mail a los evaluados
        t = threading.Thread(target=treadSendMail,args=(kaid,mastery,recommendations,fecha1,fecha2,id_config,id_class))
        threads.append(t)
        t.start()
        
        #enviar whatsapp a todos los evaluados
        #t = threading.Thread(target=sendWhatsapp,args=(kaid,nota_1,nota_2,fecha_1,fecha_2,id_config))
        #threads.append(t)
        #t.start()
    return HttpResponse()

def strip_accents(text): #reemplaza las letras con acento por letras sin acento
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def sendWhatsapp(kaid,nota_1,nota_2,fecha_1,fecha_2,id_asses_config):
    for kaid in kaids:
        student = Student.objects.get(pk=kaid)
        mensaje = 'Hola '+student.name+' tienes una evaluacion que comienza el '+fecha_1+' y termina el '+fecha_2+' que incluira las habilidades: \n'
        g = Assesment_Skill.objects.filter(id_assesment_config=id_asses_config).values('id_skill_name_id')
        n = Skill.objects.filter(id_skill_name__in=g)
        for i in n :
            skill = str(i)
            skill = strip_accents(skill)
            mensaje = mensaje+'-'+skill+'\n'
        phone = str(student.phone)
        whatsapp(mensaje,phone)
    return ()

def whatsapp(msg,num):
    mensaje = msg
    numero = num
    os.system("yowsup-cli demos -l 56955144957:S23B/CdXejaVQPWehwWmqwhnoaI= -s 569%s '%s'"%(numero,mensaje))
    return ()

def gradeData(request):
    if request.method == 'POST':
        args = request.POST
        id_assesment=args['assesment']
        get_grade = Grade.objects.filter(id_assesment=id_assesment)
        data = serializers.serialize('json', get_grade)
        struct = json.loads(data)
        grade_data = json.dumps(struct)      
    return HttpResponse(grade_data)

def treadSendMail(kaid,mastery,recommendations,fecha1,fecha2,id_config,id_class):
    """thread sendMail function"""
    print 'Iniciando sendMail \n'
    contenido = usarPlantilla(mastery,recommendations,fecha1,fecha2,id_config,id_class)
    sendMail(kaid,contenido)
    print 'Terminando sendMail \n'
    return

def sendMail(kaidstr,contenido): #recibe los datos iniciales y envia un  mail a cada student y a cada tutor
    kaids = kaidstr.split(',')
    kaids.pop(0)
    x = 0
    for kaid in kaids:
        x = x+1
        if (x>6):
            x=0
            print "esperando 5 segundos"
            time.sleep(5)

        print kaid
        student = Student.objects.get(pk=kaid)
        tutor = Tutor.objects.get(kaid_student_child=kaid)
        
        contenido_html = contenido.replace("$$nombre_usuario$$",student.name) #usarPlantilla()

        subject = 'Nueva Evaluacion'
        text_content = 'habilita el html de tu correo'
        html_content = contenido_html
        from_email = '"Bakhan Academy" <bakhanacademy@gmail.com>'
        to = str(student.email)
        to2 = str(tutor.email)
        print to
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return ()

def usarPlantilla(mastery,recommendations,fecha1,fecha2,id_config,id_class):
    skill_assesment = getSkillAssesment(id_config)
    curso = getCurso(id_class)
    archivo=open("static/plantillas/mail_nueva_evaluacion.html")
    contenido = archivo.read()
    contenido = contenido.replace("$$fecha_inicio$$",str(fecha1))
    contenido = contenido.replace("$$fecha_termino$$",str(fecha2))
    contenido = contenido.replace("$$mastery$$",str(mastery))
    contenido = contenido.replace("$$recommendations$$",str(recommendations))
    contenido = contenido.replace("$$ejercicios$$",str(skill_assesment))
    contenido = contenido.replace("$$curso$$",str(curso))
    return(contenido)

def getCurso(id_class):
    request.session.set_expiry(timeSleep)
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    curso = Class.objects.filter(pk=id_class).values('level')
    letra = Class.objects.filter(pk=id_class).values('letter')
    curso = curso[0]['level']
    letra = letra[0]['letter']
    cursoStr = N[int(curso)]
    respuesta = cursoStr+" "+letra
    return(respuesta)

def getSkillAssesment(id_asses_config): #recibe la configuracion y devuelve el html con todas las skill (un <p> por skill)
    mnsj_skills = ''
    g = Assesment_Skill.objects.filter(id_assesment_config=id_asses_config).values('id_skill_name_id')
    n = Skill.objects.filter(id_skill_name__in=g)
    for i in n :
        skill = str(i)
        skill = strip_accents(skill)
        mnsj_skills = mnsj_skills+'<p style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:16px; line-height:24px; color:#666; margin:0 0 10px; font-size:14px; color:#333">'+skill+'</p>'
    return mnsj_skills