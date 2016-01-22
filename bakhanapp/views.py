# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect
from django.template.context import RequestContext
from .forms import loginForm
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

from .models import Class,Teacher
from .models import Skill
from .models import Skill_Progress
from .models import Student
from .models import Student_Class
from .models import Student_Video
from .models import Student_Skill
from .models import Video_Playing
from .models import Skill_Attempt
from .models import Assesment_Skill
from .models import Class_Subject
from .models import Assesment
from .models import Assesment_Config
from .models import Subtopic_Skill
from .models import Subtopic_Video
from bakhanapp.models import Grade,Skill,Student_Skill,Skill_Progress
from bakhanapp.models import Subject,Chapter,Topic,Subtopic,Subtopic_Skill

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


def login(request):
    return render(request, 'login.html')

def rejected(request):
    return render(request, 'rejected.html')

@login_required()
def home(request):
    return render_to_response('home.html',context_instance=RequestContext(request))

@login_required()
def teacher(request):
    return render_to_response('teacher.html',)

def deleteAssesmentConfig(request,id_assesment_config):
    Assesment_Config.objects.get(id_assesment_config=id_assesment_config).delete()
    return redirect('configuraciones')

def newAssesmentConfig(request):
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher='2')
    if request.method == 'POST':
        args = request.POST
        skills_selected = eval(args['skills'])
        teacher=Teacher.objects.get(pk="2")
        subject=Subject.objects.get(pk="math")
        new_assesment_config = Assesment_Config(name=args['name'],
                               approval_percentage=args['approval_percentage'],
                               kaid_teacher=teacher,
                               top_score=0,
                               id_subject_name=subject
                               )
        new_assesment_config.save()
        #id_new_assesment_config=new_assesment_config.pk
        for skill in skills_selected:
            skill_tuple=Skill.objects.get(pk=skill)
            new_assesment_skill=Assesment_Skill(id_assesment_config=new_assesment_config,
                                                id_skill_name=skill_tuple)
            new_assesment_skill.save()
        return redirect('configuraciones')
    else:
        form = AssesmentConfigForm(request.POST, request.FILES)
    topictree=getTopictree('math') #Modificar para que busque el topic tree completo (desde su root)
    return render_to_response('newAssesmentConfig.html',{'form': form,'assesment_configs': assesment_configs,'topictree':topictree}, context_instance=RequestContext(request))

def editAssesmentConfig(request,id_assesment_config):
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher='2')
    if request.method == 'POST':
        config = Assesment_Config.objects.get(id_assesment_config=id_assesment_config)
        form = AssesmentConfigForm(request.POST, request.FILES,instance=config)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('configuraciones')
    else:
        config = Assesment_Config.objects.get(id_assesment_config=id_assesment_config)
        form = AssesmentConfigForm(instance=config)
    return render_to_response('newAssesmentConfig.html',{'form': form,'assesment_configs': assesment_configs}, context_instance=RequestContext(request))

@login_required()
def getTeacherAssesmentConfigs(request):#url configuraciones
    #Esta funcion entrega todas las configuraciones de evaluaciones realizadas por un profesor
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher='2')
    return render_to_response('myAssesmentConfigs.html', {'assesment_configs': assesment_configs}, context_instance=RequestContext(request))

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

def newAssesment(request,id_class):#,id_assesment_config):
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher='2')
    return render_to_response('newAssesment.html',{'assesment_configs':assesment_configs,'id_class':id_class}, context_instance=RequestContext(request))

def newAssesment2(request,id_class,id_assesment_config):
    assesment_config = Assesment_Config.objects.filter(id_assesment_config=id_assesment_config)
    if request.method == 'POST':
        args = request.POST
        config = Assesment_Config.objects.filter(id_assesment_config=args['id_assesment_conf'])
        new= Assesment(start_date=args['start_date'],
                       end_date=args['end_date'],
                       id_assesment_conf_id=int(args['id_assesment_conf']),
                       #id_class_id = args['id_class'],
                       name = args['name'],
                       max_grade=args['max_grade'],
                       min_grade = args['min_grade']
                       )
        new.save()
        setGrades(new.id_assesment,new.id_assesment_conf_id,args['id_class'])
        return redirect('home')
    else:
        form = AssesmentForm(request.POST, request.FILES)
    return render_to_response('formNewAssesment.html',{'form':form,'assesment_config':assesment_config,'id_class':id_class}, context_instance=RequestContext(request))

