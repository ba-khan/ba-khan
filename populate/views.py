from django.shortcuts import render
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext

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
import requests

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

CONSUMER_KEY = 'AStAffVHzEtpSFJ3' #clave generada para don UTPs
CONSUMER_SECRET = 'UEQj2XKfGpFSMpNh' #clave generada para don UTPs
    
CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'https://www.khanacademy.org'
SERVER_URL2 = 'https://es.khanacademy.org'
    
DEFAULT_API_RESOURCE = '/api/v1/playlists'
VERIFIER = None
    

# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            global VERIFIER
            print "kk"
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
        params={'oauth_callback': SERVER_URL +'/api/auth/default_callback'}) #'http://%s:%d/' %
            #(CALLBACK_BASE, callback_server.server_address[1])})

    print request_token
    print secret_request_token
    passw='clave1234'
    noClickParams = {'oauth_token':request_token, 'identifier':'utpbakhan', 'password':passw}
    
    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)
    print authorize_url

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
    print r.url
    
    print r.text
    print r.status_code
    #print r
    access_url = urlparse.parse_qs(urlparse.urlparse(r.url).query)
    oauth_verifier_raw = access_url["oauth_verifier"][0]
    oauth_verifier = oauth_verifier_raw.encode('ascii','ignore')
    print oauth_verifier
    #callback_server.handle_request() #Esto esperaba el click de aceptar
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': oauth_verifier})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    #print
    #while(True):
    #    get_api_resource(session)
    print session
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
                        print(chapter.id_chapter_name+" - "+topic.id_topic_name+" + "+subtopic.id_subtopic_name+" * "+skill.name_spanish)
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

def coach_students(session):
    llamada = "/api/v1/user/students"
    jason = get_api_resource2(session,llamada,SERVER_URL2)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
    for j in range(len(data)):
        print data[j]["username"]
            
@login_required()
def poblarBD(session):
    session = run_tests()
    print "logueadoooo"
    #jason = get_api_resource2(session,"/api/v1/exercises",SERVER_URL2)
    #source = unicode(jason, 'ISO-8859-1')
    #data = simplejson.loads(source)
    buscar = "'"
    reemplazar = " "
    #conn = psycopg2.connect(host="localhost", database="bakhanDB", user="postgres", password="root")
    #cur = conn.cursor()
    #kaid_student = "kaid_485871758161384306203631"
    dates = "2014-01-01T00%3A00%3A00Z&dt_end=2017-01-01T00%3A00%3A00Z"  
    
    '''
    student_skills = Student_Skill.objects.all()
    student_skills.delete()
    
    skill_attempts = Skill_Attempt.objects.all()
    skill_attempts.delete()
    
    skill_progress = Skill_Progress.objects.all()
    skill_progress.delete()

    student_videos = Student_Video.objects.all()
    student_videos.delete()

    video_playings = Video_Playing.objects.all()
    video_playings.delete()
    '''
    #coach_students(session)
    
    #'''
    #students = Student.objects.all()
    #for i in range(len(students)):
        #print i
        #poblar_student_skill(students[i], dates, session)
        #poblar_skill_attempts(students[i], dates, session)
        #poblar_skill_progress(students[i], dates, session)
        #poblar_student_video(students[i], dates, session)
        #poblar_video_playing(students[i], dates, session)
    #'''