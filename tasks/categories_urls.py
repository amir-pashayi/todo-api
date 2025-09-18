from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryApiView.as_view(), name='categories-list'),
    path('<int:id>/', views.CategoryDetailApiView.as_view(), name='categories-detail'),
]