
from sre_constants import SUCCESS
from unittest import result

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
      raise AuthenticationFailed('cho1') 
    
    try:
      payload=jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('cho') 
    
    user=User.objects.filter(id=payload['id']).first()
    
    result =UserSerializer(user).data
    
    return Response({'data': result,
                     'token':token,})

#id, fullname, email
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


######ClassAPI

#API lấy thông tin của tất cả các lớp 
@api_view(['GET'])
def get_all_class(request):   
    classes =  Class.objects.all()
        
    if classes:
        result = ClassSerializer(classes, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
# API thêm thông tin lớp  
@api_view(['POST'])
def add_class(request):
    classes = ClassSerializer(data = request.data)
    if classes.is_valid():
        classes.save()
        
        return Response(classes.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API sửa thông tin lớp 
@api_view(['PUT']) 
def update_class(request, pk):
    classes = Class.objects.get(pk = pk)
    serializer = ClassSerializer(classes,data = request.data )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status = status.HTTP_404_NOT_FOUND) 
        
#API xóa thông tin lớp  
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
    Class_list = Class.objects.all()
    if keyword:   
      Class_list = Class.objects.filter(
          Q(classname__icontains = keyword)
      )
    
    total = Class_list.count()
    data = ClassSerializer(Class_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)
        
# API lấy lớp theo ID 
@api_view(['GET'])
def get_class_by_id(request, pk):
   classes = Class.objects.filter(pk=pk).first()
   numberOfCourse=CourseInClass.objects.filter(classID=pk).count()
   numberOfMember = UserInClass.objects.filter(permissions='member',classID=pk).count()
   if classes:
      data = ClassSerializer(classes).data
      result = {'data':data,'numberOfCourse':numberOfCourse,'numberOfCMember':numberOfMember}
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)

#API thêm khóa học vào lớp 
@api_view(['POST'])
def add_course_in_class(request):
    data=request.data.copy()
    classID=data.get('classID')
    data['numberOfCourse']=CourseInClass.objects.filter(classID=classID).count()+1 
    courseinclass=CourseInClassSerializer(data=data)
    if courseinclass.is_valid():  
     
      courseinclass.save()
      return Response({'data':courseinclass.data,
                      'status':status.HTTP_201_CREATED,
                      })
    return Response(courseinclass.errors,status=status.HTTP_400_BAD_REQUEST)

#API thêm thư mục vào lớp
@api_view(['POST'])
def add_folder_in_class(request):
    data=request.data.copy()
    classID=data.get('classID')
    data['numberOfFolder']=FolderInClass.objects.filter(classID=classID).count()+1 
    folderinclass=FolderInClassSerializer(data=data)
    
    if folderinclass.is_valid():  
      folderinclass.save()
      return Response({'data':folderinclass.data,
                      'status':status.HTTP_201_CREATED,
                      })
    return Response(folderinclass.errors,status=status.HTTP_400_BAD_REQUEST)

# API tạo lớp bởi người dùng 
@api_view(['POST'])
def add_class_By_Member(request):
    data=request.data.copy()
    data['permissions']='created'
    userinclass= UserInClassSerializer(data=data)
        
    if userinclass.is_valid():
        userinclass.save()
        return Response(userinclass.data, status=status.HTTP_201_CREATED)
    
    return Response(userinclass.errors, status=status.HTTP_400_BAD_REQUEST)


# API thêm thành viên vào lớp
@api_view(['POST'])
def add_Member_To_Class(request,pk):
    data=request.data.copy()
    userID=data.get('userID')
    classID=data.get('classID')
    member=UserInClass.objects.filter(userID=userID,classID=classID).first()
    
    if ( check_Is_Member(userID,pk) ):
      if (check_Duplicate_Member(member,userID)==False ):
          data['permissions']='member'
          data['numberOfUsers']=UserInClass.objects.filter(classID=classID,permissions='member').count()+1 
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
        'status': status.HTTP_400_BAD_REQUEST
      })
      
#Hàm kiểm tra người dùng có là thành viên ko 
def check_Is_Member(userID,CreatorID):
  if userID==CreatorID:
    return False
  else:
    return True

#Hàm kiểm tra thành viên đã tồn tại trong lớp chưa 
def check_Duplicate_Member(userID,ID):
  if userID==ID:
    return True
  else:
    return False

# API lấy khóa học trong lớp 
@api_view(['GET'])
def get_all_course_in_class(request,pk):   
    courseinclass =  CourseInClass.objects.filter(classID=pk)
    if courseinclass:
        result = CourseInClassSerializer(courseinclass, many = True).data
        return Response({'data':result})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)


