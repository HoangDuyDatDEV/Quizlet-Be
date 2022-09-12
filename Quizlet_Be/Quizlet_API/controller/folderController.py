from django.shortcuts import render
from ..serializers import *
from rest_framework.response import Response
from ..models import Course
from Quizlet_API import serializers
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q



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