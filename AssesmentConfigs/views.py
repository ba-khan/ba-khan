#!usr/bin/env python
# -*- coding: utf-8 -*-
""" """
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
from bakhanapp.models import Assesment_Skill,Class_Subject,Chapter_Mineduc,Topic_Mineduc,Subtopic_Mineduc,Subtopic_Skill_Mineduc,Class,Subject,Planning,Skill_Planning

register = template.Library()

from bakhanapp.models import Skill
from bakhanapp.models import Assesment_Config,Subtopic_Skill,User_Profile
from bakhanapp.views import getTopictree
import json


##-------------------------------------------------------------------------------
## Esta funcion entrega todas las configuraciones de evaluaciones realizadas por
## un profesor
##
## @param      request  Request
##
## @return     myAssesmentConfigs.html
##
@login_required()
def getTeacherAssesmentConfigs(request):#url configuraciones
    assesment_configs = Assesment_Config.objects.filter(kaid_teacher=request.user.user_profile.kaid).order_by('-id_assesment_config')

    json_array=[]
    for assesment_config in assesment_configs:
        #print assesment_config.id_assesment_config
        assesment_skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment_config.id_assesment_config).values('id_skill_name_id')
        config_skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment_config.id_assesment_config).values('id_subtopic_skill_id')
        #print config_skills
        #skills = Skill.objects.filter(id_skill_name__in=assesment_skills).values('name_spanish')
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
            #print config_skills[i]
            skills = Skill.objects.filter(id_skill_name=assesment_skills[i]['id_skill_name_id']).values('name_spanish')
            config_json["assesment_skills"].append(assesment_skills[i])
            config_json["assesment_skills_spanish"].append(skills[0]['name_spanish'])

        for j in range(len(config_skills)):
            config_json["config_skills"].append(config_skills[j])
            
        json_array.append(config_json)
    
    json_dict={"assesmentConfigs":json_array}
    json_data = json.dumps(json_dict)
    #print (json_data)
    topictree= getTopictree('math')

    curriculum_list =  Chapter_Mineduc.objects.all().values('id_chapter_mineduc','level','year').order_by('-year','level')

    if (Class_Subject.objects.filter(kaid_teacher=request.user.user_profile.kaid)):
        isTeacher = True
        class_list = Class.objects.filter(class_subject__kaid_teacher=request.user.user_profile.kaid).values('level', 'letter', 'year', 'class_subject__id_class_subject').order_by('-year','level','letter').exclude(class_subject__curriculum__isnull=True)
    else:
        isTeacher = False

    N = ['Kinder','Primero Básico','Segundo Básico','Tercero Básico','Cuarto Básico','Quinto Básico','Sexto Básico','Septimo Básico','Octavo Básico','Primero Medio','Segundo Medio','Tercero Medio','Cuarto Medio']
    for i in range(len(class_list)):
        class_list[i]['level'] = N[int(class_list[i]['level'])]

    for i in range(len(curriculum_list)):
        curriculum_list[i]['level'] = N[int(curriculum_list[i]['level'])]

    return render_to_response('myAssesmentConfigs.html', {'assesment_configs': assesment_configs, 'topictree':topictree,'json_data': json_data,'isTeacher':isTeacher, 'class_list': class_list, 'curriculum_list': curriculum_list}, context_instance=RequestContext(request))

