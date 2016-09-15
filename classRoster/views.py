## @package classRoster
## This Python file uses the following encoding: utf-8

from django.shortcuts import render

from django.shortcuts import render, HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher
from bakhanapp.models import Class
from bakhanapp.models import Student
from bakhanapp.models import Student_Class
from bakhanapp.models import Class_Subject
from bakhanapp.models import Institution

register = template.Library()
from configs import timeSleep
import logging
import datetime
import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser
import psycopg2
import requests
from collections import OrderedDict
import json
import simplejson
import sys
from pprint import pprint
import codecs
from lib2to3.fixer_util import String
from django.core import serializers
from django.db import connection
import xlrd

import random

import urlparse

CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'https://www.khanacademy.org'
SERVER_URL2 = 'https://es.khanacademy.org'
    
DEFAULT_API_RESOURCE = '/api/v1/playlists'
VERIFIER = None

##
## @brief      Function to do the login
##
## @param      identifier       The identifier
## @param      passw            The passw
## @param      CONSUMER_KEY     The consumer key
## @param      CONSUMER_SECRET  The consumer secret
##
## @return     Session
##
def run_tests(identifier,passw, CONSUMER_KEY, CONSUMER_SECRET):
    global SERVER_URL
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
        params={'oauth_callback': SERVER_URL +'/api/auth/default_callback'}) 
    
    noClickParams = {'oauth_token':request_token, 'identifier':identifier, 'password':passw}
    
    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)

    post_url=SERVER_URL +'/api/auth2/authorize'

    r = requests.post(post_url, data=noClickParams)

    access_url = urlparse.parse_qs(urlparse.urlparse(r.url).query)
    oauth_verifier_raw = access_url["oauth_verifier"][0]
    oauth_verifier = oauth_verifier_raw.encode('ascii','ignore')
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': oauth_verifier})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    return session


##
## @brief      Gets the api resource 2.
##
## @param      sessions  The sessions
## @param      llamada   The llamada
## @param      server    The server
##
## @return     The api resource 2.
##
def get_api_resource2(sessions,llamada,server):
    url = server + llamada
    split_url = url.split('?', 1)
    params = {}
    if len(split_url) == 2:
        url = split_url[0]
        params = cgi.parse_qs(split_url[1], keep_blank_values=False)
    start = time.time()
    responses = sessions.get(url, params=params)
    encoded_response=responses.text
    end = time.time()
    return encoded_response


##
## @brief      Creates a callback server.
##
## @return     Server
##
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
                ' you can close this window.')
            #webbrowser.open('http://www.google.cl')

        def log_request(self, code='-', size='-'):
            pass

    server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server


##
## @brief      Search a teacher
##
## @param      session     The session
## @param      newTeacher  The new teacher
##
## @return     teacher's data
##
def searchTeacher(session,newTeacher):
    llamada = "/api/v1/user?username="+newTeacher
    jason = get_api_resource2(session,llamada,SERVER_URL)
    data = simplejson.loads(jason)
    return data


