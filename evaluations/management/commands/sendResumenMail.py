from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum,Count,Avg
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill
from bakhanapp.models import Video_Playing,Student,Tutor,Administrator,Institution,Class
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import unicodedata
from lib2to3.fixer_util import String
import os
import sys
from django import template
register = template.Library()
class Command(BaseCommand):
    help = 'Envia un mail con el resumen de las nota y las variables de empegno/desempegno a los administradores'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        #lastDate = date.today() - timedelta(days=1)
        lastDate = date.today() - timedelta(days=1)
        assesments = Assesment.objects.filter(end_date=lastDate).values('id_assesment','id_assesment_conf_id','start_date','end_date','name',
            'max_grade','min_grade','id_class_id')
        for assesment in assesments:
            skills = getSkillAssesment(assesment['id_assesment_conf_id'])
            assesmentConfig = Assesment_Config.objects.get(id_assesment_config=assesment['id_assesment_conf_id'])#.values('approval_percentage','top_score','importance_skill_level','importance_completed_rec')
            startDate = assesment['start_date']
            endDate = assesment['end_date']
            name = assesment['name']
            minGrade = assesment['min_grade']
            maxGrade = assesment['max_grade']
            approvalPercentage = assesmentConfig.approval_percentage
            importanceSkillLevel = assesmentConfig.importance_skill_level
            importanceRecomended = assesmentConfig.importance_completed_rec
            idAssesment = assesment['id_assesment']
            grades = Grade.objects.filter(id_assesment_id=assesment['id_assesment'])
            totalStudents = len(grades) 
            avgVideoTime = grades.aggregate(Avg('video_time'))
            avgExcerciceTime = grades.aggregate(Avg('excercice_time'))
            avgCorrectExcercice = grades.aggregate(Avg('correct'))
            avgRecomendedComplete = grades.aggregate(Avg('recomended_complete'))
            if avgRecomendedComplete['recomended_complete__avg'] is  None:
                avgRecomendedComplete['recomended_complete__avg'] = 0
            excerciceTimeUnit = ' minutos'
            videoTimeUnit = ' minutos'
            if int(avgExcerciceTime['excercice_time__avg']) == 1:
                excerciceTimeUnit = ' minuto'
            if int(avgVideoTime['video_time__avg']) == 1:
                videoTimeUnit = 'minuto'
            
            #administrators = Administrator.objects.filter(id_institution_id=1)
            id_institution = Class.objects.get(id_class=assesment['id_class_id'])
            #id_institution = Institution.objects.get(id_institution=id_class['id_institution_id']).values('id_institution')
            #print id_institution.id_institution_id
            administrators = Administrator.objects.filter(id_institution_id=id_institution.id_institution_id)
            #print administrators
            
            students = Grade.objects.filter(id_assesment_id=assesment['id_assesment']).values('kaid_student_id')
            configSkills = Skill.objects.filter(assesment_skill__id_assesment_config=assesment['id_assesment_conf_id']).values('assesment_skill__id_skill_name_id','name_spanish')
            #print configSkills
            dictSkillDomain = {}
            skillsDomain = "<table >"
            for skill in configSkills:
                skillsDomain = skillsDomain+'<tr>'
                practiced,mastery1,mastery2,mastery3,struggling = getSkillStudentDomain(skill['assesment_skill__id_skill_name_id'],startDate,endDate,students)
                skillName = Skill.objects.get(pk=skill['assesment_skill__id_skill_name_id'])
                s = str(skillName)
                skillWithoutAccent = strip_accents(s)
                unit = 150/int(totalStudents)
                unstarted = totalStudents-practiced-mastery1-mastery2-mastery3-struggling
                skillsDomain = skillsDomain+"<td style='height:20px'><p style='font-family:'Helvetica Neue',Calibri,Helvetica,Arial,sans-serif; font-size:16px;  color:#666; font-size:14px; color:#333'>"+skillWithoutAccent+"</p></td>"
                skillsDomain = skillsDomain+"<td  style='display:inline;width:150px;height:20px;align-items: center;'><div style='margin:10px 0 0 0;text-align:center;background-color:#C30202;align-items: center;width:"+str(unit*struggling)+"px;display:inline-block;height:20px'>"+str(struggling)+"</div><div style='align-items: center;text-align:center;background-color:#9CDCEB;display:inline-block;width:"+str(unit*practiced)+"px;height:20px'>"+str(practiced)+"</div><div style='align-items: center;text-align:center;background-color:#58C4DD;display:inline-block;width:"+str(unit*mastery1)+"px;height:20px'>"+str(mastery1)+"</div><div style='align-items: center;text-align:center;background-color:#29ABCA;display:inline-block;width:"+str(unit*mastery2)+"px;height:20px'>"+str(mastery2)+"</div><div style='align-items: center;text-align:center;background-color:#1C758A;display:inline-block;width:"+str(unit*mastery3)+"px;height:20px'>"+str(mastery3)+"</div><div style='align-items: center;text-align:center;background-color:#DDDDDD;display:inline-block;width:"+str(unit*unstarted)+"px;height:20px'>"+str(unstarted)+"</div></td></tr>"
                dictSkillDomain[skillWithoutAccent] = [practiced,mastery1,mastery2,mastery3,struggling]
            skillsDomain = skillsDomain+'</table>'
            print 'skills'
            print skillsDomain
            
            
            content = htmlTemplate(skillsDomain,name,startDate,endDate,minGrade,maxGrade,approvalPercentage,importanceSkillLevel,importanceRecomended,
                str(int(avgExcerciceTime['excercice_time__avg']/60))+excerciceTimeUnit,str(int(avgVideoTime['video_time__avg']/60))+videoTimeUnit,
                totalStudents,idAssesment,int(avgCorrectExcercice['correct__avg']),
                str(avgRecomendedComplete['recomended_complete__avg'])+'%')
            for admin in administrators:
                content = content.replace("$$nameAdmin$$",str(admin.name))
                #sendMail('javierperezferrada@gmail.com',content)
                sendMail(admin.email,content)
                content = content.replace(str(admin.name),"$$nameAdmin$$")

