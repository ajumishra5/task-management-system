from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import CustomUser, Task


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "role",
            "phone",
            "email_verified",
            "is_active",
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["creator", "is_deleted"]