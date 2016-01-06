from django.db import models

# Create your models here.
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
    
class Configuracion_Evaluacion(models.Model):
    id_profesor = models.ForeignKey(Profesor)
    id_materia = models.ForeignKey(Materia)
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

class Asignatura(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

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