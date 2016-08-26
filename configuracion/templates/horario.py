{% extends 'home.html' %}

{% load static %}

{% block title %}Administración de Horarios{% endblock %}

{% block body2 %}

<script src="{% static 'js/editablegrid.js' %}"></script>
<script src="{% static 'js/editablegrid_renderers.js' %}"></script>
<script src="{% static 'js/editablegrid_editors.js' %}"></script>
<script src="{% static 'js/editablegrid_validators.js' %}"></script>
<script src="{% static 'js/editablegrid_utils.js' %}"></script>
<script src="{% static 'js/editablegrid_charts.js' %}"></script>

<link rel="stylesheet" type="text/css" href="{% static 'css/editablegrid.css'%}">

<link rel="stylesheet" type="text/css" href="{% static 'css/contacts.css'%}">



{% endblock %}