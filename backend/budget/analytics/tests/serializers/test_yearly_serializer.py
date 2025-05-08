import pytest
import decimal
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.yearly import AnalyticsYearlyService
from analytics.serializers.yearly import RepresentationSerializer
from analytics.serializers.yearly import AnalyticsYearlySerializer


@pytest.mark.django_db
def test_representation_serializer():
    """Test RepresentationSerializer to ensure it works properly."""
    data = {"Test": 1000,}
    serializer = RepresentationSerializer(data).to_representation(data)
    assert serializer == data


@pytest.mark.django_db
def test_analytics_yearly_serializer(
    user: User,
    positive_category_recipe: str,
    negative_category_recipe: str,
    neutral_category_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test AnalyticsYearlySerializer to ensure it works properly."""
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

    # Test for 2025
    year_2025_service = AnalyticsYearlyService(user, year=2025)
    year_2025_data = {
        "monthly": year_2025_service.get_year_data_by_month(),
        "summary": year_2025_service.get_year_summary(),
        "period": 2025,
    }
    serializer_data = AnalyticsYearlySerializer(year_2025_data).data

    for month in range(1, 13):
        assert "positive_categories" in serializer_data["monthly"][f"{month}"]
        assert "negative_categories" in serializer_data["monthly"][f"{month}"]
        assert "neutral_categories" in serializer_data["monthly"][f"{month}"]
        assert "balance" in serializer_data["monthly"][f"{month}"]

    assert serializer_data["monthly"]["1"]["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert serializer_data["monthly"]["1"]["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert serializer_data["monthly"]["1"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["monthly"]["1"]["balance"]["_total"] == decimal.Decimal("200.00")
    assert serializer_data["monthly"]["1"]["balance"]["positive"] == decimal.Decimal("400.00")
    assert serializer_data["monthly"]["1"]["balance"]["negative"] == decimal.Decimal("200.00")
    assert serializer_data["monthly"]["1"]["balance"]["neutral"] == decimal.Decimal("0.00")

    assert serializer_data["summary"]["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert serializer_data["summary"]["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert serializer_data["summary"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["summary"]["balance"]["_total"] == decimal.Decimal("200.00")
    assert serializer_data["summary"]["balance"]["positive"] == decimal.Decimal("400.00")
    assert serializer_data["summary"]["balance"]["negative"] == decimal.Decimal("200.00")
    assert serializer_data["summary"]["balance"]["neutral"] == decimal.Decimal("0.00")

    assert serializer_data["period"] == 2025

    # Test for 2026
    year_2026_service = AnalyticsYearlyService(user, year=2026)
    year_2026_data = {
        "monthly": year_2026_service.get_year_data_by_month(),
        "summary": year_2026_service.get_year_summary(),
        "period": 2026,
    }
    serializer_data = AnalyticsYearlySerializer(year_2026_data).data

    for month in range(1, 13):
        assert "positive_categories" in serializer_data["monthly"][f"{month}"]
        assert "negative_categories" in serializer_data["monthly"][f"{month}"]
        assert "neutral_categories" in serializer_data["monthly"][f"{month}"]
        assert "balance" in serializer_data["monthly"][f"{month}"]

    assert serializer_data["monthly"]["1"]["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert serializer_data["monthly"]["1"]["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert serializer_data["monthly"]["1"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["monthly"]["1"]["balance"]["_total"] == decimal.Decimal("100.00")
    assert serializer_data["monthly"]["1"]["balance"]["positive"] == decimal.Decimal("200.00")
    assert serializer_data["monthly"]["1"]["balance"]["negative"] == decimal.Decimal("100.00")
    assert serializer_data["monthly"]["1"]["balance"]["neutral"] == decimal.Decimal("0.00")

    assert serializer_data["summary"]["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert serializer_data["summary"]["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert serializer_data["summary"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert serializer_data["summary"]["balance"]["_total"] == decimal.Decimal("100.00")
    assert serializer_data["summary"]["balance"]["positive"] == decimal.Decimal("200.00")
    assert serializer_data["summary"]["balance"]["negative"] == decimal.Decimal("100.00")
    assert serializer_data["summary"]["balance"]["neutral"] == decimal.Decimal("0.00")

    assert serializer_data["period"] == 2026
