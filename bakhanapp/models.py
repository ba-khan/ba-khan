from django.db import models

# Create your models here.
class Administrador(models.Model):
    kaid = models.CharField(max_length=30,primary_key=True)
    nombre = models.CharField(max_length=50)
    mail = models.EmailField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
    class Admin:
        pass

class Estudiante(models.Model):
    kaid = models.CharField(max_length=30,primary_key=True)
    nombre = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    nombreApoderado = models.CharField(max_length=50)
    mailApoderado = models.EmailField()
    observacion = models.CharField(max_length=300)
    puntos = models.IntegerField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
        
    class Admin:
        pass
    
    

class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    kaid_est_tutor = models.ForeignKey(Estudiante,null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
class Grupo_Estudiante(models.Model):
    id_grupo = models.ForeignKey(Grupo)
    kaid_est = models.ForeignKey(Estudiante)

class Mision(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

class Habilidad(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
 
class Estudiante_Habilidad(models.Model):
    id_habilidad = models.ForeignKey(Habilidad)
    kaid_est = models.ForeignKey(Estudiante)
    total_done = models.IntegerField()
    total_correct = models.IntegerField()
    streak = models.IntegerField()
    longest_streak = models.IntegerField()
    id_mision = models.ForeignKey(Mision,null=True) #nulleable
    exercises_states = models.CharField(max_length=30)
    exercise_progress = models.CharField(max_length=30)
    
class Nota(models.Model):
    kaid_est = models.CharField(max_length=30)
    id_evaluacion = models.CharField(max_length=30)
    nota = models.IntegerField()
    puntos_desempeno = models.IntegerField()
    puntos_empeno = models.IntegerField()

class Establecimiento(models.Model):
    nombre = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
class Profesor(models.Model):
    kaid = models.CharField(max_length=30,primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

class Curso(models.Model):
    establecimiento = models.ForeignKey(Establecimiento)
    nivel = models.CharField(max_length=50)
    letra = models.CharField(max_length=2)
    profesor = models.ForeignKey(Profesor)
        
    def __unicode__(self): # __unicode__ on Python 2
        return self.nivel
  
class Asignatura(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre  
    
  
class Configuracion_Evaluacion(models.Model):
    id_profesor = models.ForeignKey(Profesor)
    id_asignatura = models.ForeignKey(Asignatura)
    porcentaje_exigencia = models.IntegerField()
    puntaje_max = models.IntegerField()

    
class Evaluacion_habilidad(models.Model):
    id_conf_ev = models.ForeignKey(Configuracion_Evaluacion)
    id_habilidad = models.ForeignKey(Habilidad)
    
class Evaluacion(models.Model):
    id_conf_ev = models.ForeignKey(Configuracion_Evaluacion)
    fecha_termino = models.DateField()
    
class Video(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

class Estudiante_Video(models.Model):
    id_video = models.ForeignKey(Video)
    kaid_est = models.ForeignKey(Estudiante)
    seconds_watched = models.IntegerField()
    points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.id_video


class Estudiante_Curso(models.Model):
    id_curso = models.ForeignKey(Curso)
    id_estudiante = models.ForeignKey(Estudiante)

class Curso_Asignatura(models.Model):
    id_curso = models.ForeignKey(Curso)
    id_asignatura = models.ForeignKey(Asignatura)
    id_profesor = models.ForeignKey(Profesor)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

class Unidad(models.Model):
    id_unidad = models.ForeignKey(Asignatura)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

class Tema(models.Model):
    id_unidad = models.ForeignKey(Unidad)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
class Subtema(models.Model):
    id_tema = models.ForeignKey(Tema)
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre