from rest_framework import serializers


class RepresentationSerializer(serializers.Serializer):
    """Serializer for representation data in analytics."""

    def to_representation(self, instance):
        return instance


class AnalyticsHistoricalSerializer(serializers.Serializer):
    """Serializer for historical analytics."""
    yearly = RepresentationSerializer()
    summary = RepresentationSerializer()

