
from .views import *
from django.urls import path

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),  
    path('user', UserView.as_view()),
    path('editUser/<int:pk>/',edit_user),
    path('getUserBy/<int:pk>',get_user_by_id),
    path('courseAll/', get_all_course),
    path('createCourse/', add_course),
    path('updateCourse/<int:pk>/', update_course),
    path('deleteCourse/<int:pk>/', delete_course),
    path('searchCourse', search_course),
    path('getCourseBy/<int:pk>', get_course_by_id),
    path('folderAll/',get_all_folder),
    path('createFolder/', add_folder),
    path('updateFolder/<int:pk>/', update_folder),
    path('deleteFolder/<int:pk>/', delete_folder),
    path('searchFolder', search_folder),
    path('getFolderBy/<int:pk>', get_folder_by_id),
    path('classAll/', get_all_class),
    path('createClass/', add_class),
    path('updateClass/<int:pk>/', update_class),
    path('deleteClass/<int:pk>/', delete_class),
    path('searchClass', search_class),
    path('getClassBy/<int:pk>', get_class_by_id),
    path('addClassByMember', add_class_By_Member),
    path('addCourseInClass', add_course_in_class),
    path('addFolderInClass', add_folder_in_class),
    path('addMemberToClass/<str:pk>/', add_Member_To_Class),
    path('searchMemberToClass/', search_all_user_to_add_member),
    path('getAllCourseInClass/<int:pk>/', get_all_course_in_class),
    path('getAllFolderInClass/<int:pk>/',  get_all_folder_in_class),
    path('getAllMemberInClass/<int:pk>/',  get_all_user_in_class),
    path('getClassByIDCreator/<int:pk>/',  get_class_by_id_creator),
    path('getCourseByIDCreator/<int:pk>/',  get_course_by_id_creator),  
    path('getFolderByIDCreator/<int:pk>/',  get_folder_by_id_creator),  
    path('deleteMemberInClass/<int:pk>/',  delete_member_in_class),
    path('deleteAllMemberInClass/<int:pk>/',  delete_all_member_in_class),
    path('deleteCourseInClass/<int:pk>/',  delete_course_in_class),
    path('getCourseInClassBy/<int:pk>/',  get_course_in_class_by_id),
    path('getFolderInClassBy/<int:pk>/',  get_folder_in_class_by_id),
    path('deleteFolderInClass/<int:pk>/',  delete_folder_in_class),
    path('flashCardAll/<int:pk>/', get_all_flashcard),
    path('createFlashcard/', add_flashcard),
    path('updateFlashcard/<int:pk>/', update_flashcard),
    path('deleteFlashcard/<int:pk>/', delete_flashcard),
    path('addCourseInFolder', add_course_in_folder),
    path('deleteCourseInFolder/<int:pk>/',  delete_course_in_folder),
    path('getCourseInFolderBy/<int:pk>/',  get_course_in_folder_by_id),
    path('getAllCourseInFolder/<int:pk>/', get_all_course_in_folder),
]
