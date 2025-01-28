import pytest
from model_bakery import baker
from core.models import Bucket
from core.models import Location


@pytest.fixture
def bucket(bucket_recipe) -> Bucket:
    """Fixture for creating a Bucket instance."""
    return baker.make_recipe(bucket_recipe)


@pytest.fixture
def location(location_recipe) -> Location:
    """Fixture for creating a Location instance."""
    return baker.make_recipe(location_recipe)
