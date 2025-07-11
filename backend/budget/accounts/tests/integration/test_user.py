import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED, 0),
        ("authenticated_apiclient", status.HTTP_200_OK, 1),
    ],
)
def test_list_user(
    client: str,
    status_code: str,
    user: User,
    request: pytest.FixtureRequest,
    count: int,
    user_recipe: str,
):
    """Test listing users."""
    client: APIClient = request.getfixturevalue(client)

    other_user = baker.make_recipe(user_recipe)

    response = client.get("/api/users/")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert len(json) == count
        if count > 0:
            assert str(json[0]["id"]) == str(user.id)
            other_user_ids = [user["id"] for user in json]
            assert str(other_user.id) not in other_user_ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_401_UNAUTHORIZED),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_user(
    client: str,
    status_code: str,
    user: User,
    request: pytest.FixtureRequest,
):
    """Test getting a single user."""
    client: APIClient = request.getfixturevalue(client)

    response = client.get(f"/api/users/{user.id}/")
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json["id"] == str(user.id)
        assert json["email"] == user.email
        assert json["full_name"] == user.full_name
        assert "last_login" in json
        assert "created" in json
        assert "modified" in json


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_201_CREATED),
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
        data={"full_name": user.full_name, "email": user.email, "password": user.password},
    )
    json = response.json()
    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        json = response.json()
        assert json["full_name"] == user.full_name
        assert json["email"] == user.email


@pytest.mark.django_db
def test_user_cannot_access_other_profile(
    authenticated_apiclient: APIClient,
    user_recipe: str,
):
    """Test that a user cannot access another user's profile."""
    other_user = baker.make_recipe(user_recipe)

    response = authenticated_apiclient.get(f"/api/users/{other_user.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_user(
    authenticated_apiclient: APIClient,
    user: User,
):
    data = {
        "full_name": f"{user.full_name} - updated",
        "email": "updated@email.com",
        "password": "newpassword123",
    }

    response = authenticated_apiclient.put(f"/api/users/{user.id}/", data=data)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["full_name"] == data["full_name"]
    assert json["email"] == data["email"]
    user.refresh_from_db()
    assert user.check_password("newpassword123")