def getSkillStudentDomain(skill,startDate,endDate,students):
    #funcion que calcula cuantos estudiantes quedaron en cada nivel de dominio segun la skill recibida
    #print 'total students: %d'%(len(students))
    levels = Student_Skill.objects.filter(kaid_student__in=students,id_skill_name=skill,struggling=False,skill_progress__date__range=(startDate,endDate)
                ).values('kaid_student','id_student_skill','skill_progress__to_level','skill_progress__date'
                ).order_by('kaid_student','id_student_skill').distinct('kaid_student','id_student_skill')
    struggling = Student_Skill.objects.filter(kaid_student__in=students,id_skill_name=skill,struggling=True,skill_progress__date__range=(startDate,endDate)
                ).values('kaid_student','id_student_skill','skill_progress__to_level','skill_progress__date'
                ).order_by('kaid_student','id_student_skill').distinct('kaid_student','id_student_skill').count()
    practiced = 0
    mastery1 = 0
    mastery2 = 0
    mastery3 = 0
    for level in levels:
        if str(level['skill_progress__to_level']) == 'practiced':
            practiced += 1
        if str(level['skill_progress__to_level']) == 'mastery1':
            mastery1 += 1
        if str(level['skill_progress__to_level']) == 'mastery2':
            mastery2 += 1
        if str(level['skill_progress__to_level']) == 'mastery3':
            mastery3 += 1
    #print 'niveles'
    return practiced,mastery1,mastery2,mastery3,struggling

