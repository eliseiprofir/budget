from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from accounts.views import UserViewSet
from core.views import BucketViewSet
from core.views import LocationViewSet
from transactions.views import CategoryViewSet
from transactions.views import TransactionViewSet
from analytics.views.current import AnalyticsCurrentViewSet
from analytics.views.monthly import AnalyticsMonthlyViewSet
from analytics.views.yearly import AnalyticsYearlyViewSet
from analytics.views.historical import AnalyticsHistoricalViewSet


router = DefaultRouter()  # if settings.DEBUG else SimpleRouter()

# Accounts
router.register(r"users", UserViewSet, basename="user")

# Core
router.register(r"buckets", BucketViewSet, basename="bucket")
router.register(r"locations", LocationViewSet, basename="location")

# Transactions
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

# Analytics
router.register("analytics-current", AnalyticsCurrentViewSet, basename="analytics-current")
router.register("analytics-monthly", AnalyticsMonthlyViewSet, basename="analytics-monthly")
router.register("analytics-yearly", AnalyticsYearlyViewSet, basename="analytics-yearly")
router.register("analytics-historical", AnalyticsHistoricalViewSet, basename="analytics-historical")

app_name = "api"
urlpatterns = router.urls
