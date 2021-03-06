"""
WSGI config for bakhan project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import sys
import os

from django.core.wsgi import get_wsgi_application

path = '/var/www/html/bakhanprueba'

if path not in sys.path:
  sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="bakhan.settings"

application = get_wsgi_application()

