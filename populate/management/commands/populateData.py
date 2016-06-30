from django.shortcuts import render
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from django.core.management.base import BaseCommand, CommandError

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
from bakhanapp.models import Institution

import datetime
import time
from time import localtime

import cgi
import rauth
import SimpleHTTPServer
import SocketServer

import webbrowser
import psycopg2
import requests
#import xlrd
from collections import OrderedDict

import json
import simplejson
import sys
from pprint import pprint
import codecs
from lib2to3.fixer_util import String
from django.core import serializers
from django.db import connection

import random

import urlparse

import threading
from threading import Semaphore
semafaro = Semaphore(50)
    
CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'https://www.khanacademy.org'
SERVER_URL2 = 'https://es.khanacademy.org'
    
DEFAULT_API_RESOURCE = '/api/v1/playlists'
VERIFIER = None
import logging

now = datetime.datetime.now()
fecha=now.strftime("%Y-%m-%d-T-%H-%M-Z")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='populatedata'+fecha+'.log',
                    filemode='w')
logging.debug('A debug message')
logging.info('Some information')
logging.warning('A shot across the bows')
    

# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            global VERIFIER
            logging.debug("kk")
            params = cgi.parse_qs(self.path.split('?', 1)[1],
                keep_blank_values=False)
            VERIFIER = params['oauth_verifier'][0]

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('OAuth request token fetched and authorized;' +
                ' you can close this window. B!tch.')
            #webbrowser.open('http://www.google.cl')

        def log_request(self, code='-', size='-'):
            pass

    server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server


# Make an authenticated API call using the given rauth session.
#/api/v1/user?userId=&username=javierperezferrada&email=

    
def run_tests(identifier,passw, CONSUMER_KEY, CONSUMER_SECRET):
    #global CONSUMER_KEY, CONSUMER_SECRET, SERVER_URL
    global SERVER_URL
    
    # Set consumer key, consumer secret, and server base URL from user input or
    # use default values.
    #CONSUMER_KEY = CONSUMER_KEY
    #CONSUMER_SECRET = CONSUMER_SECRET
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
        params={'oauth_callback': SERVER_URL +'/api/auth/default_callback'}) #'http://%s:%d/' %
            #(CALLBACK_BASE, callback_server.server_address[1])})

    logging.debug(request_token)
    logging.debug(secret_request_token)
    
    noClickParams = {'oauth_token':request_token, 'identifier':identifier, 'password':passw}
    
    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)
    logging.debug(authorize_url)

    #webbrowser.open(authorize_url) #Abre ventana para hacer click en aceptar y loguearse


#LINKS
#https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication
#http://es.python-requests.org/es/latest/user/quickstart.html#cabeceras-personalizadas
#https://teamtreehouse.com/community/khan-academy-api-authentication-in-nodejs
#http://www.pythonforbeginners.com/requests/using-requests-in-python


    #hacer peticion POST a authorize_url con los parametros request_token, user, pass
    #headers = {'content-type': 'application/json'}
    post_url=SERVER_URL +'/api/auth2/authorize'
    #credentials = json.dumps(noClickParams)
    #session = requests.Session()
    #print session
    #r = session.post('https://www.khanacademy.org/api/auth2/authorize', data=noClickParams)#, headers=headers)
    #session = requests.Session()
    #print session
    #r = session.post(post_url, data=noClickParams)
    #print r.status_code

    r = requests.post(post_url, data=noClickParams)
    logging.debug(r.url)
    
    logging.debug(r.text)
    logging.debug(r.status_code)
    #print r
    access_url = urlparse.parse_qs(urlparse.urlparse(r.url).query)
    oauth_verifier_raw = access_url["oauth_verifier"][0]
    oauth_verifier = oauth_verifier_raw.encode('ascii','ignore')
    logging.debug(oauth_verifier)
    #callback_server.handle_request() #Esto esperaba el click de aceptar
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': oauth_verifier})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    #print
    #while(True):
    #    get_api_resource(session)
    logging.debug(session)
    return session

def getTopictree():
    topictree=[]
    temp=[]
    chapters=Chapter.objects.filter(id_subject_name_id='math')
    for chapter in chapters:
        topics=Topic.objects.filter(id_chapter_name_id=chapter.id_chapter_name)
        #print(chapter)
        for topic in topics:
            subtopics=Subtopic.objects.filter(id_topic_name_id=topic.id_topic_name)
            #print(topic)
            for subtopic in subtopics:
                subtopic_skills=Subtopic_Skill.objects.filter(id_subtopic_name_id=subtopic.id_subtopic_name)
                for subtopic_skill in subtopic_skills:
                    skills=Skill.objects.filter(id_skill_name=subtopic_skill.id_skill_name_id)
                    for skill in skills:
                        temp.append(chapter)
                        temp.append(topic)
                        temp.append(subtopic)
                        temp.append(skill)
                        logging.debug(chapter.id_chapter_name+" - "+topic.id_topic_name+" + "+subtopic.id_subtopic_name+" * "+skill.name_spanish)
                        topictree.append(temp)
                        temp=[]
    return topictree

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

    #print "JASON: \n"
    return encoded_response
    #print "\nTime: %ss\n" % (end - start)

