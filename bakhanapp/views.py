from django.shortcuts import render,HttpResponseRedirect,render_to_response
from .forms import loginForm
#from django.shortcuts import render_to_response

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

def inicio(request):
    return render_to_response('inicio.html',)