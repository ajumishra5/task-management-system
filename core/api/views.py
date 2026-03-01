from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .throttles import LoginRateThrottle
from core.models import CustomUser, Task
from .serializers import (
    UserSerializer,
    TaskSerializer,
    EmailTokenObtainPairSerializer,
)
from django.db.models import Q


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_deleted=False)
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(is_deleted=False)

        status_filter = self.request.query_params.get("status")
        priority_filter = self.request.query_params.get("priority")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        if user.is_superuser:
            return queryset

        if user.role == "manager":
            return queryset.filter(
                Q(creator=user) | Q(assigned_to=user)
            )

        return queryset.filter(assigned_to=user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
    @action(detail=True, methods=["patch"])
    def change_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get("status")

        if request.user != task.assigned_to and not request.user.is_superuser:
            return Response(
                {"detail": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        task.status = new_status
        task.save()

        return Response({"detail": "Status updated"})
    
class DashboardAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(is_deleted=False)

        return Response({
            "total": tasks.count(),
            "pending": tasks.filter(status="pending").count(),
            "completed": tasks.filter(status="completed").count(),
        })
    
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]