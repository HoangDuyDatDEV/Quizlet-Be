from sre_constants import SUCCESS
from ..models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from rest_framework import status
from rest_framework.decorators import api_view

class RegisterView(APIView):
  def post(self,request):
      serializer = UserSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)  

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
class LogoutView(APIView):
  def post(self, request):
    response=Response()
    response.delete_cookie('jwt')
    response.data = {
      'message':'success'
    }
    return response

@api_view(['GET'])
def get_user_by_id(request, pk):
   user = User.objects.filter(pk=pk).first()
   if user:
      result = UserSerializer(user).data
      return Response(result)
   else:
      return Response(status=status.HTTP_404_NOT_FOUND)