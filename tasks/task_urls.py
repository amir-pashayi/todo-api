from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksApiView.as_view(), name='tasks-list'),
    path('<int:id>/', views.TaskDetailApiView.as_view(), name='tasks-detail'),
    path('<int:id>/done/', views.TaskDoneApiView.as_view(), name='task-done'),
    path('bulk/done/', views.TaskBulkDoneApiView.as_view(), name='tasks-bulk-done'),
    path('bulk/delete/', views.TaskBulkDeleteApiView.as_view(), name='tasks-bulk-delete'),
]