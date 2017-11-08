
from django.db import models
from django.contrib.auth.models import User

from django.db.models.fields.related import ForeignKey

'''
class Auth_Group(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        db_table = 'auth_group'


class Auth_Group_Permissions(models.Model):
    group = models.ForeignKey(Auth_Group)
    permission = models.ForeignKey('Auth_Permission')

    class Meta:
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class Auth_Permission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Auth_User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        db_table = 'auth_user'


class Auth_User_Groups(models.Model):
    user = models.ForeignKey(Auth_User)
    group = models.ForeignKey(Auth_Group)

    class Meta:
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class Auth_User_User_Permissions(models.Model):
    user = models.ForeignKey(Auth_User)
    permission = models.ForeignKey(Auth_Permission)

    class Meta:
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

'''
class Administrator(models.Model):
    kaid_administrator = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=254, blank=True, null=True)
    id_institution = models.ForeignKey('Institution')
    phone = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_administrator'
        permissions = ( 
            ( "isAdmin", "Is Admin" ),
        )

    def __unicode__(self): # __unicode__ on Python 2
        return self.name
    
    class Admin:
        pass

class Assesment(models.Model):
    id_assesment = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    id_assesment_conf = models.ForeignKey('Assesment_Config')
    name = models.CharField(max_length=150)
    max_grade = models.IntegerField(blank=True, null=True)
    min_grade = models.IntegerField(blank=True, null=True)
    id_class = models.ForeignKey('Class', blank=True, null=True)
    approval_grade = models.IntegerField(blank=True, null=True)
    max_effort_bonus = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_assesment'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name


class Assesment_Config(models.Model):
    id_assesment_config = models.AutoField(primary_key=True)
    approval_percentage = models.IntegerField()
    name = models.CharField(max_length=100)
    id_subject_name = models.ForeignKey('Subject')
    kaid_teacher = models.ForeignKey('Teacher')
    importance_skill_level = models.IntegerField(blank=True, null=True)
    importance_completed_rec = models.IntegerField()
    applied = models.NullBooleanField()
    top_score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_assesment_config'


