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

    url(r'^salir$', logout, {'template_name': 'login.html', }, name="salir"),


    url(r'^authenticate/', 'bakhanapp.views.authenticate', name='authenticate'),
    url(r'^access/rejected/', 'bakhanapp.views.rejected', name='rejected'),
    url(r'^logout$', logout, {'template_name': 'log.html', }, name="salir"),
    url(r'^home/teacher/$', 'bakhanapp.views.teacher', name='teacher'),
    url(r'^home/teacher/assesment/configs$', 'bakhanapp.views.getTeacherAssesmentConfigs', name='getTeacherAssesmentConfigs'),
    url(r'^home/teacher/assesment/configs/new$', 'bakhanapp.views.newTeacherAssesmentConfig', name='newTeacherAssesmentConfig'),
    #url(r'^home/teacher/classes/', 'bakhanapp.views.getTeacherClasses', name='getTeacherClasses'),
]

