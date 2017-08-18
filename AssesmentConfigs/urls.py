from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.getTeacherAssesmentConfigs, name='getTeacherAssesmentConfigs'),
    url(r'^nueva$', views.newAssesmentConfig, name='nueva_configuracion'),
    url(r'^curriculo$', views.retrieveCurriculumTree, name='recibir_curriculo'),
    url(r'^plan$', views.retrievePlanTree, name='recibir_clase'),
    url(r'^eliminar/(?P<id_assesment_config>[0-9]+)/$', views.deleteAssesmentConfig, name='eliminar_configuracion'),
    url(r'^editar/(?P<id_assesment_config>[0-9]+)/$', views.editAssesmentConfig, name='editar_configuracion'),

]