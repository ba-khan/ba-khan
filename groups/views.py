from django.shortcuts import render
from bakhanapp.models import Group
from django.utils import timezone
# Create your views here.
def groups(request,id_class):
	return render(request, 'groups.html')

def save_groups(request,id_class):
	#Funcion de prueba que crea un nuevo grupo con datos de prueba
	g = Group()
	g.name = 'test'
	g.type = 'avanzado'
	g.start_date = timezone.now()
	g.end_date = timezone.now()
	g.kaid_student_tutor_id = 'kaid_1097501097555535353578558'
	g.save()
	return render (request,'groups.html')

def make_groups(request,id_class):
	#Funcion que entrega un arreglo con los estudiantes y su nivel de agrupamiento.
	students = Student.objects.filter(kaid_student__in=Student_Class.objects.filter(id_class_id=id_class).values('kaid_student'))#retorna todos los estudiantes de un curso
	if request.method == 'POST':
        args = request.POST
        for s in students:
        	#Por cada estudiante en id_class, se obtiene su agrupacion.
			s.type = getTypeStudent(s.kaid_student,args) #args debe contener todas las id de las skill seleccionadas para el agrupamiento.
        return s

def getTypeStudent(request,kaid_student,args):
	#Funcion que entrega en que nivel grupo debe ser organizado un estudiante
	#de acuerdo a su nivel en las skills seleccionadas por el profesor.
	#skills = Group_Skill.objects.filter(id_group_id=id_group)
	for skill in args:
		student_progress = Student_Skill.objects.filter(id_skill_name_id=skill['id_skill_id']).values('last_skill_progress')
		if student_progress == 'struggling' or student_progress == 'unstarted':
			return 'reinforcement'
		if student_progress == 'mastery1' or student_progress == 'mastery2':
			return 'intermediate'
		else:
			return 'advanced'



