
from .controller.courseController import *
from django.urls import path

urlpatterns = [
    #path('course', CourseView.as_view()),    
    path('user', UserView.as_view()),
    path('course-all/', view_course),
    path('create-course/', add_course),
    path('update-course/<int:pk>/', update_course),
    path('delete-course/<int:pk>', delete_course),
    path('search-course/<int:id>', search_course),
]