##-------------------------------------------------------------------------------
## Esta funcion edita una pauta de un profesor
##
## @param      request              Request
## @param      id_assesment_config  Id de una pauta
##
## @return     "Pauta editada correctamente"
##
def editAssesmentConfig(request,id_assesment_config):
    if request.method == 'POST':
        try:
            args = request.POST
            aux= args['forloop']
            assesment_config = Assesment_Config.objects.get(id_assesment_config=id_assesment_config)

            skills_selected = eval(args['skills'+aux])

            assesment_config.name=args['name']
            assesment_config.approval_percentage=args['approval_percentage']
            assesment_config.importance_skill_level=args['importance_skill_level'+aux]
            assesment_config.importance_completed_rec=args['importance_completed_rec'+aux]

            assesment_config.kaid_teacher_id=request.user.user_profile.kaid
            assesment_config.top_score=0
            assesment_config.id_subject_name_id='math'
            assesment_config.applied=False

            assesment_config.save()
            Assesment_Skill.objects.filter(id_assesment_config_id=id_assesment_config).delete()
            for skill in skills_selected:
                print skill
                new_assesment_skill=Assesment_Skill.objects.create(id_assesment_config=assesment_config, id_skill_name_id=skill['skill_id'],id_subtopic_skill_id=skill['id'])
            return HttpResponse("Pauta editada correctamente")
        except Exception as e:
            print "Error en la modificacion de una pauta: AssesmentConfigs/view.py:editAssesmentConfig"
            print repr(e)
            return HttpResponse('La pauta no se puede guardar!')

##
## @brief      Esta funcion borra una determinada pauta
##
## @param      request              The request
## @param      id_assesment_config  The identifier assesment configuration
##
## @return     Texto Pauta Eliminada
##
def deleteAssesmentConfig(request,id_assesment_config):
    Assesment_Config.objects.get(id_assesment_config=id_assesment_config).delete() #elimina assesment_config y assesment_skills
    return HttpResponse("Pauta Eliminada")


##
## @brief      Esta funcion crea una nueva pauta
##
## @param      request  The request
##
## @return     HttpResponse
##
def newAssesmentConfig(request):
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
                                   kaid_teacher_id=request.user.user_profile.kaid,
                                   top_score=0,
                                   id_subject_name_id='math',
                                   applied=False
                                   )

            for skill in skills_selected:
                try:
                    print skill
                    new_assesment_skill=Assesment_Skill.objects.create(id_assesment_config=new_assesment_config, id_skill_name_id=skill['skill_id'], id_subtopic_skill_id=skill['id'])
                except Exception as e:
                    print "Error en guardar habilidad: AssesmentConfigs/view.py:newAssesmentConfig"
                    print repr(e) 
                    print "Se continuara con la ejecución..."
                    continue
                
            return HttpResponse("Pauta guardada correctamente")
        else:
            print args['name']
            print args['approval_percentage']
            print args['importance_skill_level'+id]
            print args['importance_completed_rec'+id]
            print eval(args['skills'+id])
            return HttpResponse("Faltan datos. Pauta no ingresada")
    return HttpResponse()

def retrieveCurriculumTree(request):
    try:
        curriculum_id = request.GET.get('curriculum_id', None)
        Curriculum = Chapter_Mineduc.objects.get(id_chapter_mineduc=curriculum_id)
        Plan_Subject = Subject.objects.get(id_subject_name = Curriculum.id_subject.id_subject_name)
        
        topictree_json={}
        topictree_json['checkbox']={'keep_selected_style':False, 'cascade_to_hidden':False, 'cascade_to_disabled':False}
        topictree_json['plugins']=['checkbox','search']
        topictree=[]
        
        subject_obj={"id": Plan_Subject.id_subject_name, "parent":"#", "text": Plan_Subject.name_spanish, "state": {"opened":"true"}, "icon":"false"}
        topictree.append(subject_obj)
        
        unit_list = Topic_Mineduc.objects.filter(id_chapter=Curriculum.id_chapter_mineduc).order_by('index')
        for unit in unit_list:
            unit_obj = {"id": unit.id_topic_mineduc, "parent": Plan_Subject.id_subject_name, "text": "Unidad "+str(unit.index), "icon":"false"}
            topictree.append(unit_obj)

            oa_list = Subtopic_Mineduc.objects.filter(id_topic=unit.id_topic_mineduc).order_by('index')
            for oa in oa_list:
                oa_obj = {"id": oa.id_subtopic_mineduc, "parent": unit.id_topic_mineduc, "text": "Objetivo de aprendizaje "+str(oa.index), "icon":"false"}
                topictree.append(oa_obj)

                skill_list = Subtopic_Skill_Mineduc.objects.filter(id_subtopic_mineduc=oa.id_subtopic_mineduc).select_related('id_skill_name')
                for skill in skill_list:
                    subtopic_skill = Subtopic_Skill.objects.filter(id_skill_name=skill.id_skill_name.id_skill_name).values("id_subtopic_skill")
                    skill_obj = {"id": subtopic_skill[0]["id_subtopic_skill"], "parent": oa.id_subtopic_mineduc, "text": skill.id_skill_name.name_spanish, "data":{"skill_id":skill.id_skill_name.id_skill_name}, "icon":"false", "index":skill.id_skill_name.index}
                    sorted(skill_obj, key=skill_obj.get)
                    topictree.append(skill_obj)

        topictree_json['core'] = {'data':topictree}
        topictree_json_string = json.dumps(topictree_json)

        return HttpResponse(topictree_json_string, content_type="application/json")

    except Exception as e:
        print "Error en obtener los curriculos: AssesmentConfigs/view.py:retrieveCurriculumTree"
        print repr(e)
        return HttpResponse('No se pudieron obtener los datos del curriculo.')

