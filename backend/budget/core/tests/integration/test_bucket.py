import pytest

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from core.models import Bucket


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN, 0),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_bucket(
    client: str,
    status_code: str,
    bucket: Bucket,
    request: pytest.FixtureRequest,
    count: int,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    bucket.user = user
    bucket.save()

    response = client.get("/api/buckets/")

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert len(json) == count
        if count > 0:
            ids = [bucket["id"] for bucket in json]
            assert str(bucket.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_bucket(
    client: str,
    status_code: str,
    bucket: Bucket,
    request: pytest.FixtureRequest,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    bucket.user = user
    bucket.save()

    response = client.get(f"/api/buckets/{bucket.id}/")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
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
        },
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == bucket.name
        assert json["allocation_percentage"] == str(bucket.allocation_percentage)


@pytest.mark.django_db
def test_superuser_sees_all_buckets(
    admin_apiclient: APIClient,
    bucket_recipe: str,
    user_recipe: str,
):
    """Test that superuser can see all buckets."""
    user = baker.make_recipe(user_recipe)
    admin_user = baker.make_recipe(user_recipe, is_staff=True, is_superuser=True)
    user_bucket = baker.make_recipe(bucket_recipe, user=user, allocation_percentage=99)
    admin_bucket = baker.make_recipe(bucket_recipe, user=admin_user, allocation_percentage=99)

    response = admin_apiclient.get("/api/buckets/")
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) == 2
    ids = [bucket["id"] for bucket in json]
    assert str(user_bucket.id) in ids
    assert str(admin_bucket.id) in ids
