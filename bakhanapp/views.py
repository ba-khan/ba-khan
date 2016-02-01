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
from django.db.models import Count

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

import datetime

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
    return render_to_response('home.html',context_instance=RequestContext(request))

@login_required()
def teacher(request):
    return render_to_response('teacher.html',)

def getGradeStudent(id_assesment,kaid_student):
    #Funcion que entrega la nota de un estudiante en una evaluacion.
    grade = Grade.objects.filter(id_assesment=id_assesment,kaid_student=kaid_student).values('grade')
    return grade

def getSkillPoints(kaid_student,id_assesment_conf,t_begin,t_end):
    #Funcion que entrega el puntaje promedio de un estudiante, segun una configuracion de evaluacion 
    #y un rango de fechas.
    scores={'unstarted':0,'struggling':20,'practiced':40,'mastery1':60,'mastery2':80,'mastery3':100}
    configured_skills = Assesment_Skill.objects.filter(id_assesment_config=id_assesment_conf).values('id_skill_name')#skills en la configuracion actual
    points = 0
    for skill in configured_skills:
        id_student_skills = Student_Skill.objects.filter(id_skill_name_id=skill['id_skill_name'],kaid_student_id=kaid_student).values('id_student_skill')
        last_level = Skill_Progress.objects.filter(id_student_skill_id=id_student_skills[0]['id_student_skill'],date__gte = t_begin,date__lte = t_end).latest('date').values('to_level')
        points = points + scores[last_level]
    points = points / len(configured_skills)
    return points
        
def setGrades(id_assesment,id_assesment_config,id_class):
    #Funcion que guarda las notas obtenidas por los estudiantes de un curso segun una configuracion de evaluacion.
    assesment = Assesment.objects.filter(id_assesment=id_assesment).values('id_assesment','start_date','end_date','max_grade','min_grade')#obtengo assesment
    #print assesment[0]['id_assesment']
    assesment_config = Assesment_Config.objects.filter(id_assesment_config=id_assesment_config)#consulta los datos de la assesment_config involucrada
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#retorna todos los estudiantes de un curso
    for student in students:
        grade = Grade()#crea un nuevo registro grade
        grade.kaid_student_id = student.kaid_student#asigna el identificador del estudiante 
        grade.performance_points = getSkillPoints(student.kaid_student,id_assesment_config,assesment[0]['start_date'],assesment[0]['end_date'])#asigna los puntos obtenidos por desempenio
        #calcular la nota
        if grade.performance_points >= (assesment_config.aproval_percentage*100):#si obtiene mas que nota cuatro.
            x1 = assesment_config.aproval_percentage*100
            x2 = 100
            y1 = 4
            y2 = assesment[0]['max_grade']
            grade.grade = (((grade.performance_points-x1)/(x2-x1))*(y2-y1))+y1
        else:#si los puntos son menores al porcentaje de aprobacion
            x1 = 0
            x2 = assesment_config.aproval_percentage*100
            y1 = assesment[0]['min_grade']
            y2 = 4
            grade.grade = (((grade.performance_points-x1)/(x2-x1))*(y2-y1))+y1
        grade.save()

def getTotalExerciseIncorrect(kaid_s):
    #Esta funcion entrega el total de ejercicios incorrectos de un estudiante.
    incorrect = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=False,skipped=False).count()
    return incorrect

#def getExerciseIncorrectBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el total de ejercicios incorrectos de un estudiante en un tiempo determinado.
#    incorrect = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=False,skipped=False,date__gte = t_begin,date__lte = t_end).count()
#    return incorrect

def getExerciseIncorrectBetween(kaid_s,t_begin,t_end,id_assesment_conf):
    assesment_skills = Assesment_Skill.objects.filter(id_assesment_config_id=id_assesment_conf)
    skills = []
    for a in assesment_skills:
        skills.append(a.id_skill_name)
    #Esta funcion entrega el total de ejercicios incorrectos de un estudiante en un tiempo determinado.
    incorrect = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=False,skipped=False,date__gte = t_begin,date__lte = t_end, id_skill_name_id__in = skills).count()
    return incorrect

def getTotalExerciseCorrect(kaid_s):
    #Esta funcion entrega el total de ejercicios correctos de un estudiante.
    correct = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=True).count()
    return correct

#def getExerciseCorrectBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el total de ejercicios correctos de un estudiante en un tiempo determinado.
#    correct = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=True,date__gte = t_begin,date__lte = t_end).count()
#    return correct

