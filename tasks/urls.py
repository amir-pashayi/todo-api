from django.urls import path
from . import views

urlpatterns = [
    # Tasks
    path('', views.TasksApiView.as_view(), name='tasks-list'),
    path('<int:id>', views.TaskDetailApiView.as_view(), name='tasks-detail'),

    # Categories
    path('categories/', views.CategoryApiView.as_view(), name='categories-list'),
]