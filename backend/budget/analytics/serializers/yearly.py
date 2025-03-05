from rest_framework import serializers


class RepresentationSerializer(serializers.Serializer):
    """Serializer for representation data in analytics."""

    def to_representation(self, instance):
        return instance


class AnalyticsYearlySerializer(serializers.Serializer):
    """Serializer for current analytics."""
    monthly = RepresentationSerializer()
    summary = RepresentationSerializer()
    period = RepresentationSerializer()