def sendMail(email,contenido): #recibe los datos iniciales y envia un  mail a cada student y a cada tutor
    subject = 'Ha finalizado una Evaluacion'
    text_content = 'habilita el html de tu correo'
    html_content = contenido
    from_email = '"Bakhan Academy" <bakhanacademy@gmail.com>'
    to = str(email)
    #to2 = str(tutor.email)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return ()

def htmlTemplate(skills,name,startDate,endDate,minGrade,maxGrade,approvalPercentage,importanceSkillLevel,importanceRecomended,avgExcerciceTime,
    avgVideoTime,totalStudents,idAssesment,avgCorrectExcercice,avgRecomendedComplete):
    archivo=open("C:/Users/LACLO2013_B/Desktop/ba-khan/static/plantillas/resumen_assesment_mail.html")
    contenido = archivo.read()
    contenido = contenido.replace("$$grade$$","{0:.1f}".format(2.45))
    contenido = contenido.replace("$$name$$",str(name))
    contenido = contenido.replace("$$startDate$$",str(startDate.strftime('%d/%m/%Y')))
    contenido = contenido.replace("$$endDate$$",str(endDate.strftime('%d/%m/%Y')))
    contenido = contenido.replace("$$minGrade$$",str(minGrade))
    contenido = contenido.replace("$$maxGrade$$",str(maxGrade))
    contenido = contenido.replace("$$totalStudents$$",str(totalStudents))
    contenido = contenido.replace("$$approvalPercentage$$",str(approvalPercentage))
    contenido = contenido.replace("$$importanceSkillLevel$$",str(importanceSkillLevel))
    contenido = contenido.replace("$$importanceRecomended$$",str(importanceRecomended))
    contenido = contenido.replace("$$avgExcerciceTime$$",str(avgExcerciceTime))
    contenido = contenido.replace("$$avgVideoTime$$",str(avgVideoTime))
    contenido = contenido.replace("$$avgCorrectExcercice$$",str(avgCorrectExcercice))
    contenido = contenido.replace("$$avgRecomendedComplete$$",str(avgRecomendedComplete))
    contenido = contenido.replace("$$ejercicios$$",str(skills))
    rUnit = maxGrade/float(10)
    aux = 0
    qMax = 0
    grades = Grade
    for x in range(11):
        qStudents = Grade.objects.filter(id_assesment_id=idAssesment,grade__gt=aux,grade__lt=aux+rUnit).count()
        if qMax <= qStudents:
            qMax = qStudents
        aux += rUnit
    hUnit = 300/qMax #unidad basica para la altura del histograma
    aux = 0
    for i in range(11):
        varR = "$$r"+str(i)+"$$"
        varD = "$$d"+str(i)+"$$"
        varH = "$$h"+str(i)+"$$"
        contenido = contenido.replace(varR,str(aux))
        qStudents = Grade.objects.filter(id_assesment_id=idAssesment,grade__gt=aux,grade__lt=aux+rUnit).count()#.values('grade').aggregate(q=Count('grade'))
        if qStudents == 0:
            contenido = contenido.replace(varD,str(''))
            contenido = contenido.replace(varH,str(1))
        else:
            contenido = contenido.replace(varD,str(qStudents))
            contenido = contenido.replace(varH,str(qStudents*hUnit))
        
        #print qStudents*hUnit
        
        aux += rUnit
    return(contenido)

def getSkillAssesment(id_asses_config): #recibe la configuracion y devuelve el html con todas las skill (un <p> por skill)
    mnsj_skills = ''
    g = Assesment_Skill.objects.filter(id_assesment_config=id_asses_config).values('id_skill_name_id')
    n = Skill.objects.filter(id_skill_name__in=g)
    for i in n :
        skill = str(i)
        skill = strip_accents(skill)
        mnsj_skills = mnsj_skills+'<p style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:16px; line-height:24px; color:#666; margin:0 0 10px; font-size:14px; color:#333">'+skill+'</p>'
    return mnsj_skills

def strip_accents(text): #reemplaza las letras con acento por letras sin acento
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
