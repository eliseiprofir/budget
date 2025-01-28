import pytest

from typing import TYPE_CHECKING

from model_bakery import baker
from rest_framework import status

from transactions.models import Entry

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
def test_list_entry(
    client: str,
    status_code: str,
    entry: Entry,
    request: pytest.FixtureRequest,
    count: int,
):
    client: APIClient = request.getfixturevalue(client)
    response = client.get("/api/entries/")
    json = response.json()

    assert response.status_code == status_code
    assert len(json) == count
    ids = [entry["id"] for entry in json]
    assert str(entry.id) in ids


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_200_OK),
        ("authenticated_apiclient", status.HTTP_200_OK),
    ],
)
def test_get_entry(
    client: str,
    status_code: str,
    entry: Entry,
    request: pytest.FixtureRequest,
):
    client: APIClient = request.getfixturevalue(client)

    response = client.get(f"/api/entries/{entry.id}/")
    json = response.json()
    assert response.status_code == status_code
    assert json["id"] == str(entry.id)


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client", "status_code"),
    [
        ("apiclient", status.HTTP_403_FORBIDDEN),
        ("authenticated_apiclient", status.HTTP_201_CREATED),
    ],
)

def test_create_entry(
    client: str,
    status_code: str,
    request: pytest.FixtureRequest,
    entry_recipe: str,
):
    client: APIClient = request.getfixturevalue(client)

    entry = baker.prepare_recipe(entry_recipe)

    response = client.post(
        "/api/entries/",
        data={"name": entry.name},
    )
    json = response.json()
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert json["name"] == entry.name
