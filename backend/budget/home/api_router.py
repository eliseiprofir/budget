from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet
from core.views import BucketViewSet
from core.views import LocationViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# Accounts
router.register(r"users", UserViewSet, basename="user")

# Core
router.register(r"buckets", BucketViewSet, basename="buckets")
router.register(r"locations", LocationViewSet, basename="locations")

urlpatterns = router.urls
