from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.api.views import DashboardAPIView, EmailTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    # JWT
    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API router
    path("api/", include("core.api.urls")),
    path("api/dashboard/", DashboardAPIView.as_view()),
]