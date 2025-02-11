import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code", "count"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN, 0),
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
        ("apiclient", status.HTTP_403_FORBIDDEN),
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
    user: User,
):
    """Test that a user cannot access another user's profile."""
    other_user = baker.make_recipe(user_recipe)

    response = authenticated_apiclient.get(f"/api/users/{other_user.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_superuser_sees_all_users(
    admin_apiclient: APIClient,
    user_recipe: str,
    admin_user: User,
):
    """Test that superuser can see all users."""
    user = baker.make_recipe(user_recipe)

    response = admin_apiclient.get("/api/users/")
    json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(json) >= 2 # admin_user, user
    ids = [user["id"] for user in json]
    assert str(user.id) in ids
    assert str(admin_user.id) in ids


@pytest.mark.django_db
def test_superuser_can_access_any_profile(
    admin_apiclient: APIClient,
    user_recipe: str,
    user: User,
):
    """Test that superuser can access any user profile."""
    response = admin_apiclient.get(f"/api/users/{user.id}/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert str(json["id"]) == str(user.id)
