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
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress

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
import datetime
import threading
import Queue



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

@login_required()
def getTeacherClasses(request):
    request.session.set_expiry(300)
    print request.user.user_profile.kaid
    #Esta funcion entrega todos los cursos que tiene a cargo el profesor que se encuentra logueado en el sistema
    classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class'))
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    return render_to_response('myClasses.html', {'classes': classes}, context_instance=RequestContext(request))
    

def getClassSkills(request,id_class):
    #Funcion que entrega un arreglo con la cantidad de habilidades en cada nivel de dominio
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#devuelve todos los estudiantes de una clase
    students_skills = Student_Skill.objects.filter(kaid_student__in=students).values('last_skill_progress','kaid_student').annotate(scount=Count('kaid_student'))
    #print students_skills
    return students_skills


def paralellAssesment(assesment,students,queue):
    #print '****************inicio el thread*********************'
    inicio = time.time()
    assesment_json={}
    assesment_json["id"]=assesment.id_assesment
    assesment_json["name"]=assesment.name
    assesment_json["config_name"]= assesment.id_assesment_conf.name
    assesment_json["approval_percentage"]= assesment.id_assesment_conf.approval_percentage
    assesment_json["top_score"]= assesment.id_assesment_conf.top_score
    assesment_json["max_grade"]= assesment.max_grade
    assesment_json["min_grade"]= assesment.min_grade
    assesment_json["id_config"]= assesment.id_assesment_conf.id_assesment_config
    assesment_json["start_date"]= str(assesment.start_date)
    assesment_json["end_date"]= str(assesment.end_date)
    assesment_json["assesment_student"]=[]
    grades = Grade.objects.filter(id_assesment_id=assesment.id_assesment).values('kaid_student_id','correct','incorrect','video_time','excercice_time',
        'struggling','practiced','mastery1','mastery2','mastery3')
    dictGrades = {}
    for g in grades:
        dictGrades[g['kaid_student_id']] = (g['correct'],g['incorrect'],g['video_time'],g['excercice_time'],g['struggling'],g['practiced'],g['mastery1'],
            g['mastery2'],g['mastery3'])
    i=0
    for student in students:
        student_json={}
        student_json["id"]=i
        student_json["name"]=student.name
        completed_percentage=round(random.uniform(0,1),2)
        total_rec=round(random.uniform(0,1),2)
        student_json["recommendations"]={"completed_perc":completed_percentage,"total":total_rec}
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

        assesment_json["assesment_student"].append(student_json)
        i+=1
    queue.put(assesment_json)

    return queue

@login_required()
def getClassStudents(request, id_class):
    #Esta funcion entrega todos los estudiantes que pertenecen a un curso determinado y carga el dashboard
    request.session.set_expiry(600)#10 minutos
    classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_class'))
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
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
    assesments = Assesment.objects.filter(id_class_id=id_class)
    grades = Assesment.objects.filter(id_class_id=id_class).values('id_assesment','grade__kaid_student','grade__grade','grade__id_grade','grade__performance_points','grade__effort_points','grade__bonus_grade').order_by('id_assesment')
    dictGrades = {}
    for g in grades:
        name = Student.objects.filter(pk=g['grade__kaid_student']).values('name')
        name = name[0]['name']
        dictGrades[(g['id_assesment'],g['grade__kaid_student'])] = (g['grade__grade'],g['grade__id_grade'],g['grade__performance_points'],g['grade__effort_points'],g['grade__bonus_grade'],name)
    #print dictGrades[(67,'kaid_962822484535083405338400')][1]
    assesment_array=[]
    threads = []
    queue = Queue.Queue()
    for assesment in assesments:
        t = threading.Thread(target=paralellAssesment,args=(assesment,students,queue))
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
    json_array=[]
    i=0
    for student in students:
        student_json = {}
        student_json["id"] = i
        student_json['kaid'] = student.kaid_student
        student_json["name"] = student.name
        completed_percentage=round(random.uniform(0,1),2)
        total_rec=round(random.uniform(0,1),2)
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
                student_assesment['performance_points'] = dictGrades[(assesment['id'],student.kaid_student)][2]
            except:
                student_assesment['performance_points'] = None
            try:
                student_assesment['bonus_grade'] = dictGrades[(assesment['id'],student.kaid_student)][4]
            except:
                student_assesment['bonus_grade'] = 0
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
    s_skills = getClassSkills(request,id_class)
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher=kaid.kaid)
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
