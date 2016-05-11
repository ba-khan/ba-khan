from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getGroups, name='getGroups'),
    url(r'^historial/$', views.getMakedGroup, name='getMakedGroup'),
    url(r'^estudiantes/$', views.getStudentGroup, name='getStudentGroup'),
    url(r'^habilidades/$', views.getSkillGroup, name='getSkillGroup'),
    url(r'^ultimo/$', views.getLastGroup, name='getLastGroup'),
]