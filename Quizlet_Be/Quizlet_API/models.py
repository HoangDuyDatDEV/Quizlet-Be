import email
from enum import auto
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    otp=models.IntegerField()
class Class(models.Model):
    id = models.AutoField(primary_key=True)
    classname=models.CharField(max_length=255)
    description = models.TextField(null=True)
    schoolname = models.CharField(max_length=255)
    allowAddMember=models.CharField(max_length=255)
    createDate=models.DateField(auto_now_add=True)
class UserInClass(models.Model):
    id=models.AutoField(primary_key=True)
    numberOfUsers=models.IntegerField()
    permissions=models.CharField(max_length=100) 
    UserID=models.ForeignKey(User, ondelete=models.CASCADE)
    ClassID=models.ForeignKey(Class, ondelete=models.CASCADE)
class Course(models.Model):
    id=models.AutoField(primary_key=True)
    coursename=models.CharField(max_length=255)
    description=models.TextField(null=True)
    allowDisplay=models.CharField(max_length=20)
    allowEdit=models.CharField(max_length=20)
    UserID=models.ForeignKey(User, on_delete=models.CASCADE)
class CourseInClass(models.Model):
    id = models.AutoField(primary_key=True)
    numberOfCourse=models.IntegerField()
    courseID=models.ForeignKey(Course, on_delete=models.CASCADE)
    classID=models.ForeignKey(Class, on_delete=models.CASCADE)
class Folder(models.Model):
    id=models.AutoField(primary_key=True)
    foldername=models.CharField(max_length=255)
    description=models.TextField(null=True)
    UserID=models.ForeignKey(User,on_delete=models.CASCADE)
class CourseInFolder(models.Model):
    id = models.AutoField(primary_key=True)
    numberOfCourse=models.IntegerField()
    courseID=models.ForeignKey(Course, on_delete=models.CASCADE)
    folderID=models.ForeignKey(Folder, on_delete=models.CASCADE)
class FolderInClass(models.Model):
    id=models.AutoField(primary_key=True)
    numberOfFolder=models.IntegerField()
    ClassID=models.ForeignKey(Class, on_delete=models.CASCADE)
    FolderID=models.ForeignKey(Folder, on_delete=models.CASCADE)
class FlashCard(models.Model):
    id=models.AutoField(primary_key=True)
    keyword=models.CharField(max_length=255)
    defindName=models.CharField(max_length=255)
    image=models.ImageField(max_length=255)
    learned=models.CharField(max_length=20)
    CourseID=models.ForeignKey(Course, on_delete=models.CASCADE)

