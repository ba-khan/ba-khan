# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from .forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count,Sum,Max
from django.db.models import Q

import unicodedata
from django import template
from bakhanapp.models import Assesment_Skill
register = template.Library()

from bakhanapp.models import Class,Institution
from bakhanapp.models import Teacher,User_Profile
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
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill_Log

import datetime
from configs import timeSleep

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
import datetime
import threading
import Queue
from datetime import datetime
from django.http import HttpResponse
import django_excel as excel
import pyexcel as pe
import pyexcel.ext.xls

#ultimo try:#id4004 para este archivo
@permission_required('bakhanapp.isSuper', login_url="/")
def saveInstitution(request):
    request.session.set_expiry(timeSleep)
    if request.is_ajax():
        if request.method == 'POST':
            json_str = json.loads(request.body)
            try:#id4004
                institution = Institution.objects.get(pk=json_str["pk"])
                institution.name = json_str["name"]
                institution.city = json_str["city"]
                institution.address = json_str["address"]
                institution.phone = json_str["phone"]
                institution.key = json_str["key"]
                institution.secret = json_str["secret"]
                institution.identifier = json_str["identifier"]
                institution.password = json_str["password"]
                institution.save()
                return HttpResponse("Cambios guardados correctamente")
            except Exception as e:
                print '****ERROR**** en try:#id4004 bakhanapp:views.py'
                print e
                return HttpResponse("Error al guardar")
    return HttpResponse("Error")

@permission_required('bakhanapp.isSuper', login_url="/")
def deleteInstitution(request):
    request.session.set_expiry(timeSleep)
    try:#id4003 en bakhanapp:views.py
        if request.is_ajax():
            if request.method == 'POST':
                json_str = json.loads(request.body)
                institution = Institution.objects.get(pk=json_str["pk"])
                institution.delete()
                return HttpResponse(json_str["pk"])
    except Exception as e:
        print '****ERROR**** en try:#id4003 bakhanapp:views.py'
        print e
        return HttpResponse("Error al eliminar")

@permission_required('bakhanapp.isSuper', login_url="/")
def newInstitution(request):
    request.session.set_expiry(timeSleep)
    if request.method == 'POST':
        args = request.POST
        try:#id4002
            institution = Institution.objects.create(name=args['name'],
                city=args['city'],
                address=args['address'],
                phone=args['phone'],
                key=args['key'],
                secret=args['secret'],
                identifier=args['identifier'],
                password=args['password'])
            iterableArray = [institution]
            data = serializers.serialize('json', iterableArray)
            struct = json.loads(data)
            jsonResponse = json.dumps(struct)
            return HttpResponse(jsonResponse)
        except Exception as e:
            print '****ERROR**** try:#id4002'
            print e
            return HttpResponse("Error al guardar")


@login_required()
def generateClassExcel(request, id_class):
    #funcion que genera el excel de un curso completo con todas sus evaluaciones
    request.session.set_expiry(timeSleep)
    if request.method == 'GET':
        #funcion que genera el excel de una evaluacion
        assesment = Assesment.objects.filter(id_class=id_class)
        rClass = Class.objects.get(id_class=id_class)
        N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
        
        nameClass= N[int(rClass.level)]  +' '+ rClass.letter
        print nameClass
        try:#id1004
            #create multi-sheet book with array
            arrayAssesment={}
            for a in assesment:
                name_sheet = strip_acent(a.name)
                if len(name_sheet) > 22:
                    words = name_sheet.split()
                    print len(words)
                    length = 22/len(words)
                    name_sheet=''
                    for w in words:
                        name_sheet += w[:length]
                name_sheet = name_sheet.replace(' ','')
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

@login_required()
def generateAssesmentExcel(request, id_assesment):
    request.session.set_expiry(timeSleep)
    if request.method == 'GET':
        #funcion que genera el excel de una evaluacion
        assesment = Assesment.objects.get(id_assesment=id_assesment)
        #data = getArrayAssesmentDetail(id_assesment)
        #datar = getArrayAssesmentResumen(id_assesment)
        try:
            #create multi-sheet book with array
            arrayAssesment={
                "Detalle": getArrayAssesmentDetail(id_assesment),
                "Resumen": getArrayAssesmentResumen(id_assesment)
            }
            book = pe.Book(arrayAssesment)
        except Exception as e:
            print '***ERROR*** problemas al crear multiples hojas excel con dataTest'
            print e
        try:
            response = excel.make_response(book, 'xls', file_name=assesment.name)
        except Exception as e:
            print '***ERROR*** no se ha podido generar la respuesta excel'
            print e
            response = False
        return response

