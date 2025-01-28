import pytest

from typing import TYPE_CHECKING

from model_bakery import baker
from rest_framework import status

from accounts.models import User
from core.models import Bucket

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
def test_list_bucket(
    client: str,
    status_code: str,
    bucket: Bucket,
    request: pytest.FixtureRequest,
    count: int,
):
    client: APIClient = request.getfixturevalue(client)
    response = client.get("/api/buckets/")
    json = response.json()

    assert response.status_code == status_code
    assert len(json) == count
    ids = [bucket["id"] for bucket in json]
    assert str(bucket.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_200_OK),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_bucket(
    client: str,
    status_code: str,
    bucket: Bucket,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)

    response = client.get(f"/api/buckets/{bucket.id}/")
    json = response.json()
    assert response.status_code == status_code
    assert json["id"] == str(bucket.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_201_CREATED),
    ],
)
def test_create_bucket(
    client: str,
    status_code: str,
    request: pytest.FixtureRequest,
    bucket_recipe: str,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    bucket = baker.prepare_recipe(bucket_recipe)

    response = client.post(
        "/api/buckets/",
        data={
            "name": bucket.name,
            "allocation_percentage": bucket.allocation_percentage,
            "user": user.pk
        },
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == bucket.name
        assert json["allocation_percentage"] == str(bucket.allocation_percentage)
        assert json["user"] == str(user.pk)
