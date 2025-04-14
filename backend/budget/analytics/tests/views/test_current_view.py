import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse

from accounts.models import User


@pytest.mark.django_db
def test_analytics_current_view(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test for AnalyticsCurrentViewSet to ensure it works correctly."""
    baker.make_recipe(positive_transaction_recipe, user=user, amount=100, _quantity=2)
    baker.make_recipe(negative_transaction_recipe, user=user, amount=50, _quantity=2)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("api:analytics-current-list")
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert "balance" in data
    assert "locations" in data
    assert "buckets" in data

    assert data["balance"]["positive"] == 200
    assert data["balance"]["negative"] == 100
    assert data["balance"]["balance"] == 100


@pytest.mark.django_db
def test_analytics_current_view_unauthorized():
    """Test for unauthorized access."""
    client = APIClient()
    url = reverse("api:analytics-current-list")
    response = client.get(url)
    assert response.status_code == 401
