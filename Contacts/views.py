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

from django import template
from bakhanapp.models import Student
from bakhanapp.models import Student_Class
from bakhanapp.models import Tutor

register = template.Library()

import json

@login_required()
def getContacts(request, id_class):
    #request.session.set_expiry(timeSleep)
    students=Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student')).order_by('name')
    tutors=Tutor.objects.filter(kaid_student_child__in=students)
    datas = []
    for student in students:
        data = []
        data.append(student)
        try:
            tutor = Tutor.objects.get(kaid_student_child=student.kaid_student)
            data.append(tutor)
        except:
            tutor = Tutor.objects.create(name="", kaid_student_child_id=student.kaid_student)
            data.append(tutor)
        datas.append(data)
    return render_to_response('contacts.html', {'datas':datas, 'id_class':id_class}, context_instance=RequestContext(request))

@login_required()
def saveContact(request, id_class):
    if request.is_ajax():
        if request.method == 'POST':
            
            json_str = json.loads(request.body)
            student = Student.objects.get(name=json_str["studentName"])
            if(json_str["studentPhone"]):
                student.phone=json_str["studentPhone"]
            else:
                student.phone=None
            if(json_str["studentEmail"]):
                student.email=json_str["studentEmail"]
            else:
                student.email=""
                
            try:
                tutor = Tutor.objects.get(kaid_student_child_id=student.kaid_student)
                print "existe tutor"
                if (json_str["tutorName"]):
                    tutor.name=json_str["tutorName"]
                if (json_str["tutorPhone"]):
                    tutor.phone=json_str["tutorPhone"]
                else:
                    tutor.phone=None
                if (json_str["tutorEmail"]):
                    tutor.email=json_str["tutorEmail"]
                else:
                    tutor.email=""
                tutor.kaid_student_child_id= student.kaid_student
                tutor.save()
            except:
                return HttpResponse("Error al guardar")
            
            student.save()
            return HttpResponse("Cambios guardados correctamente")
        
        
        
    return HttpResponse("Error")








