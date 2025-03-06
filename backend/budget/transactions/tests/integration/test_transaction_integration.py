import pytest

from rest_framework import status
from rest_framework.test import APIClient

from model_bakery import baker

from accounts.models import User
from transactions.models import Transaction


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_200_OK, 0),
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
    client: APIClient = request.getfixturevalue(client)

    transaction.user = user
    transaction.save()

    response = client.get("/api/transactions/")
    json = response.json()

    assert response.status_code == status_code
    assert len(json) == count
    if count > 0:
        ids = [transaction["id"] for transaction in json]
        assert str(transaction.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_404_NOT_FOUND),
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


@pytest.mark.django_db
def test_superuser_sees_all_transactions(
    admin_apiclient: APIClient,
    transaction_recipe: str,
    admin_user: User,
    user: User,
):
    """Test that superuser can see all transactions."""
    user_transaction = baker.make_recipe(transaction_recipe)
    user_transaction.user = user
    user_transaction.save()

    admin_transaction = baker.make_recipe(transaction_recipe)
    admin_transaction.user = admin_user
    admin_transaction.save()

    response = admin_apiclient.get("/api/transactions/")
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) == 2
    ids = [t["id"] for t in json]
    assert str(user_transaction.id) in ids
    assert str(admin_transaction.id) in ids
