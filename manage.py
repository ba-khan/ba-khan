#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bakhan.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


##-------------------------------------------------------------------------------
## \mainpage Documentación de Ba-khan
## 
## \section intro_sec Primera sección
## 
## Aqui va la introducción
## 
## \section install_sec Instalación
## 
## \subsection step1 Paso 1: Ejemplo
## 
## Ejemplo de estructura para la página principal de la documentación
##
