from typing import TYPE_CHECKING

import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User

if TYPE_CHECKING:
    from rest_framework.test import APIClient

@pytest.fixture
def apiclient() -> APIClient:
    """Fixture for creating an unauthenticated APIClient."""
    return APIClient()

@pytest.fixture
def authenticated_apiclient(user):
    """Fixture for creating an authenticated APIClient."""
    client = APIClient()
    client.force_authenticate(user=user)
    yield client
    client.force_authenticate(user=None)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_200_OK, 1),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_user(
    client: str,
    status_code: str,
    user: User,
    request: pytest.FixtureRequest,
    count: int,
):
    client: APIClient = request.getfixturevalue(client)
    response = client.get("/api/users/")
    json = response.json()

    assert response.status_code == status_code
    assert len(json) == count
    ids = [user["id"] for user in json]
    assert str(user.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_200_OK),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_user(
    client: str,
    status_code: str,
    user: User,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)

    response = client.get(f"/api/users/{user.id}/")
    json = response.json()
    assert response.status_code == status_code
    assert json["id"] == str(user.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_201_CREATED),
    ],
)

def test_create_user(
    client: str,
    status_code: str,
    request: pytest.FixtureRequest,
    user_recipe: str,
):
    client: APIClient = request.getfixturevalue(client)

    user = baker.prepare_recipe(user_recipe)

    response = client.post(
        "/api/users/",
        data={"full_name": user.full_name, "email": user.email},
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["full_name"] == user.full_name
        assert json["email"] == user.email
