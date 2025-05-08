import pytest
import decimal
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.historical import AnalyticsHistoricalService
from analytics.serializers.historical import RepresentationSerializer
from analytics.serializers.historical import AnalyticsHistoricalSerializer


@pytest.mark.django_db
def test_representation_serializer():
    """Test RepresentationSerializer to ensure it works properly."""
    data = {"Test": 1000,}
    serializer = RepresentationSerializer(data).to_representation(data)
    assert serializer == data


@pytest.mark.django_db
def test_analytics_historical_serializer(
    user: User,
    positive_category_recipe: str,
    negative_category_recipe: str,
    neutral_category_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test AnalyticsHistoricalSerializer to ensure it works properly."""
    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 1, 1))

    positive_category = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category")
    negative_category = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category")
    neutral_category = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category")
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=year_2025, amount=200, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=year_2025, amount=100, _quantity=2)
    baker.make_recipe(neutral_transaction_recipe, user=user, category=neutral_category, date=year_2025, amount=0, _quantity=2)
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=year_2026, amount=100, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=year_2026, amount=50, _quantity=2)
    baker.make_recipe(neutral_transaction_recipe, user=user, category=neutral_category, date=year_2026, amount=0, _quantity=2)

    historical_service = AnalyticsHistoricalService(user)
    historical_data = {
        "yearly": historical_service.get_historical_data_by_year(),
        "summary": historical_service.get_historical_summary(),
    }
    serializer_data = AnalyticsHistoricalSerializer(historical_data).data

    years = historical_service.transactions.dates("date", "year").distinct()
    for year_date in years:
        year = year_date.year
        assert "positive_categories" in serializer_data["yearly"][f"{year}"]
        assert "negative_categories" in serializer_data["yearly"][f"{year}"]
        assert "neutral_categories" in serializer_data["yearly"][f"{year}"]
        assert "balance" in serializer_data["yearly"][f"{year}"]

    assert serializer_data["yearly"]["2025"]["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert serializer_data["yearly"]["2025"]["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert serializer_data["yearly"]["2025"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["yearly"]["2025"]["balance"]["positive"] == decimal.Decimal("400.00")
    assert serializer_data["yearly"]["2025"]["balance"]["negative"] == decimal.Decimal("200.00")
    assert serializer_data["yearly"]["2025"]["balance"]["neutral"] == decimal.Decimal("0.00")
    assert serializer_data["yearly"]["2025"]["balance"]["balance"] == decimal.Decimal("200.00")
    assert serializer_data["yearly"]["2026"]["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert serializer_data["yearly"]["2026"]["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert serializer_data["yearly"]["2026"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["yearly"]["2026"]["balance"]["positive"] == decimal.Decimal("200.00")
    assert serializer_data["yearly"]["2026"]["balance"]["negative"] == decimal.Decimal("100.00")
    assert serializer_data["yearly"]["2026"]["balance"]["neutral"] == decimal.Decimal("0.00")
    assert serializer_data["yearly"]["2026"]["balance"]["balance"] == decimal.Decimal("100.00")

    assert serializer_data["summary"]["positive_categories"]["Positive Category"] == decimal.Decimal("600.00")
    assert serializer_data["summary"]["negative_categories"]["Negative Category"] == decimal.Decimal("300.00")
    assert serializer_data["summary"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["summary"]["balance"]["positive"] == decimal.Decimal("600.00")
    assert serializer_data["summary"]["balance"]["negative"] == decimal.Decimal("300.00")
    assert serializer_data["summary"]["balance"]["neutral"] == decimal.Decimal("0.00")
    assert serializer_data["summary"]["balance"]["balance"] == decimal.Decimal("300.00")
