from email.policy import default
from django.contrib.auth.models import AbstractUser
import email
from enum import auto
from django.db import models


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username=None
    phone = models.IntegerField(blank=True)
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True)
    otp=models.IntegerField(blank=True)
    role=models.CharField(max_length=200,default=False)
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
   

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    coursename=models.CharField(max_length=255)
    description=models.TextField(null=True)
    allowDisplay=models.CharField(max_length=20)
    allowEdit=models.CharField(max_length=20)
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    #numberFlashcard = models.IntegerField(default=0)
    
class FlashCard(models.Model):
    id=models.AutoField(primary_key=True)
    keyword=models.CharField(max_length=255)
    defindName=models.CharField(max_length=255)
    image=models.ImageField(max_length=255, null=True)
    learned=models.CharField(max_length=20, blank=True)
    courseID=models.ForeignKey(Course, on_delete=models.CASCADE)
    
class Folder(models.Model):
    id=models.AutoField(primary_key=True)
    foldername=models.CharField(max_length=255)
    description=models.TextField(null=True)
    userID=models.ForeignKey(User,on_delete=models.CASCADE)  
    courses=models.ManyToManyField(Course, through='CourseInFolder', null=True)
class Class(models.Model):
    id = models.AutoField(primary_key=True)
    classname=models.CharField(max_length=255)
    description = models.TextField(null=True)
    schoolname = models.CharField(max_length=255)
    allowAddMember=models.CharField(max_length=255,default=True)
    createDate=models.DateField(auto_now_add=True)
    members=models.ManyToManyField(User, through='UserInClass')
    courses=models.ManyToManyField(Course, through='CourseInClass')
    folders=models.ManyToManyField(Folder, through='FolderInClass')
class UserInClass(models.Model):
    id=models.AutoField(primary_key=True)
    numberOfUsers=models.IntegerField(default=0, blank=True)
    permissions=models.CharField(max_length=100,blank=True) 
    userID=models.ForeignKey(User, on_delete=models.CASCADE)
    classID=models.ForeignKey(Class, on_delete=models.CASCADE)

    
class CourseInClass(models.Model):
    id = models.AutoField(primary_key=True)
    numberOfCourse=models.IntegerField(default=0,blank=True)
    courseID=models.ForeignKey(Course, on_delete=models.CASCADE)
    coursesName = models.CharField(max_length=100, blank=True)
    numberCard = models.IntegerField(default=0)
    classID=models.ForeignKey(Class, on_delete=models.CASCADE)

class CourseInFolder(models.Model):
    id = models.AutoField(primary_key=True)
    numberOfCourse=models.IntegerField(default=0,blank=True)
    courseID=models.ForeignKey(Course, on_delete=models.CASCADE)
    folderID=models.ForeignKey(Folder, on_delete=models.CASCADE)
class FolderInClass(models.Model):
    id=models.AutoField(primary_key=True)
    numberOfFolder=models.IntegerField(default=0,blank=True)
    classID=models.ForeignKey(Class, on_delete=models.CASCADE)
    folderID=models.ForeignKey(Folder, on_delete=models.CASCADE)

