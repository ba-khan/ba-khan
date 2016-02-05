from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getAdministrators, name='getAdministrators'),
    url(r'^nueva$', views.newAdministrator, name='nuevo_administrador'),
    url(r'^eliminar/$', views.deleteAdministrator, name='eliminar_administrador'),
    url(r'^editar/$', views.editAdministrator, name='editar_administrador'),

]