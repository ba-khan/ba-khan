from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect
from django.template.context import RequestContext
from .forms import loginForm
from .forms import AssesmentConfigForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth

from django import template
from bakhanapp.models import Assesment_Skill
register = template.Library()

from .models import Class
from .models import Student
from .models import Student_Class
from .models import Student_Video
from .models import Video_Playing
from .models import Skill_Attempt
from .models import Assesment_Skill
from .models import Skill_Progress
from .models import Class_Subject
from .models import Assesment
from .models import Assesment_Config
from .models import Grade

import datetime

import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser


def login(request):
    return render(request, 'login.html')

def rejected(request):
    return render(request, 'rejected.html')

@login_required()
def home(request):
    return render_to_response('home.html',)

@login_required()
def teacher(request):
    return render_to_response('teacher.html',)

def deleteAssesmentConfig(request,id_assesment_config):
    Assesment_Config.objects.get(id_assesment_config=id_assesment_config).delete()
    return redirect('configuraciones')

def newAssesmentConfig(request):
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher='2')
    if request.method == 'POST':
        form = AssesmentConfigForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('configuraciones')
    else:
        form = AssesmentConfigForm(request.POST, request.FILES)
    return render_to_response('newAssesmentConfig.html',{'form': form,'assesment_configs': assesment_configs}, context_instance=RequestContext(request))

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
        last_level = Skill_Progress.objects.filter(id_skill_name=skill,date__gte = t_begin,date__lte = t_end).latest('date').values('to_level')
        points = points + scores[last_level]
    points = points / len(configured_skills)
    return points
        
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
    grades = Assesment.objects.filter(id_class=id_class).values('name', 'grade__kaid_student','grade__grade')
    return grades

@login_required()
def getClassStudents(request, id_class):
    #Esta funcion entrega todos los estudiantes que pertenecen a un curso determinado
    #Select * from student where kaid_student in (Select kaid_student from student_class where id_class_id = id_class)
    classes = Class.objects.filter(id_class__in=Class_Subject.objects.filter(kaid_teacher='2').values('id_class'))

    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
    evaluations_class = Assesment.objects.filter(id_class=id_class)#.values('id_assesment')
    for student in students:
        student.t_exercise= getTotalExerciseTime(student.kaid_student)
        student.t_video= getTotalVideoTime(student.kaid_student)
        student.correct= getTotalExerciseCorrect(student.kaid_student)
        student.incorrect= getTotalExerciseIncorrect(student.kaid_student)
    classroom = Class.objects.filter(id_class=id_class)
    grades = getClassGrades(request,id_class)
    return render_to_response('studentClass.html', {'students': students, 'classroom': classroom,'classes': classes,'grades':grades}, context_instance=RequestContext(request))


CONSUMER_KEY = 'uhPpmjAMXqKwVYyJ' #clave generada para Alonsoccer
CONSUMER_SECRET = 'cY8yWWjaKBVPUQfd' #clave generada para Alonsoccer
    
CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'http://www.khanacademy.org'
    
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

