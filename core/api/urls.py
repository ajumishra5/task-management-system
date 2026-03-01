from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TaskViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("tasks", TaskViewSet, basename="tasks")

urlpatterns = router.urls