def getArrayAssesmentResumen(id_assesment):
    #load resumen data
    delta = 9
    try:#id1003
        assesment = Assesment.objects.get(id_assesment=id_assesment)
        qGrades = Grade.objects.filter(id_assesment=assesment)
        qSkills = Skill.objects.filter(assesment_skill__id_assesment_config_id=assesment.id_assesment_conf_id)
    except Exception as e:
        print '***ERROR*** problemas en bakhanapp views.py try id_1003'
        print e 
    totalSkills = qSkills.count()
    w, h = 2,7
    data = [['' for x in range(w)] for y in range(h)] 
    data[0][0] = 'Nombre de la calificacion'
    data[0][1] = assesment.name
    data[1][0] = 'Nota Minima'
    data[1][1] = assesment.min_grade
    data[2][0] = 'Nota Maxima'
    data[2][1] = assesment.max_grade
    data[3][0] = 'Nota de Aprobacion'
    data[3][1] = assesment.approval_grade
    data[4][0] = 'Bonificacion por Esfuerzo'
    data[4][1] = assesment.max_effort_bonus
    data[5][0] = 'Fecha de inicio'
    data[5][1] = assesment.start_date
    data[6][0] = 'Fecha de termino'
    data[6][1] = assesment.end_date
    try:#id1001
        wr,hr = 10,30+totalSkills
        datar = [['' for x in range(wr)] for y in range(hr)] 
        datar[0][0] = 'Nombre de la calificacion'
        datar[0][1] = data[0][1]
        datar[1][0] = 'Nota Minima'
        datar[1][1] = data[1][1]
        datar[2][0] = 'Nota Maxima'
        datar[2][1] = data[2][1]
        datar[3][0] = 'Nota de Aprobacion'
        datar[3][1] = data[3][1]
        datar[4][0] = 'Bonificacion por Esfuerzo'
        datar[4][1] = data[4][1]
        datar[5][0] = 'Fecha de inicio'
        datar[5][1] = data[5][1]
        datar[6][0] = 'Fecha de termino'
        datar[6][1] = data[6][1]

        datar[1][3] = 'Alumnos participantes'
        datar[1][4] = qGrades.count()
        datar[2][3] = 'Aprobados'
        datar[2][4] = qGrades.filter(grade__gte=assesment.approval_grade).count()
        datar[3][3] = 'Reprobados'
        datar[3][4] = qGrades.filter(grade__lt=assesment.approval_grade).count()
        #load histogram data
        datar[8][0] = 'Histograma'
        datar[9][0] = 'Desde'
        datar[9][1] = 'Hasta'
        datar[9][2] = 'Cantidad'
        rangeHistogram = (data[2][1] - data[1][1])/float(10)
        rangeHistogram = float("{0:.1f}".format(rangeHistogram))
        datar[10][0] = data[1][1]
        datar[10][1] = data[1][1] + rangeHistogram
        datar[10][2] = qGrades.filter(grade__gte=datar[10][0],grade__lt=datar[10][1]).count() 
        for i in range(8):
            datar[i+delta+2][0] = datar[i+delta+1][1] 
            datar[i+delta+2][1] = datar[i+delta+2][0] + rangeHistogram
            datar[i+delta+2][2] = qGrades.filter(grade__gte=datar[i+delta+2][0],grade__lt=datar[i+delta+2][1]).count() 
        datar[19][0] = datar[18][1] + 0.1
        datar[19][1] = data[2][1]
        datar[19][2] = qGrades.filter(grade__gte=datar[19][0],grade__lte=datar[19][1]).count() 
    except Exception as e:
        print '***ERROR*** problemas en bakhanapp views.py try id1001'
        print e
    try:#id1002
        #load q skill level
        delta2 = 23
        datar[delta2-2][0] = 'Cantidad de alumnos en cada nivel por habilidad'
        datar[delta2-1][0] = 'Habilidad'
        datar[delta2-1][1] = 'No Practicado'
        datar[delta2-1][2] = 'En Dificultad'
        datar[delta2-1][3] = 'Practicado'
        datar[delta2-1][4] = 'Nivel 1'
        datar[delta2-1][5] = 'Nivel 2'
        datar[delta2-1][6] = 'Dominado'
        
        for i in range(totalSkills):
            datar[i+delta2][0]=qSkills[i].name_spanish
            datar[i+delta2][1]=0
            datar[i+delta2][2]=0
            datar[i+delta2][3]=0
            datar[i+delta2][4]=0
            datar[i+delta2][5]=0
            datar[i+delta2][6]=0
            skill_logs = Skill_Log.objects.filter(id_skill_name=qSkills[i],id_grade__in=qGrades)
            for sl in skill_logs:
                if sl.skill_progress == 'unstarted':
                    datar[i+delta2][1]+=1
                if sl.skill_progress == 'struggling':
                    datar[i+delta2][2]+=1
                if sl.skill_progress == 'practiced':
                    datar[i+delta2][3]+=1
                if sl.skill_progress == 'mastery1':
                    datar[i+delta2][4]+=1
                if sl.skill_progress == 'mastery2':
                    datar[i+delta2][5]+=1
                if sl.skill_progress == 'mastery3':
                    datar[i+delta2][6]+=1
    except Exception as e:
        print '***ERROR*** problemas en bakhanapp views.py try id_1002'
        print e
    return datar

