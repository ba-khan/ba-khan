from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getCurriculumProposed, name='curriculum_propuesto'),
    #url(r'^nuevo$', views.newChapter, name='nuevo_chapter'),
    #url(r'^nuevotopic$', views.newTopic, name='nuevo_topic'),
    #url(r'^nuevosubtopic$', views.newSubtopic, name='nuevo_subtopic'),
    #url(r'^savevideo$', views.saveVideoExercise, name='save_videoexercise'),
]