def getExerciseCorrectBetween(kaid_s,t_begin,t_end,id_assesment_conf):
    assesment_skills = Assesment_Skill.objects.filter(id_assesment_config_id=id_assesment_conf)
    skills = []
    for a in assesment_skills:
        skills.append(a.id_skill_name)
    #Esta funcion entrega el total de ejercicios correctos de un estudiante en un tiempo determinado.
    correct = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=True,date__gte = t_begin,date__lte = t_end, id_skill_name_id__in = skills).count()
    return correct

def getTotalExerciseTime(kaid_s):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en toda su historia.
    query = Skill_Attempt.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query:
        time = time + register.time_taken
    return time

#def getExerciseTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en un rango de fechas.
#    query_set = Skill_Attempt.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end)
#    time = 0
#    for register in query_set:
#        time = time + register.time_taken
#    return time

def getExerciseTimeBetween(kaid_s,t_begin,t_end,id_assesment_conf):
    assesment_skills = Assesment_Skill.objects.filter(id_assesment_config_id=id_assesment_conf)
    skills = []
    for a in assesment_skills:
        skills.append(a.id_skill_name)
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en un rango de fechas.
    query_set = Skill_Attempt.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end, id_skill_name_id__in = skills)
    time = 0
    for register in query_set:
        time = time + register.time_taken
    return time

def getTotalVideoTime(kaid_s):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en toda su historia.
    query = Video_Playing.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query:
        time = time + register.seconds_watched
    return time

#def getVideoTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en un rango de fechas.
#    query_set = Video_Playing.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end)
    #query_set = query_set.filter(date__gte = t_begin)
    #query_set = query_set.filter(date__lte = t_begin)
#    time = 0
#    for register in query_set:
#        time = time + register.total_seconds_watched
#    return time

def getVideoTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en un rango de fechas.
    query_set = Video_Playing.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end)
    #query_set = query_set.filter(date__gte = t_begin)
    #query_set = query_set.filter(date__lte = t_begin)
    time = 0
    for register in query_set:
        time = time + register.seconds_watched
    return time

@login_required()
def getTeacherClasses(request):
    #Esta funcion entrega todos los cursos que tiene a cargo el profesor que se encuentra logueado en el sistema
    classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher='2').values('id_class'))
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    return render_to_response('myClasses.html', {'classes': classes}, context_instance=RequestContext(request))
    
def getClassGrades(request,id_class):
    #Funcion que entrega todas las notas de los estudiantes de un curso.
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
    #grades = Assesment.objects.filter(id_class=id_class).values('name', 'grade__kaid_student','grade__grade') #inner join Django
    #return grades

def getClassSkills(request,id_class):
    #Funcion que entrega un arreglo con la cantidad de habilidades en cada nivel de dominio
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#devuelve todos los estudiantes de una clase
    students_skills = Student_Skill.objects.filter(kaid_student__in=students).values('last_skill_progress','kaid_student').annotate(scount=Count('kaid_student'))
    print students_skills
    return students_skills

def getTotalNivel(kaid_student,nivel):
    total = Student_Skill.objects.filter(kaid_student=kaid_student,last_skill_progress=nivel).count()
    return total

def getClassAssesments(id_class):
    assesments = Assesment.objects.filter(id_class_id=id_class)
    return assesments

def getLastSkillsLevel(kaid_student,level):
    if level == 'struggling':
        total = Student_Skill.objects.filter(kaid_student=kaid_student, struggling=True).count()
    else:    
        total = Student_Skill.objects.filter(kaid_student=kaid_student,last_skill_progress=level,struggling=False).count()
    return total

