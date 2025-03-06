import pytest

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from transactions.models import Category
from accounts.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN, 0),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_category(
    client: str,
    status_code: str,
    category: Category,
    request: pytest.FixtureRequest,
    count: int,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    category.user = user
    category.save()

    response = client.get("/api/categories/")

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert len(json) == count
        if count > 0:
            ids = [category["id"] for category in json]
            assert str(category.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_category(
    client: str,
    status_code: str,
    category: Category,
    request: pytest.FixtureRequest,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    category.user = user
    category.save()

    response = client.get(f"/api/categories/{category.id}/")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["id"] == str(category.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_201_CREATED),
    ],
)
def test_create_category(
    client: str,
    status_code: str,
    request: pytest.FixtureRequest,
    transaction_type_recipe: str,
    category_recipe: str,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    transaction_type = baker.make_recipe(transaction_type_recipe, user=user)
    category = baker.make_recipe(category_recipe)
    response = client.post(
        "/api/categories/",
        data={
            "name": category.name,
            "transaction_type": str(transaction_type.pk),
        },
    )
    json = response.json()
    print(response.content)
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == category.name
        assert json["transaction_type"] == str(transaction_type.pk)


@pytest.mark.django_db
def test_superuser_sees_all_categories(
    admin_apiclient: APIClient,
    category_recipe: str,
    admin_user: User,
    user: User,
):
    """Test that superuser can see all transaction types."""
    user_category = baker.make_recipe(category_recipe)
    user_category.user = user
    user_category.save()

    admin_category = baker.make_recipe(category_recipe)
    admin_category.user = admin_user
    admin_category.save()

    response = admin_apiclient.get("/api/categories/")
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) == 2
    ids = [category["id"] for category in json]
    assert str(user_category.id) in ids
    assert str(admin_category.id) in ids
