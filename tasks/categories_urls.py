from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryApiView.as_view(), name='categories-list'),
    path('categories/<int:id>', views.CategoryDetailApiView.as_view(), name='categories-detail'),
]