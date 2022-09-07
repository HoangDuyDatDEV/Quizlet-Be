from models import User
from django.http import JsonResponse
from rest_framework import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
@APIView(['POST'])
def login(request):
    data=JSONParser().parse(request)
    email=data['email']
    password=data['password']
    res=User.CheckLogin(email,password)
    
    if res is False:
      return Response(status=400)
    return JsonResponse(res,safe=False)


