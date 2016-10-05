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

import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
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

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='logs/populatetree.log',
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

def update_char():
    cursor = connection.cursor()
    cursor.execute("update bakhanapp_chapter set name_spanish = replace(name_spanish, 'Á', 'Á') where name_spanish like '%Á%'")
    cursor.execute("update bakhanapp_chapter set name_spanish = replace(name_spanish, 'Á¡', 'á') where name_spanish like '%Á¡%'")
    cursor.execute("update bakhanapp_chapter set name_spanish = replace(name_spanish, 'Á©', 'é') where name_spanish like '%Á©%'")   
    cursor.execute("update bakhanapp_chapter set name_spanish = replace(name_spanish, 'Á­', 'í') where name_spanish like '%Á­%'")      
    cursor.execute("update bakhanapp_chapter set name_spanish = replace(name_spanish, 'Á³', 'ó') where name_spanish like '%Á³%'") 
    cursor.execute("update bakhanapp_chapter set name_spanish = replace(name_spanish, 'Á', '') where name_spanish like '%Á%'")  
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Á', 'Á') where name_spanish like '%Á%'")
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Á¡', 'á') where name_spanish like '%Á¡%'")
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Á©', 'é') where name_spanish like '%Á©%'")   
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Á­', 'í') where name_spanish like '%Á­%'")     
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Á³', 'ó') where name_spanish like '%Á³%'") 
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Áº', 'ú') where name_spanish like '%Áº%'") 
    cursor.execute("update bakhanapp_topic set name_spanish = replace(name_spanish, 'Á', '') where name_spanish like '%Á%'")  
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á', 'Á') where name_spanish like '%Á%'")
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á¡', 'á') where name_spanish like '%Á¡%'")
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á©', 'é') where name_spanish like '%Á©%'")   
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á­', 'í') where name_spanish like '%Á­%'")    
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Áº', '') where name_spanish like '%Áº%'")    
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á³', 'ó') where name_spanish like '%Á³%'") 
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Áº', 'ú') where name_spanish like '%Áº%'") 
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á', '') where name_spanish like '%Á%'")
    cursor.execute("update bakhanapp_subtopic set name_spanish = replace(name_spanish, 'Á±', 'ñ') where name_spanish like '%Á±%'")
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á', 'Á') where name_spanish like '%Á%'")
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á¡', 'á') where name_spanish like '%Á¡%'")
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á©', 'é') where name_spanish like '%Á©%'")   
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á­', 'í') where name_spanish like '%Á­%'")    
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Áº', '') where name_spanish like '%Áº%'")    
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á³', 'ó') where name_spanish like '%Á³%'") 
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Áº', 'ú') where name_spanish like '%Áº%'") 
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á', '') where name_spanish like '%Á%'")
    cursor.execute("update bakhanapp_skill set name_spanish = replace(name_spanish, 'Á±', 'ñ') where name_spanish like '%Á±%'")
    row = cursor.fetchone()
    return row


