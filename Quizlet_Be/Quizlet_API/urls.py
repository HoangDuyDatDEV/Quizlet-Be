
from .views import *
from django.urls import path

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),  
    path('user', UserView.as_view()),
    path('edit-user/<int:pk>/',edit_user),
    path('get-user-by/<int:pk>',get_user_by_id),
    path('course-all/', get_all_course),
    path('create-course/', add_course),
    path('update-course/<int:pk>/', update_course),
    path('delete-course/<int:pk>/', delete_course),
    path('search-course', search_course),
    path('get-course-by/<int:pk>', get_course_by_id),
    path('folder-all/',get_all_folder),
    path('create-folder/', add_folder),
    path('update-folder/<int:pk>/', update_folder),
    path('delete-folder/<int:pk>/', delete_folder),
    path('search-folder', search_folder),
    path('get-folder-by/<int:pk>', get_folder_by_id),
    path('class-all/', get_all_class),
    path('create-class/', add_class),
    path('update-class/<int:pk>/', update_class),
    path('delete-class/<int:pk>/', delete_class),
    path('search-class', search_class),
    path('get-class-by/<int:pk>', get_class_by_id),
    path('addClassByMember', add_class_By_Member),
    path('addCourseInClass', add_course_in_class),
    path('addMemberToClass/<str:pk>/', add_Member_To_Class),
   
]