def getTotalExerciseIncorrect(kaid_s):
    #Esta funcion entrega el total de ejercicios incorrectos de un estudiante.
    incorrect = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=False,skipped=False).count()
    return incorrect

def getExerciseIncorrectBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el total de ejercicios incorrectos de un estudiante en un tiempo determinado.
    incorrect = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=False,skipped=False,date__gte = t_begin,date__lte = t_end).count()
    return incorrect

def getTotalExerciseCorrect(kaid_s):
    #Esta funcion entrega el total de ejercicios correctos de un estudiante.
    correct = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=True).count()
    return correct

def getExerciseCorrectBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el total de ejercicios correctos de un estudiante en un tiempo determinado.
    correct = Skill_Attempt.objects.filter(kaid_student=kaid_s,correct=True,date__gte = t_begin,date__lte = t_end).count()
    return correct

def getTotalExerciseTime(kaid_s):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en toda su historia.
    query = Skill_Attempt.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query:
        time = time + register.time_taken
    return time

def getExerciseTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en un rango de fechas.
    query_set = Skill_Attempt.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end)
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

def getVideoTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en un rango de fechas.
    query_set = Video_Playing.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end)
    #query_set = query_set.filter(date__gte = t_begin)
    #query_set = query_set.filter(date__lte = t_begin)
    time = 0
    for register in query_set:
        time = time + register.total_seconds_watched
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
    for student in students:
        student.t_exercise= getTotalExerciseTime(student.kaid_student)
        student.t_video= getTotalVideoTime(student.kaid_student)
        student.correct= getTotalExerciseCorrect(student.kaid_student)
        student.incorrect= getTotalExerciseIncorrect(student.kaid_student)
        student.practiced = getTotalNivel(student.kaid_student,'practiced')
        student.mastery1 = getTotalNivel(student.kaid_student,'mastery1')
        student.mastery2 = getTotalNivel(student.kaid_student,'mastery2')
        student.mastery3 = getTotalNivel(student.kaid_student,'mastery3')
    classroom = Class.objects.filter(id_class=id_class)
    #grades = getClassGrades(request,id_class)
    s_skills = getClassSkills(request,id_class)
    assesment_configs = Assesment_Config.objects.filter(id_assesment_config=1)
    print assesment_configs
    return render_to_response('studentClass.html',
                                {'students': students, 'classroom': classroom,'classes': classes,
                                's_skills':s_skills, 'assesment_configs':assesment_configs}, #'grades':grades,
                                context_instance=RequestContext(request)
                            )


CONSUMER_KEY = 'uMCFkRw7QSJ3WkLs' #clave generada para don UTPs
CONSUMER_SECRET = 'tH8vhEBstXe6jFyG' #clave generada para don UTPs
    
CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'http://www.khanacademy.org'
SERVER_URL2 = 'http://es.khanacademy.org'
    
DEFAULT_API_RESOURCE = '/api/v1/playlists'
VERIFIER = None
    

# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            global VERIFIER

            params = cgi.parse_qs(self.path.split('?', 1)[1],
                keep_blank_values=False)
            VERIFIER = params['oauth_verifier'][0]

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("""<html lang="es">
                            <head>
                                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                                <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
                                <meta name="description" content="">
                                <meta name="keywords" content="">
                                <meta name="author" content="">
                                <link rel='stylesheet' type='text/css' href='https://www.khanacademy.org/genfiles/stylesheets/en/shared-package-426ede.css'>
                                <link rel='stylesheet' type='text/css' href='https://www.khanacademy.org/genfiles/stylesheets/en/nav-package-642efd.css'>
                                <link rel='stylesheet' type='text/css' href='https://www.khanacademy.org/genfiles/stylesheets/en/react-package-9b6f9e.css'>
                                <link rel='stylesheet' type='text/css' href='https://www.khanacademy.org/genfiles/stylesheets/en/odometer-package-be2a23.css'><link rel='stylesheet' type='text/css' href='https://www.khanacademy.org/genfiles/stylesheets/en/dashboard-package-756fe7.css'>
                                <link rel='stylesheet' type='text/css' href='https://www.khanacademy.org/genfiles/stylesheets/en/mobile-package-0edccb.css'>
                                <link href="/static/estilo.css" rel="stylesheet">                               
                                <title>BA-Khan</title>                                                               
                                <script>
                                    function closeMe(){
                                        var win = window.open("about:blank","_self");
                                        win.close();
                                    }
                                </script>                          
                            </head>
                              <body>                             
                                <div class="container">
                                     <div class="login-container">
                                        <h2 class="regular-header login-button-header">
                                            Ya puede cerrar esta pestana.
                                        </h2>
                                        <a role="button" aria-disabled="false" href="http://127.0.0.1:8000/inicio"  class="kui-button kui-button-submit kui-button-primary" style="width:100%;" data-reactid=".0.4.2">Listo</a>
                                       </div>
                                   </div>                           
                              </body>                           
                            </html>""")
            #webbrowser.open('http://www.google.cl')
            


        def log_request(self, code='-', size='-'):
            pass

    server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server


