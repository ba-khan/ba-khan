from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'bakhan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^',  include('login.urls', namespace="login")),#aplicacion login.
    
    #url(r'^inicio/$', 'bakhanapp.views.home', name='home'), #aplicacion bakhanapp se encarga del home.
    #esto era antes, ahora ya no hay home, pasa directo a "cursos"
    url(r'^inicio/$','bakhanapp.views.getTeacherClasses', name='cursos'),

    url(r'^inicio/cursos/(?P<id_class>[0-9]+)/grupos/', include('groups.urls', namespace="groups")),#aplicacion groups.
    url(r'^home/poblarbd/', include('populate.urls', namespace="populate")),#aplicacion para poblar la base de datos
    url(r'^inicio/curso/evaluacion/', include('evaluations.urls', namespace="evaluations")),#aplicacion para las evaluaciones

    url(r'^inicio/cursos/$', 'bakhanapp.views.getTeacherClasses', name='cursos'),
    url(r'^inicio/cursos/(?P<id_class>[0-9]+)/$', 'bakhanapp.views.getClassStudents', name='getClassStudents'),

    url(r'^inicio/pautas/', include('AssesmentConfigs.urls', namespace="AssesmentConfigs")),
    
    url(r'^inicio/cursos/(?P<id_class>[0-9]+)/contactos/', include('Contacts.urls', namespace="Contacts")), 

    url(r'^inicio/administradores/', include('ManagementTeam.urls', namespace="ManagementTeam")),
    url(r'^inicio/nomina/', include('classRoster.urls', namespace="classRoster")),
    url(r'^inicio/cursos/generateAssesmentExcel/(?P<id_assesment>[0-9]+)/$', 'bakhanapp.views.generateAssesmentExcel', name='generateAssesmentExcel'),
    

    #url(r'^home/teacher/classes/', 'bakhanapp.views.getTeacherClasses', name='getTeacherClasses'),
]