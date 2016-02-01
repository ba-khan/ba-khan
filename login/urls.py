from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^authenticate/', views.authenticate, name='authenticate'),
    url(r'^access/rejected/', views.rejected, name='rejected'),
    url(r'^salir$', logout, {'template_name': 'login.html', }, name="salir"),
    #url(r'^historial/$', views.getMakedGroup, name='getMakedGroup'),
]