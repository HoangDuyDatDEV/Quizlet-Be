from http.client import REQUEST_ENTITY_TOO_LARGE
from django.shortcuts import render

from Quizlet_API.views import add_course_to_class, permissionUser


from ..serializers import *
from rest_framework.response import Response
from ..models import *
from Quizlet_API import serializers
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q




@api_view(['GET'])
def get_all_class(request):   
    classes =  Class.objects.all()
        
    if classes:
        result = ClassSerializer(classes, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_class(request):
    classes = ClassSerializer(data = request.data)
    if classes.is_valid():
        classes.save()
        
        return Response(classes.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_class(request, pk):
    classes = Class.objects.get(pk = pk)
    serializer = ClassSerializer(data = request.data, instance=classes)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND) 
        

@api_view(['DELETE'])
def delete_class(request, pk):
    try:
        classses = Class.objects.get(pk=pk)
        classses.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    

@api_view(['GET'])
def search_class(request):
    keyword = request.GET.get('keyword','')
    Class_list = Class.objects.filter(
        Q(classname__icontains = keyword)
    )
    data = ClassSerializer(Class_list, many = True).data
    return Response(data)
        

@api_view(['GET'])
def get_class_by_id(request, pk):
   classes = Class.objects.filter(pk=pk).first()
   if classes:
      result = ClassSerializer(classes).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_course_in_class(request):
    data=request.data  
    courseID=data['courseID']
    classID=data['classID']
    numberOfCourse=data['numberOfCourse']
    add_course_to_class(classID,courseID,numberOfCourse)
    return Response(data)

@api_view(['POST'])
def add_class_By_Member(request):
    data=request.data.copy()
    data['permissions']='created'
    userinclass= UserInClassSerializer(data=data)
        
    if userinclass.is_valid():
        userID=data.get('userID')
        classID=data.get('classID')
        userinclass=userinclass.save()
        
        userinclass=UserInClassSerializer(userinclass)
        print (userinclass)
        print (userinclass.data)
        return Response(userinclass.data, status=status.HTTP_201_CREATED)
    return Response(userinclass.errors, status=status.HTTP_400_BAD_REQUEST)
