import pytest

from typing import TYPE_CHECKING

from model_bakery import baker
from rest_framework import status

from transactions.models import TransactionType

if TYPE_CHECKING:
    from rest_framework.test import APIClient


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_200_OK, 1),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_transaction_type(
    client: str,
    status_code: str,
    transaction_type: TransactionType,
    request: pytest.FixtureRequest,
    count: int,
):
    client: APIClient = request.getfixturevalue(client)
    response = client.get("/api/transaction_types/")
    json = response.json()

    assert response.status_code == status_code
    assert len(json) == count
    ids = [transaction_type["id"] for transaction_type in json]
    assert str(transaction_type.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_200_OK),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_transaction_type(
    client: str,
    status_code: str,
    transaction_type: TransactionType,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)

    response = client.get(f"/api/transaction_types/{transaction_type.id}/")
    json = response.json()
    assert response.status_code == status_code
    assert json["id"] == str(transaction_type.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_201_CREATED),
    ],
)
def test_create_transaction_type(
    client: str,
    status_code: str,
    request: pytest.FixtureRequest,
    transaction_type_recipe: str,
):
    client: APIClient = request.getfixturevalue(client)

    transaction_type = baker.prepare_recipe(transaction_type_recipe)
    response = client.post(
        "/api/transaction_types/",
        data={
            "sign": transaction_type.sign,
            "name": transaction_type.name,
        },
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["sign"] == transaction_type.sign
        assert json["name"] == transaction_type.name
