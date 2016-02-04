# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import os
import psycopg2, psycopg2.extras
import time
import smtplib
from email.mime.text import MIMEText

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
		assesment_expired.append({'id_assesment': evaluation['id_assesment'],'id_assesment_config':evaluation['id_assesment_conf_id'],'start_date':evaluation['start_date'],'end_date':evaluation['end_date'],'max_grade':evaluation['max_grade'],'min_grade':evaluation['min_grade']})
	assesment.close()
	for ev in assesment_expired:
		per = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		per.execute('''SELECT 
				  bakhanapp_assesment_config.approval_percentage
				FROM 
				  public.bakhanapp_assesment_config
				WHERE 
				  bakhanapp_assesment_config.id_assesment_config = %d'''%(ev['id_assesment_config']))
		for p in per:
			approval_percentage = p['approval_percentage']
		per.close()
		skills_selected = skills(ev['id_assesment_config'])
		grades_involved = grades(evaluation['id_assesment'])
		for g in grades_involved:
			point = getStudentPoints(g['kaid_student_id'],skills_selected,ev['start_date'],ev['end_date'])
			grade = getGrade(approval_percentage,point,ev['min_grade'],ev['max_grade'])
			set_points = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			set_points.execute('update public.bakhanapp_grade set performance_points =%d,grade =%.2f where id_grade = %d '%(point,grade,g['id_grade']))
			conn.commit()
			set_points.close()
	send_mail()

def send_mail():
	fromaddr = 'bakhanacademy@gmail.com'
	toaddrs  = 'javierperezferrada@gmail.com'
	msg = 'There was a terrible error that occured and I wanted you to know!'


	# Credentials (if needed)
	username = 'bakhanacademy'
	password = 'a123456789b'

	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

	
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
    print grade
    return grade

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
			  bakhanapp_student_skill.id_skill_name_id = %s and
			  bakhanapp_skill_progress.date>= %s)''',[kaid_student,skill[0],kaid_student,skill[0],beginDate])
        for p in progress:
        	points = points + scores[p['to_level']]
        	#print p['to_level']
        progress.close()
    points = points / len(configured_skills)
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
	skills.close()
	return skills_selected

def grades(id_assesment):
	#entrega todas las notas asociadas a la evaluacion id_assesment
	grades_involved=[]
	grades = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	grades.execute('''SELECT * FROM 
			  public.bakhanapp_grade
			WHERE  
			  bakhanapp_grade.id_assesment_id = %d'''%(id_assesment))
	for g in grades:
		grades_involved.append({'id_grade':g['id_grade'],'grade':g['grade'],'kaid_student_id':g['kaid_student_id']})
	#print grades_involved
	grades.close()
	return grades_involved




def main():
    begin()

if __name__ == "__main__":
    main()