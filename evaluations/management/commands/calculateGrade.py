import time
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Grade,Assesment,Assesment_Config
class Command(BaseCommand):
    help = 'Calcula notas al pasar la fecha de la evaluacion'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        currentDate = time.strftime("%Y-%m-%d") #fecha actual.
        assesments = Assesment.objects.filter(end_date__lte=currentDate)
        for assesment in assesments:
            print assesment
            approval_percentage = Assesment_Config.objects.get(pk=assesment.id_assesment_conf_id).approval_percentage
            print approval_percentage
