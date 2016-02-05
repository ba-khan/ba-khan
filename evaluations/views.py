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

import datetime

import unicodedata

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
    if request.method == 'POST':
        args = request.POST
        print args
        id_assesment=args['assesment']
        print id_assesment
        get_assesment = Assesment.objects.filter(id_assesment=id_assesment)
        data = serializers.serialize('json', get_assesment)
        struct = json.loads(data)
        assesment_data = json.dumps(struct)
        
    return HttpResponse(assesment_data)

def updateAssesment(request): #modifica una evaluacion 
    if request.method =='POST':
        args = request.POST
        id_assesment=args['input_id_assesment']
        fecha1=args['fecha_inicio']
        fecha2=args['fecha_termino']
        nota1=eval(args['nota_minima'])
        nota2=eval(args['nota_maxima'])
        id_config=(args['input_id_config'])
        nombre_config=args['input_nombre']
        students=eval(args['input_kaid'])
        id_class=eval(args['input_id_class'])
        
        print id_assesment
        update_Assesment = Assesment.objects.get(pk=id_assesment)
        update_Assesment.start_date=fecha1
        update_Assesment.end_date=fecha2
        update_Assesment.id_assesment_conf_id=id_config
        update_Assesment.min_grade=nota1
        update_Assesment.max_grade=nota2
        update_Assesment.name=nombre_config
        update_Assesment.id_class_id=id_class
        update_Assesment.save()
        
        delete_grades = Grade.objects.filter(id_assesment=id_assesment)
        delete_grades.delete()
        
        for s in students:
            new_grade = Grade(grade=0,
                               teacher_grade=0,
                               performance_points=0,
                               effort_points=0,
                               id_assesment_id=id_assesment,
                               kaid_student_id=s['kaid_student']
                               )
            new_grade.save() 
        
    return HttpResponse()

def getStudentAssesment(request): #entrega a todos los alumnos a los que se le realiza una evaluacion
    if request.method =='POST':
        args = request.POST
        id_assesment=args['assesment']
        get_students = Grade.objects.filter(id_assesment_id=id_assesment)
        data2 = serializers.serialize('json', get_students)
        struct2 = json.loads(data2)
        student_data = json.dumps(struct2)
    return HttpResponse(student_data)

def newAssesment3(request): #recibe el post y crea una evaluacion en assesment y una tupla en grade para cada student, ademas envia mails a todos
    if request.method == 'POST':
        args = request.POST
        fecha1=args['fecha_inicio']
        fecha2=args['fecha_termino']
        nota1=eval(args['nota_minima'])
        nota2=eval(args['nota_maxima'])
        id_config=(args['input_id_config'])
        nombre_config=args['input_nombre']
        students=eval(args['input_kaid'])
        id_class=eval(args['input_id_class'])

        new_assesment = Assesment(start_date=fecha1,
                               end_date=fecha2,
                               id_assesment_conf_id=id_config,
                               min_grade=nota1,
                               max_grade=nota2,
                               name=nombre_config,
                               id_class_id=id_class
                               )
        new_assesment.save()
        id_new_assesment=new_assesment.pk
        skill_assesment = getSkillAssesment(id_config)
        x=0
        for s in students:
            x=x+1
            aux = s['kaid_student']
            print aux
            if x>10 :
                print 'esperando'
                # Wait for 5 seconds
                time.sleep(5)
                x=0
                print 'siguiendo'
            sendMail(aux,nota1,nota2,fecha1,fecha2,skill_assesment)
            new_grade = Grade(grade=0,
                               teacher_grade=0,
                               performance_points=0,
                               effort_points=0,
                               id_assesment_id=id_new_assesment,
                               kaid_student_id=s['kaid_student']
                               )
            new_grade.save()
            update_assesment_configs = Assesment_Config.objects.get(pk=id_config)
            update_assesment_configs.applied = True
            update_assesment_configs.save()
    return HttpResponse()

