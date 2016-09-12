from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getSchedules, name='getSchedules'),
    url(r'^nuevo$', views.newSchedule, name='nuevo_horario'),
    url(r'^eliminar$', views.deleteSchedule, name='eliminar_horario'),
    url(r'^guardar$', views.saveSchedule, name='guardar_horario'),
    #url(r'^clase$', views.getClass, name='obtener_clase'),
]