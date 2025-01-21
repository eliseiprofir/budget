from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# Accounts
router.register(r"users", UserViewSet, basename="user")

urlpatterns = router.urls
