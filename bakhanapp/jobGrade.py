# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import os
import psycopg2, psycopg2.extras
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


conn = psycopg2.connect(database='bakhanDB',user='postgres',password='root', host='146.83.216.177')

def begin():
	#Función que calcula y guarda las notas de los estudiantes al finalizar el tiempo de una evaluacion y envia los respesctivos correos.
	currentDate = time.strftime("%Y-%m-%d") #fecha actual.
	#print currentDate
	assesment_expired=[]#diccionario para la iteracion, ya que dictcursor da problemas al iterar.
	assesment = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	assesment.execute("SELECT * FROM public.bakhanapp_assesment where end_date <=%s",[currentDate])#consulta las evaluaciones que ya vencieron.
	for evaluation in assesment: # guarda la informacion obtenida de las evaluaciones en un arreglo que ocntiene diccionario.
		assesment_expired.append({'id_assesment': evaluation['id_assesment'],'id_assesment_config':evaluation['id_assesment_conf_id'],
			'start_date':evaluation['start_date'],'end_date':evaluation['end_date'],'max_grade':evaluation['max_grade'],'min_grade':evaluation['min_grade'],
			'name':evaluation['name']})
	assesment.close()
	for ev in assesment_expired:
		print 'evaluacion: %s, id_evaluacion: %d'%( ev['name'],ev['id_assesment'])
		per = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#consulta el porcentaje de aprovacion de la configuracion aplicada en la evaluacion.
		per.execute('''SELECT 
				  bakhanapp_assesment_config.approval_percentage
				FROM 
				  public.bakhanapp_assesment_config
				WHERE 
				  bakhanapp_assesment_config.id_assesment_config = %d'''%(ev['id_assesment_config']))
		for p in per:
			approval_percentage = p['approval_percentage']
		per.close()
		skills_selected,spanish_skills = skills(ev['id_assesment_config'])
		grades_involved = grades(ev['id_assesment'])
		video_times = getTimeVideo(ev['id_assesment'],ev['start_date'],ev['end_date'])#se obtienen todos los tiempos en video de los alumnos.
		excercice_times = getTimeExcercice(ev['id_assesment'],ev['start_date'],ev['end_date'])
		total_corrects = getTotalCorrect(ev['id_assesment'],ev['start_date'],ev['end_date'])
		total_incorrects = getTotalIncorrect(ev['id_assesment'],ev['start_date'],ev['end_date'])
		domainLevel = getDomainLevel(ev['id_assesment'],ev['start_date'],ev['end_date'])
		for g in grades_involved:
			point = getStudentPoints(g['kaid_student_id'],skills_selected,ev['start_date'],ev['end_date'])
			grade = getGrade(approval_percentage,point,ev['min_grade'],ev['max_grade'])
			set_points = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			print 'id_nota: %d, nota: %2.f'%(g['id_grade'],grade)
			set_points.execute("update public.bakhanapp_grade set performance_points =%d,grade =%.2f,evaluated = 'TRUE' where id_grade = %d "%
				(point,grade,g['id_grade']))
			conn.commit()
			set_points.close()
			#envia correos y whatsapp
			send_mail(g['name_student'],g['email_student'],point,grade,'Usted ha obtenido la siguiente calificación',ev['name'],
				spanish_skills,video_times.get(g['kaid_student_id'],None),excercice_times.get(g['kaid_student_id'],None),
				total_corrects.get(g['kaid_student_id'],None),total_incorrects.get(g['kaid_student_id'],None),
				domainLevel.get(g['kaid_student_id'],None))
			send_whatsapp(g['name_student'],g['phone_student'],'le informamos que ha obtenido la siguiente calificacion:',point,grade,spanish_skills,video_times.get(g['kaid_student_id'],None),excercice_times.get(g['kaid_student_id'],None),
				total_corrects.get(g['kaid_student_id'],None),total_incorrects.get(g['kaid_student_id'],None),
				domainLevel.get(g['kaid_student_id'],None))
			send_mail(g['name_tutor'],g['email_tutor'],point,grade,'Su pupilo ha obtenido la siguiente calificación',ev['name'],
				spanish_skills,video_times.get(g['kaid_student_id'],None),excercice_times.get(g['kaid_student_id'],None),
				total_corrects.get(g['kaid_student_id'],None),total_incorrects.get(g['kaid_student_id'],None),
				domainLevel.get(g['kaid_student_id'],None))
			send_whatsapp(g['name_tutor'],g['phone_tutor'],'le informamos que su pupilo ha obtenido la siguiente calificacion:',point,grade,spanish_skills,video_times.get(g['kaid_student_id'],None),excercice_times.get(g['kaid_student_id'],None),
				total_corrects.get(g['kaid_student_id'],None),total_incorrects.get(g['kaid_student_id'],None),
				domainLevel.get(g['kaid_student_id'],None))
