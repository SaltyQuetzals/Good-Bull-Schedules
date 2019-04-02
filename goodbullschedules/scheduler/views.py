from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, views

from scheduler import models as scheduler_models
from scheduler import serializers as scheduler_serializers
from scraper import models as scraper_models

# Create your views here.


class IsOwner(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        return obj.owner == request.user


class CreateScheduleView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = scheduler_models.Schedule.objects.all()
    serializer_class = scheduler_serializers.ScheduleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                "name": request.data["name"],
                "term_code": request.data["term_code"],
                "owner": request.user,
                "sections": [],
                "courses": [],
            }
        )
        if serializer.is_valid():
            serializer.save()
