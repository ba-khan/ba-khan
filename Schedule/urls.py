from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getSchedules, name='getSchedules'),
    #url(r'^guardar/$', views.saveContact, name='guardar_contactos'),

]