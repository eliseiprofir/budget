import pytest
import decimal
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User


@pytest.mark.django_db
def test_analytics_monthly_view(
    user: User,
    positive_category_recipe: str,
    negative_category_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test for AnalyticsMonthlyViewSet to ensure it works correctly."""
    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    positive_category = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category")
    negative_category = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category")
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=january, amount=200, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=january, amount=100, _quantity=2)
    baker.make_recipe(positive_transaction_recipe, user=user, category=positive_category, date=february, amount=100, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, category=negative_category, date=february, amount=50, _quantity=2)


    client = APIClient()
    client.force_authenticate(user=user)

    # Test for january
    url = reverse("api:analytics-monthly-custom", kwargs={"year": 2025, "month": 1})
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()
    assert data["positive_categories"]["Positive Category"] == decimal.Decimal("400.00")
    assert data["negative_categories"]["Negative Category"] == decimal.Decimal("200.00")
    assert data["balance"]["positive"] == decimal.Decimal("400.00")
    assert data["balance"]["negative"] == decimal.Decimal("200.00")
    assert data["balance"]["balance"] == decimal.Decimal("200.00")
    assert data["period"]["year"] == 2025
    assert data["period"]["month"] == 1

    # Test for february
    url = reverse("api:analytics-monthly-custom", kwargs={"year": 2025, "month": 2})
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()
    assert data["positive_categories"]["Positive Category"] == decimal.Decimal("200.00")
    assert data["negative_categories"]["Negative Category"] == decimal.Decimal("100.00")
    assert data["balance"]["positive"] == decimal.Decimal("200.00")
    assert data["balance"]["negative"] == decimal.Decimal("100.00")
    assert data["balance"]["balance"] == decimal.Decimal("100.00")
    assert data["period"]["year"] == 2025
    assert data["period"]["month"] == 2


@pytest.mark.django_db
def test_analytics_monthly_view_unauthorized():
    """Test for unauthorized access."""
    client = APIClient()
    url = reverse("api:analytics-monthly-list")
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_analytics_monthly_view_invalid_month(user: User):
    """Test for invalid month value."""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-monthly-custom", kwargs={"year": 2025, "month": 13})
    response = client.get(url)
    assert response.status_code == 400
    assert response.json() == {"error": "Month must be between 1 and 12"}


@pytest.mark.django_db
def test_analytics_monthly_view_invalid_year(user: User):
    """Test for invalid year value."""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-monthly-custom", kwargs={"year": 1800, "month": 1})
    response = client.get(url)
    assert response.status_code == 400
    assert response.json() == {"error": "Year must be between 1900 and 2100"}


@pytest.mark.django_db
def test_analytics_monthly_view_invalid_format(user: User):
    """Test for invalid month/year format."""
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-monthly-custom", kwargs={"year": "abcd", "month": "ef"})
    response = client.get(url)
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid month or year format"}
