from rest_framework import status
from django.http import HttpResponse
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
from datetime import timedelta
import csv


class TasksApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'title']
    ordering = ['-start_date', '-end_date']
    filter_backends = [DjangoFilterBackend ,SearchFilter, OrderingFilter]
    filterset_fields = ['is_complete', 'flag', 'category']

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)

        due = self.request.query_params.get("due")
        if due:
            today = timezone.now().date()
            if due == "today":
                qs = qs.filter(end_date=today, is_complete=False)
            elif due == "overdue":
                qs = qs.filter(end_date__lt=today, is_complete=False)
            elif due == "week":
                qs = qs.filter(
                    end_date__gte=today,
                    end_date__lte=today + timedelta(days=7),
                    is_complete=False,
                )
        return qs

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


class TaskCSVExportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Task.objects.filter(user=request.user).order_by('end_date', 'title')

        due = request.query_params.get("due")
        if due in {"today", "overdue", "week"}:
            today = timezone.now().date()
            filters = {
                "today": {"end_date": today, "is_complete": False},
                "overdue": {"end_date__lt": today, "is_complete": False},
                "week": {
                    "end_date__gte": today,
                    "end_date__lte": today + timedelta(days=7),
                    "is_complete": False,
                },
            }
            qs = qs.filter(**filters[due])

        resp = HttpResponse(content_type='text/csv; charset=utf-8')
        resp['Content-Disposition'] = 'attachment; filename="tasks.csv"'

        writer = csv.writer(resp)
        writer.writerow(['id', 'title', 'description', 'end_date', 'is_complete', 'flag', 'category_id'])

        for t in qs:
            writer.writerow([
                t.id,
                t.title or '',
                (t.description or '').replace('\r\n', '\n'),
                t.end_date.isoformat() if getattr(t, 'end_date', None) else '',
                'true' if getattr(t, 'is_complete', False) else 'false',
                t.flag if hasattr(t, 'flag') else '',
                getattr(getattr(t, 'category', None), 'id', ''),
            ])

        return resp