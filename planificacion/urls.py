from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getClassList, name='curriculum_propuesto'),
    url(r'^config$', views.saveShareConfig, name='editar_config'),
    url(r'^compartido$', views.getSharedClassList, name='planes_compartidos'),
    url(r'^guardar$', views.savePlanning, name='guardar_plan'),
    url(r'^editar$', views.editPlanning, name='editar_plan'),
    url(r'^copiar$', views.copyPlanning, name='copiar_plan'),
    url(r'^eliminar$', views.deletePlanning, name='borrar_plan'),
    url(r'^report$', views.getReport, name='obtener_datos'),
    url(r'^nivel/(?P<class_subj_id>[0-9]+)/$', views.getPlan, name='acceder_plan'),
    url(r'^nivel/compartido/inst/(?P<class_subj_id>[0-9]+)/$', views.getPlan, name='acceder_plan_compartido_inst'),
    url(r'^nivel/compartido/(?P<class_subj_id>[0-9]+)/$', views.getPlan, name='acceder_plan_compartido'),
]