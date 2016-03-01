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
    help = 'Envia un mail con la nota y las variables de empegno y desempegno'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        lastDate = date.today() - timedelta(days=1)
        #cambiar end_date__lgt
        assesments = Assesment.objects.filter(end_date=lastDate).values('id_assesment_conf_id','id_assesment','name','start_date','end_date')#,'grade__grade',
            #'grade__kaid_student_id','grade__performance_points','grade__recomended_compete','grade__excercice_time','grade__video_time','grade__correct',
            #'grade__incorrect','grade__struggling','grade__mastery1','grade__mastery2','grade__mastery3','grade__practiced')#inner join django 1-N desde 1 hacia N
        #assesments = Assesment.objects.filter(end_date=lastDate)
        conf = 0 
        for assesment in assesments: #en assesment se encuantral las assesments y grades con kaid students
            grades = Grade.objects.filter(id_assesment_id=assesment['id_assesment']).values('grade','kaid_student_id','performance_points','recomended_complete','excercice_time',
                'video_time','correct','incorrect','struggling','mastery1','mastery2','mastery3','practiced')
            for grade in grades:
                content = htmlTemplate(grade['grade'],grade['performance_points'],grade['video_time'],grade['correct'],grade['incorrect'],assesment['id_assesment_conf_id'],
                    grade['practiced'],grade['mastery1'],grade['mastery2'],grade['mastery3'],grade['struggling'],assesment['name'])
                sendMail(grade['kaid_student_id'],content)
                sendWhatsapp(grade['kaid_student_id'],grade['grade'],grade['performance_points'],grade['video_time'],grade['correct'],grade['incorrect'],
                    grade['practiced'],grade['mastery1'],grade['mastery2'],grade['mastery3'],grade['struggling'])

def sendWhatsapp(kaid,grade,points,video_time,corrects,incorrects,
                practiced,mastery1,mastery2,mastery3,struggling):
    student = Student.objects.get(pk=kaid)
    mensaje = 'Hola, ha finalizado una evaluacion para: '+student.name+'\n'
    mensaje = mensaje + 'Nota obtenida: '+str(grade)+'\n'
    mensaje = mensaje + 'Puntos: '+str(points)+'\n'
    mensaje = mensaje + 'Tiempo en Videos: '+str(video_time)+'minutos \n'
    mensaje = mensaje + 'Correctas: '+str(corrects)+'\n'
    mensaje = mensaje + 'Incorrectas: '+str(incorrects)+'\n'
    mensaje = mensaje + 'Nivel de dominio:\n'
    mensaje = mensaje + 'Practicados - '+str(practiced)+'\n'
    mensaje = mensaje + 'Nivel 1 - '+str(mastery1)+'\n'
    mensaje = mensaje + 'Nivel 2 - '+str(mastery2)+'\n'
    mensaje = mensaje + 'Dominado - '+str(mastery3)+'\n'
    mensaje = mensaje + 'Dificultad - '+str(struggling)+'\n'
    phone = str(student.phone)
    whatsapp(mensaje,phone)
    return ()

def whatsapp(msg,num):
    mensaje = msg
    numero = num
    os.system("yowsup-cli demos -l 56955144957:S23B/CdXejaVQPWehwWmqwhnoaI= -s 569%s '%s'"%(numero,mensaje))
    return ()


def sendMail(kaid,contenido): #recibe los datos iniciales y envia un  mail a cada student y a cada tutor
    student = Student.objects.get(pk=kaid)
    tutor = Tutor.objects.get(kaid_student_child=kaid)
    
    contenido_html = contenido.replace("$$nombre_usuario$$",str(student.name)) #usarPlantilla()

    subject = 'Ha finalizado una Evaluacion'
    text_content = 'habilita el html de tu correo'
    html_content = contenido_html
    from_email = '"Bakhan Academy" <bakhanacademy@gmail.com>'
    to = str(student.email)
    to2 = str(tutor.email)
    print to
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return ()

