from django.db import models

# Create your models here.
class Establecimiento(models.Model):
    nombre = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre

class Establecimiento(models.Model):
    nombre = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.nombre
    
class Entrada(models.Model):
    blog = models.ForeignKey(Blog)
    titulo = models.CharField(max_length=255)
    texto = models.TextField()
    fecha_publicacion = models.DateField()
    autores = models.ManyToManyField(Autor)
    n_comentarios = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __unicode__(self): # __unicode__ on Python 2
        return self.titulo