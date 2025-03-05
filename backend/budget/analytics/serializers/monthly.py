from rest_framework import serializers


class RepresentationSerializer(serializers.Serializer):
    """Serializer for representation data in analytics."""

    def to_representation(self, instance):
        return instance


class AnalyticsMonthlySerializer(serializers.Serializer):
    """Serializer for current month analytics."""
    positive_categories = RepresentationSerializer()
    negative_categories = RepresentationSerializer()
    balance = RepresentationSerializer()
    period = RepresentationSerializer()
