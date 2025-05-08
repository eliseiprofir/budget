from rest_framework import serializers


class RepresentationSerializer(serializers.Serializer):
    """Serializer for representation data in analytics."""

    def to_representation(self, instance):
        return instance


class BalanceSerializer(serializers.Serializer):
    """Serializer for balance data."""
    positive = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    negative = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    neutral = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)


class AnalyticsCurrentSerializer(serializers.Serializer):
    """Serializer for current status analytics."""
    locations = RepresentationSerializer()
    buckets = RepresentationSerializer()
    balance = BalanceSerializer()
