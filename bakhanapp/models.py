
from django.db import models
from django.contrib.auth.models import User

from django.db.models.fields.related import ForeignKey

class User_Profile(models.Model):
    kaid = models.CharField(max_length=40)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

class Institution(models.Model):
    id_institution = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15,null=True)
    last_load = models.CharField(max_length=25)
    key = models.CharField(max_length=20)
    secret = models.CharField(max_length=20)
    identifier = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
class Administrator(models.Model):
    kaid_administrator = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    id_institution = models.ForeignKey(Institution)
    
    class Meta:
        permissions = ( 
            ( "isAdmin", "Is Admin" ),
        )

    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
    class Admin:
        pass

class Student(models.Model):
    kaid_student = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    points = models.IntegerField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
        
    class Admin:
        pass
    
class Tutor(models.Model):
    id_tutor = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,null=True)
    phone = models.IntegerField(null=True)
    kaid_student_child = models.ForeignKey(Student)
    
class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    kaid_student_tutor = models.ForeignKey(Student,null=True)
    master = models.IntegerField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
class Group_Student(models.Model):
    id_group = models.ForeignKey(Group)
    kaid_student = models.ForeignKey(Student)
    
class Teacher(models.Model):
    kaid_teacher = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=50)
    id_institution = models.ForeignKey(Institution)
    email = models.EmailField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name

class Class(models.Model):
    id_class = models.AutoField(primary_key=True)
    id_institution = models.ForeignKey(Institution, related_name='id_institution_class')
    level = models.IntegerField()
    letter = models.CharField(max_length=2)
    year = models.IntegerField()

    class Meta:
        unique_together = ('id_institution', 'level', 'letter', 'year')
    
class Student_Class(models.Model):
    id_student_class = models.AutoField(primary_key=True)
    id_class = models.ForeignKey(Class)
    kaid_student = models.ForeignKey(Student)
    
    class Meta:
        unique_together = ('id_class', 'kaid_student')

class Subject(models.Model):
    id_subject_name = models.CharField(max_length=50,primary_key=True)
    name_spanish = models.CharField(max_length=50)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

class Class_Subject(models.Model):
    id_class_subject = models.AutoField(primary_key=True)
    id_class = models.ForeignKey(Class)
    id_subject_name = models.ForeignKey(Subject)
    kaid_teacher = models.ForeignKey(Teacher)
    
    class Meta:
        unique_together = ('id_class', 'id_subject_name')

class Chapter(models.Model):
    id_chapter_name = models.CharField(max_length=150,primary_key=True)
    id_subject_name = models.ForeignKey(Subject)
    name_spanish = models.CharField(max_length=150)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

class Topic(models.Model):
    id_topic_name = models.CharField(max_length=150,primary_key=True)
    id_chapter_name = models.ForeignKey(Chapter)
    name_spanish = models.CharField(max_length=150)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

    
class Subtopic(models.Model):
    id_subtopic_name = models.CharField(max_length=150,primary_key=True)
    id_topic_name = models.ForeignKey(Topic)
    name_spanish = models.CharField(max_length=150)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

class Skill(models.Model):
    id_skill_name = models.CharField(max_length=150,primary_key=True)
    name_spanish = models.CharField(max_length=150,null=True)
    name = models.CharField(max_length=150,null=True)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

class Assesment_Config(models.Model):
    id_assesment_config = models.AutoField(primary_key=True)
    kaid_teacher = models.ForeignKey(Teacher)
    id_subject_name = models.ForeignKey(Subject)
    approval_percentage = models.IntegerField()
    top_score = models.IntegerField()
    name = models.CharField(max_length=100)
    importance_skill_level=models.IntegerField()
    importance_completed_rec=models.IntegerField()
    applied=models.BooleanField()
    

    
class Assesment(models.Model):
    id_assesment = models.AutoField(primary_key=True)
    id_assesment_conf = models.ForeignKey(Assesment_Config)
    id_class = models.ForeignKey(Class)
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=150)
    max_grade = models.IntegerField()
    min_grade = models.IntegerField()
    approval_grade = models.IntegerField()
    max_effort_bonus = models.IntegerField()

    def __unicode__(self): # __unicode__ on Python 2
        return self.name

