from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getClassList, name='curriculum_propuesto'),
    url(r'^guardar$', views.savePlanning, name='guardar_plan'),
    url(r'^editar$', views.editPlanning, name='editar_plan'),
    url(r'^eliminar$', views.deletePlanning, name='borrar_plan'),
    url(r'^nivel/(?P<class_subj_id>[0-9]+)/$', views.getPlan, name='acceder_plan'),
]