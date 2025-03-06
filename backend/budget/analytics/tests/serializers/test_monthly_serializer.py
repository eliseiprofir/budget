import pytest
import decimal
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.monthly import AnalyticsMonthlyService
from analytics.serializers.monthly import RepresentationSerializer
from analytics.serializers.monthly import AnalyticsMonthlySerializer


@pytest.mark.django_db
def test_representation_serializer():
    """Test RepresentationSerializer to ensure it works properly."""
    data = {"Test": 1000,}
    serializer = RepresentationSerializer(data).to_representation(data)
    assert serializer == data


@pytest.mark.django_db
def test_analytics_monthly_serializer(
    user: User,
    positive_category_recipe: str,
    negative_category_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test AnalyticsMonthlySerializer to ensure it works properly."""
    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    positive_category = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category")
    negative_category = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category")
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=january, amount=200, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=january, amount=100, _quantity=2)
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=february, amount=100, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=february, amount=50, _quantity=2)

    # Test for January
    january_service = AnalyticsMonthlyService(user, year=2025, month=1)
    january_data = {
        "positive_categories": january_service.get_positive_categories_data(),
        "negative_categories": january_service.get_negative_categories_data(),
        "balance": january_service.get_balance(),
        "period": {
            "year": 2025,
            "month": 1
        }
    }
    serializer_data = AnalyticsMonthlySerializer(january_data).data
    assert serializer_data["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert serializer_data["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert serializer_data["balance"]["positive"] == decimal.Decimal("400.00")
    assert serializer_data["balance"]["negative"] == decimal.Decimal("200.00")
    assert serializer_data["balance"]["balance"] == decimal.Decimal("200.00")
    assert serializer_data["period"]["year"] == 2025
    assert serializer_data["period"]["month"] == 1

    # Test for February
    february_service = AnalyticsMonthlyService(user, year=2025, month=2)
    february_data = {
        "positive_categories": february_service.get_positive_categories_data(),
        "negative_categories": february_service.get_negative_categories_data(),
        "balance": february_service.get_balance(),
        "period": {
            "year": 2025,
            "month": 2
        }
    }
    serializer_data = AnalyticsMonthlySerializer(february_data).data
    assert serializer_data["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert serializer_data["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert serializer_data["balance"]["positive"] == decimal.Decimal("200.00")
    assert serializer_data["balance"]["negative"] == decimal.Decimal("100.00")
    assert serializer_data["balance"]["balance"] == decimal.Decimal("100.00")
    assert serializer_data["period"]["year"] == 2025
    assert serializer_data["period"]["month"] == 2
