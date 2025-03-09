from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from analytics.services.monthly import AnalyticsMonthlyService
from analytics.serializers.monthly import AnalyticsMonthlySerializer


class AnalyticsMonthlyViewSet(viewsets.ViewSet):
    """ViewSet for current month analytics functionality. Add month (YYYY-MM) in URL path for custom month analytics."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get current analytics summary for the current month and year."""
        current_month = timezone.now().month
        current_year = timezone.now().year
        service = AnalyticsMonthlyService(request.user, month=current_month, year=current_year)
        data = service.get_summary()
        serializer = AnalyticsMonthlySerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<year>.+)-(?P<month>.+)')
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

            service = AnalyticsMonthlyService(request.user, month=month, year=year)
            data = service.get_summary()
            serializer = AnalyticsMonthlySerializer(data)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid month or year format"}, status=400)
