from django.shortcuts import render,HttpResponseRedirect,render_to_response
from .forms import loginForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth


#from django.shortcuts import render_to_response

import cgi
import rauth
import SimpleHTTPServer
import SocketServer
import time
import webbrowser


def log(request):
    return render(request, 'log.html')

def denegado(request):
    return render(request, 'denegado.html')

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

@login_required()
def inicio(request):
    return render_to_response('inicio.html',)




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
            self.wfile.write("<HEAD> <meta http-equiv='refresh' content='1; url=javascript:window.close();'> </HEAD> ")
            #webbrowser.open('http://www.google.cl')
            


        def log_request(self, code='-', size='-'):
            pass

    server = SocketServer.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server


# Make an authenticated API call using the given rauth session.
#/api/v1/user?userId=&username=javierperezferrada&email=

def get_api_resource(session):
    resource_url = '/api/v1/user?userId=&username=&email='

    url = SERVER_URL + resource_url
    split_url = url.split('?', 1)
    params = {}

    # Separate out the URL's parameters, if applicable.
    if len(split_url) == 2:
        url = split_url[0]
        params = cgi.parse_qs(split_url[1], keep_blank_values=False)

    start = time.time()
    response = session.get(url, params=params)
    end = time.time()
    json_response = response.json()
    email = json_response['email']
    username = json_response['username']
    kaid = json_response['kaid']
    if email == 'javierperezferrada@gmail.com':
        user = auth.authenticate(username=username, password=kaid)
        return True
    else:
        return False

def run_tests(request):
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
    webbrowser.open_new(authorize_url)

    callback_server.handle_request()
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
        params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    if get_api_resource(session):
        return HttpResponseRedirect('/inicio')
    else:
        return HttpResponseRedirect('/acceso/denegado')


