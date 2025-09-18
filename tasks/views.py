from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, IdsPayloadSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

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



class TaskBulkDoneApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = IdsPayloadSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        ids = payload.validated_data["ids"]

        qs = Task.objects.filter(user=request.user, id__in=ids)
        requested_ids = set(ids)
        found_ids = set(qs.values_list("id", flat=True))
        not_found_ids = sorted(list(requested_ids - found_ids))

        with transaction.atomic():
            updated = qs.filter(is_complete=False).update(is_complete=True)
            skipped = qs.filter(is_complete=True).count()

        return Response(
            {
                "requested": len(ids),
                "updated": updated,
                "skipped_already_done": skipped,
                "not_found_or_forbidden_ids": not_found_ids,
                "timestamp": timezone.now(),
            },
            status=status.HTTP_200_OK,
        )


class TaskBulkDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = IdsPayloadSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        ids = payload.validated_data["ids"]

        qs = Task.objects.filter(user=request.user, id__in=ids)
        requested_ids = set(ids)
        found_ids = set(qs.values_list("id", flat=True))
        not_found_ids = sorted(list(requested_ids - found_ids))

        with transaction.atomic():
            deleted_count, _ = qs.delete()

        return Response(
            {
                "requested": len(ids),
                "deleted": deleted_count,
                "not_found_or_forbidden_ids": not_found_ids,
                "timestamp": timezone.now(),
            },
            status=status.HTTP_200_OK,
        )