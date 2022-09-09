from .controller.userController import *
from django.urls import path

urlpatterns = [
   
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    # path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
]