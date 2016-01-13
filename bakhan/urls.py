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
    url(r'^inicio/configuraciones/$', 'bakhanapp.views.getTeacherAssesmentConfigs', name='configuraciones'),
    url(r'^inicio/configuraciones/nueva$', 'bakhanapp.views.newAssesmentConfig', name='nueva_configuracion'),
    url(r'^inicio/configuraciones/eliminar/(?P<id_assesment_config>[0-9]+)/$', 'bakhanapp.views.deleteAssesmentConfig',name='eliminar_configuracion'),

    url(r'^salir$', logout, {'template_name': 'login.html', }, name="salir"),


    url(r'^authenticate/', 'bakhanapp.views.authenticate', name='authenticate'),
    url(r'^access/rejected/', 'bakhanapp.views.rejected', name='rejected'),

    #url(r'^home/teacher/classes/', 'bakhanapp.views.getTeacherClasses', name='getTeacherClasses'),
]

