#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Assesment_Config,Assesment



class AssesmentConfigForm(forms.ModelForm):
    class Meta:
        model = Assesment_Config
        fields = ('id_assesment_config','kaid_teacher','id_subject_name','approval_percentage','top_score','name',)

class AssesmentForm(forms.ModelForm):
    class Meta:
        model = Assesment
        fields = ('id_assesment_conf','start_date','end_date','min_grade','max_grade','name',)