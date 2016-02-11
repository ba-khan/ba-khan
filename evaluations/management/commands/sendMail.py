from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Assesment
from bakhanapp.models import Student
from bakhanapp.models import Tutor
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Skill

from django.core.mail import EmailMultiAlternatives

import unicodedata

class Command(BaseCommand):
    help = 'help!'

    def add_arguments(self, parser):
        parser.add_argument('kaids', nargs='+', type=str)
        parser.add_argument('nota1', nargs='+', type=str)
        parser.add_argument('nota2', nargs='+', type=str)
        parser.add_argument('fecha1', nargs='+', type=str)
        parser.add_argument('fecha2', nargs='+', type=str)
        parser.add_argument('id_config', nargs='+', type=str)

    def handle(self, *args, **options):
        for kaid_str in options['kaids']:
            kaid = kaid_str
        for nt1 in options['nota1']:
            nota1 = nt1
        for nt2 in options['nota2']:
            nota2 = nt2
        for fe1 in options['fecha1']:
            fecha1 = fe1
        for fe2 in options['fecha2']:
            fecha2 = fe2
        for ic in options['id_config']:
            id_config = ic


        contenido = usarPlantilla(nota1,nota2,fecha1,fecha2,id_config)
        sendMail(kaid,contenido)
        self.stdout.write('success')


def sendMail(kaidstr,contenido): #recibe los datos iniciales y envia un  mail a cada student y a cada tutor
    kaids = kaidstr.split(',')
    kaids.pop(0)
    for kaid in kaids:
        print kaid
        student = Student.objects.get(pk=kaid)
        tutor = Tutor.objects.get(kaid_student_child=kaid)
        
        contenido_html = contenido.replace("$$nombre_usuario$$",student.name) #usarPlantilla()

        subject = 'Nueva Evaluacion'
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

def usarPlantilla(nota1,nota2,fecha1,fecha2,id_config):
    print nota1
    print nota2
    print fecha1
    print fecha2
    print id_config
    skill_assesment = getSkillAssesment(id_config)
    archivo=open("static/plantillas/mail_nueva_evaluacion.html")
    contenido = archivo.read()
    contenido = contenido.replace("$$fecha_inicio$$",str(fecha1))
    contenido = contenido.replace("$$fecha_termino$$",str(fecha2))
    contenido = contenido.replace("$$nota_minima$$",str(nota1))
    contenido = contenido.replace("$$nota_maxima$$",str(nota2))
    contenido = contenido.replace("$$ejercicios$$",str(skill_assesment))
    print contenido
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