# API lấy thư mục trong lớp 
@api_view(['GET'])
def get_all_folder_in_class(request,pk):   
    folderinclass =  FolderInClass.objects.filter(classID=pk)
        
    if folderinclass:
        result = FolderInClassSerializer(folderinclass, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
# API lấy thông tin khóa học trong lớp theo id
@api_view(['GET'])
def get_course_in_class_by_id(request, pk):
   courseinclass = CourseInClass.objects.filter(pk=pk).first()
   
   if courseinclass:
      result = CourseInClassSerializer(courseinclass).data
      return Response({'data':result})
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)
      
# API lấy thông tin folder trong lớp theo id
@api_view(['GET'])
def get_folder_in_class_by_id(request, pk):
   folderinclass = FolderInClass.objects.filter(pk=pk).first()
   
   if folderinclass:
      result = FolderInClassSerializer(folderinclass).data
      return Response({'data':result})
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)


# API lấy thành viên trong lớp 
@api_view(['GET'])
def get_all_user_in_class(request,pk):   
    userinclass =  UserInClass.objects.filter(classID=pk,permissions='member')
        
    if userinclass:
        result = UserInClassSerializer(userinclass, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API xóa thành viên trong lớp 
@api_view(['DELETE'])
def delete_member_in_class(request, pk):
    try:
        userinclass = UserInClass.objects.get(pk=pk)
        userinclass.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})

#API xóa tất cả thành viên trong lớp
@api_view(['DELETE'])
def delete_all_member_in_class(request,pk):
    try:
        userinclass = UserInClass.objects.filter(permissions='member',classID=pk)
        userinclass.delete()
        return Response({'success': True})
    except Exception as e:
      
        return Response({'success':False, 'error':str(e)})
# API xóa khóa học trong lớp
@api_view(['DELETE'])
def delete_course_in_class(request,pk):
    try:
        courseinclass = CourseInClass.objects.get(pk=pk)
        courseinclass.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})

# API xóa thư mục trong lớp
@api_view(['DELETE'])
def delete_folder_in_class(request,pk):
    try:
        folderinclass = FolderInClass.objects.get(pk=pk)
        folderinclass.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
#API lấy user để thêm thành viên vào lớp
@api_view(['GET'])
def search_all_user_to_add_member(request):   
    keyword = request.GET.get('keyword','')
    User_list = User.objects.all()
    if keyword:
      User_list = User.objects.filter(
          Q(fullname__icontains = keyword)
      )
    data = UserSerializer(User_list, many = True).data
    result = {'data':data}
    return Response(result)
    # data=request.data
    # classID=data.get('classID')
    # userinclassID=UserInClass.objects.get(classID=classID).userID
    # user_list = User.objects.get(userinclassID).id
    # userid= User.objects.all()
    # for !user_list user_list in userid:
    #  if  check_is_valid_in_class(userinclassID)==1:
    #  user_list = User.objects.filter(Q(fullname__icontains = fullname))
    #  data = UserSerializer(user_list, many = True).data
    #  result = {'data':data}
    #  return Response(result)


    
   
########## CourseAPI

#API lấy tất cả các khóa học
@api_view(['GET'])
def get_all_course(request):   
    courses = Course.objects.all()
        
    if courses:
        result = CourseSerializer(courses, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
#API tạo khóa học
@api_view(['POST'])
def add_course(request):
    course = CourseSerializer(data = request.data)
    
    if course.is_valid():
        course.save()
        return Response(course.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

#API sửa đổi thông tin khóa học
@api_view(['PUT'])
def update_course(request, pk):
    course = Course.objects.get(pk = pk)
    serializer = CourseSerializer(data = request.data, instance=course)
    
    if course.is_valid():
        course.save()
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND) 
        
#API xóa khóa học
@api_view(['DELETE'])
def delete_course(request, pk):
    try:
        courses = Course.objects.get(pk=pk)
        courses.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})

 #API tìm kiếm khóa học  
@api_view(['GET'])
def search_course(request):
    keyword = request.GET.get('keyword','')
    Course_list = Course.objects.all()
    if keyword:
      Course_list = Course.objects.filter(
          Q(coursename__icontains = keyword)
      )
    total = Course_list.count()
    data = CourseSerializer(Course_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)

# API lấy thông tin khóa học bằng id        
@api_view(['GET'])
def get_course_by_id(request, pk):
   courses = Course.objects.filter(pk=pk).first()
   if courses:
      result = CourseSerializer(courses).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)

##### FlashcardAPI 
#API thêm flashcard
@api_view(['POST'])
def add_flashcard(request):
    flashcard = FlashcardSerializer(data = request.data)
    
    if flashcard.is_valid():
        flashcard.save()
        return Response({'data':flashcard.data,
                          'status':status.HTTP_201_CREATED,
                          })
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
#API xóa flashcard
@api_view(['DELETE'])
def delete_flashcard(request, pk):
    try:
        flashcard = FlashCard.objects.get(pk=pk)
        flashcard.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})


