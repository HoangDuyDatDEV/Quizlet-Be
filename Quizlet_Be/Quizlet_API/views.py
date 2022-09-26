
from sre_constants import SUCCESS

from xmlrpc.client import ResponseError
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.exceptions import AuthenticationFailed,ValidationError
import jwt,datetime
from rest_framework import status
from rest_framework.decorators import api_view
from http.client import REQUEST_ENTITY_TOO_LARGE
from django.shortcuts import render
from Quizlet_API import serializers
from django.db.models import Q

# UserAPI
# Api đăng ký
class RegisterView(APIView):
  def post(self,request):
      serializer = UserSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)  
#API đăng nhập 
class LoginView(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user=User.objects.filter(email=email).first()

    if user is None :
      raise AuthenticationFailed({
        'sucess': False,
        'message':'tai khoan khong ton tai',
        'status': status.HTTP_404_NOT_FOUND
      })
       
    if not user.check_password(password):
      raise AuthenticationFailed({
        'sucess': False,
        'message':'sai mat khau',
        'status': status.HTTP_404_NOT_FOUND
      })
    
    
    payload={
      'id':user.id,
      'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat':datetime.datetime.utcnow()

    }

    token =jwt.encode(payload,'secret',algorithm='HS256')
    
    response=Response()
   
    response.set_cookie(key='jwt',value=token,httponly=True)
    
    
    user=User.objects.filter(id=payload['id']).first()
    serializer=UserSerializer(user)

    response.data = {
      'sucess':True,
      'message': 'Dang nhap thanh cong',
      'jwt':token,
      'status': status.HTTP_200_OK,
      'data':serializer.data
    }
    return response
#API lấy thông tin user đang đăng nhập
class UserView(APIView):

  def get(self, request):
    token = request.COOKIES.get('jwt')
    
    if not token:
      raise AuthenticationFailed('Unauthenticated') 
    
    try:
      payload=jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated') 
    
    user=User.objects.filter(id=payload['id']).first()
    
    serializer=UserSerializer(user)
    
    return Response(serializer.data)
#API đăng xuất
class LogoutView(APIView):
  def post(self, request):
    response=Response()
    response.delete_cookie('jwt')
    response.data = {
      'message':'success'
    }
    return response
# API lấy thông tin user theo id
@api_view(['GET'])
def get_user_by_id(request, pk):
   user = User.objects.filter(pk=pk).first()
   if user:
      result = UserSerializer(user).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)
      
# API thay đổi thông tin user
@api_view(['PUT'])
def edit_user(request, pk):
    users = User.objects.get(pk = pk)
    data=request.data
    serializer = UpdateUserSerializer(users,data)
    
    
    if users.email==data['email']:
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
        else:
          return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND)
    else:
        return Response({'response':"bạn không có quyền thay đổi thông tin người dùng"})


#ClassAPI

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
    classID=data.get('classID')
    courseinclass=CourseInClassSerializer(data=data)
    if courseinclass.is_valid():  
      courseinclass.save()
      numberOfCourses=CourseInClass.objects.filter(classID=classID).count()
      return Response({'data':courseinclass.data,
                      'status':status.HTTP_201_CREATED,
                      'numberOfCourses':numberOfCourses
                      })
    return Response(courseinclass.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_folder_in_class(request):
    data=request.data
    classID=data.get('classID')
    folderinclass=FolderInClassSerializer(data=data)
    if folderinclass.is_valid():  
      folderinclass.save()
      numberOfFolder=FolderInClass.objects.filter(classID=classID).count()
      return Response({'data':folderinclass.data,
                      'status':status.HTTP_201_CREATED,
                      'numberOfFolder':numberOfFolder
                      })
    return Response(folderinclass.errors,status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['POST'])
def add_Member_To_Class(request,pk):
    data=request.data.copy()
    userID=data.get('userID')
    classID=data.get('classID')
    member=UserInClass.objects.filter(userID=userID).first()
    
    if ( check_Is_Member(userID,pk) ):
      if (check_Duplicate_Member(member,userID)==False and member.permissions !='member' ):
          data['permissions']='member'
          userinclass= UserInClassSerializer(data=data)
          
          if userinclass.is_valid():
            userinclass=userinclass.save()
            userinclass=UserInClassSerializer(userinclass)
            return Response(userinclass.data, status=status.HTTP_201_CREATED)
          return Response(userinclass.errors, status=status.HTTP_400_BAD_REQUEST)
      else:
        raise  ValidationError ({
        'sucess': False,
        'message':'đã tồn tại thành viên này trong lớp',
        'status': status.HTTP_404_NOT_FOUND
      })
    else:
      raise  ValidationError ({
        'sucess': False,
        'message':'NGười tạo lớp không thể là thành viên',
        'status': status.HTTP_404_NOT_FOUND
      })
      
# 
def check_Is_Member(userID,CreatorID):
  if userID==CreatorID:
    return False
  else:
    return True
def check_Duplicate_Member(userID,ID):
  if userID==ID:
    return True
  else:
    return False

@api_view(['GET'])
def get_all_course_in_class(request):   
    courseinclass =  CourseInClass.objects.all()
        
    if courseinclass:
        result = CourseInClassSerializer(courseinclass, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_folder_in_class(request):   
    folderinclass =  FolderInClass.objects.all()
        
    if folderinclass:
        result = FolderInClassSerializer(folderinclass, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_user_in_class(request,pk):   
    courseinclass =  CourseInClass.objects.get(permissions='member',classID=pk)

    if courseinclass:
        result = CourseInClassSerializer(courseinclass, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_member_in_class(request, pk):
    try:
        userinclass = UserInClass.objects.get(pk=pk)
        userinclass.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})

@api_view(['DELETE'])
def delete_all_member_in_class(request,pk):
    try:
        userinclass = UserInClass.objects.get(permissions='member',classID=pk)
        userinclass.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})

@api_view(['DELETE'])
def delete_course_in_class(request,pk):
    try:
        courseinclass = CourseInClass.objects.get(pk=pk)
        courseinclass.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})




# CourseAPI
@api_view(['GET'])
def get_all_course(request):   
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


# FolderAPI


@api_view(['GET'])
def get_all_folder(request):   
    folders =  Folder.objects.all()
        
    if folders:
        result = FolderSerializer(folders, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def add_folder(request):
    folder = FolderSerializer(data = request.data)
    
    if folder.is_valid():
        folder.save()
        return Response(folder.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_folder(request, pk):
    folder = Folder.objects.get(pk = pk)
    serializer = FolderSerializer(data = request.data, instance=folder)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND) 
        

@api_view(['DELETE'])
def delete_folder(request, pk):
    try:
        folders = Folder.objects.get(pk=pk)
        folders.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    

@api_view(['GET'])
def search_folder(request):
    keyword = request.GET.get('keyword','')
    folder_list = Folder.objects.filter(
        Q(foldername__icontains = keyword)
    )
    data = FolderSerializer(folder_list, many = True).data
    return Response(data)
        

@api_view(['GET'])
def get_folder_by_id(request, pk):
   folders = Folder.objects.filter(pk=pk).first()
   if folders:
      result = FolderSerializer(folders).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)