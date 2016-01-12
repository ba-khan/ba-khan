from django.contrib import admin

from models import Student,Administrator,Teacher, Class,Institution

admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Institution)