##
## @brief      Gets the roster.
##
## @param      request  The request
##
## @return     The roster.
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def getRoster(request):
    request.session.set_expiry(timeSleep)
    students = []
    teachers = Teacher.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id'))

    institution = Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')
    students = Student.objects.filter(id_institution_id=institution).order_by('name')

    classes = Class.objects.filter(id_institution_id=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id')).order_by('level','letter')
    #for clas in classes:
        #a = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=clas.id_class).values('kaid_student_id'))
        #for b in a:
            #students.append(b)
    if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
        isTeacher = True
    else:
        isTeacher = False
    return render_to_response('classRoster.html', {'students':students, 'teachers':teachers, 'classes':classes,'isTeacher':isTeacher}, context_instance=RequestContext(request))


##
## @brief      { function_description }
##
## @param      request  The request
##
## @return     { description_of_the_return_value }
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def newTeacherClass(request):
    if request.method == 'POST':
        newTeacher = request.POST["username"]

        inst = Institution.objects.get(id_institution=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id'))

        keys = inst.key
        secrets = inst.secret
        identifiers = inst.identifier
        passes = inst.password

        sessions = run_tests(identifiers,passes,keys,secrets)
        data = searchTeacher(sessions,newTeacher)

        #if data["is_child_account"]==False and data["nickname"]==newTeacher: FALTA UNA VALIDACION MAS
        if data["username"]==newTeacher:
            try:
                teacher = Teacher.objects.get(kaid_teacher=data["kaid"])
                return HttpResponse("Ya existe el profesor.")
            except:
                if data["email"]==None:
                    email=""
                else:
                    email = data["email"]
                teacher = Teacher.objects.create(kaid_teacher=data["kaid"], name=data["username"], email=email, id_institution_id=inst.id_institution)
                return HttpResponse("Nuevo profesor creado.")
        else:
            return HttpResponse("No se encuentra el profesor.")


##
## @brief      { function_description }
##
## @param      request  The request
##
## @return     { description_of_the_return_value }
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def newClass(request):
    if request.method == 'POST':
        newClass = request.POST
        level = int(newClass["level"])
        letter = newClass["letter"]
        year = newClass["year"]
        additional = newClass["additional"]
        if additional=="":
            additional = None
        #teacher = newClass["teacher"]
        teacher = Teacher.objects.get(name=newClass["teacher"])
        kaid_teacher = teacher.kaid_teacher
        students = newClass.getlist("students[]")

        inst = Institution.objects.get(id_institution=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id'))
        id_institution = int(inst.id_institution)
        try:
            curso = Class.objects.get(level=level,letter=letter,id_institution_id=id_institution, additional=additional)
            return HttpResponse("Ya existe el curso")
        except:
            curso = Class.objects.create(level=level, letter=letter, id_institution_id=id_institution, year=year, additional=additional)
            id_curso = int(curso.id_class)
            class_subject = Class_Subject.objects.create(id_class_id=id_curso, id_subject_name_id='math', kaid_teacher_id=kaid_teacher)
            for student in students:
                aux = Student.objects.get(name=student)
                student_class = Student_Class.objects.create(id_class_id=id_curso, kaid_student_id=aux.kaid_student)
            return HttpResponse("Nuevo curso creado")


##
## @brief      { function_description }
##
## @param      request  The request
##
## @return     { description_of_the_return_value }
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def viewClass(request):
    if request.method == 'POST':
        classObj = request.POST
        clas = Class.objects.get(id_class=classObj['idClass'])
        students = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=classObj['idClass']).values('kaid_student_id')).order_by('name')
        teacher = Teacher.objects.filter(kaid_teacher=Class_Subject.objects.filter(id_class_id=classObj['idClass']).values('kaid_teacher_id'))
        data_teacher = serializers.serialize('json', teacher)
        struct_teacher = json.loads(data_teacher)

        data_students = serializers.serialize('json', students)
        struct_students = json.loads(data_students)
        struct_students.append(struct_teacher)
        students = json.dumps(struct_students)

        return HttpResponse(students)


##
## @brief      { function_description }
##
## @param      request  The request
##
## @return     { description_of_the_return_value }
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def editClass(request):
    if request.method == 'POST':
        newClass = request.POST
        level = int(newClass["level"])
        letter = newClass["letter"]
        year = int(newClass["year"])
        additional = newClass["additional"]
        id_class = newClass["idClass"]
        if additional=="":
            additional = None
        teacher = Teacher.objects.get(name=newClass["teacher"])
        kaid_teacher = teacher.kaid_teacher
        students = newClass.getlist("students[]")

        inst = Institution.objects.get(id_institution=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id'))
        id_institution = int(inst.id_institution)
        try:

            curso = Class.objects.get(id_class=id_class)
            #level=level,letter=letter,id_institution_id=id_institution, year=year, additional=additional
            curso.level=level
            curso.letter=letter
            curso.id_institution_id=id_institution
            curso.year=year
            curso.additional=additional
            curso.save()
            #id_class=curso.id_class
            class_subject = Class_Subject.objects.get(id_class_id=id_class)
            class_subject.kaid_teacher_id = kaid_teacher
            class_subject.save() #GUARDA EL PROFESOR

            student_class = Student_Class.objects.filter(id_class_id=id_class)
            student_class.delete()

            for student in students:
                aux = Student.objects.get(name=student)
                student_class = Student_Class.objects.create(id_class_id=id_class, kaid_student_id=aux.kaid_student)

            return HttpResponse("Curso editado correctamente")
        except:
            return HttpResponse("Error al editar")


##
## @brief      Uploads an excel.
##
## @param      request  The request
##
## @return     { description_of_the_return_value }
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def uploadExcel(request):
    if request.method == 'POST':
        try:
            excel = request.FILES
            wb = xlrd.open_workbook(filename=None, file_contents=excel['file-0'].read())
            sh = wb.sheet_by_index(0)
        except:
            return HttpResponse(json.dumps("False"))
        # List to hold dictionaries
        students_list = []
        class_list = []
        name_class = []
        class_splited = []
        clas = OrderedDict()
        # Iterate through each row in worksheet and fetch values into dict
        for rownum in range(1, sh.nrows):
            row_values = sh.row_values(rownum)
            student = OrderedDict()
            try:
                student['name'] = row_values[0]
                student['points'] = int(row_values[11])
                student['class'] = row_values[12]
                student['kaid'] = row_values[13][28:]

                aux = row_values[12]
            except:
                return HttpResponse(json.dumps("False"))
            aux = aux.split(', ')
            #print len(aux2)
            for i in range(0,len(aux)):
                j = aux[i]
                if j in name_class:
                    pass
                else:
                    name_class.append(j)
                    clase = splitClass(aux[i])
                    class_splited.append(clase)
                if j in clas:
                    clas[j].append(student)
                else:
                    clas[j] = []
                    clas[j].append(student)
                

        # Serialize the list of dicts to JSON
        class_list.append(clas)
        class_list.append(name_class)
        class_list.append(class_splited)

        j = json.dumps(class_list)

        return HttpResponse(j)


##
## @brief      Saves an excel class.
##
## @param      request  The request
##
## @return     { description_of_the_return_value }
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def saveExcelClass(request):
    if request.method == 'POST':
        newClass = request.POST
        level = int(newClass['excelClassJson[level]'])
        letter = newClass["excelClassJson[letter]"]
        year = newClass["excelClassJson[year]"]
        additional = newClass["excelClassJson[additional]"]
        if additional=="":
            additional = None
        #teacher = newClass["teacher"]
        teacher = Teacher.objects.get(name=newClass["excelClassJson[teacher]"])
        kaid_teacher = teacher.kaid_teacher
        students = newClass.getlist("excelClassJson[students][]")
        kaid = newClass.getlist("excelClassJson[kaid][]")

        inst = Institution.objects.get(id_institution=Teacher.objects.filter(kaid_teacher=request.user.user_profile.kaid).values('id_institution_id'))
        id_institution = int(inst.id_institution)
        #print "antes del for"
        for student in students:
            estudiante= student.encode('utf-8', errors='replace')
            indice = students.index(student)
            #print estudiante
            #print indice
            #print kaid[indice]
            try:
                aux = Student.objects.filter(nickname=student)
                if not aux:
                    newStudent=Student(kaid_student=kaid[indice], name=estudiante, nickname=estudiante, id_institution_id=id_institution, new_student=True)
                    newStudent.save()
                else:
                    continue
                    #print "else"
            except Exception as e:
                print e
                #if e=="Student matching query does not exist.":
                #    print "entro al try"
                #    newStudent=Student(kaid=kaid[indice], name=estudiante, nickname=estudiante, id_institution_id=id_institution)
                #    print "new student ok"
                #    newStudent.save()
                #    print "guardo newstudent"
                #    return HttpResponse("Estudiantes nuevos creados")

            #if aux.id_institution_id!=id_institution:
            #    return HttpResponse("Estudiantes no corresponden a esta institución")

        #curso = Class.objects.get(level=level,letter=letter,id_institution_id=id_institution, additional=additional, year=year)
        #print curso.id_class
        #student_class = Student_Class.objects.filter(id_class_id=curso.id_class)
        #print len(students)
        #print len(student_class)
        try:
            curso = Class.objects.get(level=level,letter=letter,id_institution_id=id_institution, additional=additional, year=year)
            student_class = Student_Class.objects.filter(id_class_id=curso.id_class)
            #print student_class
            #print len(students)
            #print len(student_class)
            try:
                if len(students)!=len(student_class):
                    #print "try"
                    student_class.delete()
                    #print "delete"
                    for k in kaid:
                        try:
                            aux = Student.objects.get(kaid_student=k)
                            if not aux:
                                aux = Student.objects.get(kaid_student=k)
                                student_class = Student_Class.objects.create(id_class_id=curso.id_class, kaid_student_id=aux.kaid_student)
                            else:
                                student_class = Student_Class.objects.create(id_class_id=curso.id_class, kaid_student_id=aux.kaid_student)
                        except Exception as e:
                            print e
                    '''
                    for student in students:
                        estudiante= student.encode('utf-8', errors='replace')
                        print estudiante
                        try:
                            aux = Student.objects.get(name=estudiante)
                            if not aux:
                                aux = Student.objects.get(nickname=estudiante)
                                student_class = Student_Class.objects.create(id_class_id=curso.id_class, kaid_student_id=aux.kaid_student)
                            else:
                                student_class = Student_Class.objects.create(id_class_id=curso.id_class, kaid_student_id=aux.kaid_student)
                        except:
                            continue
                    '''
                    return HttpResponse("Curso editado correctamente.")
                else:
                    return HttpResponse("Ya existe el curso.")
            except Exception as e:
                print e
        except:
            curso = Class.objects.create(level=level, letter=letter, id_institution_id=id_institution, year=year, additional=additional)
            id_curso = int(curso.id_class)
            class_subject = Class_Subject.objects.create(id_class_id=id_curso, id_subject_name_id='math', kaid_teacher_id=kaid_teacher)
            for k in kaid:
                try:
                    aux = Student.objects.get(kaid_student=k)
                    if not aux:
                        aux = Student.objects.get(kaid_student=k)
                        student_class = Student_Class.objects.create(id_class_id=curso.id_class, kaid_student_id=aux.kaid_student)
                    else:
                        student_class = Student_Class.objects.create(id_class_id=curso.id_class, kaid_student_id=aux.kaid_student)
                except Exception as e:
                    print e
                    '''
            for student in students:
                try:
                    aux = Student.objects.get(name=student)
                    if not aux:
                        aux = Student.objects.get(nickname=student)
                        student_class = Student_Class.objects.create(id_class_id=id_curso, kaid_student_id=aux.kaid_student)
                    else:
                        student_class = Student_Class.objects.create(id_class_id=id_curso, kaid_student_id=aux.kaid_student)
                except:
                    continue
            return HttpResponse("Nuevo curso creado")
                    '''
        
        return HttpResponse("Curso creado correctamente")


##
## @brief      Splits a class.
##
## @param      className  The class name
##
## @return     Splited class
##
def splitClass(className):
    cur = className.split('-')
    curso = cur[0]
    longnivel = len(curso)
    if longnivel!=3:
        nivel = 0
        letra = "#"
        adicional = curso
        try:
            anio = cur[1]
        except:
            anio = 0
    else:
        adicional = ""
        try:
            nivel = int(curso[0])
            letra = curso[2]
            anio = cur[1]
            if curso[1]=='M':
                nivel = nivel +8
            else:
                if curso[1]!='B':
                    nivel = 0
        except:
            nivel = 0
            letra = "#"
            anio=0
    #print nivel, letra, anio, adicional

    clase = OrderedDict()
    clase["nivel"]=nivel
    clase["letra"]=letra
    clase["anio"]=anio
    clase["adicional"]=adicional
    return clase