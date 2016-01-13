#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Assesment_Config

class loginForm(forms.Form):
    usuario = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña', max_length=100)

class AssesmentConfigForm(forms.ModelForm):
    class Meta:
        model = Assesment_Config
        fields = ('id_assesment_config','kaid_teacher','id_subject_name','approval_percentage','top_score','name',)