# Make an authenticated API call using the given rauth session.
#/api/v1/user?userId=&username=javierperezferrada&email=

def get_api_resource(session,request):
    resource_url = '/api/v1/user?userId=&username=&email='

    url = SERVER_URL + resource_url
    split_url = url.split('?', 1)
    params = {}

    # Separate out the URL's parameters, if applicable.
    if len(split_url) == 2:
        url = split_url[0]
        params = cgi.parse_qs(split_url[1], keep_blank_values=False)

    #start = time.time()
    response = session.get(url, params=params)
    #end = time.time()
    json_response = response.json()
    email = json_response['email']
    #username = json_response['username']
    user = auth.authenticate(username=email, password=email)
    if user:
        auth.login(request, user)
        return True
    else:
        user = User.objects.create_user(username=email,email=email,password=email)
        user.save()
        return False

def authenticate(request):
    global CONSUMER_KEY, CONSUMER_SECRET, SERVER_URL
    
    # Set consumer key, consumer secret, and server base URL from user input or
    # use default values.
    CONSUMER_KEY = CONSUMER_KEY
    CONSUMER_SECRET = CONSUMER_SECRET
    SERVER_URL = SERVER_URL

    # Create an OAuth1Service using rauth.
    service = rauth.OAuth1Service(
           name='test',
           consumer_key=CONSUMER_KEY,
           consumer_secret=CONSUMER_SECRET,
           request_token_url=SERVER_URL + '/api/auth2/request_token',
           access_token_url=SERVER_URL + '/api/auth2/access_token',
           authorize_url=SERVER_URL + '/api/auth2/authorize',
           base_url=SERVER_URL + '/api/auth2')

    callback_server = create_callback_server()

    # 1. Get a request token.
    request_token, secret_request_token = service.get_request_token(
        params={'oauth_callback': 'http://%s:%d/' %
            (CALLBACK_BASE, callback_server.server_address[1])})
    
    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)
    #return HttpResponseRedirect(authorize_url)
    webbrowser.open(authorize_url, new=0)
    
    callback_server.handle_request()
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    if get_api_resource(session,request):
        return HttpResponseRedirect('/inicio')
    else:
        return HttpResponseRedirect('/access/rejected')
    
def run_tests():
    global CONSUMER_KEY, CONSUMER_SECRET, SERVER_URL
    
    # Set consumer key, consumer secret, and server base URL from user input or
    # use default values.
    CONSUMER_KEY = CONSUMER_KEY
    CONSUMER_SECRET = CONSUMER_SECRET
    SERVER_URL = SERVER_URL

    # Create an OAuth1Service using rauth.
    service = rauth.OAuth1Service(
           name='test',
           consumer_key=CONSUMER_KEY,
           consumer_secret=CONSUMER_SECRET,
           request_token_url=SERVER_URL + '/api/auth2/request_token',
           access_token_url=SERVER_URL + '/api/auth2/access_token',
           authorize_url=SERVER_URL + '/api/auth2/authorize',
           base_url=SERVER_URL + '/api/auth2')

    callback_server = create_callback_server()

    # 1. Get a request token.
    request_token, secret_request_token = service.get_request_token(
        params={'oauth_callback': 'http://%s:%d/' %
            (CALLBACK_BASE, callback_server.server_address[1])})
    
    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)
    webbrowser.open(authorize_url)

    callback_server.handle_request()
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    #print
    #while(True):
    #    get_api_resource(session)
    return session

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

def get_api_resource2(session,llamada,server):

    url = server + llamada
    split_url = url.split('?', 1)
    params = {}

    # Separate out the URL's parameters, if applicable.
    if len(split_url) == 2:
        url = split_url[0]
        params = cgi.parse_qs(split_url[1], keep_blank_values=False)

    start = time.time()
    response = session.get(url, params=params)
    encoded_response=response.text.encode(sys.stdout.encoding,errors='replace')
    end = time.time()
    

    print "JASON: \n"
    return encoded_response
    print "\nTime: %ss\n" % (end - start)

