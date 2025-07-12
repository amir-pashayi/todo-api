from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path('register/', views.UserRegisterApiView.as_view(), name='user_register'),
    path('me/', views.UserDetailApiView.as_view(), name='user_detail'),

    #JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]