def getArrayAssesmentDetail(id_assesment):
    infoAssesment = Assesment.objects.filter(id_assesment=id_assesment)
    delta = 9
    viewFields = ['Estudiante','Recomendadas Completadas','Ejercicios Incorrectos',
        'Ejercicios Correctos','Tiempo en Ejercicios','Tiempo en Videos',
        'En Dificultad','Practicado','Nivel 1','Nivel 2','Dominado',
        'Nota','Bonificacion por esfuerzo']
    totalFields = len(viewFields)
    #carga al arreglo los datos de la evaluacion id_assesment
    try: #id01
        assesment = Assesment.objects.get(id_assesment=id_assesment)
        config = Assesment_Config.objects.get(id_assesment_config=assesment.id_assesment_conf_id)
        skills = Skill.objects.filter(assesment_skill__id_assesment_config_id=assesment.id_assesment_conf_id).values('name_spanish')
        grades = Student.objects.filter(grade__id_assesment_id=id_assesment
            ).values('name','grade__grade',
            'grade__bonus_grade','grade__recomended_complete','grade__incorrect','grade__correct','grade__excercice_time',
            'grade__video_time','grade__struggling','grade__practiced','grade__mastery1','grade__mastery2','grade__mastery3').order_by('name')
    except Exception as e:
        print '***ERROR*** try: #id01 in generateAssesmentExce(request, id_assesment)'
        print e

    totalGrades = grades.count()
    totalConf = 10 
    totalSkills = skills.count()
    #print '***DEBUG***'
    #print totalSkills

    #crea el arreglo inicial
    w, h = totalFields +10 ,totalGrades+totalConf+totalSkills + delta + 10
    data = [['' for x in range(w)] for y in range(h)] 

    #carga del arreglo assesment
    data[0][0] = 'Nombre de la calificacion'
    data[0][1] = assesment.name
    data[1][0] = 'Nota Minima'
    data[1][1] = assesment.min_grade
    data[2][0] = 'Nota Maxima'
    data[2][1] = assesment.max_grade
    data[3][0] = 'Nota de Aprobacion'
    data[3][1] = assesment.approval_grade
    data[4][0] = 'Bonificacion por Esfuerzo'
    data[4][1] = assesment.max_effort_bonus
    data[5][0] = 'Fecha de inicio'
    data[5][1] = assesment.start_date
    data[6][0] = 'Fecha de termino'
    data[6][1] = assesment.end_date
    #carga las notas y las variables disponibles en grade
    for k in range(totalFields):
        data[delta-1][k] = viewFields[k]
    for i in range(totalGrades):
        for j in range(totalFields):
            if j==0:
                data[i+delta][j] = grades[i]['name']
            if j==1:
                data[i+delta][j] = grades[i]['grade__recomended_complete']
            if j==2:
                data[i+delta][j] = grades[i]['grade__incorrect']
            if j==3:
                data[i+delta][j] = grades[i]['grade__correct']
            if j==4:
                m, s = divmod(grades[i]['grade__excercice_time'], 60)
                print "%d:%02d:%02d" % (h, m, s)
                data[i+delta][j] = "%02d:%02d" % (m, s)
            if j==5:
                data[i+delta][j] = grades[i]['grade__video_time']
            if j==6:
                data[i+delta][j] = grades[i]['grade__struggling']
            if j==7:
                data[i+delta][j] = grades[i]['grade__practiced']
            if j==8:
                data[i+delta][j] = grades[i]['grade__mastery1']
            if j==9:
                data[i+delta][j] = grades[i]['grade__mastery2']
            if j==10:
                data[i+delta][j] = grades[i]['grade__mastery3']
            elif j==11:
                data[i+delta][j] = grades[i]['grade__grade']
            elif j==12:
                data[i+delta][j] = grades[i]['grade__bonus_grade']
    #load skills to excel array data
    data[totalGrades+delta+1][0]='Habilidades evaluadas:'
    for l in range(totalSkills):
        data[totalGrades+delta+2+l][0]=skills[l]['name_spanish']
    return data

def getSkillAssesment(request,id_class):
    if request.method == 'POST':
        args = request.POST
        id_asses_config = args['id_asses_config']
        g = Assesment_Skill.objects.filter(id_assesment_config=id_asses_config).values('id_skill_name_id')
        n = Skill.objects.filter(id_skill_name__in=g)
        data = serializers.serialize('json', n)
        struct = json.loads(data)
        skills = json.dumps(struct)
    return HttpResponse(skills)


@login_required()
def home(request):
    request.session.set_expiry(timeSleep)
    return render_to_response('home.html',context_instance=RequestContext(request))

@login_required()
def teacher(request):
    return render_to_response('teacher.html',)

@login_required()
def getTeacherClasses(request):
    #funcion que es llamada con la url:/inicio
    request.session.set_expiry(timeSleep)
    #print request.user.user_profile.kaid
    #Esta funcion corresponde a estar logueado en el sistema
    #Si la persona logeada es un super usario, muestra las opciones para crear, editar y eliminar instituciones.
    if(request.user.has_perm('bakhanapp.isSuper')):
        print '********dep**********'
        try:#id4001
            institutions = Institution.objects.all().order_by('pk')
            for i in institutions:
                date_posted = i.last_load.replace('%3A',':')
                date = datetime.strptime(date_posted, '%Y-%m-%dT%H:%M:%SZ')
                i.last_load = date.strftime('%d/%m/%Y %H:%M:%S')
            return render_to_response('institutions.html',{'institutions':institutions}, context_instance=RequestContext(request))
        except Exception as e:
            print '****ERROR****'
            print 'ha fallado try:#id4001 en bakhanapp:views.py'
            print e
        
    #Si la persona logeada es un administrador, muestra todos los cursos de su establecimiento.
    if(request.user.has_perm('bakhanapp.isAdmin')):
        classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).order_by('level','letter')
    else:
        classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class')).order_by('level','letter')
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
        isTeacher = True
    else:
        isTeacher = False
    return render_to_response('myClasses.html', {'classes': classes,'isTeacher':isTeacher}, context_instance=RequestContext(request))
    

def getClassSkills(request,id_class):
    request.session.set_expiry(timeSleep)
    #Funcion que entrega un arreglo con la cantidad de habilidades en cada nivel de dominio
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#devuelve todos los estudiantes de una clase
    students_skills = Student_Skill.objects.filter(kaid_student__in=students).values('last_skill_progress','kaid_student').annotate(scount=Count('kaid_student'))
    #print students_skills
    return students_skills


