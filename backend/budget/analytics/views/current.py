from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.serializers.current import AnalyticsCurrentSerializer
from analytics.services.cache_utils import get_or_generate_current_report


class AnalyticsCurrentViewSet(viewsets.ViewSet):
    """ViewSet for current analytics functionality."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get complete current analytics summary. First checks cache - if not available, generates and caches it."""
        data = get_or_generate_current_report(request.user)
        serializer = AnalyticsCurrentSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def cache_status(self, request):
        """Check cache status for the current user's report and returns useful information."""
        user_id = request.user.id
        cache_key = f"current_report_{user_id}"
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
            "ttl_seconds": ttl,
            "expires_at": expires_at,
            "generated_at": generated_at,
        }

        return Response(response_data)