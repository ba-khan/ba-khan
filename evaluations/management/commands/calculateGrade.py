import time
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress
class Command(BaseCommand):
    help = 'Calcula notas al pasar la fecha de la evaluacion'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        currentDate = time.strftime("%Y-%m-%d") #fecha actual.
        assesments = Assesment.objects.filter(end_date__lte=currentDate)
        for assesment in assesments:
            approval_percentage = Assesment_Config.objects.get(pk=assesment.id_assesment_conf_id).approval_percentage
            skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment.id_assesment_conf_id).values('id_skill_name_id')
            grades_involved = Grade.objects.filter(id_assesment_id=assesment.pk)
            for grade in grades_involved:
                grade.performance_points = getSkillPoints(grade.kaid_student_id,skills,assesment.start_date,assesment.end_date)
                grade.save()

def getSkillPoints(kaid_student,configured_skills,t_begin,t_end):
    #Funcion que entrega el puntaje promedio de un estudiante, segun una configuracion de evaluacion 
    #y un rango de fechas.
    scores={'unstarted':0,'struggling':20,'practiced':40,'mastery1':60,'mastery2':80,'mastery3':100}
    points = 0
    for skill in configured_skills:
        id_student_skills = Student_Skill.objects.filter(id_skill_name_id=skill,kaid_student_id=kaid_student).values('id_student_skill')
        last_level = Skill_Progress.objects.filter(id_student_skill_id=id_student_skills,date__gte = t_begin,date__lte = t_end).latest('date').values('to_level')
        points = points + scores[last_level]
    points = points / len(configured_skills)
    return points