def parallelAssesment(assesment,students,queue):
    #print '****************inicio el thread*********************'
    inicio = time.time()
    assesment_json={}
    assesment_json["id"]=assesment.id_assesment
    assesment_json["name"]=assesment.name
    assesment_json["config_name"]= assesment.id_assesment_conf.name
    assesment_json["approval_percentage"]= assesment.id_assesment_conf.approval_percentage
    assesment_json["approval_grade"]= assesment.approval_grade
    assesment_json["top_score"]= assesment.id_assesment_conf.top_score
    assesment_json["max_grade"]= assesment.max_grade
    assesment_json["min_grade"]= assesment.min_grade
    assesment_json["id_config"]= assesment.id_assesment_conf.id_assesment_config
    assesment_json["start_date"]= str(assesment.start_date)
    assesment_json["end_date"]= str(assesment.end_date)
    assesment_json["assesment_student"]=[]
    grades = Grade.objects.filter(id_assesment_id=assesment.id_assesment).values('kaid_student_id','correct','incorrect','video_time','excercice_time',
        'struggling','practiced','mastery1','mastery2','mastery3','total_recomended','recomended_complete')
    dictGrades = {}
    dictSkills = {}
    for g in grades:
        dictGrades[g['kaid_student_id']] = (g['correct'],g['incorrect'],g['video_time'],g['excercice_time'],g['struggling'],g['practiced'],g['mastery1'],
            g['mastery2'],g['mastery3'],g['total_recomended'],g['recomended_complete'])
    i=0
    try:#id2001
        #print assesment.id_assesment 
        g = Grade.objects.filter(id_assesment_id=assesment.id_assesment).values('id_grade')
        #print g.count()
        #print g
        #print g
        #skills_complete = Skill.objects.filter(skill_log__id_grade__in=g, skill_log__skill_progress='practiced').values('name_spanish','skill_log__skill_progress')
        #skills_practiced = Skill_Log.objects.filter(skill_progress='practiced',id_grade_id__in=g).values('id_skill_name_id')
        #skills_mastery1 = Skill_Log.objects.filter(skill_progress='mastery1',id_grade_id__in=g).values('id_skill_name_id')
        #skills_mastery2 = Skill_Log.objects.filter(skill_progress='mastery2',id_grade_id__in=g).values('id_skill_name_id')
        #skills_mastery3 = Skill_Log.objects.filter(skill_progress='mastery3',id_grade_id__in=g).values('id_skill_name_id')
  
        #skills_complete = Skill.objects.filter((Q(skill_log__skill_progress='practiced')|Q(skill_log__skill_progress='mastery1')|Q(skill_log__skill_progress='mastery2')|Q(skill_log__skill_progress='mastery3'))&Q(student_skill__id_grade_id__in=g)).values('name_spanish', 'student_skill__kaid_student_id')
        #print skills_complete
        #print skills_complete
        #print "skills_copmplete abajo"
        #print len(skills_complete)
        #for s in skills_complete:
        #    print s
            #print "aca abajo"
            #print s['name_spanish']
            #print s['student_skill__kaid_student_id']
        #    dictSkills[s['student_skill__kaid_student_id']] = (s['name_spanish'])
        #    print s['name_spanish']
            #dictSkills[s['name_spanish'] = (s['name_spanish'])
        #print dictGrades[0]
    except Exception as e:
        #print '***ERROR*** ha fallado try:#id2001 bakhanapp/views.py'
        print e
    
    for student in students:
        skills_completadas=[]
        skills_no_completadas=[]
        student_json={}
        student_json["id"]=i
        student_json["name"]=student.nickname

        try:#id2002
            #if student.kaid_student=='kaid_650486821916405105888593':
            #print student.kaid_student
            g_student=g.filter(kaid_student_id=student.kaid_student)

            skills_complete = Skill.objects.filter((Q(skill_log__skill_progress='practiced')|Q(skill_log__skill_progress='mastery1')|
                Q(skill_log__skill_progress='mastery2')|Q(skill_log__skill_progress='mastery3')),
                skill_log__id_grade=g_student).values('name_spanish')
            #    print "len abajo"
            #    print len(skills_complete)
            for s in skills_complete:
                #print s['name_spanish']
                skills_completad = s['name_spanish']
                skills_completadas.append(skills_completad)
            #skills_completadas = dictSkills[student.kaid_student]
            #print skills_completadas
            #print len(skills_completadas)
        except Exception as e:
            skills_completadas = []
            #print "***ERROR*** ha fallado try:#id2002 bakhanapp/views.py"
            print e

        try:#id2003
            #if student.kaid_student=='kaid_650486821916405105888593':
            #print student.kaid_student
            g_student=g.filter(kaid_student_id=student.kaid_student)

            skills_no_complete = Skill.objects.filter((Q(skill_log__skill_progress='unstarted')|Q(skill_log__skill_progress='struggling')),skill_log__id_grade=g_student).values('name_spanish')
            #    print "len abajo"
            #    print len(skills_complete)
            for s in skills_no_complete:
                #print s['name_spanish']
                skills_no_completad = s['name_spanish']
                skills_no_completadas.append(skills_no_completad)
            #skills_completadas = dictSkills[student.kaid_student]
            #print skills_completadas
            #print len(skills_completadas)
        except Exception as e:
            skills_no_completadas = []
            #print "***ERROR*** ha fallado try:#id2003 bakhanapp/views.py"
            print e
        try:
            student_json["skills_time"] = dictGrades[student.kaid_student][3]
        except:
            student_json["skills_time"] = 0
        try:
            student_json["video_time"] = dictGrades[student.kaid_student][2]
        except:
            student_json["video_time"] = 0            
        student_exercise={}
        try:
            student_exercise["correct"] = dictGrades[student.kaid_student][0]
        except:
            student_exercise["correct"] = 0
        try:
            student_exercise["incorrect"] = dictGrades[student.kaid_student][1]
        except:
            student_exercise["incorrect"] = 0
        student_json["exercises"]=student_exercise
        skills_level={}
        try:
            skills_level["struggling"] = dictGrades[student.kaid_student][4]
        except:
            skills_level["struggling"] = 0
        try:
            skills_level["practiced"] = dictGrades[student.kaid_student][5]
        except:
            skills_level["practiced"] = 0
        try:
            skills_level["mastery1"] = dictGrades[student.kaid_student][6]
        except:
            skills_level["mastery1"] = 0
        try:
            skills_level["mastery2"] = dictGrades[student.kaid_student][7]
        except:
            skills_level["mastery2"] = 0
        try:
            skills_level["mastery3"] = dictGrades[student.kaid_student][8]
        except:
            skills_level["mastery3"] = 0
        student_json["skills_level"]=skills_level
        try:
            completed_percentage=dictGrades[student.kaid_student][10]/float(dictGrades[student.kaid_student][9])
        except:
            completed_percentage = 0
        try:
            total_rec=dictGrades[student.kaid_student][9]/float(1000)
        except:
            total_rec = 0
        student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec, "skills_com":skills_completadas, "skills_no_com":skills_no_completadas}

        assesment_json["assesment_student"].append(student_json)

        #print student_json
        #print "separador"
        
        i+=1
    queue.put(assesment_json)

    return queue