def poblar_skill():
    '''
    for i in range(len(data)):   
        consulta = """UPDATE bakhanapp_skill SET name = '"""+data[i]["name"].replace(buscar,reemplazar)+"""' WHERE id_skill_name = '"""+data[i]["id"]+"""';"""
        cur.execute(consulta)
        conn.commit()
    '''

def poblar_student_skill(name_student, kaid_student, dates, session):
    #print "entro al poblar"
    skills=Skill.objects.values('name')
    #print skills
    #obtiene todos los skills de la tabla Skill
    for j in range(len(skills)):
        #print j
        #para cada skill realiza una llamada a la API entregandole ese skill y el username del estudiante
        #llamada = "/api/v1/user/exercises?kaid=&userId=&username="+name_student+"&email=&exercises="+skills[j]['name']
        llamada = "/api/v1/user/exercises/"+skills[j]["name"]+"?exercise_name="+skills[j]["name"]+"&userId=&username="+name_student+"&email="
        #logging.debug(llamada)
        #intenta obtener el json de la llamada si existe
        try:
            #print j
            jason = get_api_resource2(session,llamada,SERVER_URL2)
            logging.info("el json es "+jason)
            source = unicode(jason, 'ISO-8859-1')
            logging.info("source es "+source)
            data = simplejson.loads(source)
            logging.info("data es "+data)
            try:
                stdnt_skillid = Student_Skill.objects.filter(id_skill_name_id=data["exercise_model"]["id"], kaid_student_id=data["kaid"]).values("id_student_skill")
                #print stdnt_skillid
                if data["last_attempt_number"]>0:
                    data["last_attempt_number"]=1
                #si la fecha maximum_exercise_progress_dt no es nulo inserta
                if data["maximum_exercise_progress_dt"]!=None:
                    try:
                        #relleno de la tabla Student_Skill con los datos de esa skill para ese estudiante
                        student_skill = Student_Skill(id_student_skill=stdnt_skillid["id_student_skill"],
                                                        total_done = data["total_done"]+data["last_attempt_number"],
                                                        total_correct = data["total_correct"],
                                                        streak = data["streak"],
                                                        longest_streak = data["longest_streak"],
                                                        last_skill_progress = data["exercise_progress"]["level"],
                                                        total_hints = data["last_count_hints"],
                                                        struggling = data["exercise_states"]["struggling"],
                                                        id_skill_name_id = data["exercise_model"]["id"],
                                                        kaid_student_id = data["kaid"])
                                                                                   
                    
                        student_skill.save()
                    except Exception as e:#id10
                        logging.error('ha fallado try:#id10 en populateStudentSkill.py')
                        logging.info(e)

                else:
                    if data["total_done"]!=None and data["total_done"]>0:
                            #si el total_done es distinto de null y mayor que 0, debe insertar
                        try:    
                            student_skill = Student_Skill(id_student_skill=stdnt_skillid["id_student_skill"],
                                                        total_done = data["total_done"]+data["last_attempt_number"],
                                                        total_correct = data["total_correct"],
                                                        streak = data["streak"],
                                                        longest_streak = data["longest_streak"],
                                                        last_skill_progress = data["exercise_progress"]["level"],
                                                        total_hints = data["last_count_hints"],
                                                        struggling = data["exercise_states"]["struggling"],
                                                        id_skill_name_id = data["exercise_model"]["id"],
                                                        kaid_student_id = data["kaid"])
                                                                                       
                           
                            student_skill.save()

                        except Exception as e:#id11
                            logging.error('ha fallado try:#id11 en populateStudentSkill.py')
                            logging.info(e)


            except Exception as e:
                #print "error"
                if data["last_attempt_number"]>0:
                    data["last_attempt_number"]=1
                #si la fecha maximum_exercise_progress_dt no es nulo inserta
                if data["maximum_exercise_progress_dt"]!=None:
                    try:
                        #relleno de la tabla Student_Skill con los datos de esa skill para ese estudiante
                        student_skill = Student_Skill(total_done = data["total_done"]+data["last_attempt_number"],
                                                                                   total_correct = data["total_correct"],
                                                                                   streak = data["streak"],
                                                                                   longest_streak = data["longest_streak"],
                                                                                   last_skill_progress = data["exercise_progress"]["level"],
                                                                                   total_hints = data["last_count_hints"],
                                                                                   struggling = data["exercise_states"]["struggling"],
                                                                                   id_skill_name_id = data["exercise_model"]["id"],
                                                                                   kaid_student_id = data["kaid"]
                                                                                   )
                                                                                   
                    
                        student_skill.save()
                    except Exception as e:#id12
                        logging.error('ha fallado try:#id12 en populateStudentSkill.py')
                        logging.info(e)

                else:
                    if data["total_done"]!=None and data["total_done"]>0:
                        try:
                            #si el total_done es distinto de null y mayor que 0, debe insertar
                            
                            student_skill = Student_Skill(total_done = data["total_done"]+data["last_attempt_number"],
                                                                                       total_correct = data["total_correct"],
                                                                                       streak = data["streak"],
                                                                                       longest_streak = data["longest_streak"],
                                                                                       last_skill_progress = data["exercise_progress"]["level"],
                                                                                       total_hints = data["last_count_hints"],
                                                                                       struggling = data["exercise_states"]["struggling"],
                                                                                       id_skill_name_id = data["exercise_model"]["id"],
                                                                                       kaid_student_id = data["kaid"]
                                                                                       )
                                                                                       
                           
                            student_skill.save()
                        except Exception as e:#id13
                            logging.error('ha fallado try:#id13 en populateStudentSkill.py')
                            logging.info(e)
   
 
            #pregunta por el last_attempt_number de la consulta, si es mayor que 0 lo reemplaza por 1
                   
        except Exception as e:#id01
                logging.error('ha fallado try:#id01 en populateStudentSkill.py')
                logging.info(e)

