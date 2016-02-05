from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getAdministrators, name='getAdministrators'),
    url(r'^guardar$', views.saveAdministrator, name='guardar_administrador'),
    url(r'^eliminar$', views.deleteAdministrator, name='eliminar_administrador'),

]