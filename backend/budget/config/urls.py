"""
URL configuration for budget project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.serializers_jwt import CustomTokenObtainPairView

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    # User management
    path("accounts/", include("allauth.urls")),
    path("_allauth/", include("allauth.headless.urls")),
    # API base url
    path("api/", include("config.api_router")),
    path("api/auth/", include("rest_framework.urls")),
    # JWT Authentication
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
