from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getGroups, name='getGroups'),
    url(r'^historial/$', views.getMakedGroup, name='getMakedGroup'),
    

]