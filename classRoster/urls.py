from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getRoster, name='getRoster'),
    url(r'^newTeacherClass$', views.newTeacherClass, name='newTeacherClass'),
    url(r'^newClass$', views.newClass, name='newClass'),
    #url(r'^historial/$', views.getMakedGroup, name='getMakedGroup'),
    #url(r'^estudiantes/$', views.getStudentGroup, name='getStudentGroup'),
    #url(r'^habilidades/$', views.getSkillGroup, name='getSkillGroup'),
]