def poblar_skill_attempts(name_student, kaid_student, dates, session):
    student_skills = Student_Skill.objects.filter(kaid_student_id=kaid_student)
    for i in range(len(student_skills)):
        skills=Skill.objects.filter(id_skill_name=student_skills[i].id_skill_name_id).values('id_skill_name','name')
        #print skills[0]["id_skill_name"]
        llamada = "/api/v1/user/exercises/"+skills[0]["name"]+"/log?userId=&username="+name_student+"&email=&dt_start="+dates
        jason = get_api_resource2(session,llamada,SERVER_URL)
        source = unicode(jason, 'ISO-8859-1')
        data = simplejson.loads(source)
        try:
            for j in range(len(data)):
                #print data[j]["time_done"]
                skill_attempts = Skill_Attempt(count_attempts = data[j]["count_attempts"],
                                                                       mission = data[j]["mission"],
                                                                       time_taken = data[j]["time_taken"],
                                                                       count_hints = data[j]["count_hints"],
                                                                       skipped = data[j]["skipped"],
                                                                       points_earned = 0,
                                                                       date = data[j]["time_done"],
                                                                       correct = data[j]["correct"],
                                                                       id_skill_name_id = skills[0]["id_skill_name"],
                                                                       kaid_student_id = kaid_student,
                                                                       problem_number = data[j]["problem_number"]
                                                                       )
                skill_attempts.save()

        except Exception as e:
            print e
            #print "otra materia (?)"
    #print "listeilors"


def poblar_skill_progress(student_name,kaid_student,dates,session):
#realiza la llamada a la API entregandole el username del estudiante y el rango de fechas
    llamada = "/api/v1/user/exercises/progress_changes?userId=&username="+student_name+"&email=&dt_start="+dates
    jason = get_api_resource2(session,llamada,SERVER_URL2)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    
    #print len(data)
    try:
        for i in range(len(data)):
            #para cada progreso lo debe guardar en la tabla skill_progress
            #print i
            #print data[i]["exercise_name"]
            skill = Skill.objects.filter(name=data[i]["exercise_name"]).values('id_skill_name','name')
            try:
                student_skill=Student_Skill.objects.filter(kaid_student_id=kaid_student,id_skill_name_id=skill[0]["id_skill_name"]).values('id_student_skill')
                new_progress = Skill_Progress(to_level=data[i]["to_progress"]["level"], 
                    from_level=data[i]["from_progress"]["level"], 
                    date=data[i]["date"], 
                    id_student_skill_id=student_skill[0]["id_student_skill"])
                new_progress.save()
            except Exception as e:
                print e
            '''    
            except:
                student_skill=Student_Skill.objects.filter(kaid_student_id=kaid_student).values("id_student_skill")
                new_progress = Skill_Progress(to_level=data[i]["to_progress"]["level"], 
                    from_level=data[i]["from_progress"]["level"], 
                    date=data[i]["date"], 
                    id_student_skill_id=student_skill[0]["id_student_skill"])
                new_progress.save()
            '''    
            #print student_skill[0]["id_student_skill"]
            '''
            new_progress = Skill_Progress(to_level=data[i]["to_progress"]["level"], 
                        from_level=data[i]["from_progress"]["level"], 
                        date=data[i]["date"], 
                        id_skill_name_id=data[i]["exercise_name"],
                        kaid_student=kaid_student,
                        id_student_skill_id=student_skill[0]["id_student_skill"])
            new_progress.save()

            '''
            #print "guardo bien"
    except Exception as e:
        print e
            
