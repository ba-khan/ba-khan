from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'bakhan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bakhanapp.views.login', name='login'),
    url(r'^inicio/$', 'bakhanapp.views.home', name='home'),
    url(r'^inicio/cursos/$', 'bakhanapp.views.getTeacherClasses', name='cursos'),
    url(r'^inicio/cursos/(?P<id_class>[0-9]+)/$', 'bakhanapp.views.getClassStudents', name='getClassStudents'),
    url(r'^inicio/cursos/(?P<id_class>[0-9]+)/grupos/', include('groups.urls', namespace="groups")),
    url(r'^inicio/curso/(?P<id_class>[0-9]+)/evaluaciones/nueva$', 'bakhanapp.views.newAssesment',name='nueva_evaluacion'),
    url(r'^inicio/curso/(?P<id_class>[0-9]+)/evaluaciones/nueva/(?P<id_assesment_config>[0-9]+)/$', 'bakhanapp.views.newAssesment2',name='nueva_evaluacion2'),
    url(r'^inicio/configuraciones/$', 'bakhanapp.views.getTeacherAssesmentConfigs', name='configuraciones'),
    url(r'^inicio/configuraciones/nueva$', 'bakhanapp.views.newAssesmentConfig', name='nueva_configuracion'),
    url(r'^inicio/configuraciones/eliminar/(?P<id_assesment_config>[0-9]+)/$', 'bakhanapp.views.deleteAssesmentConfig',name='eliminar_configuracion'),
    url(r'^inicio/configuraciones/editar/(?P<id_assesment_config>[0-9]+)/$', 'bakhanapp.views.editAssesmentConfig',name='editar_configuracion'),
    url(r'^home/poblarbd/$', 'bakhanapp.views.poblarBD', name='poblarBD'),
    url(r'^salir$', logout, {'template_name': 'login.html', }, name="salir"),
    
    url(r'^inicio/cursos/(?P<id_class>[0-9]+)/habilidades/$', 'bakhanapp.views.getSkillAssesment', name='getSkillAssesment'), 
    url(r'^inicio/curso/evaluacion/$', 'bakhanapp.views.newAssesment3', name='newAssesment3'),


    url(r'^authenticate/', 'bakhanapp.views.authenticate', name='authenticate'),
    url(r'^access/rejected/', 'bakhanapp.views.rejected', name='rejected'),

    #url(r'^home/teacher/classes/', 'bakhanapp.views.getTeacherClasses', name='getTeacherClasses'),
]

