from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet
from core.views import BucketViewSet
from core.views import LocationViewSet
from transactions.views import EntryViewSet
from transactions.views import CategoryViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# Accounts
router.register(r"users", UserViewSet, basename="user")

# Core
router.register(r"buckets", BucketViewSet, basename="bucket")
router.register(r"locations", LocationViewSet, basename="location")

# Transactions
router.register(r"entries", EntryViewSet, basename="entry")
router.register(r"categories", CategoryViewSet, basename="category")

app_name = "api"
urlpatterns = router.urls
