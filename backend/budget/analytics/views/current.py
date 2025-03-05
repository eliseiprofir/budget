from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from analytics.services.current import AnalyticsCurrentService
from analytics.serializers.current import AnalyticsCurrentSerializer

class AnalyticsCurrentViewSet(viewsets.ViewSet):
    """ViewSet for current analytics functionality."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get complete current analytics summary."""
        service = AnalyticsCurrentService(request.user)
        data = service.get_summary()
        serializer = AnalyticsCurrentSerializer(data)
        return Response(serializer.data)