def getSkillsCorrect(grade_id):
    #skls = Skill_Log.objects.filter(id_grade_id=grade_id)
    skls = Skill.objects.filter(skill_log__id_grade_id=grade_id).values('name_spanish','skill_log__id_grade_id','skill_log__id_skill_name_id','skill_log__incorrect','skill_log__correct','skill_log__skill_progress')
    aux = []
    for s in skls:
        #name = Skill.objects.get(pk=s.id_skill_name_id).name_spanish
        #aux2 = [s.id_grade_id,s.id_skill_name_id,s.incorrect,s.correct,name]
        aux2 = [s['name_spanish'],s['skill_log__id_grade_id'],s['skill_log__id_skill_name_id'],s['skill_log__incorrect'],s['skill_log__correct'],s['skill_log__skill_progress']]
        aux.append(aux2)
    return aux

@login_required()
def getClassStudents(request, id_class):
    #Esta funcion entrega todos los estudiantes que pertenecen a un curso determinado y carga el dashboard
    request.session.set_expiry(timeSleep)#10 minutos
    id_institition_request=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')
    if(request.user.has_perm('bakhanapp.isAdmin')):
        classes = Class.objects.filter(id_institution_id=id_institition_request)
    else:
        classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class'))
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    try:
        clas = Class.objects.get(id_class=id_class)
        if (clas) and (classes.filter(id_class=id_class)):
            for i in range(len(classes)):
                classes[i].level = N[int(classes[i].level)] 
            students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
            #students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
            incorrect = Skill_Attempt.objects.filter(Q(kaid_student__in=students)&Q(correct=False)&(Q(skipped=False)|(Q(skipped=True)&Q(task_type__startswith='mastery.')))).values('kaid_student_id').annotate(incorrect=Count('kaid_student_id'))   
            correct = Skill_Attempt.objects.filter(kaid_student__in=students,correct=True).values('kaid_student_id').annotate(correct=Count('kaid_student_id'))
            time_excercice = Skill_Attempt.objects.filter(kaid_student__in=students).values('kaid_student_id').annotate(time=Sum('time_taken'))    
            time_video = Video_Playing.objects.filter(kaid_student__in=students).values('kaid_student_id').annotate(time=Sum('seconds_watched'))   
            practiced = Student_Skill.objects.filter(kaid_student__in=students,last_skill_progress='practiced',struggling=False).values('kaid_student_id').annotate(practiced=Count('last_skill_progress')) 
            mastery1 = Student_Skill.objects.filter(kaid_student__in=students,last_skill_progress='mastery1',struggling=False).values('kaid_student_id').annotate(mastery1=Count('last_skill_progress'))
            mastery2 = Student_Skill.objects.filter(kaid_student__in=students,last_skill_progress='mastery2',struggling=False).values('kaid_student_id').annotate(mastery2=Count('last_skill_progress'))
            mastery3 = Student_Skill.objects.filter(kaid_student__in=students,last_skill_progress='mastery3',struggling=False).values('kaid_student_id').annotate(mastery3=Count('last_skill_progress'))
            struggling = Student_Skill.objects.filter(kaid_student__in=students,struggling=True).values('kaid_student_id').annotate(struggling=Count('last_skill_progress'))
            total_recomended = Grade.objects.filter(kaid_student__in=students).values('kaid_student_id').annotate(total_recomended=Sum('total_recomended')) #Student_Skill.objects.filter(kaid_student__in=students,struggling=True).values('kaid_student_id').annotate(struggling=Count('last_skill_progress'))
            recomended_complete = Grade.objects.filter(kaid_student__in=students).values('kaid_student_id').annotate(recomended_complete=Sum('recomended_complete'))

            assesments = Assesment.objects.filter(id_class_id=id_class)
            grades = Assesment.objects.filter(id_class_id=id_class).values('id_assesment','grade__kaid_student','grade__grade','grade__id_grade','grade__performance_points','grade__effort_points','grade__bonus_grade','grade__teacher_grade','grade__comment').order_by('id_assesment')
            dictGrades = {}
            for g in grades:
                name = Student.objects.filter(pk=g['grade__kaid_student']).values('name', 'nickname')
                name = name[0]['nickname']
                skls = getSkillsCorrect(g['grade__id_grade'])
                dictGrades[(g['id_assesment'],g['grade__kaid_student'])] = (g['grade__grade'],g['grade__id_grade'],g['grade__performance_points'],g['grade__effort_points'],g['grade__bonus_grade'],name,skls,g['grade__teacher_grade'],g['grade__comment'])
            #print dictGrades[(67,'kaid_962822484535083405338400')][1]
            assesment_array=[]
            threads = []
            queue = Queue.Queue()
            for assesment in assesments:
                t = threading.Thread(target=parallelAssesment,args=(assesment,students,queue))
                threads.append(t)
                t.start()
            for assesment in assesments:
                response = queue.get()
                assesment_array.append(response)
            dictTotalTimeExcercice = {}
            dictTotalIncorrect = {}
            dictTotalCorrect = {}
            dictTotalTimeVideo = {}
            dictPracticed = {}
            dictMastery1 ={}
            dictMastery2 ={}
            dictMastery3 ={}
            dictStruggling ={}
            dictTotalRecomended={}
            dictRecomendedComplete={}
            for vid in time_video:
                dictTotalTimeVideo[vid['kaid_student_id']] = vid['time']
            for te in time_excercice:
                dictTotalTimeExcercice[te['kaid_student_id']] = te['time']
            for cor in correct:
                dictTotalCorrect[cor['kaid_student_id']] = cor['correct']
            for inc in incorrect:
                dictTotalIncorrect[inc['kaid_student_id']]=inc['incorrect'] 
            for pract in practiced:
                dictPracticed[pract['kaid_student_id']]=pract['practiced']
            for mas in mastery1:
                dictMastery1[mas['kaid_student_id']] = mas['mastery1'] 
            for mas in mastery2:
                dictMastery2[mas['kaid_student_id']] = mas['mastery2'] 
            for mas in mastery3:
                dictMastery3[mas['kaid_student_id']] = mas['mastery3']
            for mas in struggling:
                dictStruggling[mas['kaid_student_id']] = mas['struggling']
            for total in total_recomended:
                dictTotalRecomended[total['kaid_student_id']] = total['total_recomended']
            for recomended in recomended_complete:
                dictRecomendedComplete[recomended['kaid_student_id']] = recomended['recomended_complete']
            json_array=[]
            i=0
            for student in students:
                skills_completadas=[]
                skills_no_completadas=[]
                student_json = {}
                student_json["id"] = i
                student_json['kaid'] = student.kaid_student
                student_json["name"] = student.nickname
                try:#id3002
                    #if student.kaid_student=='kaid_650486821916405105888593':
                    #print student.kaid_student
                    g = Grade.objects.filter(kaid_student_id=student.kaid_student).values('id_grade')

                    skills_complete = Skill.objects.filter((Q(skill_log__skill_progress='practiced')|Q(skill_log__skill_progress='mastery1')|
                        Q(skill_log__skill_progress='mastery2')|Q(skill_log__skill_progress='mastery3')),
                        skill_log__id_grade=g).values('name_spanish').distinct('name_spanish')
                    #    print "len abajo"
                    #    print len(skills_complete)
                    for s in skills_complete:
                        #print s['name_spanish']
                        skills_completad = s['name_spanish']
                        skills_completadas.append(skills_completad)
                    #skills_completadas = dictSkills[student.kaid_student]
                    #print skills_completadas
                    #print len(skills_completadas)
                except Exception as e:
                    skills_completadas = []
                    #print "***ERROR*** ha fallado try:#id2002 bakhanapp/views.py"
                    print e

                try:#id3003
                    #if student.kaid_student=='kaid_650486821916405105888593':
                    #print student.kaid_student
                    g = Grade.objects.filter(kaid_student_id=student.kaid_student).values('id_grade')

                    skills_no_complete = Skill.objects.filter((Q(skill_log__skill_progress='unstarted')|Q(skill_log__skill_progress='struggling')),
                    skill_log__id_grade=g).values('name_spanish')
                    #    print "len abajo"
                    #    print len(skills_complete)
                    for s in skills_no_complete:
                        #print s['name_spanish']
                        skills_no_completad = s['name_spanish']
                        skills_no_completadas.append(skills_no_completad)
                    #skills_completadas = dictSkills[student.kaid_student]
                    #print skills_completadas
                    #print len(skills_completadas)
                except Exception as e:
                    skills_no_completadas = []
                    #print "***ERROR*** ha fallado try:#id3003 bakhanapp/views.py"
                    print e

                try:
                    completed_percentage=dictRecomendedComplete[student.kaid_student]/float(dictTotalRecomended[student.kaid_student])
                except:
                    completed_percentage = 0
                try:
                    total_rec = dictTotalRecomended[student.kaid_student]/float(1000)
                except:
                    total_rec = 0
                student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec, "skills_com":skills_completadas, "skills_no_com":skills_no_completadas}
                try:
                    student_json["skills_time"] = dictTotalTimeExcercice[student.kaid_student]
                except:
                    student_json["skills_time"] = 0
                try:
                    student_json["video_time"] = dictTotalTimeVideo[student.kaid_student]
                except:
                    student_json["video_time"] = 0
                student_exercise={}
                try:
                    student_exercise["correct"] = dictTotalCorrect[student.kaid_student]
                except:
                    student_exercise["correct"] = 0
                try:
                    student_exercise["incorrect"] = dictTotalIncorrect[student.kaid_student]
                except:
                    student_exercise["incorrect"] = 0
                student_json["exercises"]=student_exercise 
                skills_level={}
                try:
                    skills_level["struggling"] = dictStruggling[student.kaid_student]
                except:
                    skills_level["struggling"] = 0
                try:
                    skills_level["practiced"] = dictPracticed[student.kaid_student]
                except:
                    skills_level["practiced"] = 0
                try:
                    skills_level["mastery1"] = dictMastery1[student.kaid_student]
                except:
                    skills_level["mastery1"] = 0
                try:
                    skills_level["mastery2"] = dictMastery2[student.kaid_student]
                except:
                    skills_level["mastery2"] = 0
                try:
                    skills_level["mastery3"] = dictMastery3[student.kaid_student]
                except:
                    skills_level["mastery3"] = 0
                student_json["skills_level"] = skills_level
                for assesment in assesment_array:
                    #print dictAssesment[(67,'kaid_962822484535083405338400')]
                    student_assesment = {}
                    id_assesment = "assesment"+(str)(assesment["id"])
                    id_assesment_num = assesment["id"]
                    random_effort = round(random.uniform(1,100))
                    try:
                        student_assesment["grade"] = round(dictGrades[(assesment['id'],student.kaid_student)][0],1)
                        student_assesment["grade_id"] = dictGrades[(assesment['id'],student.kaid_student)][1]
                        student_assesment["effort"] = dictGrades[(assesment['id'],student.kaid_student)][3]+0.1
                    except:
                        student_assesment["grade"] = None
                        student_assesment["effort"] = 0.1
                        student_assesment["grade_id"] = 0
                    try:
                        student_assesment["teacher_grade"] = dictGrades[(assesment['id'],student.kaid_student)][7]
                    except:
                        student_assesment["teacher_grade"] = 0
                    try:
                        student_assesment["comment"] = dictGrades[(assesment['id'],student.kaid_student)][8]
                    except:
                        student_assesment["comment"] = "sin comentarios"
                    try:
                        student_assesment['performance_points'] = dictGrades[(assesment['id'],student.kaid_student)][2]
                    except:
                        student_assesment['performance_points'] = None
                    try:
                        student_assesment['bonus_grade'] = round(dictGrades[(assesment['id'],student.kaid_student)][4],1)
                    except:
                        student_assesment['bonus_grade'] = 0
                    try:
                        student_assesment['skills'] = dictGrades[(assesment['id'],student.kaid_student)][6]
                    except:
                        student_assesment['skills'] = []
                    try:
                        student_assesment['name'] = dictGrades[(assesment['id'],student.kaid_student)][5]
                    except:
                        student_assesment['name'] = "s/n"
                    student_json[id_assesment] = student_assesment
                i+=1
                json_array.append(student_json)
            json_dict={"students":json_array, "assesments":assesment_array}
            
            #json_dict = json.dumps(json_dict, sort_keys=True)

            json_data = json.dumps(json_dict)
            classroom = Class.objects.filter(id_class=id_class)
            if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
                isTeacher = True
                assesment_configs = Assesment_Config.objects.filter(kaid_teacher=request.user.user_profile.kaid)
            else:
                isTeacher = False
                assesment_configs = Assesment_Config.objects.filter(kaid_teacher_id__in=Teacher.objects.filter(id_institution_id=id_institition_request))
            spanish_classroom = N[int(classroom[0].level)] +' '+ classroom[0].letter
            s_skills = getClassSkills(request,id_class)
            
            return render_to_response('studentClass.html',
                                        {'students': students, 'classroom': classroom,'jason_data': json_data, 'classes': classes,
                                        's_skills':s_skills, 'assesment_configs':assesment_configs,'spanish_classroom':spanish_classroom,'isTeacher':isTeacher}, #'grades':grades,
                                        context_instance=RequestContext(request)
                                    )
        else:
            return HttpResponseRedirect("/inicio")
    except Exception as e:
        print '***ERROR*** no se ha podido cargar el dashboard'
        print e
        return HttpResponseRedirect("/inicio")




