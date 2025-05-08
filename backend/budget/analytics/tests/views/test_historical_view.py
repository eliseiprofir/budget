import pytest
import decimal
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.historical import AnalyticsHistoricalService


@pytest.mark.django_db
def test_analytics_yearly_view(
    user: User,
    positive_category_recipe: str,
    negative_category_recipe: str,
    neutral_category_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
    neutral_transaction_recipe: str
):
    """Test for AnalyticsYearlyViewSet to ensure it works correctly."""
    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 1, 1))

    positive_category = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category")
    negative_category = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category")
    neutral_category = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category")
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=year_2025, amount=200, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=year_2025, amount=100, _quantity=2)
    baker.make_recipe(neutral_transaction_recipe, user=user, category=neutral_category, date=year_2025, amount=10, _quantity=1)
    baker.make_recipe(neutral_transaction_recipe, user=user, category=neutral_category, date=year_2025, amount=-10, _quantity=1)
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=year_2026, amount=100, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=year_2026, amount=50, _quantity=2)
    baker.make_recipe(neutral_transaction_recipe, user=user, category=neutral_category, date=year_2026, amount=10, _quantity=1)
    baker.make_recipe(neutral_transaction_recipe, user=user, category=neutral_category, date=year_2026, amount=-10, _quantity=1)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-historical-list")
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    historical_service = AnalyticsHistoricalService(user)
    years = historical_service.transactions.dates("date", "year").distinct()
    for year_date in years:
        year = year_date.year
        assert "positive_categories" in data["yearly"][f"{year}"]
        assert "negative_categories" in data["yearly"][f"{year}"]
        assert "neutral_categories" in data["yearly"][f"{year}"]
        assert "balance" in data["yearly"][f"{year}"]

    assert data["yearly"]["2025"]["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert data["yearly"]["2025"]["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert data["yearly"]["2025"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert data["yearly"]["2025"]["balance"]["_total"] == decimal.Decimal("200.00")
    assert data["yearly"]["2025"]["balance"]["positive"] == decimal.Decimal("400.00")
    assert data["yearly"]["2025"]["balance"]["negative"] == decimal.Decimal("200.00")
    assert data["yearly"]["2025"]["balance"]["neutral"] == decimal.Decimal("0.00")
    assert data["yearly"]["2026"]["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert data["yearly"]["2026"]["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert data["yearly"]["2026"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert data["yearly"]["2026"]["balance"]["_total"] == decimal.Decimal("100.00")
    assert data["yearly"]["2026"]["balance"]["positive"] == decimal.Decimal("200.00")
    assert data["yearly"]["2026"]["balance"]["negative"] == decimal.Decimal("100.00")
    assert data["yearly"]["2026"]["balance"]["neutral"] == decimal.Decimal("0.00")

    assert data["summary"]["positive_categories"]["Positive Category"] == decimal.Decimal("600.00")
    assert data["summary"]["negative_categories"]["Negative Category"] == decimal.Decimal("300.00")
    assert data["summary"]["neutral_categories"]["Neutral Category"] == decimal.Decimal("0.00")
    assert data["summary"]["balance"]["_total"] == decimal.Decimal("300.00")
    assert data["summary"]["balance"]["positive"] == decimal.Decimal("600.00")
    assert data["summary"]["balance"]["negative"] == decimal.Decimal("300.00")
    assert data["summary"]["balance"]["neutral"] == decimal.Decimal("0.00")


@pytest.mark.django_db
def test_analytics_yearly_view_unauthorized():
    """Test for unauthorized access."""
    client = APIClient()
    url = reverse("api:analytics-historical-list")
    response = client.get(url)
    assert response.status_code == 401
