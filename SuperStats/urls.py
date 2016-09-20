from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getSuperStats, name='getSuperStats'),
    url(r'^seleccion$', views.selectSuperStats, name='selectSuperStats'),
    url(r'^seleccioncurso$', views.selectClass, name='selectClass'),
    #url(r'^guardar$', views.saveSchedule, name='guardar_horario'),
]