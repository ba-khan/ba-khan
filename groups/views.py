from django.shortcuts import render

# Create your views here.
def groups(request,id_class):
	return render(request, 'groups.html')