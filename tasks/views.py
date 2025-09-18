from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class TasksApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'title']
    ordering = ['-start_date', '-end_date']
    filter_backends = [DjangoFilterBackend ,SearchFilter, OrderingFilter]
    filterset_fields = ['is_complete', 'flag', 'category']


    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        return queryset
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CategoryApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CategoryDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        return queryset
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class TaskDoneApiView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        task = get_object_or_404(Task, pk=id, user=request.user)
        if task.is_complete:
            return Response({'detail': 'already done'}, status=status.HTTP_200_OK)
        task.is_complete = True
        task.save(update_fields=['is_complete'])
        return Response({'detail': 'Task marked as done'}, status=status.HTTP_200_OK)