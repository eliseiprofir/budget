from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from analytics.serializers.monthly import AnalyticsMonthlySerializer
from analytics.services.cache_utils import get_or_generate_monthly_report


class AnalyticsMonthlyViewSet(viewsets.ViewSet):
    """ViewSet for month analytics functionality. Add month (YYYY-MM) in URL path for custom month analytics."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get analytics summary for the current month and year."""
        current_month = timezone.now().month
        current_year = timezone.now().year
        data = get_or_generate_monthly_report(request.user, year=current_year, month=current_month)
        serializer = AnalyticsMonthlySerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def cache_status(self, request):
        """Check cache status for the current user's monthly report and returns useful information."""
        user_id = request.user.id

        current_month = timezone.now().month
        current_year = timezone.now().year

        cache_key = f"monthly_report_{user_id}_{current_year}_{current_month}"
        cached_report = cache.get(cache_key)
        is_cached = cached_report is not None

        ttl = None
        expires_at = None
        generated_at = None

        if is_cached:
            try:
                if hasattr(cache, "ttl"):
                    ttl = cache.ttl(cache_key)
                    if ttl is not None:
                        expires_at = (timezone.now() + timezone.timedelta(seconds=ttl)).isoformat()
            except (NotImplemented, AttributeError):
                pass

            if isinstance(cached_report, dict) and "generated_at" in cached_report:
                generated_at = cached_report["generated_at"]

        response_data = {
            "is_cached": is_cached,
            "cache_key": cache_key,
            "month": current_month,
            "year": current_year,
            "ttl_seconds": ttl,
            "expires_at": expires_at,
            "generated_at": generated_at,
        }

        return Response(response_data)

    @action(detail=False, methods=["get"], url_path='cache-status/(?P<year>\d{4})-(?P<month>\d{1,2})')
    def cache_status_for_date(self, request, year=None, month=None):
        """Check cache status for a specific year-month."""
        user_id = request.user.id

        try:
            year = int(year)
            month = int(month)

            # Validate month and year
            if month < 1 or month > 12:
                return Response({"error": "Month must be between 1 and 12"}, status=400)
            if year < 1900 or year > 2100:
                return Response({"error": "Year must be between 1900 and 2100"}, status=400)

        except ValueError:
            return Response({"error": "Invalid year or month format"}, status=400)

        cache_key = f"monthly_report_{user_id}_{year}_{month}"
        cached_report = cache.get(cache_key)
        is_cached = cached_report is not None

        ttl = None
        expires_at = None
        generated_at = None

        if is_cached:
            try:
                if hasattr(cache, "ttl"):
                    ttl = cache.ttl(cache_key)
                    if ttl is not None:
                        expires_at = (timezone.now() + timezone.timedelta(seconds=ttl)).isoformat()
            except (NotImplemented, AttributeError):
                pass

            if isinstance(cached_report, dict) and "generated_at" in cached_report:
                generated_at = cached_report["generated_at"]

        response_data = {
            "is_cached": is_cached,
            "cache_key": cache_key,
            "month": month,
            "year": year,
            "ttl_seconds": ttl,
            "expires_at": expires_at,
            "generated_at": generated_at,
        }

        return Response(response_data)

    @action(detail=False, methods=['get'], url_path=r'(?P<year>\d{4})-(?P<month>\d{1,2})')
    def custom(self, request, year=None, month=None):
        """Get analytics summary for a specific month and year (YYYY-MM)."""
        try:
            year = int(year)
            month = int(month)

            # Validate month and year
            if month < 1 or month > 12:
                return Response({"error": "Month must be between 1 and 12"}, status=400)
            if year < 1900 or year > 2100:  # Arbitrary reasonable range
                return Response({"error": "Year must be between 1900 and 2100"}, status=400)

            data = get_or_generate_monthly_report(request.user, year=year, month=month)
            serializer = AnalyticsMonthlySerializer(data)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid month or year format"}, status=400)

    @action(detail=False, methods=['get'], url_path=r'(?P<invalid_format>.+)')
    def invalid_format(self, request, invalid_format=None):
        """Handle invalid format requests."""
        return Response({"error": "Invalid format. Use YYYY-MM format."}, status=400)