@login_required()
def getClassStudents(request, id_class):
    #Esta funcion entrega todos los estudiantes que pertenecen a un curso determinado
    #Select * from student where kaid_student in (Select kaid_student from student_class where id_class_id = id_class)
    classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher='2').values('id_class'))

    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
    #evaluations_class = Assesment.objects.filter(id_class=id_class)#.values('id_assesment')
    #jason = '['
    
    assesments = getClassAssesments(id_class)
    assesment_array=[]
    
    for assesment in assesments:
        assesment_json={}
        assesment_json["id"]=assesment.id_assesment
        assesment_json["name"]=assesment.name
        assesment_json["config_name"]= assesment.id_assesment_conf.name
        assesment_json["approval_percentage"]= assesment.id_assesment_conf.approval_percentage
        assesment_json["top_score"]= assesment.id_assesment_conf.top_score
        assesment_json["max_grade"]=assesment.max_grade
        assesment_json["min_grade"]=assesment.min_grade
        assesment_json["assesment_student"]=[]
        for student in students:
            student_json={}
            student_json["name"]=student.name
            completed_percentage=round(random.uniform(0,1),2)
            total_rec=round(random.uniform(0,1),2)
            student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec}
            student.t_exercise= getExerciseTimeBetween(student.kaid_student,assesment.start_date,assesment.end_date,assesment.id_assesment_conf_id)
            student_json["skills_time"]=student.t_exercise
            student.t_video= getVideoTimeBetween(student.kaid_student,assesment.start_date,assesment.end_date)
            student_json["video_time"]=student.t_video
            student.correct= getExerciseCorrectBetween(student.kaid_student,assesment.start_date,assesment.end_date,assesment.id_assesment_conf_id)
            student.incorrect= getExerciseIncorrectBetween(student.kaid_student,assesment.start_date,assesment.end_date,assesment.id_assesment_conf_id)
            student_json["corrects"]=[(student.correct),(student.incorrect)]
            skills_level={}
            #student.struggling = getLastSkillsLevel(student.kaid_student, 'struggling')
            #skills_level["struggling"]=(student.struggling)
            skills_level["struggling"]=round(random.uniform(1,20),0)
            #student.practiced = getLastSkillsLevel(student.kaid_student,'practiced')
            #skills_level["practiced"]=(student.practiced)
            skills_level["practiced"]=round(random.uniform(1,20),0)
            #student.mastery1 = getLastSkillsLevel(student.kaid_student,'mastery1')
            #skills_level["mastery1"]=(student.mastery1)
            skills_level["mastery1"]=round(random.uniform(1,20),0)
            #student.mastery2 = getLastSkillsLevel(student.kaid_student,'mastery2')
            #skills_level["mastery2"]=(student.mastery2)
            skills_level["mastery2"]=round(random.uniform(1,20),0)
            #student.mastery3 = getLastSkillsLevel(student.kaid_student,'mastery3')
            #skills_level["mastery3"]=(student.mastery3)
            skills_level["mastery3"]=round(random.uniform(0,20),0)
            student_json["skills_level"]=skills_level
            assesment_json["assesment_student"].append(student_json)
        assesment_array.append(assesment_json)
        
    json_array=[]
    i=0
    for student in students:
        i+=1
        student_json={}
        student_json["name"]=student.name
        student.t_exercise= getTotalExerciseTime(student.kaid_student)
        completed_percentage=round(random.uniform(0,1),2)
        total_rec=round(random.uniform(0,1),2)
        student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec}
        student_json["skills_time"]=student.t_exercise
        student.t_video= getTotalVideoTime(student.kaid_student)
        student_json["video_time"]=student.t_video
        student.correct= getTotalExerciseCorrect(student.kaid_student)
        student.incorrect= getTotalExerciseIncorrect(student.kaid_student)
        student_json["corrects"]=[(student.correct),(student.incorrect)]
        skills_level={}
        student.struggling = getLastSkillsLevel(student.kaid_student, 'struggling')
        skills_level["struggling"]=(student.struggling)
        student.practiced = getLastSkillsLevel(student.kaid_student,'practiced')
        skills_level["practiced"]=(student.practiced)
        student.mastery1 = getLastSkillsLevel(student.kaid_student,'mastery1')
        skills_level["mastery1"]=(student.mastery1)
        student.mastery2 = getLastSkillsLevel(student.kaid_student,'mastery2')
        skills_level["mastery2"]=(student.mastery2)
        student.mastery3 = getLastSkillsLevel(student.kaid_student,'mastery3')
        skills_level["mastery3"]=(student.mastery3)
        student_json["skills_level"]=skills_level
        for assesment in assesment_array:
            student_assesment={}
            id_assesment = "assesment"+(str)(assesment["id"])
            random_grade=round(random.uniform(2,7),1)
            random_effort=round(random.uniform(1,100))
            student_assesment["grade"]=random_grade
            student_assesment["effort"]=random_effort
            student_json[id_assesment]= student_assesment
        json_array.append(student_json)
    
    
    json_dict={"students":json_array, "assesments":assesment_array}
    json_data = json.dumps(json_dict)
    classroom = Class.objects.filter(id_class=id_class)
    s_skills = getClassSkills(request,id_class)
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher='2')
    return render_to_response('studentClass.html',
                                {'students': students, 'classroom': classroom,'jason_data': json_data, 'classes': classes,
                                's_skills':s_skills, 'assesment_configs':assesment_configs}, #'grades':grades,
                                context_instance=RequestContext(request)
                            )




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
        skill_id="skill"+str(id)
        skill_obj={"id":skill_id, "parent":skill.id_subtopic_name_id, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false"}
        topictree.append(skill_obj)
        id=id+1
    print("--- %s seconds ---" % (time.time() - start_time))
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

