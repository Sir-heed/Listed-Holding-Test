from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "firstname",
            "lastname",
            "email",
            "user_type",
            "phone",
            "is_active",
            "status"
        ]

    @staticmethod
    def get_status(self):
        return self.status
    

class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "firstname",
            "middle_name",
            "lastname",
            "phone",
            "image",
            "user_type",
            "password"
        )

    def validate(self, attrs):
        if not self.instance:
            email = attrs.get("email", None)
            if email:
                email = attrs["email"].lower().strip()
                if get_user_model().objects.filter(email=email).exists():
                    raise serializers.ValidationError({"email": "Email already exists"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get("password", False):
            instance.set_password(validated_data.get("password"))
            instance.save()
        return instance


class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.is_deleted:
            raise exceptions.AuthenticationFailed(
                _("Account deleted."), code="authentication"
            )
        if not user.verified:
            raise exceptions.AuthenticationFailed(
                _("Account not yet verified."), code="authentication"
            )
        token = super().get_token(user)
        # Add custom claims
        token.id = user.id
        token["email"] = user.email
        token["user_type"] = user.user_type
        token["firstname"] = user.firstname
        token["lastname"] = user.lastname
        if user.image:
            token["image"] = user.image.url
        token["phone"] = user.phone
        token["user_type"] = user.user_type
        user.save_last_login()
        return token