class Assesment_Skill(models.Model):
    id_assesment_skill = models.AutoField(primary_key=True)
    id_assesment_config = models.ForeignKey(Assesment_Config)
    id_skill_name = models.ForeignKey('Skill')
    id_subtopic_skill = models.ForeignKey('Subtopic_Skill', blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_assesment_skill'
        unique_together = (('id_assesment_config', 'id_skill_name', 'id_subtopic_skill'),)


class Chapter(models.Model):
    id_chapter_name = models.CharField(primary_key=True, max_length=150)
    name_spanish = models.CharField(max_length=150)
    id_subject_name = models.ForeignKey('Subject')
    index = models.IntegerField(blank=True, null=True)
    type_chapter = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_chapter'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish


class Chapter_Mineduc(models.Model):
    id_chapter_mineduc = models.AutoField(primary_key=True)
    index = models.IntegerField(blank=True, null=True)
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_chapter_mineduc'


class Class(models.Model):
    id_class = models.AutoField(primary_key=True)
    level = models.IntegerField()
    letter = models.CharField(max_length=2)
    year = models.IntegerField()
    id_institution = models.ForeignKey('Institution')
    additional = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_class'
        unique_together = (('id_institution', 'level', 'letter', 'additional'),)


class Class_Schedule(models.Model):
    id_class_schedule = models.AutoField(primary_key=True)
    id_schedule = models.ForeignKey('Schedule', blank=True, null=True)
    day = models.CharField(max_length=20, blank=True, null=True)
    kaid_teacher = models.ForeignKey('Teacher', blank=True, null=True)
    id_class = models.ForeignKey(Class, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_class_schedule'
        unique_together = (('id_schedule', 'day', 'kaid_teacher'),)


class Class_Subject(models.Model):
    id_class_subject = models.AutoField(primary_key=True)
    id_class = models.ForeignKey(Class)
    id_subject_name = models.ForeignKey('Subject')
    kaid_teacher = models.ForeignKey('Teacher')

    class Meta:
        db_table = 'bakhanapp_class_subject'
        unique_together = (('id_class', 'id_subject_name'),)


#Al parecer este modelo no es usado ya que solo existia en la BD y no en Django(?)
class Config_Skill(models.Model):
    id_assesment_config_id = models.IntegerField(blank=True, null=True)
    id_subtopic_skill_id = models.IntegerField(blank=True, null=True)
    id_config_skill = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'bakhanapp_config_skill'


class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    grade = models.FloatField()
    teacher_grade = models.FloatField(blank=True, null=True)
    performance_points = models.FloatField(blank=True, null=True)
    effort_points = models.FloatField(blank=True, null=True)
    id_assesment = models.ForeignKey(Assesment)
    kaid_student = models.ForeignKey('Student')
    comment = models.CharField(max_length=300, blank=True, null=True)
    evaluated = models.NullBooleanField()
    recomended_complete = models.IntegerField(blank=True, null=True)
    excercice_time = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    correct = models.IntegerField(blank=True, null=True)
    incorrect = models.IntegerField(blank=True, null=True)
    struggling = models.IntegerField(blank=True, null=True)
    practiced = models.IntegerField(blank=True, null=True)
    mastery1 = models.IntegerField(blank=True, null=True)
    mastery2 = models.IntegerField(blank=True, null=True)
    mastery3 = models.IntegerField(blank=True, null=True)
    hints = models.IntegerField(blank=True, null=True)
    videos = models.IntegerField(blank=True, null=True)
    nothing = models.IntegerField(blank=True, null=True)
    bonus_grade = models.FloatField(blank=True, null=True)
    unstarted = models.IntegerField(blank=True, null=True)
    total_recomended = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_grade'
        unique_together = (('kaid_student', 'id_assesment'),)


class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    kaid_student_tutor_id = models.CharField(max_length=40, blank=True, null=True)
    master = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_group'

    def __unicode__(self): # __unicode__ on Python 2
        return self.type


class Group_Student(models.Model):
    id_group = models.ForeignKey(Group)
    kaid_student = models.ForeignKey('Student')

    class Meta:
        db_table = 'bakhanapp_group_student'


class Institution(models.Model):
    id_institution = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    last_load = models.CharField(max_length=50, blank=True, null=True)
    key = models.CharField(max_length=20, blank=True, null=True)
    secret = models.CharField(max_length=20, blank=True, null=True)
    identifier = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self): # __unicode__ on Python 2
        return self.name

    class Meta:
        db_table = 'bakhanapp_institution'


class Planning(models.Model):
    id_planning = models.AutoField(primary_key=True)
    curso = models.CharField(max_length=20, blank=True, null=True)
    oa = models.CharField(max_length=500, blank=True, null=True)
    clase = models.CharField(max_length=50, blank=True, null=True)
    objetivo = models.CharField(max_length=500, blank=True, null=True)
    inicio = models.CharField(max_length=500, blank=True, null=True)
    ejerciciokhan = models.CharField(max_length=500, blank=True, null=True)
    videokhan = models.CharField(max_length=500, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    cierre = models.CharField(max_length=500, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_planning'
        unique_together = (('curso', 'oa'),)


class Related_Video_Exercise(models.Model):
    id_related = models.AutoField(primary_key=True)
    id_video = models.CharField(max_length=150, blank=True, null=True)
    id_exercise = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_related_video_exercise'


class Schedule(models.Model):
    id_schedule = models.AutoField(primary_key=True)
    start_time = models.CharField(max_length=10, blank=True, null=True)
    end_time = models.CharField(max_length=10, blank=True, null=True)
    id_institution = models.ForeignKey(Institution, blank=True, null=True)
    name_block = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_schedule'
        unique_together = (('start_time', 'end_time', 'id_institution'),)


class Skill(models.Model):
    id_skill_name = models.CharField(primary_key=True, max_length=150)
    name_spanish = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    url_skill = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_skill'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish


class Skill_Attempt(models.Model):
    id_skill_attempt = models.AutoField(primary_key=True)
    count_attempts = models.IntegerField()
    mission = models.CharField(max_length=150, blank=True, null=True)
    time_taken = models.IntegerField()
    count_hints = models.IntegerField()
    skipped = models.BooleanField()
    points_earned = models.IntegerField()
    date = models.DateTimeField()
    correct = models.BooleanField()
    id_skill_name = models.ForeignKey(Skill)
    kaid_student = models.ForeignKey('Student')
    problem_number = models.IntegerField()
    video = models.NullBooleanField()
    task_type = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_skill_attempt'
        unique_together = (('id_skill_name', 'kaid_student', 'problem_number'),)


class Skill_Log(models.Model):
    id_skill_log = models.AutoField(primary_key=True)
    correct = models.IntegerField(blank=True, null=True)
    incorrect = models.IntegerField(blank=True, null=True)
    id_grade = models.ForeignKey(Grade, blank=True, null=True)
    id_skill_name = models.ForeignKey(Skill, blank=True, null=True)
    skill_progress = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_skill_log'


class Skill_Planning(models.Model):
    id_skill_planning = models.AutoField(primary_key=True)
    id_planning = models.ForeignKey(Planning, blank=True, null=True)
    id_skill = models.ForeignKey(Skill, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_skill_planning'


class Skill_Progress(models.Model):
    id_skill_progress = models.AutoField(primary_key=True)
    to_level = models.CharField(max_length=50)
    from_level = models.CharField(max_length=50)
    date = models.DateTimeField()
    id_student_skill = models.ForeignKey('Student_Skill')

    class Meta:
        db_table = 'bakhanapp_skill_progress'
        unique_together = (('to_level', 'from_level', 'date', 'id_student_skill'),)

    class Meta:
        ordering = ['-date']


class Student(models.Model):
    kaid_student = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    id_institution = models.ForeignKey(Institution, blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    last_update = models.DateField(blank=True, null=True)
    new_student = models.NullBooleanField()

    class Meta:
        db_table = 'bakhanapp_student'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name

    class Admin:
        pass


class Student_Class(models.Model):
    id_student_class = models.AutoField(primary_key=True)
    id_class = models.ForeignKey(Class)
    kaid_student = models.ForeignKey(Student)

    class Meta:
        db_table = 'bakhanapp_student_class'
        unique_together = (('id_class', 'kaid_student'),)


class Student_Skill(models.Model):
    id_student_skill = models.AutoField(primary_key=True)
    total_done = models.IntegerField()
    total_correct = models.IntegerField()
    streak = models.IntegerField()
    longest_streak = models.IntegerField()
    last_skill_progress = models.CharField(max_length=50)
    total_hints = models.IntegerField()
    struggling = models.BooleanField()
    id_skill_name = models.ForeignKey(Skill)
    kaid_student_id = models.CharField(max_length=40)

    class Meta:
        db_table = 'bakhanapp_student_skill'


class Student_Video(models.Model):
    id_student_video = models.AutoField(primary_key=True)
    total_seconds_watched = models.IntegerField()
    total_points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    id_video_name = models.ForeignKey('Video')
    kaid_student = models.ForeignKey(Student)
    youtube_id = models.CharField(max_length=15)

    class Meta:
        db_table = 'bakhanapp_student_video'
        unique_together = (('id_video_name', 'kaid_student'),)


class Subject(models.Model):
    id_subject_name = models.CharField(primary_key=True, max_length=50)
    name_spanish = models.CharField(max_length=50)

    class Meta:
        db_table = 'bakhanapp_subject'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish


class Subtopic(models.Model):
    id_subtopic_name = models.CharField(primary_key=True, max_length=150)
    name_spanish = models.CharField(max_length=150)
    id_topic_name = models.ForeignKey('Topic')
    index = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_subtopic'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish


class Subtopic_Mineduc(models.Model):
    id_subtopic_mineduc = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    id_topic = models.ForeignKey('Topic_Mineduc', blank=True, null=True)
    ae_oe = models.CharField(db_column='AE_OE', max_length=500, blank=True, null=True)  # Field name made lowercase.
    index = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_subtopic_mineduc'
        unique_together = (('name', 'id_topic'),)


class Subtopic_Skill(models.Model):
    id_subtopic_skill = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill)
    id_subtopic_name = models.ForeignKey(Subtopic)

    class Meta:
        db_table = 'bakhanapp_subtopic_skill'
        unique_together = (('id_skill_name', 'id_subtopic_name'),)


class Subtopic_Skill_Mineduc(models.Model):
    id_subtopic_skill_mineduc = models.AutoField(primary_key=True)
    id_skill_name = models.ForeignKey(Skill, blank=True, null=True)
    id_subtopic_mineduc = models.ForeignKey(Subtopic_Mineduc, blank=True, null=True)
    id_tree = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_subtopic_skill_mineduc'


class Subtopic_Video(models.Model):
    id_subtopic_video = models.AutoField(primary_key=True)
    id_subtopic_name = models.ForeignKey(Subtopic)
    id_video_name = models.ForeignKey('Video')

    class Meta:
        db_table = 'bakhanapp_subtopic_video'
        unique_together = (('id_video_name', 'id_subtopic_name'),)


class Subtopic_Video_Mineduc(models.Model):
    id_subtopic_video_mineduc = models.AutoField(primary_key=True)
    id_video_name = models.ForeignKey('Video', blank=True, null=True)
    id_subtopic_name_mineduc = models.ForeignKey(Subtopic_Mineduc, blank=True, null=True)
    id_tree = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_subtopic_video_mineduc'


class Teacher(models.Model):
    kaid_teacher = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    id_institution = models.ForeignKey(Institution)

    class Meta:
        db_table = 'bakhanapp_teacher'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name


class Topic(models.Model):
    id_topic_name = models.CharField(primary_key=True, max_length=150)
    name_spanish = models.CharField(max_length=150)
    id_chapter_name = models.ForeignKey(Chapter)
    index = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_topic'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish


class Topic_Mineduc(models.Model):
    id_topic_mineduc = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    id_chapter = models.ForeignKey(Chapter_Mineduc, blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    descripcion_topic = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_topic_mineduc'
        unique_together = (('name', 'id_chapter'),)


class Tutor(models.Model):
    id_tutor = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    kaid_student_child = models.ForeignKey(Student)

    class Meta:
        db_table = 'bakhanapp_tutor'


class User_Profile(models.Model):
    kaid = models.CharField(max_length=40, blank=True, null=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        db_table = 'bakhanapp_user_profile'


class Video(models.Model):
    id_video_name = models.CharField(primary_key=True, max_length=150)
    name_spanish = models.CharField(max_length=150, blank=True, null=True)
    index = models.IntegerField(blank=True, null=True)
    url_video = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_video'

    def __unicode__(self): # __unicode__ on Python 2
        return self.name_spanish


class Video_Planning(models.Model):
    id_video_planning = models.AutoField(primary_key=True)
    id_planning = models.ForeignKey(Planning, blank=True, null=True)
    id_video = models.ForeignKey(Video, blank=True, null=True)

    class Meta:
        db_table = 'bakhanapp_video_planning'


class Video_Playing(models.Model):
    id_video_playing = models.AutoField(primary_key=True)
    seconds_watched = models.IntegerField()
    points_earned = models.IntegerField()
    last_second_watched = models.IntegerField()
    is_video_complete = models.BooleanField()
    date = models.DateTimeField()
    id_video_name = models.ForeignKey(Video)
    kaid_student = models.ForeignKey(Student)

    class Meta:
        db_table = 'bakhanapp_video_playing'
        unique_together = (('date', 'id_video_name', 'kaid_student'),)