def poblar_student_video(student_name,kaid_student, dates, session):
    llamada = "/api/v1/user/videos?userId=&username="+student_name+"&email=&dt_start="+dates
    jason = get_api_resource2(session,llamada,SERVER_URL)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    #print "videos: ", len(data)
    for k in range(len(data)):
        #if data[i]["points"] >0 :
        #Tratar de hacer una especie de update_or_create()
        try:
            student_video = Student_Video(total_seconds_watched = data[k]["seconds_watched"],
                                                                       total_points_earned = data[k]["points"],
                                                                       last_second_watched = data[k]["last_second_watched"],
                                                                       is_video_complete = data[k]["completed"],
                                                                       id_video_name_id = data[k]["video"]["id"],
                                                                       kaid_student_id = kaid_student,
                                                                       youtube_id = data[k]["video"]["youtube_id"]
                                                                       )
            student_video.save()
        except Exception as e:
            print e
            #print "error"
    #print "listo student_video"

def poblar_video_playing(student_name,kaid_student, dates, session):   
    student_videos = Student_Video.objects.filter(kaid_student_id=kaid_student).values('youtube_id','id_video_name_id')
    for i in range(len(student_videos)):
        llamada = "/api/v1/user/videos/"+student_videos[i]["youtube_id"]+"/log?userId=&username="+student_name+"&email=&dt_start="+dates
        jason = get_api_resource2(session,llamada,SERVER_URL2)
        source = unicode(jason, 'ISO-8859-1')
        data = simplejson.loads(source)
        try:
            for j in range(len(data)):
                try:
                    idvideo = Video_Playing.objects.filter(date=data[j]["time_watched"], id_video_name_id=student_videos[i]["id_video_name_id"], kaid_student_id= kaid_student).values('id_video_playing')
                    #print idvideo[0]['id_video_playing']
                    video_playing = Video_Playing(id_video_playing=idvideo[0]['id_video_playing'], seconds_watched = data[j]["seconds_watched"],
                                                                               points_earned = data[j]["points_earned"],
                                                                               last_second_watched = data[j]["last_second_watched"],
                                                                               is_video_complete = data[j]["is_video_completed"],
                                                                               date = data[j]["time_watched"],
                                                                               id_video_name_id = student_videos[i]["id_video_name_id"],
                                                                               kaid_student_id = kaid_student
                                                                               )
                    video_playing.save()
                except:
                    video_playing = Video_Playing(seconds_watched = data[j]["seconds_watched"],
                                                                               points_earned = data[j]["points_earned"],
                                                                               last_second_watched = data[j]["last_second_watched"],
                                                                               is_video_complete = data[j]["is_video_completed"],
                                                                               date = data[j]["time_watched"],
                                                                               id_video_name_id = student_videos[i]["id_video_name_id"],
                                                                               kaid_student_id = kaid_student
                                                                               )
                    video_playing.save()

        except Exception as e:
            print e
            #print "error"
    #print "listo video_playing"

def coach_students(session): #ver los estudiantes que tienen como coach a cierto usuario. no entrega info de cursos
    llamada = "/api/v1/user/students"
    jason = get_api_resource2(session,llamada,SERVER_URL2)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    #with open('data.txt', 'w') as outfile:
    #    json.dump(data, outfile)
    logging.debug(len(data))
    for j in range(len(data)):
        logging.debug(data[j]["username"])

def poblar_students(session):
    # Open the workbook and select the first worksheet
    wb = xlrd.open_workbook('6BA-2016-Alabama.xlsx')
    sh = wb.sheet_by_index(0)
     
    # List to hold dictionaries
    students_list = []
     
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        student = OrderedDict()
        row_values = sh.row_values(rownum)
        student['name'] = row_values[0]
        student['points'] = int(row_values[11])
        student['class'] = row_values[12]
        student['kaid'] = row_values[13][28:]

        new_student = Student(kaid_student=row_values[13][28:],name=row_values[0],email=row_values[0],points=int(row_values[11]),phone=0)
        new_student.save()

        new_student_class = Student_Class(id_class_id=12,kaid_student_id=row_values[13][28:])

        new_student_class.save()
                
     
        students_list.append(student)
        logging.debug(students_list[rownum-1]['points'])
     
    # Serialize the list of dicts to JSON
    j = json.dumps(students_list)
            

