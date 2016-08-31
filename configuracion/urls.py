from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getSchedules, name='getSchedules'),
    url(r'^nuevo$', views.newSchedule, name='nuevo_horario'),
    url(r'^eliminar$', views.deleteSchedule, name='eliminar_horario'),
]