def htmlTemplate(grade,points,video_time,corrects,incorrects,id_assesment_config,
                practiced,mastery1,mastery2,mastery3,struggling,name):
    skill_assesment = getSkillAssesment(id_assesment_config)
    #archivo=open("/var/www/html/bakhanproyecto/static/plantillas/end_assesment_mail.html")
    archivo=open("static/plantillas/end_assesment_mail.html")
    contenido = archivo.read()
    contenido = contenido.replace("$$grade$$","{0:.1f}".format(grade))
    contenido = contenido.replace("$$points$$",str(points))
    contenido = contenido.replace("$$video_time$$",str(video_time))
    contenido = contenido.replace("$$corrects$$",str(corrects))
    contenido = contenido.replace("$$incorrects$$",str(incorrects))
    contenido = contenido.replace("$$practiced$$",str(practiced))
    contenido = contenido.replace("$$mastery1$$",str(mastery1))
    contenido = contenido.replace("$$mastery2$$",str(mastery2))
    contenido = contenido.replace("$$mastery3$$",str(mastery3))
    contenido = contenido.replace("$$struggling$$",str(struggling))
    contenido = contenido.replace("$$assesmentName$$",str(name))
    contenido = contenido.replace("$$ejercicios$$",str(skill_assesment))
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

def getDomainLevel(id_assesment_config,kaid_student):
    practiced = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,student_skill__kaid_student_id=kaid_student,student_skill__last_skill_progress='practiced').values(
        'student_skill__id_student_skill','student_skill__last_skill_progress').annotate(practiced=Count('student_skill__id_student_skill')).aggregate(Sum('practiced'))
    mastery1 = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,student_skill__kaid_student_id=kaid_student,student_skill__last_skill_progress='mastery1').values(
        'student_skill__id_student_skill','student_skill__last_skill_progress').annotate(mastery1=Count('student_skill__id_student_skill')).aggregate(Sum('mastery1'))
    mastery2 = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,student_skill__kaid_student_id=kaid_student,student_skill__last_skill_progress='mastery2').values(
        'student_skill__id_student_skill','student_skill__last_skill_progress').annotate(mastery2=Count('student_skill__id_student_skill')).aggregate(Sum('mastery2'))
    mastery3 = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,student_skill__kaid_student_id=kaid_student,student_skill__last_skill_progress='mastery3').values(
        'student_skill__id_student_skill','student_skill__last_skill_progress').annotate(mastery3=Count('student_skill__id_student_skill')).aggregate(Sum('mastery3'))
    struggling = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,student_skill__kaid_student_id=kaid_student,student_skill__struggling=True).values(
        'student_skill__id_student_skill','student_skill__last_skill_progress').annotate(struggling=Count('student_skill__id_student_skill')).aggregate(Sum('struggling'))
    if practiced['practiced__sum'] == None:
        practiced['practiced__sum'] = 0
    if mastery1['mastery1__sum'] == None:
        mastery1['mastery1__sum'] = 0
    if mastery2['mastery2__sum'] == None:
        mastery2['mastery2__sum'] = 0
    if mastery3['mastery3__sum'] == None:
        mastery3['mastery3__sum'] = 0
    if struggling['struggling__sum'] == None:
        struggling['struggling__sum'] = 0
    return practiced['practiced__sum'], mastery1['mastery1__sum'], mastery2['mastery2__sum'], mastery3['mastery3__sum'], struggling['struggling__sum']


def getSkillAttemptIncorrect(id_assesment_config,kaid_student):
    skills = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,skill_attempt__kaid_student_id=kaid_student,skill_attempt__correct=False,skill_attempt__skipped=False).values('name_spanish',
        'skill_attempt__correct').annotate(incorrects = Count('skill_attempt__correct')).aggregate(Sum('incorrects'))
    #print 'respuesta de una consulta'
    if skills['incorrects__sum'] == None:
        incorrects = 0
    else:
        incorrects = skills['incorrects__sum']
    return incorrects

def getSkillAttemptCorrect(id_assesment_config,kaid_student):
    skills = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config,skill_attempt__kaid_student_id=kaid_student,skill_attempt__correct=True).values('name_spanish',
        'skill_attempt__correct').annotate(corrects = Count('skill_attempt__correct')).aggregate(Sum('corrects'))
    #print 'respuesta de una consulta'
    if skills['corrects__sum'] == None:
        corrects = 0
    else:
        corrects = skills['corrects__sum']
    return corrects

def getSelectedSkills(id_assesment_config):
    skills = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config).values('name_spanish','assesment_skill__id_assesment_config_id')
    return skills

def getVideoTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en un rango de fechas.
    query_set = Video_Playing.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end).aggregate(Sum('seconds_watched'))
    if query_set['seconds_watched__sum'] == None:
        return 0
    else:
        return query_set['seconds_watched__sum']/60

def strip_accents(text): #reemplaza las letras con acento por letras sin acento
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