#API sửu đổi flashcard
@api_view(['PUT'])
def update_flashcard(request, pk):
    flashcard = FlashCard.objects.get(pk = pk)
    serializer = FlashcardSerializer(data = request.data, instance=FlashCard)
    
    if flashcard.is_valid():
        flashcard.save()
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND) 

#API lấy tất cả các flashcard theo khóa học
@api_view(['GET'])
def get_all_flashcard(request, pk):   
    flashcard = FlashCard.objects.filter(courseID=pk)
        
    if flashcard:
        result = CourseSerializer(flashcard, many = True).data
        return Response({'result':result,'status':status.HTTP_200_OK})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)





############# FolderAPI

#API lấy tất cả thư mục 
@api_view(['GET'])
def get_all_folder(request):   
    folders =  Folder.objects.all()
        
    if folders:
        result = FolderSerializer(folders, many = True).data
        return Response(result)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
#API thêm thư mục
@api_view(['POST'])
def add_folder(request):
    folder = FolderSerializer(data = request.data)
    
    if folder.is_valid():
        folder.save()
        return Response(folder.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

#API sửa đổi thông tin thư mục
@api_view(['PUT'])
def update_folder(request, pk):
    folder = Folder.objects.get(pk = pk)
    serializer = FolderSerializer(data = request.data, instance=folder)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND) 
        
#API xóa thông tin thư mục
@api_view(['DELETE'])
def delete_folder(request, pk):
    try:
        folders = Folder.objects.get(pk=pk)
        folders.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})
    
# tìm kiếm thư mục
@api_view(['GET'])
def search_folder(request):
    keyword = request.GET.get('keyword','')
    folder_list = Folder.objects.all()
    if keyword:
      folder_list = Folder.objects.filter(
          Q(foldername__icontains = keyword)
      )
    total = folder_list.count()
    data = FolderSerializer(folder_list, many = True).data
    result = {'total':total, 'data':data}
    return Response(result)
        
#tìm kiếm thông tin thư mục theo id
@api_view(['GET'])
def get_folder_by_id(request, pk):
   folders = Folder.objects.filter(pk=pk).first()
   if folders:
      result = FolderSerializer(folders).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)


#API thêm khóa học vào thư mục
@api_view(['POST'])
def add_course_in_folder(request):
    data=request.data.copy()
    folderID=data.get('folderID')
    data['numberOfCourse']=CourseInFolder.objects.filter(folderID=folderID).count()+1 
    courseinfolder=CourseInFolderSerializer(data=data)
    if courseinfolder.is_valid():  
     
      courseinfolder.save()
      return Response({'data':courseinfolder.data,
                      'status':status.HTTP_201_CREATED,
                      })
    return Response(courseinfolder.errors,status=status.HTTP_400_BAD_REQUEST)

#API xóa khóa học trong thư mục
@api_view(['DELETE'])
def delete_course_in_folder(request,pk):
    try:
        courseinfolder = CourseInFolder.objects.get(pk=pk)
        courseinfolder.delete()
        return Response({'success': True})
    except Exception as e:
        return Response({'success':False, 'error':str(e)})

# API lấy khóa học trong thư mục 
@api_view(['GET'])
def get_all_course_in_folder(request,pk):   
    courseinfolder =  CourseInFolder.objects.filter(folderID=pk)
  
    if courseinfolder:
        result = CourseInFolderSerializer(courseinfolder, many = True).data
        return Response({'data':result})
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)

# API lấy thông tin khóa học trong thư mục theo id
@api_view(['GET'])
def get_course_in_folder_by_id(request, pk):
   courseinfolder = CourseInFolder.objects.filter(pk=pk).first()
   
   if courseinfolder:
      result = CourseInFolderSerializer(courseinfolder).data
      return Response({'data':result,
                        })
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)
  
  
#API lấy lớp theo id người tạo lớp
@api_view(['GET'])
def get_class_by_id_creator(request, pk):
    members=User.objects.filter(Q(id=pk))
    classes=Class.objects.filter(members__in=members)
    if classes:
          data = ClassSerializer(classes,many=True).data
          total = classes.count()
          result = {'total' : total, 'data':data}
          return Response(result)
    else:
          return Response(status=status.HTTP_404_NOT_FOUND)
      
#API lấy course theo id người tạo folder         
@api_view(['GET'])
def get_course_by_id_creator(request, pk):
    courses=Course.objects.filter(userID=pk)

    if courses:
          result = CourseSerializer(courses,many=True).data
          return Response(result)
    else:
          return Response(status=status.HTTP_404_NOT_FOUND)
      
#API lấy folder theo id người tạo folder         
@api_view(['GET'])
def get_folder_by_id_creator(request, pk):
    folders=Folder.objects.filter(userID=pk)

    if folders:
          result = FolderSerializer(folders,many=True).data
          return Response(result)
    else:
          return Response(status=status.HTTP_404_NOT_FOUND)