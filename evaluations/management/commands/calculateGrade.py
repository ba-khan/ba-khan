import time
from datetime import date, timedelta
import json
from django.core.management.base import BaseCommand, CommandError
from bakhanapp.models import Grade,Assesment,Assesment_Config,Assesment_Skill,Student_Skill,Skill_Progress,Skill_Attempt
from bakhanapp.models import Subtopic_Skill,Subtopic_Video,Video_Playing
from django.db.models import Count,Sum,Max

class Command(BaseCommand):
    help = 'Calcula notas al pasar la fecha de la evaluacion'

    def handle(self, *args, **options):
        #funcion que se ejecutara al hacer python manage.py calculateGrade
        #currentDate = time.strftime("%Y-%m-%d") #fecha actual.
        percentageVideoTime = 0.2
        percentageExcerciceTime = 0.2
        percentageIncorrects = 0.6
        percentageHints = 0.35
        percentageVideo = 0.5
        percentageNothing = 0.15
        today = date.today() #- timedelta(days=1)
        #print lastDate
        assesments = Assesment.objects.all()#filter(end_date__lte=currentDate)
        for assesment in assesments:
            approval_percentage = Assesment_Config.objects.get(pk=assesment.id_assesment_conf_id).approval_percentage
            skills = Assesment_Skill.objects.filter(id_assesment_config_id=assesment.id_assesment_conf_id).values('id_skill_name_id')
            grades_involved = Grade.objects.filter(id_assesment_id=assesment.pk)
            students = grades_involved.values('kaid_student_id')
            incorrect = Skill_Attempt.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,correct=False,skipped=False,date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(incorrect=Count('kaid_student_id'))
            hints = Skill_Attempt.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,correct=False,skipped=False,
                date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(hints=Sum('count_hints'))
            videos = Skill_Attempt.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,correct=False,skipped=False,video=True,
                date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(videos=Count('kaid_student_id'))
            nothing = Skill_Attempt.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,correct=False,skipped=False,video=False,count_hints=0,
                date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(nothing=Count('kaid_student_id'))
            correct = Skill_Attempt.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,correct=True,date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(correct=Count('kaid_student_id'))
            time_excercice = Skill_Attempt.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(time=Sum('time_taken'))
            query1 = Subtopic_Skill.objects.filter(id_skill_name_id__in=skills).values('id_subtopic_name_id')
            query2 = Subtopic_Video.objects.filter(id_subtopic_name_id__in=query1).values('id_video_name_id')
            time_video = Video_Playing.objects.filter(kaid_student__in=students,id_video_name_id__in=query2,
                date__range=(assesment.start_date,assesment.end_date)).values('kaid_student_id').annotate(time=Sum('seconds_watched'))#en esta query falta que filtre por skills
            levels = Student_Skill.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,struggling=False,skill_progress__date__range=(assesment.start_date,assesment.end_date)
                ).values('kaid_student','id_student_skill','skill_progress__to_level','skill_progress__date'
                ).order_by('kaid_student','id_student_skill').distinct('kaid_student','id_student_skill')#,skill_progress__to_level='practiced'
            struggling = Student_Skill.objects.filter(kaid_student__in=students,id_skill_name_id__in=skills,struggling=True
                ).values('kaid_student','id_student_skill'
                ).order_by('kaid_student','id_student_skill')
            dictNothing = {}
            dictVideos = {}
            dictIncorrect = {}
            dictCorrect = {}
            dictTimeExcercice = {}
            dictTimeVideo = {}
            dictHints = {}
            for n in nothing:
                dictNothing[n['kaid_student_id']] = n['nothing']
            for v in videos:
                dictVideos[v['kaid_student_id']] = v['videos']
            for hin in hints:
                dictHints[hin['kaid_student_id']] = hin['hints']
            for inc in incorrect:
                dictIncorrect[inc['kaid_student_id']]=inc['incorrect']
            for cor in correct:
                dictCorrect[cor['kaid_student_id']] = cor['correct']
            for te in time_excercice:
                dictTimeExcercice[te['kaid_student_id']] = te['time']
            for vid in time_video:
                dictTimeVideo[vid['kaid_student_id']] = vid['time']
            for grade in grades_involved:
                if grade.evaluated == False:
                    grade.performance_points = getSkillPoints(grade.kaid_student_id,skills,assesment.start_date,assesment.end_date)
                    grade.grade = getGrade(approval_percentage,grade.performance_points,assesment.min_grade,assesment.max_grade)
                    try:
                        grade.excercice_time = dictTimeExcercice[grade.kaid_student_id]
                    except:
                        grade.excercice_time = 0
                    try:
                        grade.video_time = dictTimeVideo[grade.kaid_student_id]
                    except:
                        grade.video_time = 0
                    try:
                        grade.correct = dictCorrect[grade.kaid_student_id]
                    except:
                        grade.correct = 0
                    try:
                        grade.incorrect = dictIncorrect[grade.kaid_student_id]
                    except:
                        grade.incorrect = 0
                    try:
                        grade.hints = dictHints[grade.kaid_student_id]
                    except:
                        grade.hints = 0
                    try:
                        grade.videos = dictVideos[grade.kaid_student_id]
                    except:
                        grade.videos = 0
                    try:
                        grade.nothing = dictNothing[grade.kaid_student_id]
                    except:
                        grade.nothing = 0
                    try:
                        grade.struggling = struggling.filter(kaid_student_id=grade.kaid_student_id).count()
                    except:
                        grade.struggling = 0
                    try:
                        grade.practiced = levels.filter(kaid_student_id=grade.kaid_student_id,skill_progress__to_level='practiced').count()
                    except:
                        grade.practiced = 0
                    try:
                        grade.mastery1 = levels.filter(kaid_student_id=grade.kaid_student_id,skill_progress__to_level='mastery1').count()
                    except:
                        grade.mastery1 = 0
                    try:
                        grade.mastery2 = levels.filter(kaid_student_id=grade.kaid_student_id,skill_progress__to_level='mastery2').count()
                    except:
                        grade.mastery2 = 0
                    try:
                        grade.mastery3 = levels.filter(kaid_student_id=grade.kaid_student_id,skill_progress__to_level='mastery3').count()
                    except:
                        grade.mastery3 = 0
                    if assesment.end_date < today:
                        grade.evaluated = True
                    grade.save()
            #Aqui comienza el calculo de la bonificacion de empegno.        
            grades = Grade.objects.filter(id_assesment_id=assesment.pk)
            bestVideoTime = grades.aggregate(Max('video_time'))
            bestExcerciceTime = grades.aggregate(Max('excercice_time'))
            bestHints = grades.aggregate(Max('hints'))
            bestVideos = grades.aggregate(Max('videos'))
            bestNothing = grades.aggregate(Max('nothing'))
            for grade in grades:
                if grade.evaluated == False:
                    try:
                        video = grade.video_time / float(bestVideoTime['video_time__max']) 
                    except:
                        video = 0
                    try:
                        excercice = grade.excercice_time / float(bestExcerciceTime['excercice_time__max'])
                    except:
                        excercice = 0
                    try:
                        hints = grade.hints / float(bestHints['hints__max']) 
                    except:
                        hints = 0
                    try:
                        videos = grade.videos / float(bestVideos['videos__max'])
                    except:
                        videos = 0
                    try:    
                        nothing = grade.nothing / float(bestNothing['nothing__max'])
                    except:
                        nothing = 0
                    try:
                        incorrects = hints * percentageHints + videos * percentageVideo + nothing * percentageNothing
                        grade.effort_points = video * percentageVideoTime + excercice * percentageExcerciceTime + incorrects * percentageIncorrects
                    except:
                        grade.effort_points = 0.1
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
