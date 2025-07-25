from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksApiView.as_view(), name='tasks-list'),
    path('<int:id>', views.TaskDetailApiView.as_view(), name='tasks-detail'),
    path('done/<int:id>', views.TaskDoneApiView.as_view(), name='task-done'),
]