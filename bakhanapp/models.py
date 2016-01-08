from django.db import models

# Create your models here.
class Institution(models.Model):
    id_institution = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
class Administrator(models.Model):
    kaid_administrator = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=50)
    mail = models.EmailField()
    id_institution = models.ForeignKey(Institution)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
    class Admin:
        pass

class Student(models.Model):
    kaid_student = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    tutor_name = models.CharField(max_length=50)
    tutor_mail = models.EmailField()
    points = models.IntegerField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
        
    class Admin:
        pass
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    kaid_student_tutor = models.ForeignKey(Student,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
class Group_Student(models.Model):
    id_group = models.ForeignKey(Group)
    kaid_student = models.ForeignKey(Student)
    
class Teacher(models.Model):
    kaid_teacher = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=50)
    id_institution = models.ForeignKey(Institution)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name

class Class(models.Model):
    id_institution = models.ForeignKey(Institution)
    level = models.CharField(max_length=50)
    letter = models.CharField(max_length=2)
    kaid_teacher = models.ForeignKey(Teacher)
    
class Student_Class(models.Model):
    id_class = models.ForeignKey(Class)
    kaid_student = models.ForeignKey(Student)

class Subject(models.Model):
    id_subject = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

class Class_Subject(models.Model):
    id_class = models.ForeignKey(Class)
    id_subject = models.ForeignKey(Subject)
    kaid_teacher = models.ForeignKey(Teacher)

class Chapter(models.Model):
    id_chapter_name = models.CharField(max_length=50,primary_key=True)
    id_subject = models.ForeignKey(Subject)
    name_esp = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

class Topic(models.Model):
    id_topic_name = models.CharField(max_length=50,primary_key=True)
    id_chapter_name = models.ForeignKey(Chapter)
    name_esp = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

    
class Subtopic(models.Model):
    id_subtopic_name = models.CharField(max_length=50,primary_key=True)
    id_topic_name = models.ForeignKey(Topic)
    name_esp = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

class Skill(models.Model):
    id_skill_name = models.CharField(max_length=100,primary_key=True)
    name_esp = models.CharField(max_length=100)
    id_subtopic_name = models.ForeignKey(Subtopic)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

class Assesment_Config(models.Model):
    kaid_teacher = models.ForeignKey(Teacher)
    id_subject = models.ForeignKey(Subject)
    approval_percentage = models.IntegerField()
    top_score = models.IntegerField()
    assesment_name = models.CharField(max_length=50)
    
class Assesment_skill(models.Model):
    id_assesment_conf = models.ForeignKey(Assesment_Config)
    id_skill_name = models.ForeignKey(Skill)
    
class Assesment(models.Model):
    id_assesment_conf = models.ForeignKey(Assesment_Config)
    start_date = models.DateField()
    end_date = models.DateField()

class Grade(models.Model):
    kaid_student = models.ForeignKey(Student)
    id_assesment = models.ForeignKey(Assesment)
    grade = models.IntegerField()
    performance_point = models.IntegerField()
    effort_points = models.IntegerField()

class Video(models.Model):
    id_video_name = models.CharField(max_length=100,primary_key=True)
    name_esp = models.CharField(max_length=100)
    id_subtopic_name = models.ForeignKey(Subtopic)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

class Student_Skill(models.Model):
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    total_done = models.IntegerField()
    total_correct = models.IntegerField()
    streak = models.IntegerField()
    longest_streak = models.IntegerField()
    exercises_states = models.CharField(max_length=30)
    exercise_progress = models.CharField(max_length=30)

class Student_Video(models.Model):
    id_video_name = models.ForeignKey(Video)
    kaid_student = models.ForeignKey(Student)
    total_seconds_watched = models.IntegerField()
    total_points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()

class Skill_Attempt(models.Model):
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    errors = models.IntegerField()
    mission = models.CharField(max_length=100)
    time_taken = models.IntegerField()
    count_hints = models.IntegerField()
    skipped = models.BooleanField()
    
class Video_Playing(models.Model):
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    seconds_watched = models.IntegerField()
    points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    date = models.DateField()
