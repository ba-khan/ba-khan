#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/budi
#	python manage.py populateTest 1>>/var/www/html/bakhanproyecto/logs/resultado_de_salida.log  2>>/var/www/html/bakhanproyecto/logs/err.log
cd /var/www/html/bakhanproyecto/
python manage.py populateTest
