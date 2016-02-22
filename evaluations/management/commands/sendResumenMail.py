from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum,Count,Avg
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill,Video_Playing,Student,Tutor
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import unicodedata
import os
class Command(BaseCommand):
    help = 'Envia un mail con el resumen de las nota y las variables de empegno/desempegno a los administradores'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        #lastDate = date.today() - timedelta(days=1)
        lastDate = date.today() - timedelta(days=16)
        assesments = Assesment.objects.filter(end_date=lastDate).values('id_assesment','id_assesment_conf_id','start_date','end_date','name','max_grade','min_grade')
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

            


            content = htmlTemplate(skills,name,startDate,endDate,minGrade,maxGrade,approvalPercentage,importanceSkillLevel,importanceRecomended,
                avgExcerciceTime['excercice_time__avg'],avgVideoTime['video_time__avg'],totalStudents,idAssesment)
            sendMail('javierperezferrada@gmail.com',content)




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
    avgVideoTime,totalStudents,idAssesment):
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
    contenido = contenido.replace("$$ejercicios$$",str(skills))

    hUnit = 300/totalStudents #unidad basica para la altura del histograma
    print hUnit
    rUnit = maxGrade/float(10)
    #print rUnit,maxGrade
    aux = 0
    grades = Grade
    for i in range(10):
        varR = "$$r"+str(i)+"$$"
        varD = "$$d"+str(i)+"$$"
        varH = "$$h"+str(i)+"$$"
        contenido = contenido.replace(varR,str(aux))
        qStudents = Grade.objects.filter(id_assesment_id=idAssesment,grade__gt=aux,grade__lt=aux+rUnit).count()#.values('grade').aggregate(q=Count('grade'))
        contenido = contenido.replace(varD,str(qStudents))
        print qStudents*hUnit
        contenido = contenido.replace(varH,str(qStudents*hUnit))
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
