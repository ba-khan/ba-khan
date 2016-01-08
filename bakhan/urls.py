from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout

urlpatterns = [
    # Examples:
    # url(r'^$', 'bakhan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bakhanapp.views.log', name='log'),
    url(r'^home/$', 'bakhanapp.views.getTeacherClasses', name='getTeacherClasses'),
    url(r'^home/teacher/$', 'bakhanapp.views.teacher', name='teacher'),
    #url(r'^home/teacher/classes/', 'bakhanapp.views.getTeacherClasses', name='getTeacherClasses'),
    url(r'^home/class/(?P<id_class>[0-9]+)/$', 'bakhanapp.views.getClassStudents', name='getClassStudents'),
    url(r'^authenticate/', 'bakhanapp.views.authenticate', name='authenticate'),
    url(r'^access/rejected/', 'bakhanapp.views.rejected', name='rejected'),
    url(r'^logout$', logout, {'template_name': 'log.html', }, name="logout"),
]

