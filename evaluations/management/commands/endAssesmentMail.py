from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Sum
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill,Video_Playing

class Command(BaseCommand):
    help = 'Envia un mail con la nota y las variables de empegno y desempegno'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        lastDate = date.today() - timedelta(days=1)
        #cambiar end_date__lgt
        assesments = Assesment.objects.filter(end_date__lte=lastDate).values('id_assesment_conf_id','id_assesment','name','start_date','end_date','grade__grade',
            'grade__kaid_student_id','grade__performance_points')#inner join django 1-N desde 1 hacia N
        #assesments = Assesment.objects.filter(end_date=lastDate)
        conf = 0 
        for assesment in assesments: #en assesment se encuantral las assesments y grades con kaid students
            if conf != assesment['id_assesment_conf_id']: #consulta las habilidaes cuando cambia assesment_config
                skills = getSelectedSkills(assesment['id_assesment_conf_id']) 
                conf = assesment['id_assesment_conf_id']
            video_time = getVideoTimeBetween(assesment['grade__kaid_student_id'],assesment['start_date'],assesment['end_date'])
            print video_time


def getSelectedSkills(id_assesment_config):
    skills = Skill.objects.filter(assesment_skill__id_assesment_config_id=id_assesment_config).values('name_spanish','assesment_skill__id_assesment_config_id')
    return skills

def getVideoTimeBetween(kaid_s,t_begin,t_end):
    #Esta funcion entrega el tiempo que un estudiante ha utilizado en videos en un rango de fechas.
    query_set = Video_Playing.objects.filter(kaid_student=kaid_s,date__gte = t_begin,date__lte = t_end).aggregate(Sum('seconds_watched'))
    if query_set['seconds_watched__sum'] == None:
        return 0
    else:
        return query_set['seconds_watched__sum']
