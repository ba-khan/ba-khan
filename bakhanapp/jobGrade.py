# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import os
import psycopg2, psycopg2.extras
import time

conn = psycopg2.connect(database='bakhanDB',user='postgres',password='root', host='146.83.216.177')

def begin():
	#Funcion que calcula y guarda las notas de los estudiantes al finalizar el tiempo de una evaluacion.
	currentDate = time.strftime("%Y-%m-%d") #fecha actual.
	#print currentDate
	assesment_expired=[]#diccionario para la iteracion, ya que dictcursor da problemas al iterar.
	assesment = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	assesment.execute("SELECT * FROM public.bakhanapp_assesment where end_date =%s",[currentDate])#consulta las evaluaciones que vencen hoy.
	for evaluation in assesment: # itero sobre cada evaluacion que vence hoy.
		assesment_expired.append({'id_assesment': evaluation['id_assesment'],'id_assesment_config':evaluation['id_assesment_conf_id']})

	for ev in assesment_expired:
		print ev['id_assesment_config']
		#print "Nombre ,id ,fecha: %s, %d,%s " % (row['name'],row['id_assesment'],row['end_date'])
		skills_selected = skills(ev['id_assesment_config'])
		for s in skills_selected:
			print s
		#grades_involved = grades(evaluation['id_assesment'])
		#for g in grades_involved:
			#point = getStudentPoints(g['kaid_student_id'],skills_selected,evaluation['start_date'],evaluation['end_date'])
	


def getStudentPoints(kaid_student,configured_skills,beginDate,endDate):
    #entrega el promedio de la puntuacion obtenida por el alumno kaid_student en las habilidades skills 
    #print 'puntos entre %s  %s'%(dateBegin,dateEnd)
    scores={'unstarted':0,'struggling':20,'practiced':40,'mastery1':60,'mastery2':80,'mastery3':100}
    #configured_skills = Assesment_Skill.objects.filter(id_assesment_config=id_assesment_conf).values('id_skill_name')#skills en la configuracion actual
    points = 0
    for skill in configured_skills:
        #id_student_skills = Student_Skill.objects.filter(id_skill_name_id=skill['id_skill_name'],kaid_student_id=kaid_student).values('id_student_skill')
        #last_level = Skill_Progress.objects.filter(id_student_skill_id=id_student_skills[0]['id_student_skill'],date__gte = t_begin,date__lte = t_end).latest('date').values('to_level')
        progress = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        progress.execute('''SELECT 
  bakhanapp_student_skill.kaid_student_id, 
  bakhanapp_skill_progress.to_level,
  bakhanapp_skill_progress.date, 
  bakhanapp_student_skill.id_skill_name_id
FROM 
  public.bakhanapp_student_skill, 
  public.bakhanapp_skill_progress
WHERE 
  bakhanapp_student_skill.id_student_skill = bakhanapp_skill_progress.id_student_skill_id AND
  bakhanapp_student_skill.kaid_student_id = %s AND 
  bakhanapp_student_skill.id_skill_name_id = %s and
  bakhanapp_skill_progress.date = (select max(bakhanapp_skill_progress.date) from public.bakhanapp_student_skill, 
  public.bakhanapp_skill_progress
WHERE 
  bakhanapp_student_skill.id_student_skill = bakhanapp_skill_progress.id_student_skill_id AND
  bakhanapp_student_skill.kaid_student_id = %s AND 
  bakhanapp_student_skill.id_skill_name_id = %s)''',[kaid_student,skill['id_skill_name_id'],kaid_student,skill['id_skill_name_id']])
        for p in progress:
        	points = points + scores[p['to_level']]
        	print p['to_level']
    return points




def skills(id_assesment_config):
	# entrega todas las skills involucradas en la evaluacion id_assesment_config
	skills_selected=[]
	skills = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	skills.execute('''SELECT 
			  bakhanapp_assesment_skill.id_skill_name_id
			FROM 
			  public.bakhanapp_assesment_config, 
			  public.bakhanapp_assesment_skill
			WHERE 
			  bakhanapp_assesment_config.id_assesment_config = bakhanapp_assesment_skill.id_assesment_config_id AND  
			  bakhanapp_assesment_config.id_assesment_config = %d'''%(id_assesment_config))
	for s in skills:
		skills_selected.append(s)
	return skills_selected

def grades(id_assesment):
	#entrega todas las notas asociadas a la evaluacion id_assesment
	grades = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	grades.execute('''SELECT * FROM 
			  public.bakhanapp_grade
			WHERE  
			  bakhanapp_grade.id_assesment_id = %d'''%(id_assesment))
	return grades




def main():
    begin()

if __name__ == "__main__":
    main()