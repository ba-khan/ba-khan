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
                    filename='populate\management\commands\populate.log',
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


def coach_students(session, id_institution): #ver los estudiantes que tienen como coach a cierto usuario. no entrega info de cursos
    llamada = "/api/v1/user/students"
    jason = get_api_resource2(session,llamada,SERVER_URL2)
    source = unicode(jason, 'ISO-8859-1')
    data = simplejson.loads(source)
    #with open('data.txt', 'w') as outfile:
    #    json.dump(data, outfile)
    logging.debug(len(data))
    for j in range(len(data)):
        if data[j]["email"]!=None:
            email = data[j]["email"]
        else:
            email = data[j]["username"]
        try:
            if data[j]["username"]=="":
                new_student = Student(kaid_student=data[j]["kaid"],name=data[j]["nickname"],email=email,points=data[j]["points"],phone=0, id_institution_id=id_institution)
                new_student.save()
            else:
                new_student = Student(kaid_student=data[j]["kaid"],name=data[j]["username"],email=email,points=data[j]["points"],phone=0, id_institution_id=id_institution)
                new_student.save()
        except Exception as e:
            print e
            #logging.debug("error con estudiante "+data[j]["username"])
            #logging.debug(data[j]["username"])

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
 


class Command(BaseCommand):
    help = 'Puebla la base de datos con los estudiantes'

    def handle(self, *args, **options):
        #CONSUMER_KEY = 'AStAffVHzEtpSFJ3' #clave generada para don UTPs
        #CONSUMER_KEY = '8Bn3UyhPHamgCvGN' #Clave para LeonardoMunoz esc Alabama
        #keys = ['AStAffVHzEtpSFJ3','8Bn3UyhPHamgCvGN']
        #CONSUMER_SECRET = 'UEQj2XKfGpFSMpNh' #clave generada para don UTPs
        #CONSUMER_SECRET  = '2zcpyDHnfTd5VWz9' #secret para LeonardoMunoz esc Alabama
        #secrets = ['UEQj2XKfGpFSMpNh','2zcpyDHnfTd5VWz9']
        #passw='clave1234'
        #identifier='utpbakhan'
        #passw='CONTRASENA'
        #identifier='LeonardoMunoz'
        #identifiers = ['utpbakhan','LeonardoMunoz']
        #passes = ['clave1234', 'CONTRASENA']

        #meter los parametros anteriores en alguna parte de la base de datos

        institution = Institution.objects.all()

        for inst in institution:
            keys = inst.key
            secrets = inst.secret
            identifiers = inst.identifier
            passes = inst.password

            print identifiers
            print passes
            print keys
            print secrets

            try:
                session = run_tests(identifiers,passes,keys,secrets)

                coach_students(session, inst.id_institution)

            except Exception as e:
                print e
                # cambio de clave en institution 4, no entra a bd
