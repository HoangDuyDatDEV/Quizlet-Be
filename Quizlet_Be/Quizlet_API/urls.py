
from Quizlet_API.controller.classController import *
from Quizlet_API.controller.folderController import *
from .controller.courseController import *
from django.urls import path

urlpatterns = [
    #path('course', CourseView.as_view()),    
    path('user', UserView.as_view()),
    path('course-all/', view_course),
    path('create-course/', add_course),
    path('update-course/<int:pk>/', update_course),
    path('delete-course/<int:pk>/', delete_course),
    path('search-course', search_course),
    path('get-course-by/<int:pk>', get_course_by_id),
    path('folder-all/', view_folder),
    path('create-folder/', add_folder),
    path('update-folder/<int:pk>/', update_folder),
    path('delete-folder/<int:pk>/', delete_folder),
    path('search-folder', search_folder),
    path('get-folder-by/<int:pk>', get_folder_by_id),
    path('class-all/', view_class),
    path('create-class/', add_class),
    path('update-class/<int:pk>/', update_class),
    path('delete-class/<int:pk>/', delete_class),
    path('search-class', search_class),
    path('get-class-by/<int:pk>', get_class_by_id),
]
