from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getStatistics, name='getStatistics'),
    #url(r'^seleccion$', views.selectSchedule, name='select_class_schedule'),
    #url(r'^eliminar$', views.deleteSchedule, name='eliminar_horario'),
    #url(r'^guardar$', views.saveSchedule, name='guardar_horario'),
]