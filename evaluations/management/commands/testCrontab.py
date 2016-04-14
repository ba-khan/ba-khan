from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Class

class Command(BaseCommand):
    help = 'Calcula notas al pasar la fecha de la evaluacion'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        c = Class(id_class=1,level=9,letter=x,year=2020,id_institution_id=1)
        c.save()