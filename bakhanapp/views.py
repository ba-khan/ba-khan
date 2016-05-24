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
from django.db.models import Count,Sum


from django import template
from bakhanapp.models import Assesment_Skill
register = template.Library()

from bakhanapp.models import Class
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


@login_required()
def generateAssesmentExcel(request, id_assesment):
    request.session.set_expiry(timeSleep)
    if request.method == 'GET':
        #args = request.POST
        #id_assesment = args['id_assesment']
        #id_assesment = 19
        infoAssesment = Assesment.objects.filter(id_assesment=id_assesment)
        
        #funcion que genera el excel de una evaluacion
        #variables
        
        delta = 7
        viewFields = ['Estudiante','Recomendadas Completadas','Ejercicios Incorrectos',
            'Ejercicios Correctos','Tiempo en Ejercicios','Tiempo en Videos',
            'En Dificultad','Practicado','Nivel 1','Nivel 2','Dominado',
            'Nota','Bonificacion por esfuerzo']
        totalFields = len(viewFields)
        #carga al arreglo los datos de la evaluacion id_assesment
        try:
            assesment = Assesment.objects.get(id_assesment=id_assesment)
            grades = Student.objects.filter(grade__id_assesment_id=id_assesment
                ).values('name','grade__grade',
                'grade__bonus_grade','grade__recomended_complete','grade__incorrect','grade__correct','grade__excercice_time',
                'grade__video_time','grade__struggling','grade__practiced','grade__mastery1','grade__mastery2','grade__mastery3')
        except Exception as e:
            print '***ERROR*** Ha fallado la query linea 424'
            print e

        totalGrades = grades.count()

        #crea el arreglo inicial
        w, h = totalFields +10 ,totalGrades + delta + 10
        data = [['' for x in range(w)] for y in range(h)] 
        print '***************debug******************'
        print assesment
        
        data[0][0] = 'Evaluacion'
        data[0][1] = assesment.name
        data[1][0] = 'Nota Minima'
        data[1][1] = assesment.min_grade
        data[2][0] = 'Nota Maxima'
        data[2][1] = assesment.max_grade
        data[3][0] = 'Nota de Aprobacion'
        data[3][1] = assesment.approval_grade
        data[4][0] = 'Bonificacion por Esfuerzo'
        data[4][1] = assesment.max_effort_bonus
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
                    data[i+delta][j] = grades[i]['grade__excercice_time']
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
        try:
            response = excel.make_response(pe.Sheet(data), 'xls', file_name=assesment.name)
        except Exception as e:
            print '***ERROR*** no se ha podido generar la respuesta excel'
            print e
            response = False
        return response


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
    #Esta funcion entrega todos los cursos que tiene a cargo el profesor que se encuentra logueado en el sistema
    #Si la persona logeada es un administrador, muestra todos los cursos de su establecimiento.
    if(request.user.has_perm('bakhanapp.isAdmin')):
        classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).order_by('level','letter')
    else:
        classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class')).order_by('level','letter')
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    return render_to_response('myClasses.html', {'classes': classes}, context_instance=RequestContext(request))
    

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
    for g in grades:
        dictGrades[g['kaid_student_id']] = (g['correct'],g['incorrect'],g['video_time'],g['excercice_time'],g['struggling'],g['practiced'],g['mastery1'],
            g['mastery2'],g['mastery3'],g['total_recomended'],g['recomended_complete'])
    i=0
    for student in students:
        student_json={}
        student_json["id"]=i
        student_json["name"]=student.name

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
        student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec}

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
            incorrect = Skill_Attempt.objects.filter(kaid_student__in=students,correct=False,skipped=False).values('kaid_student_id').annotate(incorrect=Count('kaid_student_id'))   
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
                name = Student.objects.filter(pk=g['grade__kaid_student']).values('name')
                name = name[0]['name']
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
                student_json = {}
                student_json["id"] = i
                student_json['kaid'] = student.kaid_student
                student_json["name"] = student.name
                try:
                    completed_percentage=dictRecomendedComplete[student.kaid_student]/float(dictTotalRecomended[student.kaid_student])
                except:
                    completed_percentage = 0
                try:
                    total_rec = dictTotalRecomended[student.kaid_student]/float(1000)
                except:
                    total_rec = 0
                student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec}
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
            if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid,id_class_id=id_class)):
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
    subject_chapter=Chapter.objects.all()
    for chapter in subject_chapter:
        chapter_obj={"id":chapter.id_chapter_name, "parent": chapter.id_subject_name_id, "text":chapter.name_spanish, "icon":"false"}
        topictree.append(chapter_obj)
    chapter_topic=Topic.objects.all()
    for topic in chapter_topic:
        topic_obj={"id":topic.id_topic_name, "parent": topic.id_chapter_name_id, "text":topic.name_spanish, "icon":"false"}
        topictree.append(topic_obj)
    topic_subtopic=Subtopic.objects.all()
    for subtopic in topic_subtopic:
        subtopic_obj={"id":subtopic.id_subtopic_name, "parent": subtopic.id_topic_name_id, "text":subtopic.name_spanish, "icon":"false"}
        topictree.append(subtopic_obj)
    subtopic_skill=Subtopic_Skill.objects.select_related('id_skill_name')
    id=0
    for skill in subtopic_skill:
        skill_id=skill.id_subtopic_skill
        skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false"}
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
