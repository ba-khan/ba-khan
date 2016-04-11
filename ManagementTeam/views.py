# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher

register = template.Library()
from configs import timeSleep

import json


@permission_required('bakhanapp.isAdmin', login_url="/inicio")
def getAdministrators(request):
    request.session.set_expiry(timeSleep)
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except:
        return render_to_response('administrators.html', context_instance=RequestContext(request))
    administrators = Administrator.objects.filter(id_institution=teacher.id_institution_id).order_by('name')
    #print administrators
    return render_to_response('administrators.html', {'administrators': administrators}, context_instance=RequestContext(request))

@permission_required('bakhanapp.isAdmin', login_url="/inicio")
def saveAdministrator(request):
    request.session.set_expiry(timeSleep)
    user = Teacher.objects.get(email=request.user.email) #el usuario que está logueado
    if request.is_ajax():
        if request.method == 'POST':
            json_str = json.loads(request.body)
            try:
                admin = Administrator.objects.get(kaid_administrator=json_str["adminName"])

                if (json_str["adminPhone"]):
                    admin.phone=json_str["adminPhone"]
                else:
                    admin.phone=None
                if (json_str["adminEmail"]):
                    admin.email=json_str["adminEmail"]
                else:
                    admin.email=""
                admin.id_institution_id = user.id_institution_id
                admin.save()
                return HttpResponse("Cambios guardados correctamente")
            except:
                return HttpResponse("Error al guardar")


    return HttpResponse("Error")

@permission_required('bakhanapp.isAdmin', login_url="/inicio")
def deleteAdministrator(request):
    request.session.set_expiry(timeSleep)
    if request.is_ajax():
        if request.method == 'POST':
            json_str = json.loads(request.body)
            admin = Administrator.objects.get(kaid_administrator=json_str["adminName"])
            admin.delete()
            return HttpResponse("Administrador eliminado correctamente")
    return HttpResponse("Error al eliminar")

@permission_required('bakhanapp.isAdmin', login_url="/inicio")
def newAdministrator(request):
    request.session.set_expiry(timeSleep)
    user = Teacher.objects.get(email=request.user.email)
    if request.method == 'POST':
        args = request.POST
        try:
            administrator = Administrator.objects.create(kaid_administrator=args['name'],
                name=args['name'],
                email=args['email'],
                id_institution_id=user.id_institution_id,
                phone=args['phone'])
            return HttpResponse("Administrador guardado correctamente")
        except:
            return HttpResponse("Error al guardar")
    return HttpResponse("Error al guardar")