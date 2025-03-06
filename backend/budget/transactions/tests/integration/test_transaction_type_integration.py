import pytest

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import TransactionType
from accounts.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN, 0),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_transaction_type(
    client: str,
    status_code: str,
    transaction_type: TransactionType,
    request: pytest.FixtureRequest,
    count: int,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    transaction_type.user = user
    transaction_type.save()

    response = client.get("/api/transaction-types/")

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert len(json) == count
        if count > 0:
            ids = [transaction_type["id"] for transaction_type in json]
            assert str(transaction_type.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_transaction_type(
    client: str,
    status_code: str,
    transaction_type: TransactionType,
    request: pytest.FixtureRequest,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    transaction_type.user = user
    transaction_type.save()

    response = client.get(f"/api/transaction-types/{transaction_type.id}/")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
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

    transaction_type = baker.make_recipe(transaction_type_recipe)

    response = client.post(
        "/api/transaction-types/",
        data={
            "name": transaction_type.name,
        },
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == transaction_type.name


@pytest.mark.django_db
def test_superuser_sees_all_transaction_types(
    admin_apiclient: APIClient,
    transaction_type_recipe: str,
    admin_user: User,
    user: User,
):
    """Test that superuser can see all transaction types."""
    user_transaction_type = baker.make_recipe(transaction_type_recipe)
    user_transaction_type.user = user
    user_transaction_type.save()

    admin_transaction_type = baker.make_recipe(transaction_type_recipe)
    admin_transaction_type.user = admin_user
    admin_transaction_type.save()

    response = admin_apiclient.get("/api/transaction-types/")
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) == 2
    ids = [transaction_type["id"] for transaction_type in json]
    assert str(user_transaction_type.id) in ids
    assert str(admin_transaction_type.id) in ids