def getDomainLevel(assesment,beginDate,endDate):
	domain = {}
	domainLevel = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	domainLevel.execute("""SELECT 
		  bakhanapp_grade.kaid_student_id, 
		  count(CASE WHEN bakhanapp_skill_progress.to_level='mastery1' THEN 1 ELSE null END) as mastery1,
		  count(CASE WHEN bakhanapp_skill_progress.to_level='mastery2' THEN 1 ELSE null END) as mastery2,
		  count(CASE WHEN bakhanapp_skill_progress.to_level='mastery3' THEN 1 ELSE null END) as mastery3,
		  count(CASE WHEN bakhanapp_skill_progress.to_level='practiced' THEN 1 ELSE null END) as practiced,
		  count(CASE WHEN bakhanapp_skill_progress.to_level='struggling' THEN 1 ELSE null END) as struggling
		FROM 
		  public.bakhanapp_grade, 
		  public.bakhanapp_assesment, 
		  public.bakhanapp_assesment_skill, 
		  public.bakhanapp_skill_progress, 
		  public.bakhanapp_student_skill
		WHERE 
		  bakhanapp_grade.kaid_student_id = bakhanapp_student_skill.kaid_student_id AND
		  bakhanapp_assesment.id_assesment = bakhanapp_grade.id_assesment_id AND
		  bakhanapp_assesment.id_assesment_conf_id = bakhanapp_assesment_skill.id_assesment_config_id AND
		  bakhanapp_assesment_skill.id_skill_name_id = bakhanapp_student_skill.id_skill_name_id AND
		  bakhanapp_student_skill.id_student_skill = bakhanapp_skill_progress.id_student_skill_id AND
		  bakhanapp_grade.id_assesment_id = %d AND 
		  bakhanapp_skill_progress.date >= '%s' AND
		  bakhanapp_skill_progress.date <= '%s' 
		GROUP BY 
		  bakhanapp_grade.kaid_student_id"""%(assesment,beginDate,endDate))
	for level in domainLevel:
		domain[level['kaid_student_id']]={'struggling':level['struggling'],'practiced':level['practiced'],'mastery1':level['mastery1'],'mastery2':level['mastery2'],'mastery3':level['mastery3']}
	domainLevel.close()
	return domain

def getTotalIncorrect(assesment,beginDate,endDate):
	incorrects = {}
	total_incorrects = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	total_incorrects.execute("""SELECT  
		  bakhanapp_grade.kaid_student_id, 
		   count(CASE WHEN bakhanapp_skill_attempt.correct='f' THEN 1 ELSE null END) as incorrect
		FROM 
		  public.bakhanapp_grade, 
		  public.bakhanapp_skill_attempt, 
		  public.bakhanapp_assesment_skill, 
		  public.bakhanapp_assesment
		WHERE 
		  bakhanapp_grade.kaid_student_id = bakhanapp_skill_attempt.kaid_student_id AND
		  bakhanapp_skill_attempt.id_skill_name_id = bakhanapp_assesment_skill.id_skill_name_id AND
		  bakhanapp_assesment.id_assesment = bakhanapp_grade.id_assesment_id AND
		  bakhanapp_assesment.id_assesment_conf_id = bakhanapp_assesment_skill.id_assesment_config_id AND
		  bakhanapp_grade.id_assesment_id = %d AND 
		  bakhanapp_skill_attempt.date >= '%s' AND
		  bakhanapp_skill_attempt.date <= '%s' AND
		  bakhanapp_skill_attempt.skipped = 'f'
		GROUP BY 
		  bakhanapp_grade.kaid_student_id"""%(assesment,beginDate,endDate))
	for total in total_incorrects:
		incorrects[total['kaid_student_id']]=total['incorrect']
	total_incorrects.close()
	return incorrects

