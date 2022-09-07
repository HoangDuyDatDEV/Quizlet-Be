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

    def CheckLogin(email, password):
      try:
        user=User.objects.get(email=email,password=password)
        if user is not None:
           return{
            'id':user.id,
            'email':user.email,
            'password':user.password,
            'full_name':user.full_name,
           }
        else:
           return{
            'id':None,
            'email':None,
            'password':None,
            'full_name':None
        }
      except:
        print('Checklogin failed')
        return False
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
    UserID=models.ForeignKey(User, on_delete=models.CASCADE)
    ClassID=models.ForeignKey(Class, on_delete=models.CASCADE)
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

