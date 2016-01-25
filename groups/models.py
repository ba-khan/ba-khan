from django.db import models

from bakhanapp.models import Group,Skill,Student

class Master_Group(models.Model):
	name = models.CharField(max_length=50)

class Group_Skill(models.Model):
	id_group = models.ForeignKey(Group)
	id_skill = models.ForeignKey(Skill)

class Sub_Group(models.Model):
	id_group = models.ForeignKey(Group)

class Student_Sub_Group(models.Model):
	id_sub_group = models.ForeignKey(Sub_Group)
	kaid_student = models.ForeignKey(Student)


