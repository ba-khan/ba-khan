# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
from django.template.context import RequestContext
from .forms import loginForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
import urllib2
import cgi

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
import cgitb

def login(request):
    return render(request, 'login.html')

def rejected(request):
    return render(request, 'rejected.html')




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
    return render_to_response('aut.html',{'url': authorize_url,'call': callback_server}, context_instance=RequestContext(request))

def wait(request):
    callback_server = create_callback_server()

    callback_server.handle_request()
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    if get_api_resource(session,request):
        return HttpResponseRedirect("/inicio")
    else:
        return HttpResponseRedirect("/access/rejected/ %}")
    
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
    urllib2.urlopen(authorize_url)

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

