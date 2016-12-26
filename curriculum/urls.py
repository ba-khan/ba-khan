from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getCurriculum, name='getCurriculum'),
    url(r'^nuevo$', views.newChapter, name='nuevo_chapter'),
    url(r'^nuevotopic$', views.newTopic, name='nuevo_topic'),
    url(r'^nuevosubtopic$', views.newSubtopic, name='nuevo_subtopic'),
    url(r'^savevideo$', views.saveVideoExercise, name='save_videoexercise'),
    url(r'^deletevideoexercise$', views.deleteVideoExercise, name='deletevideoexercise'),
    url(r'^deletesubtopic$', views.deleteSubtopic, name='deletesubtopic'),
    url(r'^deletetopic$', views.deleteTopic, name='deletetopic'),
    url(r'^deletechapter$', views.deleteChapter, name='deletechapter'),
    url(r'^downloadCurriculum$', views.downloadCurriculum, name='downloadCurriculum'),

    url(r'^nivel/(?P<id_chapter>[0-9]+)/$', 'curriculum.views.getCurriculumNivel', name='getCurriculumNivel'),
]