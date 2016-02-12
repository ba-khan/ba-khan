import time
import json
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress
class Command(BaseCommand):
    help = 'Calcula notas al pasar la fecha de la evaluacion'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        currentDate = time.strftime("%Y-%m-%d") #fecha actual.
        print currentDate
        assesments = Assesment.objects.filter(end_date__lte=currentDate)
        for assesment in assesments:
            print assesment.name
            approval_percentage = Assesment_Config.objects.get(pk=assesment.id_assesment_conf_id).approval_percentage
            skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment.id_assesment_conf_id).values('id_skill_name_id')
            grades_involved = Grade.objects.filter(id_assesment_id=assesment.pk)
            #print grades_involved
            for grade in grades_involved:
                if grade.evaluated == False:
                    if grade.performance_points == 0:
                        grade.performance_points = getSkillPoints(grade.kaid_student_id,skills,assesment.start_date,assesment.end_date)
                    if grade.grade == 0:
                        grade.grade = getGrade(approval_percentage,grade.performance_points,assesment.min_grade,assesment.max_grade)
                    grade.evaluated = True
                    grade.save()

def getGrade(percentage,points,min_grade,max_grade):
    #calcula la nota
    if points >= percentage:#si obtiene mas que nota cuatro.
        x1 = percentage
        x2 = 100.0
        y1 = 4.0
        y2 = max_grade
        grade = (((points-x1)/(x2-x1))*(y2-y1))+y1
    else:#si los puntos son menores al porcentaje de aprobacion
        x1 = 0.0
        x2 = percentage
        y1 = min_grade
        y2 = 4.0
        grade = (((points-x1)/(x2-x1))*(y2-y1))+y1
    #print grade
    return grade

def getSkillPoints(kaid_student,configured_skills,t_begin,t_end):
    #Funcion que entrega el puntaje promedio de un estudiante, segun una configuracion de evaluacion 
    #y un rango de fechas.
    scores={'unstarted':0,'struggling':20,'practiced':40,'mastery1':60,'mastery2':80,'mastery3':100}
    points = 0
    for skill in configured_skills:
        #print 'id_skill_name_id %s'%(skill['id_skill_name_id'])
        try: 
            #print skill['id_skill_name_id']
            id_student_skills = Student_Skill.objects.filter(id_skill_name_id=skill['id_skill_name_id'],kaid_student_id=kaid_student)#.values('id_student_skill')
            for id_student_skill in id_student_skills:
                id_student_skill = id_student_skill.id_student_skill
        except: 
            print "no data id_student_skills"
        try: 
            last_level = Skill_Progress.objects.filter(id_student_skill_id=id_student_skill,date__gte = t_begin,date__lte = t_end).values('to_level').latest('date')
            points = points + scores[last_level['to_level']]
        except: 
            print 'no hay registros'
    points = points / len(configured_skills)
    return points