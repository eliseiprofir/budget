import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_current_analytics(
    client: str,
    status_code: int,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)
    
    url = reverse("api:analytics-current-list")
    response = client.get(url)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert "balance" in json
        assert "locations" in json
        assert "buckets" in json


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_monthly_analytics(
    client: str,
    status_code: int,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)
    
    url = reverse("api:analytics-monthly-list")
    response = client.get(url)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert "balance" in json
        assert "positive_categories" in json
        assert "negative_categories" in json
        assert "period" in json
        assert isinstance(json["period"]["year"], int)
        assert isinstance(json["period"]["month"], int)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_yearly_analytics(
    client: str,
    status_code: int,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)
    
    url = reverse("api:analytics-yearly-list")
    response = client.get(url)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert "monthly" in json
        assert isinstance(json["monthly"], dict)
        # Check first month structure
        first_month = json["monthly"]["1"]
        assert "balance" in first_month
        assert "positive_categories" in first_month
        assert "negative_categories" in first_month


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_historical_analytics(
    client: str,
    status_code: int,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)
    
    url = reverse("api:analytics-historical-list")
    response = client.get(url)

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert "yearly" in json
        assert "summary" in json
        assert isinstance(json["yearly"], dict)
        assert isinstance(json["summary"], dict)
        assert "balance" in json["summary"]
        assert "positive_categories" in json["summary"]
        assert "negative_categories" in json["summary"]


@pytest.mark.django_db
def test_superuser_access(admin_apiclient: APIClient):
    """Test that superuser has access to all analytics endpoints."""
    endpoints = [
        "api:analytics-current-list",
        "api:analytics-monthly-list",
        "api:analytics-yearly-list",
        "api:analytics-historical-list",
    ]

    for endpoint in endpoints:
        url = reverse(endpoint)
        response = admin_apiclient.get(url)
        assert response.status_code == status.HTTP_200_OK
