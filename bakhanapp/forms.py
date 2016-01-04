#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

class loginForm(forms.Form):
    usuario = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña', max_length=100)