def threadPopulate(students,dates,session):
    """thread populate function"""
    semafaro.acquire()
    try:
        poblar_student_skill(students.name, students.kaid_student, dates, session) #listo
    except:
        msg="error student_skill " + students.name
        logging.debug(msg)
    try:
        poblar_skill_attempts(students.name,students.kaid_student, dates, session) #listo
    except:
        msg = "error student_attempts "+students.name
        logging.debug(msg)

    try:
        poblar_skill_progress(students.name,students.kaid_student, dates, session) #listo
    except:
        msg="error student_progress "+ students.name
        logging.debug(msg)
  
    try:
        poblar_student_video(students.name,students.kaid_student, dates, session) #listo
    except:
        msg="error student_video "+ students.name
        logging.debug(msg)

    try:
        poblar_video_playing(students.name,students.kaid_student, dates, session)
    except:
        msg="error video_playing "+ students.name
        logging.debug(msg)
  
    msg = threading.currentThread().getName() + "Terminado"
    logging.debug(msg)
    semafaro.release()
    return


class Command(BaseCommand):
    help = 'Puebla la base de datos con ejercicios y videos vistos por los estudiantes'

    def handle(self, *args, **options):
        CONSUMER_KEY = 'AStAffVHzEtpSFJ3' #clave generada para don UTPs
        #CONSUMER_KEY = '8Bn3UyhPHamgCvGN' #Clave para LeonardoMunoz esc Alabama
        #keys = ['AStAffVHzEtpSFJ3','8Bn3UyhPHamgCvGN']
        CONSUMER_SECRET = 'UEQj2XKfGpFSMpNh' #clave generada para don UTPs
        #CONSUMER_SECRET  = '2zcpyDHnfTd5VWz9' #secret para LeonardoMunoz esc Alabama
        #secrets = ['UEQj2XKfGpFSMpNh','2zcpyDHnfTd5VWz9']
        #passw='clave1234'
        #identifier='utpbakhan'
        #passw='CONTRASENA'
        #identifier='LeonardoMunoz'
        #identifiers = ['utpbakhan','LeonardoMunoz']
        #passes = ['clave1234', 'CONTRASENA']

        #meter los parametros anteriores en alguna parte de la base de datos

        #institution = Institution.objects.all()
        institution = Institution.objects.filter(id_institution=5)


        for inst in institution:
            keys = inst.key
            secrets = inst.secret
            identifiers = inst.identifier
            passes = inst.password

            try:

                session = run_tests(identifiers,passes,keys,secrets)

                #coach_students(session, inst.id_institution)

                #print "logueadoooo"
                #jason = get_api_resource2(session,"/api/v1/exercises",SERVER_URL2)
                #source = unicode(jason, 'ISO-8859-1')
                #data = simplejson.loads(source)
                buscar = "'"
                reemplazar = " "
                #conn = psycopg2.connect(host="localhost", database="bakhanDB", user="postgres", password="root")
                #cur = conn.cursor()
                #kaid_student = "kaid_485871758161384306203631"

                today = time.strftime("%Y-%m-%dT%H:%M:%SZ", localtime())
                today = today.replace(":","%3A")
                yesterday = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(1),'%Y-%m-%d')
                #instituto = Institution.objects.get(id_institution= i)
                yesterday = inst.last_load

                inst.last_load = today
                inst.save()

                msg="hoy: " + today
                logging.debug(msg)
                msg="ayer: " + yesterday
                logging.debug(msg)
                #dates = yesterday+"&dt_end="+today
                dates = "2016-06-28T00%3A00%3A00Z&dt_end=2016-06-30T00%3A00%3A00Z"  



                #consulta = Class.objects.filter(id_institution_id=inst.id_institution).values("id_class")

                #for cons in consulta:
                    #print cons["id_class"]
                threads = []
                #students = Student.objects.filter(student_class__id_class_id=cons["id_class"])
                students = Student.objects.filter(id_institution_id=inst.id_institution)
                
                for i in students:
                    #print students[i].name
                    t = threading.Thread(target=threadPopulate,args=(i,dates,session))
                    threads.append(t)
                    t.start()

            except Exception as e:
                print e