def sendMail(kaid,nota_1,nota_2,fecha_1,fecha_2,skill_assesment): #recibe los datos iniciales y envia un  mail a cada student y a cada tutor
    student = Student.objects.get(pk=kaid)
    tutor = Tutor.objects.get(kaid_student_child=kaid)
    subject = 'Nueva Evaluacion'
    text_content = 'Mensaje...nLinea 2nLinea3'
    print 'antes del html_content'
    html_content = '<div><table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#2c3747" style="background-color:#e2e2e2; font-size:12px; font-family:Helvetica,Arial,Geneva,sans-serif"><tbody><tr><td><table cellpadding="0" cellspacing="0" border="0" width="600" align="center" bgcolor="#e2e2e2"><tbody><tr><td><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tbody><tr><td><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tbody><tr><td><table cellpadding="0" cellspacing="0" border="0" width="600" align="center" bgcolor="#2c3747" style="margin-top:20px"><tbody><tr><td><table cellpadding="10" cellspacing="0" border="0" width="600" align="center"><tbody><tr><td align="center" width="175" valign="middle"><a target="_blank"><img src="http://www.khanacademy.org/imaget/ka-email-banner-logo.png?code=bWFzdGVyeV90YXNrX2VtYWlsX29wZW4KX2dhZV9iaW5nb19yYW5kb206U2ZfQWNMb29ROGVOc0taUndkVEgzdEc3dEhBSERLem0xN1JianJpcQ==" width="194" height="20" border="0" alt="Khan Academy"> </a></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table cellpadding="0" cellspacing="0" border="0" width="600" align="center"><tbody><tr><td><table cellpadding="0" cellspacing="0" width="600" align="center" style="border-width:1px; border-spacing:0px; border-style:solid; border-color:#cccccc; border-collapse:collapse; background-color:#ffffff"><tbody><tr><td style="background-color:#f7f7f7; font-family:Helvetica Neue,Calibri,Helvetica,Arial,sans-serif; font-size:15px; color:black; border-bottom:1px solid #ddd"><table cellpadding="0" cellspacing="0" border="0" width="500" align="center" style="margin:28px 50px; font-size:15px; line-height:24px"><tbody><tr><td><table width="500" cellpadding="0" cellspacing="0" border="0" style=""><tbody><tr><td><img src="http://www.khanacademy.org/images/mission-badges/arithmetic-100x100.png?4" width="70" height="70" style="left:-10px"> </td><td><p style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:16px; line-height:24px; color:#666; margin:0 0 10px; font-size:14px; color:#333"><strong>'+student.name+',</strong><br>Tienes una Nueva Evaluacion en curso</p></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td><table cellpadding="0" cellspacing="0" border="0" width="500" align="center" style="margin:10px 50px"><tbody><tr><td><a target="_blank"><div style="padding:20px 0" id="Cuadro_Azul"><table width="500" cellpadding="0" cellspacing="0" border="0" style="background-color:#1C758A; border-radius:4px"><tbody><tr><td style="padding:25px 5px; vertical-align:top"><div style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; border:none; color:#fff; font-size:18px; text-decoration:none; line-height:28px"><p><div>Fecha Inicio: '+fecha_1+'</div></p><p><div>Fecha Termino: '+fecha_2+'</div></p><p><div>Nota Minima: '+str(nota_1)+'</div></p><p><div>Nota Maxima: '+str(nota_2)+'</div></p></div></td></tr></tbody></table></div></a><a target="_blank" style="text-decoration:none"><div style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:12px; line-height:20px; font-weight:bold; text-transform:uppercase; color:#777; margin-top:20px">Ejercicios a Evaluar:</div>'+skill_assesment+'</a><br></td></tr></tbody></table></td></tr><tr><td style="background-color:#f7f7f7; font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:15px; color:black; border-top:1px solid #ddd"><table cellpadding="0" cellspacing="0" border="0" width="500" align="center" style="margin:28px 50px; font-size:15px; line-height:24px"><tbody><tr><td><a href="https://es.khanacademy.org/" target="_blank" style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; border:1px solid #76a015; background-color:#7fac05; color:white; display:inline-block; padding:0 32px; margin:0; border-radius:5px; font-size:16px; line-height:40px; text-decoration:none; display:block; text-align:center; font-size:20px; line-height:45px; background-color:#1C758A; border-color:#1C758A">Anda a Khan para empezar a Practicar</a></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div>'
    from_email = '"Bakhan Academy" <bakhanacademy@gmail.com>'
    print 'antes del to student.mail'
    to = str(student.email)
    to2 = str(tutor.email)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse()

def getSkillAssesment(id_asses_config): #recibe la configuracion y devuelve el html con todas las skill (un <p> por skill)
    mnsj_skills = ''
    g = Assesment_Skill.objects.filter(id_assesment_config=id_asses_config).values('id_skill_name_id')
    n = Skill.objects.filter(id_skill_name__in=g)
    for i in n :
        skill = str(i)
        print skill
        skill = strip_accents(skill)
        print skill
        mnsj_skills = mnsj_skills+'<p style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:16px; line-height:24px; color:#666; margin:0 0 10px; font-size:14px; color:#333">'+skill+'</p>'
    return mnsj_skills

def strip_accents(text): #reemplaza las letras con acento por letras sin acento
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def sendWhatsapp(phone):
    #aqui va la magia
    return ()