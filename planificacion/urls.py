from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getCurriculumProposed, name='curriculum_propuesto'),
    url(r'^guardar$', views.savePlanning, name='guardarplan'),
    url(r'^eliminar$', views.deletePlanning, name='eliminarplan'),
    url(r'^nivel/(?P<level>[0-9]+)/$', views.getCurriculumPropuesto, name='getCurriculumPropuesto'),
]