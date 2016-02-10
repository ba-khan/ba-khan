from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getContacts, name='getContacts'),
    url(r'^guardar/$', views.saveContact, name='guardar_contactos'),

]