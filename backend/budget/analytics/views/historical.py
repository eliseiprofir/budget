from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from analytics.services.historical import AnalyticsHistoricalService
from analytics.serializers.historical import AnalyticsHistoricalSerializer


class AnalyticsHistoricalViewSet(viewsets.ViewSet):
    """ViewSet for current analytics functionality."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get complete current analytics summary."""
        service = AnalyticsHistoricalService(request.user)
        data = service.get_summary()
        serializer = AnalyticsHistoricalSerializer(data)
        return Response(serializer.data)
