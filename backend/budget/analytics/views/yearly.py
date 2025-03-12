from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from analytics.services.yearly import AnalyticsYearlyService
from analytics.serializers.yearly import AnalyticsYearlySerializer
from analytics.services.cache_utils import get_or_generate_yearly_report


class AnalyticsYearlyViewSet(viewsets.ViewSet):
    """ViewSet for yearly analytics functionality. Add year (YYYY) in URL path for custom year analytics."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get complete yearly analytics summary."""
        current_year = timezone.now().year
        data = get_or_generate_yearly_report(request.user, year=current_year)
        serializer = AnalyticsYearlySerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<year>.+)')
    def custom(self, request, year=None):
        """Get analytics summary for a specific year (YYYY)."""
        try:
            year = int(year)

            # Validate year
            if year < 1900 or year > 2100:  # Arbitrary reasonable range
                return Response(
                    {"error": "Year must be between 1900 and 2100"}, status=400
                )

            data = get_or_generate_yearly_report(request.user, year=year)
            serializer = AnalyticsYearlySerializer(data)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid year format"}, status=400)

    @action(detail=False, methods=["get"])
    def cache_status(self, request):
        """Check cache status for the current user's yearly report and returns useful information."""
        user_id = request.user.id

        current_year = timezone.now().year
        year = request.query_params.get("year", current_year)

        cache_key = f"yearly_report_{user_id}_{year}"
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
            "year": year,
            "ttl_seconds": ttl,
            "expires_at": expires_at,
            "generated_at": generated_at,
        }

        return Response(response_data)

    @action(detail=False, methods=["get"], url_path=r"(?P<year>.+)/cache-status")
    def year_cache_status(self, request, year):
        """Check cache status for a specific year from URL path."""
        user_id = request.user.id

        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year format"}, status=400)

        cache_key = f"yearly_report_{user_id}_{year}"
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
                        expires_at = (
                            timezone.now() + timezone.timedelta(seconds=ttl)
                        ).isoformat()
            except (NotImplemented, AttributeError):
                pass

            if isinstance(cached_report, dict) and "generated_at" in cached_report:
                generated_at = cached_report["generated_at"]

        response_data = {
            "is_cached": is_cached,
            "cache_key": cache_key,
            "year": year,
            "ttl_seconds": ttl,
            "expires_at": expires_at,
            "generated_at": generated_at,
        }

        return Response(response_data)