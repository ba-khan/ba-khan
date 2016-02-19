from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum,Count
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill,Video_Playing,Student,Tutor
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import unicodedata
import os
class Command(BaseCommand):
    help = 'Envia un mail con el resumen de las nota y las variables de empegno/desempegno a los administradores'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        lastDate = date.today() - timedelta(days=1)
        assesments = Assesment.objects.filter(end_date=lastDate).values('id_assesment','id_assesment_conf_id')
        for assesment in assesments:
            skills = getSkillAssesment(assesment['id_assesment_conf_id'])
            conf = assesment['id_assesment_conf_id']
            
            content = htmlTemplate(skills)
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

def htmlTemplate(skills):
    archivo=open("C:/Users/LACLO2013_B/Desktop/ba-khan/static/plantillas/resumen_assesment_mail.html")
    contenido = archivo.read()
    contenido = contenido.replace("$$grade$$","{0:.1f}".format(2.45))
    #contenido = contenido.replace("$$skills$$",str(points))
    #contenido = contenido.replace("$$video_time$$",str(video_time))
    #contenido = contenido.replace("$$corrects$$",str(corrects))
    #contenido = contenido.replace("$$incorrects$$",str(incorrects))
    #contenido = contenido.replace("$$practiced$$",str(practiced))
    #contenido = contenido.replace("$$mastery1$$",str(mastery1))
    #contenido = contenido.replace("$$mastery2$$",str(mastery2))
    #contenido = contenido.replace("$$mastery3$$",str(mastery3))
    #contenido = contenido.replace("$$struggling$$",str(struggling))
    contenido = contenido.replace("$$ejercicios$$",str(skills))
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
