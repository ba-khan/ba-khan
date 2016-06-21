# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
#from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect,HttpResponse
#from django.template.context import RequestContext
#from .forms import loginForm
#from django.contrib.auth import  login,authenticate,logout
#from django.contrib.auth.decorators import login_required,permission_required
#from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.models import User
#from django.contrib import auth
#from django.db.models import Count

#from django import template
#from bakhanapp.models import Assesment_Skill
#register = template.Library()

#from bakhanapp.models import Class
#from bakhanapp.models import Teacher
#from bakhanapp.models import Skill
#from bakhanapp.models import Skill_Progress
#from bakhanapp.models import Student
#from bakhanapp.models import Student_Class
#from bakhanapp.models import Student_Video
#from bakhanapp.models import Student_Skill
#from bakhanapp.models import Video
#from bakhanapp.models import Video_Playing
#from bakhanapp.models import Skill_Attempt
#from bakhanapp.models import Assesment_Skill
#from bakhanapp.models import Class_Subject
#from bakhanapp.models import Assesment
#from bakhanapp.models import Assesment_Config
#from bakhanapp.models import Subtopic_Skill
#from bakhanapp.models import Subtopic_Video
#from bakhanapp.models import Grade,Skill
#from bakhanapp.models import Student_Skill
#from bakhanapp.models import Skill_Progress
#from bakhanapp.models import Subject
#from bakhanapp.models import Chapter
#from bakhanapp.models import Topic
#from bakhanapp.models import Subtopic
#from bakhanapp.models import Subtopic_Skill

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
#from django.core import serializers
#from django.db import connection

import random
from random import randint

import time

from websocket_server import WebsocketServer


import threading


CONSUMER_KEY = 'uMCFkRw7QSJ3WkLs' #clave generada para don UTPs
CONSUMER_SECRET = 'tH8vhEBstXe6jFyG' #clave generada para don UTPs
    
CALLBACK_BASE = '146.83.216.177' #IP Servidor
#CALLBACK_BASE = "127.0.0.1"
#CALLBACK_BASE = "192.168.1.139"
SERVER_URL = 'http://www.khanacademy.org'
SERVER_URL2 = 'http://es.khanacademy.org'
    
DEFAULT_API_RESOURCE = '/api/v1/playlists'
#VERIFIER = None

VERIFIERS_ARRAY = {}
SERVICES_ARRAY = {}
REQUEST_TOKENS_ARRAY = {}
SECRET_REQUEST_TOKEN_ARRAY = {}
    

# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):
            #global VERIFIER
            global VERIFIERS_ARRAY
            global SERVICES_ARRAY
            global server
            
            #print self.path
            params = cgi.parse_qs(self.path.split('?', 1)[1],
                keep_blank_values=False)
            id_client = params["id_client"][0]

            
            VERIFIERS_ARRAY[id_client] = params['oauth_verifier'][0]
            #print id_client
            #print VERIFIERS_ARRAY[id_client]
            
            
            
            for client in server.clients:
                print "cliente"
                if client['id'] == int(id_client):
                    # 4. Get an access token.
                    service = SERVICES_ARRAY[id_client]
                    request_token = REQUEST_TOKENS_ARRAY[id_client]
                    secret_request_token = SECRET_REQUEST_TOKEN_ARRAY[id_client]
                    session = service.get_auth_session(request_token, secret_request_token,
                        params={'oauth_verifier': VERIFIERS_ARRAY[id_client]})

                    
                    # 5. Get user data from the API Khan request
                    login_data = get_api_resource(session)

                    # 6. Send Khan user data to the client
                    server.send_message(client, login_data)
                    break


            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("""<html lang="es">
                            <head>
                                <title>BA-Khan</title>                                                               
                                <script>
                                    myWindow = window.open("", "_self", "myWindow", "width=200, height=100")
                                    function closeWin() {
                                        myWindow.close();
                                    }
                                </script>                          
                            </head>
                              <body>                             
                                <script>closeWin()</script>                       
                              </body>                           
                            </html>""")

            

        def log_request(self, code='-', size='-'):
            pass
    server = SocketServer.TCPServer((CALLBACK_BASE, 5432), CallbackHandler)
    #server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler) #Ocupar puerto 0 para puerto random (fallo de seguridad)
    return server

callback_server = create_callback_server()

#callback_server.handle_request()
#callback_server.serve_forever()

# Make an authenticated API call using the given rauth session.
#/api/v1/user?userId=&username=javierperezferrada&email=

def get_api_resource(session):#,request):
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
    #print json_response
    email = json_response['email']  
    username = json_response['nickname']
    kaid = json_response['kaid']
    avatar_url = json_response['avatar_url']
    login_data={"login":{"username":username,"email":email,"kaid":kaid,"avatar_url":avatar_url}}
    json_data = json.dumps(login_data)
    return json_data


def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    #server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    global callback_server
    #if len(message) > 200:
    #    message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))
    if (message=="login"):
        id_client=str(client['id'])
        # Create an OAuth1Service using rauth.
        SERVICES_ARRAY[id_client] = rauth.OAuth1Service(
               name=id_client,
               consumer_key=CONSUMER_KEY,
               consumer_secret=CONSUMER_SECRET,
               request_token_url=SERVER_URL + '/api/auth2/request_token',
               access_token_url=SERVER_URL + '/api/auth2/access_token',
               authorize_url=SERVER_URL + '/api/auth2/authorize',
               base_url=SERVER_URL + '/api/auth2')

        #callback_server = create_callback_server()
        
        # 1. Get a request token.
        #request_token, secret_request_token = service.get_request_token(
        #    params={'oauth_callback': 'http://%s:%d/' %
        #        (CALLBACK_BASE, callback_server.server_address[1])})

        request_token, secret_request_token = SERVICES_ARRAY[id_client].get_request_token(
            params={'oauth_callback': 'http://%s:%d?id_client=%s' %
                (CALLBACK_BASE, callback_server.server_address[1],id_client)})
        REQUEST_TOKENS_ARRAY[id_client]=request_token
        SECRET_REQUEST_TOKEN_ARRAY[id_client]=secret_request_token
        # 2. Authorize your request token.
        authorize_url = SERVICES_ARRAY[id_client].get_authorize_url(request_token)
        #server.send_message_to_all("url:"+authorize_url)
        #print authorize_url
        
        # 3. Send Authorize url
        url_data={"url":authorize_url}
        json_data = json.dumps(url_data)
        server.send_message(client,json_data)
        
        #callback_server.handle_request()
        #callback_server.server_close()

        # 4. Get an access token.
        #session = service.get_auth_session(request_token, secret_request_token,
        #    params={'oauth_verifier': VERIFIERS_ARRAY[id_client]})

        
        # 5. Get user data from the API Khan request
        #login_data = get_api_resource(session)

        # 6. Send Khan user data to the client
        #server.send_message(client, login_data)
    
def runWebsocketServer():
    global server
    server.run_forever()
def runAuthServer():
    global callback_server
    callback_server.serve_forever()





#PORT=9001
PORT=8080
SERVERHOST= "0.0.0.0"
server = WebsocketServer(PORT, SERVERHOST)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

#server.run_forever()
#callback_server.serve_forever()

t1 = threading.Thread(target=runWebsocketServer, args=[])
t2 = threading.Thread(target=runAuthServer, args=[])
t1.start()
t2.start()

