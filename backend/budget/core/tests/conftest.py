import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from model_bakery import baker

from core.management.commands.createdefaultsuperuser import DEFAULT_EMAIL
from core.models import Bucket
from core.models import Location

User = get_user_model()


@pytest.fixture
def bucket(bucket_recipe) -> Bucket:
    """Fixture for creating a Bucket instance."""
    return baker.make_recipe(bucket_recipe)


@pytest.fixture
def location(location_recipe) -> Location:
    """Fixture for creating a Location instance."""
    return baker.make_recipe(location_recipe)

@pytest.fixture
def defaultsuperuser():
    call_command("createdefaultsuperuser")
    return User.objects.get(email=DEFAULT_EMAIL)
