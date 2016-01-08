from django.shortcuts import render,HttpResponseRedirect,render_to_response
from django.template.context import RequestContext
from .forms import loginForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth

from .models import Class
from .models import Student
from .models import Student_Class
from .models import Student_Video
from .models import Video_Playing
from .models import Skill_Attempt

import datetime

import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser


def log(request):
    return render(request, 'log.html')

def rejected(request):
    return render(request, 'rejected.html')

@login_required()
def home(request):
    return render_to_response('home.html',)

@login_required()
def teacher(request):
    return render_to_response('teacher.html',)

def getTotalExerciseTime(kaid_s):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en toda su historia.
    query = Skill_Attempt.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query:
        time = time + register.time_taken
    return time

def getExerciseTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en ejercicios en un rango de fechas.
    query_set = Skill_Attempt.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query_set:
        if register.date>=t_begin and register.date<=t_end:
            time = time + register.time_taken
    return time

def getTotalVideoTime(kaid_s):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en toda su historia.
    query = Student_Video.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query:
        time = time + register.total_seconds_watched
    return time

def getVideoTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en un rango de fechas.
    query_set = Video_Playing.objects.filter(kaid_student=kaid_s)
    time = 0
    for register in query_set:
        if register.date>=t_begin and register.date<=t_end:
            time = time + register.total_seconds_watched
    return time

@login_required()
def getTeacherClasses(request):
    #Esta funcion entrega todos los cursos que tiene a cargo el profesor que se encuentra logueado en el sistema
    classes = Class.objects.filter(kaid_teacher='2')
    N = ['kinder','1ro basico','2do basico','3ro basico','4to basico','5to basico','6to basico','7mo basico','8vo basico','1ro medio','2do medio','3ro medio','4to medio']
    for i in range(len(classes)):
        classes[i].level = N[int(classes[i].level)] 
    return render_to_response('myClasses.html', {'classes': classes}, context_instance=RequestContext(request))
    
@login_required()
def getClassStudents(request, id_class):
    #Esta funcion entrega todos los estudiantes que pertenecen a un curso determinado
    #Select * from student where kaid_student in (Select kaid_student from student_class where id_class_id = id_class)
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))
    classroom = Class.objects.filter(id=id_class)
    return render_to_response('studentClass.html', {'students': students, 'classroom': classroom}, context_instance=RequestContext(request))


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
                                        <a role="button" aria-disabled="false" href="http://127.0.0.1:8000/home"  class="kui-button kui-button-submit kui-button-primary" style="width:100%;" data-reactid=".0.4.2">Listo</a>
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
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/access/rejected')

#funcion no utilizada por el momento, ya que se esta redirigiendo toda la autentificacion a K.A.
def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = loginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/inicio/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()

    return render(request, 'login.html', {'form': form})
    # return render_to_response('login.html')

