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
from bakhanapp.models import Assesment_Skill

register = template.Library()


from bakhanapp.models import Skill

from bakhanapp.models import Assesment_Config,Subtopic_Skill,User_Profile


from bakhanapp.views import getTopictree



import json


# Create your views here.
@login_required()
def getTeacherAssesmentConfigs(request):#url configuraciones
    #Esta funcion entrega todas las configuraciones de evaluaciones realizadas por un profesor
    request.session.set_expiry(300)#5 minutos de inactividad
    kaid = User_Profile.objects.get(user=request.user.id)
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher=kaid.kaid).order_by('-id_assesment_config')

    json_array=[]
    for assesment_config in assesment_configs:
        #print assesment_config.id_assesment_config
        assesment_skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment_config.id_assesment_config).values('id_skill_name_id')
        config_skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment_config.id_assesment_config).values('id_subtopic_skill_id')
       #print assesment_skills
        skills = Skill.objects.filter(id_skill_name__in=assesment_skills).values('name_spanish')
        #print skills
        config_json={}
        config_json["id_assesment_config"]=assesment_config.id_assesment_config
        config_json["approval_percentage"]=assesment_config.approval_percentage
        config_json["top_score"]=assesment_config.top_score
        config_json["name"]=assesment_config.name
        config_json["id_subject_name_id"]=assesment_config.id_subject_name_id
        config_json["kaid_teacher_id"]=assesment_config.kaid_teacher_id
        config_json["importance_skill_level"]=assesment_config.importance_skill_level
        config_json["importance_completed_rec"]=assesment_config.importance_completed_rec
        config_json["applied"]=assesment_config.applied
        config_json["assesment_skills"]=[]
        config_json["assesment_skills_spanish"]=[]
        config_json["config_skills"]=[]
        for i in range(len(assesment_skills)):
            config_json["assesment_skills"].append(assesment_skills[i])
            config_json["assesment_skills_spanish"].append(skills[i])
            config_json["config_skills"].append(config_skills[i])
        #print config_json["assesment_skills"]
        json_array.append(config_json)
    
    json_dict={"assesmentConfigs":json_array}
    json_data = json.dumps(json_dict)
    #print (json_data)
    topictree= getTopictree('math')
    return render_to_response('myAssesmentConfigs.html', {'assesment_configs': assesment_configs, 'topictree':topictree,'json_data': json_data}, context_instance=RequestContext(request))

def editAssesmentConfig(request,id_assesment_config):
    kaid = User_Profile.objects.get(user=request.user.id)
    if request.method == 'POST':
        args = request.POST
        aux= args['forloop']

        assesment_config = Assesment_Config.objects.get(id_assesment_config=id_assesment_config)
        skills_selected = eval(args['skills'+aux])
        assesment_config.name=args['name']
        assesment_config.approval_percentage=args['approval_percentage']
        assesment_config.importance_skill_level=args['importance_skill_level'+aux]
        assesment_config.importance_completed_rec=args['importance_completed_rec'+aux]

        assesment_config.kaid_teacher_id=kaid.kaid
        assesment_config.top_score=0
        assesment_config.id_subject_name_id='math'
        assesment_config.applied=False

        assesment_config.save()
        Assesment_Skill.objects.filter(id_assesment_config_id=id_assesment_config).delete()

        for skill in skills_selected:
                new_assesment_skill=Assesment_Skill.objects.create(id_assesment_config=assesment_config,
                                                    id_skill_name_id=skill['skill_id'],id_subtopic_skill_id=skill['id'])
    return HttpResponse("Pauta editada correctamente")


def deleteAssesmentConfig(request,id_assesment_config):
    Assesment_Config.objects.get(id_assesment_config=id_assesment_config).delete() #elimina assesment_config y assesment_skills
    return HttpResponse("Pauta Eliminada")

def newAssesmentConfig(request):
    
    kaid = User_Profile.objects.get(user=request.user.id)
    if request.method == 'POST':
        args = request.POST
        id = args['id']

        if (args['name'] and args['approval_percentage'] and args['importance_skill_level'+id] and args['importance_completed_rec'+id] and eval(args['skills'+id])):
            skills_selected = eval(args['skills'+id])
            
            #subtopic_skills = eval(args['subtopic_skill'+id])
            subject="math"
            new_assesment_config = Assesment_Config.objects.create(name=args['name'],
                                   approval_percentage=args['approval_percentage'],
                                   importance_skill_level=args['importance_skill_level'+id],
                                   importance_completed_rec=args['importance_completed_rec'+id],
                                   kaid_teacher_id=kaid.kaid,
                                   top_score=0,
                                   id_subject_name_id='math',
                                   applied=False
                                   )

            for skill in skills_selected:
                print skill['skill_id']
                try:
                    new_assesment_skill=Assesment_Skill.objects.create(id_assesment_config=new_assesment_config,
                                                        id_skill_name_id=skill['skill_id'],id_subtopic_skill_id=skill['id'])
                except:
                    continue
                
            return HttpResponse("Pauta guardada correctamente")
        else:
            return HttpResponse("Faltan datos. Pauta no ingresada")
        
    
    return HttpResponse()