class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    kaid_student = models.ForeignKey(Student)
    id_assesment = models.ForeignKey(Assesment)
    grade = models.FloatField()
    teacher_grade = models.FloatField(null=True)
    performance_points = models.FloatField()
    effort_points = models.FloatField()
    recomended_complete = models.IntegerField(null=True)
    excercice_time = models.IntegerField(null=True)
    video_time = models.IntegerField(null=True)
    correct = models.IntegerField(null=True)
    incorrect = models.IntegerField(null=True)
    hints = models.IntegerField(null=True)
    videos = models.IntegerField(null=True)
    nothing = models.IntegerField(null=True)
    struggling = models.IntegerField(null=True)
    practiced = models.IntegerField(null=True)
    mastery1 = models.IntegerField(null=True)
    mastery2 = models.IntegerField(null=True)
    mastery3 = models.IntegerField(null=True)
    comment = models.CharField(max_length=300,null=True)
    evaluated = models.BooleanField(default=False)
    bonus_grade = models.FloatField(null=True)
    unstarted = models.IntegerField(null=True)
    total_recomended = models.IntegerField(null=True)
    
    class Meta:
        unique_together = ('kaid_student', 'id_assesment')

class Video(models.Model):
    id_video_name = models.CharField(max_length=150,primary_key=True)
    name_spanish = models.CharField(max_length=150,null=True)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

class Student_Skill(models.Model):
    id_student_skill = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    total_done = models.IntegerField()
    total_correct = models.IntegerField()
    streak = models.IntegerField()
    longest_streak = models.IntegerField()
    last_skill_progress = models.CharField(max_length=50)
    total_hints = models.IntegerField()
    struggling = models.BooleanField()
    
    class Meta:
        unique_together = ('id_skill_name', 'kaid_student')
        
class Student_Video(models.Model):
    id_student_video = models.AutoField(primary_key=True)
    id_video_name = models.ForeignKey(Video)
    kaid_student = models.ForeignKey(Student)
    total_seconds_watched = models.IntegerField()
    total_points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    youtube_id = models.CharField(max_length=15)
    
    class Meta:
        unique_together = ('id_video_name', 'kaid_student')

class Skill_Attempt(models.Model):
    id_skill_attempt = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    problem_number = models.IntegerField()
    count_attempts = models.IntegerField()
    mission = models.CharField(max_length=150,null=True)
    time_taken = models.IntegerField()
    count_hints = models.IntegerField()
    skipped = models.BooleanField()
    points_earned = models.IntegerField()
    date = models.DateTimeField()
    correct = models.BooleanField()
    video = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('id_skill_name', 'kaid_student', 'problem_number')
    
class Video_Playing(models.Model):
    id_video_playing = models.AutoField(primary_key=True)
    id_video_name = models.ForeignKey(Video)
    kaid_student = models.ForeignKey(Student)
    seconds_watched = models.IntegerField()
    points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    date = models.DateTimeField()

class Skill_Progress(models.Model):
    id_skill_progress = models.AutoField(primary_key=True)
    id_student_skill = models.ForeignKey(Student_Skill)
    to_level = models.CharField(max_length=50)
    from_level = models.CharField(max_length=50)
    date = models.DateTimeField()
    
    class Meta:
      ordering = ['-date']

class Subtopic_Video(models.Model):
    id_subtopic_video = models.AutoField(primary_key=True)
    id_video_name = models.ForeignKey(Video)
    id_subtopic_name = models.ForeignKey(Subtopic)
    
    class Meta:
        unique_together = ('id_video_name', 'id_subtopic_name')
        
class Subtopic_Skill(models.Model):
    id_subtopic_skill = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    id_subtopic_name = models.ForeignKey(Subtopic)
    
    class Meta:
        unique_together = ('id_skill_name', 'id_subtopic_name')
        
class Assesment_Skill(models.Model):
    id_assesment_skill = models.AutoField(primary_key=True)
    id_assesment_config = models.ForeignKey(Assesment_Config)
    id_skill_name = models.ForeignKey(Skill)
    id_subtopic_skill = models.ForeignKey(Subtopic_Skill)
    
    class Meta:
        unique_together = ('id_assesment_config', 'id_skill_name')


class Skill_Log(models.Model):
    id_skill_log = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    correct = models.IntegerField(null=True)
    incorrect =  models.IntegerField(null=True)
    id_grade = models.ForeignKey(Grade)
    skill_progress = models.CharField(max_length=20)
