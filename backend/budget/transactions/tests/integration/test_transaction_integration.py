import pytest

from django.core.cache import cache

from rest_framework import status
from rest_framework.test import APIClient

from model_bakery import baker

from accounts.models import User
from transactions.models import Transaction


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED, 0),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_transaction(
    client: str,
    status_code: str,
    transaction: Transaction,
    request: pytest.FixtureRequest,
    count: int,
    user: User,
):
    cache.clear()
    
    client: APIClient = request.getfixturevalue(client)

    transaction.user = user
    transaction.save()

    response = client.get("/api/transactions/")

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        json = response.json()["results"]
        assert len(json) == count
        if count > 0:
            ids = [transaction["id"] for transaction in json]
            assert str(transaction.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_transaction(
    client: str,
    status_code: str,
    transaction: Transaction,
    request: pytest.FixtureRequest,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    transaction.user = user
    transaction.save()

    response = client.get(f"/api/transactions/{transaction.id}/")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["id"] == str(transaction.id)
