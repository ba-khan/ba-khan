from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill

class Command(BaseCommand):
    help = 'Envia un mail con la nota y las variables de empegno y desempegno'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        lastDate = date.today() - timedelta(days=1)
        assesments = Assesment.objects.filter(end_date=lastDate).values('id_assesment_conf_id','id_assesment','name','grade__grade',
            'grade__kaid_student_id','grade__performance_points')#inner join django 1-N desde 1 hacia N
        #assesments = Assesment.objects.filter(end_date=lastDate)
        conf = 0 
        for assesment in assesments: 
            if conf != assesment['id_assesment_conf_id']:
                skills = getSelectedSkills(assesment['id_assesment_conf_id']) 
                conf = assesment['id_assesment_conf_id']
                print skills

def getSelectedSkills(id_assesment_config):
    skills = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config).values('name_spanish','assesment_skill__id_assesment_config_id')
    return skills
        
