from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksApiView.as_view(), name='tasks-list'),
]