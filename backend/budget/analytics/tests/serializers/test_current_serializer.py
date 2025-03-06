import pytest
import decimal
from model_bakery import baker

from accounts.models import User
from analytics.services.current import AnalyticsCurrentService
from analytics.serializers.current import BalanceSerializer
from analytics.serializers.current import RepresentationSerializer
from analytics.serializers.current import AnalyticsCurrentSerializer


@pytest.mark.django_db
def test_representation_serializer():
    """Test RepresentationSerializer to ensure it works properly."""
    data = {
        "Back": 1000,
        "Cash": 200,
        "total": 1200,
    }

    serializer = RepresentationSerializer(data).to_representation(data)
    assert serializer == data

@pytest.mark.django_db
def test_balance_serializer():
    """Test BalanceSerializer to ensure it works properly."""
    data = {
        "positive": 1000,
        "negative": 200,
        "balance": 800
    }

    serializer = BalanceSerializer(data=data)

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == data

@pytest.mark.django_db
def test_analytics_current_serializer(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test AnalyticsCurrentSerializer to ensure it works properly."""
    baker.make_recipe(positive_transaction_recipe, user=user, amount=100, _quantity=3)
    baker.make_recipe(negative_transaction_recipe, user=user, amount=50, _quantity=2)

    service_data = AnalyticsCurrentService(user).get_summary()
    serializer_data = AnalyticsCurrentSerializer(service_data).data

    assert "balance" in serializer_data
    assert "locations" in serializer_data
    assert "buckets" in serializer_data

    assert serializer_data["balance"]["positive"] == decimal.Decimal("300.00")
    assert serializer_data["balance"]["negative"] == decimal.Decimal("100.00")
    assert serializer_data["balance"]["balance"] == decimal.Decimal("200.00")