def poblar_skill():
    '''
    for i in range(len(data)):   
        consulta = """UPDATE bakhanapp_skill SET name = '"""+data[i]["name"].replace(buscar,reemplazar)+"""' WHERE id_skill_name = '"""+data[i]["id"]+"""';"""
        cur.execute(consulta)
        conn.commit()
    '''

def poblar_skill_attempts(kaid_student, dates, session):
    student_skills = Student_Skill.objects.all()
    for i in range(len(student_skills)):
        skills=Skill.objects.filter(id_skill_name=student_skills[i].id_skill_name_id).values('id_skill_name','name')
        print skills[0]["name"]
        llamada = "/api/v1/user/exercises/"+skills[0]["name"]+"/log?userId="+kaid_student+"&username=&email=&dt_start="+dates
        jason = get_api_resource2(session,llamada,SERVER_URL)
        source = unicode(jason, 'ISO-8859-1')
        data = simplejson.loads(source)
        for j in range(len(data)):
            print data[j]["problem_number"]

            skill_attempts = Skill_Attempt.objects.create(count_attempts = data[j]["count_attempts"],
                                                                   mission = data[j]["mission"],
                                                                   time_taken = data[j]["time_taken"],
                                                                   count_hints = data[j]["count_hints"],
                                                                   skipped = data[j]["skipped"],
                                                                   points_earned = 0,
                                                                   date = data[j]["time_done"][:10],
                                                                   correct = data[j]["correct"],
                                                                   id_skill_name_id = skills[0]["id_skill_name"],
                                                                   kaid_student_id = data[j]["kaid"],
                                                                   problem_number = data[j]["problem_number"]
                                                                   )

def poblar_topictree(session,buscar, reemplazar,cur,conn):
    topictree = get_api_resource2(session,"/api/v1/topictree",SERVER_URL2)
    source_topictree = unicode(topictree, 'ISO-8859-1')
    data_topictree = simplejson.loads(source_topictree)
    #print data_topictree[i]["translated_title"]

    chapters=""
    topics=""
    subtopics=""
    videos = ""
    skills = ""
    subtopic_skills = ""
    id_subtopic_skills = 1
    subtopic_videos = ""
    id_subtopic_videos = 1
    cant_chapters = len(data_topictree["children"][1]["children"])
    for i in range(0,cant_chapters):
        #chapters = chapters+(data["children"][1]["children"][i]["slug"])+";"
        #chapters = chapters+(data["children"][1]["children"][i]["translated_title"])+";"
        #chapters = chapters+(data["children"][1]["slug"])+"\n"
        cant_topic = len(data_topictree["children"][1]["children"][i]["children"])
        for j in range(0,cant_topic):
            #topics = topics+(data["children"][1]["children"][i]["children"][j]["slug"])+";"
            #topics = topics+(data["children"][1]["children"][i]["children"][j]["translated_title"])+";"
            #topics = topics+(data["children"][1]["children"][i]["slug"])+"\n"
            cant_subtopic = len(data_topictree["children"][1]["children"][i]["children"][j]["children"])
            for k in range(0,cant_subtopic):
                #subtopics = subtopics+(data["children"][1]["children"][i]["children"][j]["children"][k]["slug"])+";"
                #subtopics = subtopics+(data["children"][1]["children"][i]["children"][j]["children"][k]["translated_title"])+";"
                #subtopics = subtopics+(data["children"][1]["children"][i]["children"][j]["slug"])+"\n"
                cant_videos = len(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["children"])
                for l in range(0,cant_videos):
                    consulta = """UPDATE bakhanapp_video SET name_spanish = '"""+data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["children"][l]["translated_title"].replace(buscar,reemplazar)+"""' WHERE id_video_name = '"""+data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["children"][l]["id"]+"""';"""
                    cur.execute(consulta)
                    conn.commit()
                    if (data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["kind"]=="Exercise"):
                        skills = skills+(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])+";"
                        skills = skills+(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["slug"])+"\n"
                        #subtopic_skills = subtopic_skills+(str)(id_subtopic_skills)+";"
                        subtopic_skills = subtopic_skills+(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])+";"
                        subtopic_skills = subtopic_skills+(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["slug"])+"\n"
                        id_subtopic_skills+=1
                    if (data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["kind"]=="Video"):
                        videos = videos+(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])+";"
                        videos = videos+(data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["slug"])+"\n"
                        #subtopic_videos = subtopic_videos+(str)(id_subtopic_videos)+";"
                        #subtopic_videos = subtopic_videos+(data["children"][1]["children"][i]["children"][j]["children"][k]["slug"])+";"
                        #subtopic_videos = subtopic_videos+(data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])+"\n"
                        id_subtopic_videos+=1
                        
