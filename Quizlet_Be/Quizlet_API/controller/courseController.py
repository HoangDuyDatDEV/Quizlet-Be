
from django.shortcuts import render
from ..serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course
from Quizlet_API import serializers
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q


class UserView(APIView):
    def get(self, request):
        user_list = User.objects.all()
        data = UserSerializer(user_list, many = True).data
        return Response(data)
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status = 404)
        
        


class CourseView(APIView):
    def get(self, request):
        course_list = Course.objects.all()
        data =  CourseSerializer(course_list, many = True).data
        return Response(data)
    
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 404)
     
   
@api_view(['GET'])
def view_course(request):   
    courses = Course.objects.all()
        
    if courses:
        result = CourseSerializer(courses, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_course(request):
    course = CourseSerializer(data = request.data)
    
    if course.is_valid():
        course.save()
        return Response(course.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_course(request, pk):
    course = Course.objects.get(pk = pk)
    serializer = CourseSerializer(data = request.data, instance=course)
    
    if course.is_valid():
        course.save()
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND) 
        

@api_view(['DELETE'])
def delete_course(request, pk):
    try:
        courses = Course.objects.get(pk=pk)
        courses.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    
@api_view(['GET'])
def search_course(request):
    keyword = request.GET.get('keyword','')
    course_list = Course.objects.filter(
        Q(coursename__icontains = keyword)
    )
    data = CourseSerializer(course_list, many = True).data
    return Response(data)
        
@api_view(['GET'])
def get_course_by_id(request, pk):
   courses = Course.objects.filter(pk=pk).first()
   if courses:
      result = CourseSerializer(courses).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)