def getTotalCorrect(assesment,beginDate,endDate):
	corrects = {}
	total_corrects = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	total_corrects.execute("""SELECT  
		  bakhanapp_grade.kaid_student_id, 
		  count(CASE WHEN bakhanapp_skill_attempt.correct THEN 1 ELSE null END) as correct
		FROM 
		  public.bakhanapp_grade, 
		  public.bakhanapp_skill_attempt, 
		  public.bakhanapp_assesment_skill, 
		  public.bakhanapp_assesment
		WHERE 
		  bakhanapp_grade.kaid_student_id = bakhanapp_skill_attempt.kaid_student_id AND
		  bakhanapp_skill_attempt.id_skill_name_id = bakhanapp_assesment_skill.id_skill_name_id AND
		  bakhanapp_assesment.id_assesment = bakhanapp_grade.id_assesment_id AND
		  bakhanapp_assesment.id_assesment_conf_id = bakhanapp_assesment_skill.id_assesment_config_id AND
		  bakhanapp_grade.id_assesment_id = %d AND 
		  bakhanapp_skill_attempt.date >= '%s' AND
		  bakhanapp_skill_attempt.date <= '%s' 
		GROUP BY 
		  bakhanapp_grade.kaid_student_id"""%(assesment,beginDate,endDate))
	for total in total_corrects:
		corrects[total['kaid_student_id']]=total['correct']
	total_corrects.close()
	return corrects

def getTimeExcercice(assesment,beginDate,endDate):
	times = {}
	excercice_time = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	excercice_time.execute("""SELECT 
		  bakhanapp_grade.kaid_student_id, 
		  sum(bakhanapp_skill_attempt.time_taken) as time
		FROM 
		  public.bakhanapp_grade, 
		  public.bakhanapp_skill_attempt
		WHERE 
		  bakhanapp_grade.kaid_student_id = bakhanapp_skill_attempt.kaid_student_id AND
		  bakhanapp_grade.id_assesment_id = %d AND 
		  bakhanapp_skill_attempt.date >= '%s' AND
		  bakhanapp_skill_attempt.date <= '%s' 
		GROUP BY 
		  bakhanapp_grade.kaid_student_id
"""%(assesment,beginDate,endDate))
	for time in excercice_time:
		times[time['kaid_student_id']]=time['time']
	excercice_time.close()
	return times

def getTimeVideo(assesment,beginDate,endDate):
	times = {}
	video_time = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	video_time.execute("""SELECT 
		  bakhanapp_grade.kaid_student_id, 
		  sum(bakhanapp_video_playing.seconds_watched) as time
		FROM 
		  public.bakhanapp_grade, 
		  public.bakhanapp_video_playing
		WHERE 
		  bakhanapp_grade.kaid_student_id = bakhanapp_video_playing.kaid_student_id AND
		  bakhanapp_grade.id_assesment_id = %d AND 
		  bakhanapp_video_playing.date >= '%s' AND
		  bakhanapp_video_playing.date <= '%s' 
		GROUP BY 
		  bakhanapp_grade.kaid_student_id;
"""%(assesment,beginDate,endDate))
	for time in video_time:
		times[time['kaid_student_id']]=time['time']
	video_time.close()
	return times



