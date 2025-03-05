from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from analytics.services.yearly import AnalyticsYearlyService
from analytics.serializers.yearly import AnalyticsYearlySerializer


class AnalyticsYearlyViewSet(viewsets.ViewSet):
    """ViewSet for current analytics functionality."""

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get complete current analytics summary."""
        current_year = timezone.now().year
        service = AnalyticsYearlyService(request.user, year=current_year)
        data = {
            "monthly": service.get_year_data_by_month(),
            "summary": service.get_year_summary(),
            "period": current_year,
        }
        serializer = AnalyticsYearlySerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<year>\d+)')
    def custom_year_analytics(self, request, year=None, month=None):
        """Get analytics summary for a specific year in ISO format (YYYY)."""
        try:
            year = int(year)

            # Validate year
            if year < 1900 or year > 2100:  # Arbitrary reasonable range
                return Response({"error": "Year must be between 1900 and 2100"}, status=400)

            service = AnalyticsYearlyService(request.user, year=year)
            data = {
                "monthly": service.get_year_data_by_month(),
                "summary": service.get_year_summary(),
                "period": year,
            }
            serializer = AnalyticsYearlySerializer(data)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid year format"}, status=400)