def poblar_skill_progress(kaid_student,dates,session):
    llamada = "/api/v1/user/exercises/progress_changes?userId="+kaid_student+"&username=&email=&dt_start="+dates
    jason = get_api_resource2(session,llamada,SERVER_URL2)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    for i in range(len(data)):
        skill = Skill.objects.filter(name=data[i]["exercise_name"]).values('id_skill_name','name')
        #print skill[0]["id_skill_name"]
        print skill[0]["name"]
        student_skill=Student_Skill.objects.filter(kaid_student_id=kaid_student,id_skill_name_id=skill[0]["id_skill_name"]).values('id_student_skill')
        if (student_skill):
            print student_skill[0]["id_student_skill"]
            skill_progress = Skill_Progress.objects.create(to_level = data[i]["to_progress"]["level"],
                                                                   from_level = data[i]["from_progress"]["level"],
                                                                   date = data[i]["date"],
                                                                   id_student_skill_id = student_skill[0]["id_student_skill"]
                                                                   )
            print data[i]["date"]
            
def poblar_student_video(kaid_student, dates, session):
    llamada = "/api/v1/user/videos?userId="+kaid_student+"&username=&email=&dt_start="+dates
    jason = get_api_resource2(session,llamada,SERVER_URL2)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    for i in range(len(data)):
        if data[i]["points"] >0 :
            student_video = Student_Video.objects.create(total_seconds_watched = data[i]["seconds_watched"],
                                                                       total_points_earned = data[i]["points"],
                                                                       last_second_watched = data[i]["last_second_watched"],
                                                                       is_video_complete = data[i]["completed"],
                                                                       id_video_name_id = data[i]["video"]["id"],
                                                                       kaid_student_id = kaid_student,
                                                                       youtube_id = data[i]["video"]["youtube_id"]
                                                                       )

def poblar_video_playing(kaid_student, dates, session):   
    student_videos = Student_Video.objects.filter(kaid_student_id=kaid_student).values('youtube_id','id_video_name_id')
    for i in range(len(student_videos)):
        llamada = "/api/v1/user/videos/"+student_videos[i]["youtube_id"]+"/log?userId"+kaid_student+"=&username=&email=&dt_start="+dates
        jason = get_api_resource2(session,llamada,SERVER_URL2)
        source = unicode(jason, 'ISO-8859-1')
        data = simplejson.loads(source)
        for j in range(len(data)):
            video_playing = Video_Playing.objects.create(seconds_watched = data[j]["seconds_watched"],
                                                                       points_earned = data[j]["points_earned"],
                                                                       last_second_watched = data[j]["last_second_watched"],
                                                                       is_video_complete = data[j]["is_video_completed"],
                                                                       date = data[j]["time_watched"],
                                                                       id_video_name_id = student_videos[i]["id_video_name_id"],
                                                                       kaid_student_id = kaid_student
                                                                       )
            
@login_required()
def poblarBD(session):
    session = run_tests()
    #jason = get_api_resource2(session,"/api/v1/exercises",SERVER_URL2)
    #source = unicode(jason, 'ISO-8859-1')
    #data = simplejson.loads(source)
    buscar = "'"
    reemplazar = " "
    conn = psycopg2.connect(host="localhost", database="bakhanDB", user="postgres", password="root")
    cur = conn.cursor()
    kaid_student = "kaid_485871758161384306203631"
    dates = "2014-01-01T00%3A00%3A00Z&dt_end=2017-01-01T00%3A00%3A00Z"
    
    #poblar_topictree(session,buscar, reemplazar,cur,conn)

    #poblar_skill()
        
    #poblar_skill_attempts(kaid_student, dates, session)
    
    #poblar_skill_progress(kaid_student, dates, session)
    
    #poblar_student_video(kaid_student, dates, session)
    
    #poblar_video_playing(kaid_student, dates, session)    
