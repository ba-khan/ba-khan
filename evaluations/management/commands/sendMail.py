from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Assesment
from bakhanapp.models import Student
from bakhanapp.models import Tutor

from django.core.mail import EmailMultiAlternatives

class Command(BaseCommand):
    help = 'help!'

    def add_arguments(self, parser):
        parser.add_argument('kaids', nargs='+', type=str)
        parser.add_argument('contenido', nargs='+', type=str)

    def handle(self, *args, **options):
        for kaid_str in options['kaids']:
            kaid = kaid_str
        for content in options['contenido']:
            contenido = content

        sendMail(kaid,contenido)
        self.stdout.write('success')


def sendMail(kaidstr,contenido): #recibe los datos iniciales y envia un  mail a cada student y a cada tutor
    kaids = kaidstr.split(',')
    for kaid in kaids:
        student = Student.objects.get(pk=kaid)
        tutor = Tutor.objects.get(kaid_student_child=kaid)
        
        contenido_html = contenido.replace("$$nombre_usuario$$",student.name) #usarPlantilla()

        subject = 'Nueva Evaluacion'
        text_content = 'habilita el html de tu correo'
        html_content = contenido_html
        from_email = '"Bakhan Academy" <bakhanacademy@gmail.com>'
        to = str(student.email)
        to2 = str(tutor.email)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to,to2])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return ()