def send_whatsapp(name_student,phone,msg,point,grade,skills,time_video,time_excercice,total_corrects,total_incorrects,domain):
	os.system("""yowsup-cli demos -l 56955144957:S23B/CdXejaVQPWehwWmqwhnoaI= -s 569%d '%s,%s %d con una puntuacion de %d, las habilidades evaluadas fueron:\n %s \n
		tiempo en videos: %d \n tiempo en Ejercicios: %d \n Total Correctos: %d \n Total Incorrectos: %d \n 
		Practicado: %d, Nivel 1: %d, Nivel 2: %d, Dominados: %d, En Dificultad: %d '"""%(phone,name_student,msg,point,grade,skills,time_video,time_excercice,
			total_corrects,total_incorrects,domain['practiced'],domain['mastery1'],domain['mastery2'],domain['mastery3'],domain['struggling']))
	
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
			  bakhanapp_skill_progress.date>= %s)''',[kaid_student,skill['id_skill_name'],kaid_student,skill['id_skill_name'],beginDate])
        for p in progress:
        	points = points + scores[p['to_level']]
        	#print p['to_level']
        progress.close()
    points = points / len(configured_skills)
    return points




def skills(id_assesment_config):
	# entrega todas las skills involucradas en la evaluacion id_assesment_config
	skills_selected=[]
	spanish_skills = ''
	skills = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	skills.execute('''SELECT 
		  bakhanapp_assesment_skill.id_assesment_config_id, 
		  bakhanapp_assesment_skill.id_skill_name_id, 
		  bakhanapp_skill.name_spanish AS name
		FROM 
		  public.bakhanapp_assesment_skill, 
		  public.bakhanapp_skill
		WHERE 
		  bakhanapp_assesment_skill.id_skill_name_id = bakhanapp_skill.id_skill_name AND  
		  bakhanapp_assesment_skill.id_assesment_config_id = %d'''%(id_assesment_config))
	for s in skills:
		skills_selected.append({'id_assesment_config_id':s['id_assesment_config_id'],'id_skill_name':s['id_skill_name_id'],'name':s['name']})
		spanish_skills = spanish_skills +'\n'+ s['name'] 
	skills.close()
	return skills_selected,spanish_skills

def grades(id_assesment):
	#entrega todas las notas asociadas a la evaluacion id_assesment
	grades_involved=[]
	grades = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	grades.execute('''SELECT 
		  bakhanapp_student.name AS name_student, 
		  bakhanapp_student.email AS email_student,
		  bakhanapp_student.phone AS phone_student,  
		  bakhanapp_tutor.name AS name_tutor, 
		  bakhanapp_tutor.email AS email_tutor, 
		  bakhanapp_tutor.phone AS phone_tutor,
		  bakhanapp_grade.id_grade, 
		  bakhanapp_grade.grade, 
		  bakhanapp_grade.kaid_student_id,
		  bakhanapp_grade.evaluated
		FROM 
		  public.bakhanapp_grade, 
		  public.bakhanapp_student, 
		  public.bakhanapp_tutor
		WHERE 
		  bakhanapp_grade.kaid_student_id = bakhanapp_student.kaid_student AND
		  bakhanapp_grade.kaid_student_id = bakhanapp_tutor.kaid_student_child_id and
		  bakhanapp_grade.evaluated = 'FALSE' and
		  bakhanapp_grade.id_assesment_id = %d'''%(id_assesment))
	for g in grades:
		grades_involved.append({'id_grade':g['id_grade'],'grade':g['grade'],'kaid_student_id':g['kaid_student_id'],
			'name_student':g['name_student'],'email_student':g['email_student'],'phone_student':g['phone_student'],
			'name_tutor':g['name_tutor'],'email_tutor':g['email_tutor'],'phone_tutor':g['phone_tutor']})
	#print grades_involved
	grades.close()
	return grades_involved

def send_mail(name,email,points,grade,typeMsg,evaluation,skills,time_video,time_excercice,total_corrects,total_incorrects,domain):
	me = "bakhanacademy@gmail.com"
	you = email

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Evaluacion terminada."
	msg['From'] = me
	msg['To'] = you

	# Create the body of the message (a plain-text and an HTML version).
	text = ""
	html = """\
	<html>
	  <head></head>
	  <body>
		<div>
			<table width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#2c3747" style="background-color:#e2e2e2; 
			font-size:12px; font-family:Helvetica,Arial,Geneva,sans-serif">
				<tbody>
					<tr>
						<td>
							<table cellpadding="0" cellspacing="0" border="0" width="600" align="center" bgcolor="#e2e2e2">
								<tbody>
									<tr>
										<td>
											<table cellpadding="0" cellspacing="0" border="0" width="600" align="center">
												<tbody>
													<tr>
														<td>
															<table cellpadding="0" cellspacing="0" border="0" width="600" align="center">
																<tbody>
																	<tr>
																		<td>
																			<table cellpadding="0" cellspacing="0" border="0" width="600" align="center" 
																			bgcolor="#2c3747" style="margin-top:20px">
																				<tbody>
																					<tr>
																						<td>
																							<table cellpadding="10" cellspacing="0" border="0" width="600" 
																							align="center">
																								<tbody>
																									<tr>
																										<td align="center" width="175" valign="middle">
																										<a target="_blank">
																											<img src="http://www.khanacademy.org/imaget/ka-email-banner-logo.png?code=bWFzdGVyeV90YXNrX2VtYWlsX29wZW4KX2dhZV9iaW5nb19yYW5kb206U2ZfQWNMb29ROGVOc0taUndkVEgzdEc3dEhBSERLem0xN1JianJpcQ==" width="194" height="20" border="0" alt="Khan Academy"> 
																										</a>
																									</td>
																								</tr>
																							</tbody>
																						</table>
																					</td>
																				</tr>
																			</tbody>
																		</table>
																	</td>
																</tr>
															</tbody>
														</table>
													</td>
												</tr>
											</tbody>
										</table>
									</td>
								</tr>
							</tbody>
						</table>
						<table cellpadding="0" cellspacing="0" border="0" width="600" align="center">
							<tbody>
								<tr>
									<td>
										<table cellpadding="0" cellspacing="0" width="600" align="center" style="border-width:1px; border-spacing:0px;
										border-style:solid; border-color:#cccccc; border-collapse:collapse; background-color:#ffffff">
											<tbody>
												<tr>
													<td style="background-color:#f7f7f7; font-family:Helvetica Neue,Calibri,Helvetica,Arial,sans-serif; 
													font-size:15px; color:black; border-bottom:1px solid #ddd">
														<table cellpadding="0" cellspacing="0" border="0" width="500" align="center" style="margin:28px 50px; 
														font-size:15px; line-height:24px">
															<tbody>
																<tr>
																	<td>
																		<table width="500" cellpadding="0" cellspacing="0" border="0" style="">
																			<tbody>
																				<tr>
																					<td>
																						<img src="http://www.khanacademy.org/images/mission-badges/arithmetic-100x100.png?4" width="70" height="70" style="left:-10px"> 
																					</td>
																						<td>
																							<p style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:16px; line-height:24px; color:#666; margin:0 0 10px; font-size:14px; color:#333">
																								<strong>"""+name+""",</strong>
																									<br>"""+typeMsg+""" en evaluacion:<br>
																									"""+evaluation+"""</p>
																								</td>
																							</tr>
																						</tbody>
																					</table>
																				</td>
																			</tr>
																		</tbody>
																	</table>
																</td>
															</tr>
															<tr>
																<td>
																	<table cellpadding="0" cellspacing="0" border="0" width="500" align="center" 
																	style="margin:10px 50px">
																	<tbody>
																		<tr>
																			<td>
																				<a target="_blank"><div style="padding:20px 0" id="Cuadro_Azul">
																					<table width="500" cellpadding="0" cellspacing="0" border="0" 
																					style="background-color:#1C758A; border-radius:4px">
																					<tbody>
																						<tr>
																							<td style="padding:25px 5px; vertical-align:top">
																								<div style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; border:none; color:#fff; font-size:18px; text-decoration:none; line-height:28px">
																								<p>
																									<div>Puntos Obtenidos: """+str(points)+"""</div>
																								</p>
																								<p>
																									<div>Nota Obtenida: """+str(grade)+"""</div>
																								</p>
																								<p>
																									<div>Tiempo en videos: """+str(time_video)+"""</div>
																								</p>
																								<p>
																									<div>Tiempo en Ejercicios: """+str(time_excercice)+"""</div>
																								</p>
																								<p>
																									<div>Ejercicios correctos: """+str(total_corrects)+"""</div>
																								</p>
																								<p>
																									<div>Ejercicios incorrectos: """+str(total_incorrects)+"""</div>
																								</p>
																								<p>
																									<div>Nivel de dominio :Practicadas: """+str(domain['practiced'])+"""</div>
																								</p>
																								<p>
																									<div>Nivel de dominio :Nivel 1: """+str(domain['mastery1'])+"""</div>
																								</p>
																								<p>
																									<div>Nivel de dominio :Nivel 2: """+str(domain['mastery2'])+"""</div>
																								</p>
																								<p>
																									<div>Nivel de dominio :Practicadas: """+str(domain['mastery3'])+"""</div>
																								</p>
																								<p>
																									<div>Nivel de dominio :En dificultad: """+str(domain['struggling'])+"""</div>
																								</p>
																						</div>
																					</td>
																				</tr>
																			</tbody>
																		</table>
																	</div>
																</a>
																<a target="_blank" style="text-decoration:none">
																	<div style="font-family:"Helvetica Neue",Calibri,Helvetica,Arial,sans-serif; font-size:12px; line-height:20px; font-weight:bold; text-transform:uppercase; color:#777; margin-top:20px">Ejercicios a Evaluar:
																	</div>"""+skills+"""</a><br>
																<br>
																	</td>
																</tr>
															</tbody>
														</table>
													</td>
												</tr>
												
										</tbody>
									</table>
								</td>
							</tr>
						</tbody>
					</table>
				</div>'''

	  </body>
	</html>
	"""

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)


	try: 
		username = 'bakhanacademy@gmail.com'
		password = 'a123456789b'
		 
		# Enviando el correo
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		server.sendmail(me, you, msg.as_string())
		server.quit()
		print "Correo enviado" 
	except: 
		print """Error: el mensaje no pudo enviarse. 
		Compruebe que sendmail se encuentra instalado en su sistema"""




def main():
    begin()

if __name__ == "__main__":
    main()
