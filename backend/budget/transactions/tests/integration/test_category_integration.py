import pytest

from typing import TYPE_CHECKING

from model_bakery import baker
from rest_framework import status

from transactions.models import Category

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
def test_list_category(
    client: str,
    status_code: str,
    category: Category,
    request: pytest.FixtureRequest,
    count: int,
):
    client: APIClient = request.getfixturevalue(client)
    response = client.get("/api/categories/")
    json = response.json()

    assert response.status_code == status_code
    assert len(json) == count
    ids = [category["id"] for category in json]
    assert str(category.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_200_OK),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_category(
    client: str,
    status_code: str,
    category: Category,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)

    response = client.get(f"/api/categories/{category.id}/")
    json = response.json()
    assert response.status_code == status_code
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
    category_recipe: str,
    bucket_recipe: str,
):
    client: APIClient = request.getfixturevalue(client)

    category = baker.prepare_recipe(category_recipe)
    bucket = baker.make_recipe(bucket_recipe)
    response = client.post(
        "/api/categories/",
        data={
            "name": category.name,
            "bucket": bucket.pk,
        },
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == category.name
        assert json["bucket"] == str(bucket.pk)
