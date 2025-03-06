import pytest
import decimal
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User


@pytest.mark.django_db
def test_analytics_yearly_view(
    user: User,
    positive_category_recipe: str,
    negative_category_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test for AnalyticsYearlyViewSet to ensure it works correctly."""
    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 1, 1))

    positive_category = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category")
    negative_category = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category")
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=year_2025, amount=200, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=year_2025, amount=100, _quantity=2)
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=year_2026, amount=100, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=year_2026, amount=50, _quantity=2)

    client = APIClient()
    client.force_authenticate(user=user)

    # Test for 2025
    url = reverse("api:analytics-yearly-custom", kwargs={"year": 2025})
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    for month in range(1, 13):
        assert "positive_categories" in data["monthly"][f"{month}"]
        assert "negative_categories" in data["monthly"][f"{month}"]
        assert "balance" in data["monthly"][f"{month}"]

    assert data["monthly"]["1"]["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert data["monthly"]["1"]["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert data["monthly"]["1"]["balance"]["positive"] == decimal.Decimal("400.00")
    assert data["monthly"]["1"]["balance"]["negative"] == decimal.Decimal("200.00")
    assert data["monthly"]["1"]["balance"]["balance"] == decimal.Decimal("200.00")

    assert data["summary"]["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert data["summary"]["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert data["summary"]["balance"]["positive"] == decimal.Decimal("400.00")
    assert data["summary"]["balance"]["negative"] == decimal.Decimal("200.00")
    assert data["summary"]["balance"]["balance"] == decimal.Decimal("200.00")

    assert data["period"] == 2025

    # Test for 2026
    url = reverse("api:analytics-yearly-custom", kwargs={"year": 2026})
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()
    for month in range(1, 13):
        assert "positive_categories" in data["monthly"][f"{month}"]
        assert "negative_categories" in data["monthly"][f"{month}"]
        assert "balance" in data["monthly"][f"{month}"]

    assert data["monthly"]["1"]["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert data["monthly"]["1"]["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert data["monthly"]["1"]["balance"]["positive"] == decimal.Decimal("200.00")
    assert data["monthly"]["1"]["balance"]["negative"] == decimal.Decimal("100.00")
    assert data["monthly"]["1"]["balance"]["balance"] == decimal.Decimal("100.00")

    assert data["summary"]["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert data["summary"]["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert data["summary"]["balance"]["positive"] == decimal.Decimal("200.00")
    assert data["summary"]["balance"]["negative"] == decimal.Decimal("100.00")
    assert data["summary"]["balance"]["balance"] == decimal.Decimal("100.00")

    assert data["period"] == 2026


@pytest.mark.django_db
def test_analytics_yearly_view_unauthorized():
    """Test for unauthorized access."""
    client = APIClient()
    url = reverse("api:analytics-yearly-list")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_analytics_monthly_view_invalid_year(user: User):
    """Test for invalid year value."""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-yearly-custom", kwargs={"year": 1800})
    response = client.get(url)
    assert response.status_code == 400
    assert response.json() == {"error": "Year must be between 1900 and 2100"}


@pytest.mark.django_db
def test_analytics_monthly_view_invalid_format(user: User):
    """Test for invalid year format."""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-yearly-custom", kwargs={"year": "abcd"})
    response = client.get(url)
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid year format"}
