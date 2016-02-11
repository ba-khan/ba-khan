from django.contrib import admin

from models import Student,Administrator,Teacher, Class,Institution,Group,Group_Student,Student_Class,Subject,Class_Subject,Chapter,Topic,Subtopic
from models import Skill,Assesment_Config,Assesment_Skill,Assesment,Grade,Video,Student_Skill,Student_Video,Skill_Attempt,Video_Playing,Skill_Progress

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
