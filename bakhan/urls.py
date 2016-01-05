from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'bakhan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bakhanapp.views.log', name='log'),
    url(r'^inicio/', 'bakhanapp.views.inicio', name='inicio'),
    url(r'^run/', 'bakhanapp.views.run_tests', name='run_tests'),
    url(r'^acceso/denegado/', 'bakhanapp.views.denegado', name='denegado'),
]
