from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress

class Command(BaseCommand):
    help = 'Envia un mail con la nota y las variables de empegno y desempegno'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        lastDate = date.today() - timedelta(days=1)
        assesments = Assesment.objects.filter(end_date=lastDate).values('name','grade__grade',
            'grade__kaid_student_id','grade__performance_points')#inner join django 1-N desde 1 hacia N
        for assesment in assesments: 
            print assesment['grade__grade']
            #grades = Grade.objects.filter()
        