def retrievePlanTree(request):
    try:
        subject_id = request.GET.get('class_subject_id', None)
        Subj = Class_Subject.objects.get(id_class_subject=subject_id)
        Curriculum = Chapter_Mineduc.objects.get(id_chapter_mineduc=Subj.curriculum_id)
        Plan_Subject = Subject.objects.get(id_subject_name=Subj.id_subject_name.id_subject_name)
        plan_list = Planning.objects.filter(class_subject=Subj).order_by('class_date')

        topictree_json={}
        topictree_json['checkbox']={'keep_selected_style':False, 'cascade_to_hidden':False, 'cascade_to_disabled':False}
        topictree_json['plugins']=['checkbox','search']
        topictree=[]
        
        subject_obj={"id": Plan_Subject.id_subject_name, "parent":"#", "text": Plan_Subject.name_spanish, "state": {"opened":"true"}, "icon":"false"}
        topictree.append(subject_obj)

        unit_list = Topic_Mineduc.objects.filter(id_chapter=Curriculum.id_chapter_mineduc).order_by('index')
        for unit in unit_list:
            unit_obj = {"id": unit.id_topic_mineduc, "parent": Plan_Subject.id_subject_name, "text": "Unidad "+str(unit.index), "icon":"false"}
            topictree.append(unit_obj)

            oa_list = Subtopic_Mineduc.objects.filter(id_topic=unit.id_topic_mineduc).order_by('index')
            for oa in oa_list:
                oa_obj = {"id": oa.id_subtopic_mineduc, "parent": unit.id_topic_mineduc, "text": "Objetivo de aprendizaje "+str(oa.index), "icon":"false"}
                topictree.append(oa_obj)

                for plan in plan_list:
                    if (plan.class_subtopic.id_subtopic_mineduc == oa.id_subtopic_mineduc):
                        plan_obj = {"id": plan.id_planning, "parent": oa.id_subtopic_mineduc, "text": plan.class_name, "icon":"false"}
                        topictree.append(plan_obj)

                        skill_list = Skill_Planning.objects.filter(id_planning=plan.id_planning).select_related('id_skill')
                        for skill in skill_list:
                            subtopic_skill = Subtopic_Skill.objects.filter(id_skill_name=skill.id_skill.id_skill_name).values("id_subtopic_skill")
                            skill_obj = {"id": subtopic_skill[0]["id_subtopic_skill"], "parent": plan.id_planning , "text": skill.id_skill.name_spanish, "data":{"skill_id":skill.id_skill.id_skill_name}, "icon":"false", "index": skill.id_skill.index}
                            sorted(skill_obj, key=skill_obj.get)
                            topictree.append(skill_obj)

        topictree_json['core'] = {'data':topictree}
        topictree_json_string = json.dumps(topictree_json)

        return HttpResponse(topictree_json_string, content_type="application/json")

    except Exception as e:
        print "Error en obtener los curriculos: AssesmentConfigs/view.py:retrievePlanTree"
        print repr(e)
        return HttpResponse('No se pudieron obtener los datos del curso.')

