""" This file... """

from django.contrib import admin

from bakhanapp.models import Student, Administrator
from bakhanapp.models import Teacher, Class, Institution, Group
from bakhanapp.models import Group_Student, Student_Class
from bakhanapp.models import Subject, Class_Subject, Chapter
from bakhanapp.models import Topic, Subtopic, Skill, Assesment_Config
from bakhanapp.models import Assesment_Skill, Assesment
from bakhanapp.models import Grade, Video, Student_Skill, Student_Video
from bakhanapp.models import Skill_Attempt, Video_Playing, Skill_Progress

admin.site.register(Skill_Progress)
admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Institution)
admin.site.register(Group)
admin.site.register(Group_Student)
admin.site.register(Student_Class)
admin.site.register(Subject)
admin.site.register(Class_Subject)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Skill)
admin.site.register(Assesment_Config)
admin.site.register(Assesment_Skill)
admin.site.register(Assesment)
admin.site.register(Grade)
admin.site.register(Video)
admin.site.register(Student_Skill)
admin.site.register(Student_Video)
admin.site.register(Skill_Attempt)
admin.site.register(Video_Playing)
