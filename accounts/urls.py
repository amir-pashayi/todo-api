from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.UserRegisterApiView.as_view(), name='user_register'),
    path('me/', views.UserDetailApiView.as_view(), name='user_detail'),
]