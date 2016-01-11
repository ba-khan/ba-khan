from django.db import models

# Create your models here.
class Institution(models.Model):
    id_institution = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15,null=True)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
class Administrator(models.Model):
    kaid_administrator = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    id_institution = models.ForeignKey(Institution)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
    class Admin:
        pass

class Student(models.Model):
    kaid_student = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    tutor_name = models.CharField(max_length=50,null=True)
    tutor_email = models.EmailField(max_length=50,null=True)
    points = models.IntegerField()
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
        
    class Admin:
        pass
    
class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
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
    name_spanish = models.CharField(max_length=150)
    id_subtopic_name = models.ForeignKey(Subtopic)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish

class Assesment_Config(models.Model):
    id_assesment_config = models.AutoField(primary_key=True)
    kaid_teacher = models.ForeignKey(Teacher)
    id_subject_name = models.ForeignKey(Subject)
    approval_percentage = models.IntegerField()
    top_score = models.IntegerField()
    name = models.CharField(max_length=100)
    
class Assesment_Skill(models.Model):
    id_assesment_skill = models.AutoField(primary_key=True)
    id_assesment_config = models.ForeignKey(Assesment_Config)
    id_skill_name = models.ForeignKey(Skill)
    
    class Meta:
        unique_together = ('id_assesment_config', 'id_skill_name')
    
class Assesment(models.Model):
    id_assesment = models.AutoField(primary_key=True)
    id_assesment_conf = models.ForeignKey(Assesment_Config)
    start_date = models.DateField()
    end_date = models.DateField()
    id_group = models.ForeignKey(Group)

class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    kaid_student = models.ForeignKey(Student)
    id_assesment = models.ForeignKey(Assesment)
    grade = models.IntegerField()
    teacher_grade = models.IntegerField(null=True)
    performance_points = models.IntegerField()
    effort_points = models.IntegerField()
    
    class Meta:
        unique_together = ('kaid_student', 'id_assesment')

class Video(models.Model):
    id_video_name = models.CharField(max_length=150,primary_key=True)
    name_spanish = models.CharField(max_length=150)
    id_subtopic_name = models.ForeignKey(Subtopic)
    
    def __unicode__(self): # __unicode__ on Python 2
        return self.name_esp

class Student_Skill(models.Model):
    id_student_skill = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    total_done = models.IntegerField()
    total_correct = models.IntegerField()
    streak = models.IntegerField()
    longest_streak = models.IntegerField()
    skill_progress = models.CharField(max_length=50)
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
    
    class Meta:
        unique_together = ('id_video_name', 'kaid_student')

class Skill_Attempt(models.Model):
    id_skill_attempt = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey(Student)
    errors = models.IntegerField()
    mission = models.CharField(max_length=150,null=True)
    time_taken = models.IntegerField()
    count_hints = models.IntegerField()
    skipped = models.BooleanField()
    points_earned = models.IntegerField()
    date = models.DateField()
    correct = models.BooleanField()
    
class Video_Playing(models.Model):
    id_video_playing = models.AutoField(primary_key=True)
    id_video_name = models.ForeignKey(Video)
    kaid_student = models.ForeignKey(Student)
    seconds_watched = models.IntegerField()
    points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    date = models.DateField()

class Skill_Progress(models.Model):
    id_skill_progress = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    to_level = models.CharField(max_length=50)
    from_level = models.CharField(max_length=50)
    date = models.DateField()