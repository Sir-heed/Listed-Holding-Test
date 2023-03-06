from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from user.permissions import IsAdmin
from .filters import UserFilter
from user.serializers import CreateUserSerializer, CustomObtainTokenPairSerializer, UserSerializer

class AuthViewSets(viewsets.ModelViewSet):
    """User ViewSets"""

    queryset = get_user_model().objects.exclude(is_deleted=True)
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = UserFilter
    search_fields = ["email", "firstname", "lastname", "phone", "middle_name"]
    ordering_fields = [
        "created_at",
        "last_login",
        "email",
        "firstname",
        "lastname",
        "phone",
    ]

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return CreateUserSerializer
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
            permission_classes = [AllowAny]
        elif self.action in ["delete", "partial_update", "list"]:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_deleted = True
        user.save()
        return Response(data="delete success")

    @action(
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        serializer_class=UserSerializer,
        detail=False,
        url_path="me",
    )
    def me(self, request, pk=None):
        user = request.user
        return Response(
            {"success": True, "data": self.serializer_class(user).data},
            status=status.HTTP_200_OK,
        )

class CustomObtainTokenPairView(TokenObtainPairView):
    """Login with email and password"""

    serializer_class = CustomObtainTokenPairSerializer
