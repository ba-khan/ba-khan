# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import os
import psycopg2, psycopg2.extras
import time
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jobGrade import getDomainLevel


conn = psycopg2.connect(database='bakhanDB',user='postgres',password='root', host='146.83.216.177')

def begin():
	#Job que envia correos al equipo de gestion del colegio una vez terminada una evaluacion.
	assesment_expired = getAssesment('Alonsus')
	#print assesment_expired
	for assesment in assesment_expired:
		print 'curso: %d%s, evaluacion: %s'%(assesment['level'],assesment['letter'],assesment['name'])
		domainLevel = getDomainLevel(assesment['id_assesment'],assesment['start_date'],assesment['end_date'])
		print domainLevel

def getAssesment(admin):
	lastDate = date.today() - timedelta(days=1)
	#print currentDate
	assesment_expired=[]#diccionario para la iteracion, ya que dictcursor da problemas al iterar.
	assesment = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)#hace que la respuesta a la consulta se entrege como diccionario.
	#cur.execute("SELECT * FROM public.bakhanapp_assesment")#consulto por todas las evaluciones existentes en bakhanDB
	assesment.execute("""SELECT 
		  bakhanapp_administrator.name, 
		  bakhanapp_institution.city, 
		  bakhanapp_class.level, 
		  bakhanapp_class.letter, 
		  bakhanapp_assesment.id_assesment, 
		  bakhanapp_assesment.name, 
		  bakhanapp_assesment.start_date, 
		  bakhanapp_assesment.end_date
		FROM 
		  public.bakhanapp_institution, 
		  public.bakhanapp_administrator, 
		  public.bakhanapp_class, 
		  public.bakhanapp_assesment
		WHERE 
		  bakhanapp_institution.id_institution = bakhanapp_class.id_institution_id AND
		  bakhanapp_administrator.id_institution_id = bakhanapp_institution.id_institution AND
		  bakhanapp_class.id_class = bakhanapp_assesment.id_class_id AND
		  bakhanapp_administrator.kaid_administrator = '%s'"""%(admin))#consulta las evaluaciones que ya vencieron.
	for evaluation in assesment: # guarda la informacion obtenida de las evaluaciones en un arreglo que ocntiene diccionario.
		assesment_expired.append({'id_assesment':evaluation['id_assesment'],'level': evaluation['level'],'letter':evaluation['letter'],
			'name':evaluation['name'],'start_date':evaluation['start_date'],'end_date':evaluation['end_date']})
	assesment.close()
	#print assesment_expired
	return assesment_expired


def main():
    begin()

if __name__ == "__main__":
    main()
