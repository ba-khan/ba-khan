from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    #url(r'^$', views.getAdministrators, name='getSettings'),
    #url(r'^guardar$', views.saveAdministrator, name='guardar_horario'),
    #url(r'^nuevo$', views.newAdministrator, name='nuevo_horario'),
    #url(r'^eliminar$', views.deleteAdministrator, name='eliminar_horario'),
    url(r'^$', views.getSchedules, name='getSchedules'),
    url(r'^guardar$', views.saveAdministrator, name='guardar_administrador'),
    url(r'^nuevo$', views.newAdministrator, name='nuevo_administrador'),
    url(r'^eliminar$', views.deleteAdministrator, name='eliminar_administrador'),
]