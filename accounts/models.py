from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ClassRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    req_to = models.CharField(max_length=100, default='')
    msg = models.CharField(max_length=1500, default='')
    time = models.DateTimeField(auto_now_add=True)


class CoursesOffered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default='')
    study_level = models.CharField(max_length=100, default='')
    subject = models.CharField(max_length=100,)

    def __str__(self):
        return self.user.username

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1500, default='')
    expertise = models.CharField(max_length=100, default='')
    edu_qualification = models.CharField(max_length=100, default='')
    tutor_image = models.ImageField(upload_to='profile_image', blank=True)
    charge_hr = models.IntegerField(default=100)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1500, default='')
    school = models.CharField(max_length=100, default='')
    fav_subjects = models.CharField(max_length=100, default='')
    student_image = models.ImageField(upload_to='profile_image', blank=True)
    grade = models.IntegerField(default=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    profession = models.CharField(max_length=100, default='')
    user_type = models.CharField(max_length=50,)


    def __str__(self):
        return self.user.username
