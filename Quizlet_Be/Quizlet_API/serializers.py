from dataclasses import fields
from pyexpat import model
from rest_framework import serializers 
from rest_framework.serializers import ModelSerializer
from .models import *
class UserSerializer(serializers.ModelSerializer):
   
   email = serializers.EmailField()
  
   class Meta:
     model = User
     fields=['id','fullname','password','email']
     extra_kwargs = {'password':{'write_only': True,}
     }
   
   def create(self,validated_data):
    
    password=validated_data.pop('password',None)
    instance=self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance

   
   def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
class UpdateUserSerializer(ModelSerializer):
    class Meta:
     model = User
     fields = '__all__'
class ClassSerializer(ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
   

class FolderSerializer(ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
class CourseInClassSerializer(ModelSerializer):
    class Meta:
        model = CourseInClass
        fields = '__all__'
    
class UserInClassSerializer(ModelSerializer):
    class Meta:
        model = UserInClass
        fields = '__all__'
class FolderInClassSerializer(ModelSerializer):
    class Meta:
        model = FolderInClass
        fields = '__all__'
class FlashcardSerializer(ModelSerializer):
    class Meta:
        model = FlashCard
        fields = '__all__'   
class CourseInFolderSerializer(ModelSerializer):
    class Meta:
        model =CourseInFolder
        fields = '__all__'
    