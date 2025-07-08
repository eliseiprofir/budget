import pytest

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from core.models import Location


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED, 0),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_location(
    client: str,
    status_code: str,
    location: Location,
    request: pytest.FixtureRequest,
    count: int,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    location.user = user
    location.save()

    response = client.get("/api/locations/")

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert len(json) == count
        if count > 0:
            ids = [location["id"] for location in json]
            assert str(location.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_location(
    client: str,
    status_code: str,
    location: Location,
    request: pytest.FixtureRequest,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    location.user = user
    location.save()

    response = client.get(f"/api/locations/{location.id}/")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["id"] == str(location.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED),
        ("authenticated_apiclient", status.HTTP_201_CREATED),
    ],
)
def test_create_location(
    client: str,
    status_code: str,
    request: pytest.FixtureRequest,
    location_recipe: str,
    user: User,
):
    client: APIClient = request.getfixturevalue(client)

    location = baker.prepare_recipe(location_recipe)

    response = client.post(
        "/api/locations/",
        data={
            "name": location.name,
            "user": user.pk
        },
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == location.name
