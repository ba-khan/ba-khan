from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getCurriculum, name='getCurriculum'),
    url(r'^nuevo$', views.newChapter, name='nuevo_chapter'),
    url(r'^nuevotopic$', views.newTopic, name='nuevo_topic'),
    url(r'^nuevosubtopic$', views.newSubtopic, name='nuevo_subtopic'),
    url(r'^savevideo$', views.saveVideoExercise, name='save_videoexercise'),
    #url(r'^getvideo$', views.getVideoExercise, name='get_videoexercise'),
    #url(r'^seleccion$', views.selectSuperStats, name='selectSuperStats'),
    #url(r'^comparacion$', views.compareSuperStats, name='compareSuperStats'),
    #url(r'^seleccioncurso$', views.selectClass, name='selectClass'),
    #url(r'^guardar$', views.saveSchedule, name='guardar_horario'),
]