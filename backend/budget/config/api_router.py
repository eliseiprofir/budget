from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet
from core.views import BucketViewSet
from core.views import LocationViewSet
from transactions.views import TransactionTypeViewSet
from transactions.views import CategoryViewSet
from transactions.views import TransactionViewSet
# from analytics.views import AnalyticsViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

# Accounts
router.register(r"users", UserViewSet, basename="user")

# Core
router.register(r"buckets", BucketViewSet, basename="bucket")
router.register(r"locations", LocationViewSet, basename="location")

# Transactions
router.register(r"transaction_types", TransactionTypeViewSet, basename="transaction_type")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

# Analytics
# router.register(r"analytics", AnalyticsViewSet, basename="analytics")

app_name = "api"
urlpatterns = router.urls