def getTopictree(subject):
    topictree_json={}
    topictree_json['checkbox']={'keep_selected_style':False}
    topictree_json['plugins']=['checkbox','search']
    topictree=[]
    start_time=time.time()
    #string_query ='''select c.name_spanish as chapter_name, t.name_spanish as topic_name, st.name_spanish as subtopic_name, s.id_skill_name as skill_id, s.name_spanish as skill_name
    #             from bakhanapp_chapter c, bakhanapp_skill s, bakhanapp_topic t, bakhanapp_subtopic st, bakhanapp_subtopic_skill ss
    #             where c.id_chapter_name=t.id_chapter_name_id and t.id_topic_name=st.id_topic_name_id and st.id_subtopic_name=ss.id_subtopic_name_id and ss.id_skill_name_id=s.id_skill_name
    #             order by c.name_spanish, t.name_spanish, st.name_spanish'''
    #cursor=connection.cursor()
    #cursor.execute(string_query)
    #query_result = dictfetchall(cursor)
    #last_chapter=''
    #last_topic=''
    #last_subtopic=''
    #last_skill=''
    #chapters=[]
    #for query_tuple in query_result:
    #    current_chapter=query_tuple['chapter_name']
    #    current_topic=query_tuple['topic_name']
    #    current_subtopic=query_tuple['subtopic_name']
    #    current_skill=query_tuple['skill_name']
    #    current_skill_id=query_tuple['skill_id']
    #    
    #    if last_chapter=="" or last_chapter!=current_chapter:
    #        chapter={"text":current_chapter, "data":{}, "children":[]}
    #        chapters.append(chapter)
    #        last_chapter=current_chapter

    #    if last_topic=="" or last_topic!=current_topic:
    #        topic={"text":current_topic, "data":{}, "children":[]}
    #        chapter["children"].append(topic)
    #        last_topic=current_topic    
        
    #    if last_subtopic=="" or last_subtopic!=current_subtopic:
    #        subtopic={"text":current_subtopic, "data":{}, "children":[]}
    #        topic["children"].append(subtopic)
    #        last_subtopic=current_subtopic 
    #    skill={"text":current_skill, "data":{"skill_id": current_skill_id}, "children":[]}
    #    subtopic["children"].append(skill)
    subjects=Subject.objects.all()
    for subject in subjects:
        subject_obj={"id": subject.id_subject_name, "parent":"#", "text": subject.name_spanish, "state": {"opened":"true"}, "icon":"false"}
        topictree.append(subject_obj)
    subject_chapter=Chapter.objects.order_by('index')
    for chapter in subject_chapter:
        chapter_obj={"id":chapter.id_chapter_name, "parent": chapter.id_subject_name_id, "text":chapter.name_spanish, "icon":"false"}
        topictree.append(chapter_obj)
    chapter_topic=Topic.objects.order_by('index')
    for topic in chapter_topic:
        topic_obj={"id":topic.id_topic_name, "parent": topic.id_chapter_name_id, "text":topic.name_spanish, "icon":"false"}
        topictree.append(topic_obj)
    topic_subtopic=Subtopic.objects.exclude(index=None).order_by('index')
    for subtopic in topic_subtopic:
        subtopic_obj={"id":subtopic.id_subtopic_name, "parent": subtopic.id_topic_name_id, "text":subtopic.name_spanish, "icon":"false"}
        topictree.append(subtopic_obj)
    subtopic_skill=Subtopic_Skill.objects.filter(id_subtopic_name_id__in=topic_subtopic).select_related('id_skill_name')
    id=0
    for skill in subtopic_skill:
        skill_id=skill.id_subtopic_skill
        skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
        sorted(skill_obj, key=skill_obj.get)
        topictree.append(skill_obj)
        id=id+1
    #print("--- %s seconds ---" % (time.time() - start_time))
    #print topictree
    #temp=[]
    #chapters=Chapter.objects.filter(id_subject_name_id=subject)
    #for chapter in chapters:
    #    chapter_obj={'text':chapter.name_spanish,'children':[]}
    #    topics=Topic.objects.filter(id_chapter_name_id=chapter.id_chapter_name)
        #print(chapter)
    #    for topic in topics:
    #        topic_obj={'text':topic.name_spanish,'children':[]}
    #        subtopics=Subtopic.objects.filter(id_topic_name_id=topic.id_topic_name)
            #print(topic)
    #        for subtopic in subtopics:
    #            subtopic_obj={'text':subtopic.name_spanish,'children':[]}
    #            subtopic_skills=Subtopic_Skill.objects.filter(id_subtopic_name_id=subtopic.id_subtopic_name)
    #            for subtopic_skill in subtopic_skills:
    #                skills=Skill.objects.filter(id_skill_name=subtopic_skill.id_skill_name_id)
    #                for skill in skills:
    #                    skill_obj={'text': skill.name_spanish, 'children':[]}
    #                    subtopic_obj['children'].append(skill_obj)
                        #temp.append(chapter)
                        #temp.append(topic)
                        #temp.append(subtopic)
                        #temp.append(skill)
                        #print(chapter.id_chapter_name+" - "+topic.id_topic_name+" + "+subtopic.id_subtopic_name+" * "+skill.name_spanish)
                        #topictree.append(temp)
    #                    temp=[]
    #            topic_obj['children'].append(subtopic_obj)
    #        chapter_obj['children'].append(topic_obj)
    #    topictree.append(chapter_obj)
    #topictree_json['core']={'data':chapters}
    topictree_json['core']={'data':topictree}
    #topictree_data=serialize('json',topictree_json)
    topictree_json_string=json.dumps(topictree_json)
    return topictree_json_string

def dictfetchall(cursor):
    #Returns all rows from a cursor as a dict
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def strip_acent(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

@permission_required('bakhanapp.isSuper',login_url="/")
def getAssesment(request):
    aux = Assesment.objects.all().order_by("id_assesment")
    for a in aux:
        pauta = Assesment_Config.objects.get(pk=a.id_assesment_conf_id)
        a.id_assesment_conf_id = pauta.name
        rClass = Class.objects.get(pk=a.id_class_id)
        N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']       
        nameClass= N[int(rClass.level)]  +' '+ rClass.letter
        institucion = Institution.objects.get(pk=rClass.id_institution_id)
        #####el max y el min grade se utilizan para pasar el nombre de la clase y la institucion#####
        a.max_grade = nameClass
        a.min_grade = institucion.name
    try:
        return render_to_response('deleteAssesment.html',{'aux': aux},context_instance=RequestContext(request))
    except Exception as e:
        print e
 