def poblar_topictree(session,buscar, reemplazar):
    topictree = get_api_resource2(session,"/api/v1/topictree",SERVER_URL2)
    source = unicode(topictree, 'ISO-8859-1')
    data = simplejson.loads(source)
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
    cant_chapters = len(data["children"][1]["children"])
    for i in range(0,cant_chapters):

        aux1 = (data["children"][1]["children"][i]["slug"])
        aux2 = (data["children"][1]["children"][i]["translated_title"])
        aux3 = (data["children"][1]["slug"])
        new_chapter = Chapter(id_chapter_name=aux1,name_spanish=aux2,id_subject_name_id=aux3, index=i)
        new_chapter.save()

        cant_topic = len(data["children"][1]["children"][i]["children"])
        
        for j in range(0,cant_topic):
       
            aux1 = data["children"][1]["children"][i]["children"][j]["slug"]
            aux2 = data["children"][1]["children"][i]["children"][j]["translated_title"]
            aux3 = data["children"][1]["children"][i]["slug"]
            new_topic = Topic(id_topic_name=aux1,name_spanish=aux2,id_chapter_name_id=aux3, index=j)
            new_topic.save()
          
            cant_subtopic = len(data["children"][1]["children"][i]["children"][j]["children"])
            for k in range(0,cant_subtopic):
           
                aux1 = data["children"][1]["children"][i]["children"][j]["children"][k]["slug"]
                aux2 = data["children"][1]["children"][i]["children"][j]["children"][k]["translated_title"]
                aux3 = data["children"][1]["children"][i]["children"][j]["slug"]
                new_subtopic = Subtopic(id_subtopic_name=aux1,name_spanish=aux2,id_topic_name_id=aux3, index=k)
                new_subtopic.save()
           
                videos_view = len(data["children"][1]["children"][i]["children"][j]["children"][k]["children"])

                for m in range(0,videos_view):
                    aux1 = data["children"][1]["children"][i]["children"][j]["children"][k]["children"][m]["id"]
                    aux2 = data["children"][1]["children"][i]["children"][j]["children"][k]["children"][m]["related_exercise_url"]
                    try:
                        aux3 = aux2[10:]
                        skrelated = Skill.objects.filter(name=aux3).values('id_skill_name')
                        new_video = Video(id_video_name=aux1, related_skill=skrelated[0]["id_skill_name"])
                        new_video.save()
                    except:
                        new_video = Video(id_video_name=aux1)
                        new_video.save()
                
                cant_videos = len(data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"])
                #print cant_videos
                
                for l in range(0,cant_videos):
                    #consulta = """UPDATE bakhanapp_video SET name_spanish = '"""+data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["children"][l]["translated_title"].replace(buscar,reemplazar)+"""' WHERE id_video_name = '"""+data_topictree["children"][1]["children"][i]["children"][j]["children"][k]["children"][l]["id"]+"""';"""
                    #cur.execute(consulta)
                    #conn.commit()
                  
                    if (data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["kind"]=="Exercise"):
                        aux1 = (data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])
                        aux2 = (data["children"][1]["children"][i]["children"][j]["children"][k]["translated_title"])
                        aux3 = (data["children"][1]["children"][i]["children"][j]["children"][k]["slug"])
                        new_skill = Skill(id_skill_name=aux1,name_spanish=aux2,name=aux3, index=l)
                        new_skill.save()
                        #print aux2

                        aux4 = (data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])
                        aux5 = (data["children"][1]["children"][i]["children"][j]["children"][k]["slug"])
                        try:
                            new_subtopic_skill = Subtopic_Skill(id_skill_name_id=aux4,id_subtopic_name_id=aux5)
                            new_subtopic_skill.save()
                        except:
                            pass
                        #id_subtopic_skills+=1
                    
                    if (data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["kind"]=="Video"):
                        aux1 = (data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])
                        aux2 = (data["children"][1]["children"][i]["children"][j]["children"][k]["translated_title"])
                        aux3 = (data["children"][1]["children"][i]["children"][j]["children"][k]["slug"])
                        videon = Video.objects.get(pk=aux1)
                        videon.name_spanish=aux2
                        videon.index=l
                        videon.save()
                        #new_video = Video(id_video_name=aux1,name_spanish=aux2, index=l)
                        #new_video.save()
               
                        aux4 = (data["children"][1]["children"][i]["children"][j]["children"][k]["slug"])
                        aux5 = (data["children"][1]["children"][i]["children"][j]["children"][k]["child_data"][l]["id"])
                        try:
                            new_subtopic_video = Subtopic_Video(id_subtopic_name_id=aux4,id_video_name_id=aux5)
                            new_subtopic_video.save()
                        except:
                            pass
                        #id_subtopic_videos+=1
        	     
                skills = get_api_resource2(session,"/api/v1/topic/"+data["children"][1]["children"][i]["children"][j]["children"][k]["slug"]+"/exercises",SERVER_URL2)
                source = unicode(skills, 'ISO-8859-1')
                data_skills = simplejson.loads(source)
                for p in range(len(data_skills)):
                    #logging.debug(data_skills[p]["translated_title"])
                    Skill.objects.filter(id_skill_name=data_skills[p]["content_id"]).update(name_spanish=data_skills[p]["translated_title"],name=data_skills[p]["name"])
                
                videos = get_api_resource2(session,"/api/v1/topic/"+data["children"][1]["children"][i]["children"][j]["children"][k]["slug"]+"/videos",SERVER_URL2)
                sourcevid = unicode(videos, 'ISO-8859-1')
                data_videos = simplejson.loads(sourcevid)
                for q in range(len(data_videos)):
                    #logging.debug(data_skills[p]["translated_title"])
                    Video.objects.filter(id_video_name=data_videos[q]["content_id"]).update(name_spanish=data_videos[q]["translated_title"])                    
                              

class Command(BaseCommand):
    help = 'Puebla la base de datos con al arbol'

    def handle(self, *args, **options):
        try:
            CONSUMER_KEY = 'AStAffVHzEtpSFJ3' #clave generada para don UTPs
            #CONSUMER_KEY = '8Bn3UyhPHamgCvGN' #Clave para LeonardoMunoz esc Alabama
            #keys = ['AStAffVHzEtpSFJ3','8Bn3UyhPHamgCvGN']
            CONSUMER_SECRET = 'UEQj2XKfGpFSMpNh' #clave generada para don UTPs
            #CONSUMER_SECRET  = '2zcpyDHnfTd5VWz9' #secret para LeonardoMunoz esc Alabama
            #secrets = ['UEQj2XKfGpFSMpNh','2zcpyDHnfTd5VWz9']
            passw='clave1234'
            identifier='utpbakhan'
            #passw='CONTRASENA'
            #identifier='LeonardoMunoz'
            #identifiers = ['utpbakhan','LeonardoMunoz']
            #passes = ['clave1234', 'CONTRASENA']

            #meter los parametros anteriores en alguna parte de la base de datos

            #institution = Institution.objects.all()
            session = run_tests(identifier,passw,CONSUMER_KEY,CONSUMER_SECRET)
            buscar = "'"
            reemplazar = " "
            Chapter.objects.all().update(index=None)
            Topic.objects.all().update(index=None)
            Subtopic.objects.all().update(index=None)
            Video.objects.all().update(index=None)
            Skill.objects.all().update(index=None)
            poblar_topictree(session,buscar,reemplazar)
            update_char()
        except Exception as e:
            print e
