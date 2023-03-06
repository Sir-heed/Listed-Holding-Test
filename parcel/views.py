from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from parcel.filters import ParcelFilter
from parcel.models import Parcel
from parcel.serializers import CancelParcelSerializer, ParcelSerializer
from user.permissions import IsAdmin

# Create your views here.
class ParcelViewSets(viewsets.ModelViewSet):
    """User ViewSets"""

    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ParcelFilter
    search_fields = ["title"]
    ordering_fields = [
        "created_at"
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.user_type != 'ADMIN':
            qs = qs.filter(created_by=user)
        return qs
    
    def get_serializer_class(self):
        if self.action in ["partial_update"]:
            return CancelParcelSerializer
        return super().get_serializer_class()

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["delete", "partial_update"]:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]