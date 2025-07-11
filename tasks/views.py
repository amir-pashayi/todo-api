from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.filters import OrderingFilter, SearchFilter

class TasksApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'title']
    ordering = ['-start_date', '-end_date']
    filter_backends = [SearchFilter, OrderingFilter]


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


