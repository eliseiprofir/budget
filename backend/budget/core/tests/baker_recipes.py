from faker import Faker
from model_bakery.recipe import Recipe
from model_bakery.recipe import foreign_key

from accounts.tests.baker_recipes import user_recipe
from core.models import Bucket
from core.models import Location

__all__ = ["bucket_recipe", "location_recipe"]

fake = Faker()

bucket_recipe = Recipe(
    Bucket,
    name=lambda: fake.word(),
    allocation_percentage=lambda: fake.pydecimal(
        left_digits=2,
        right_digits=2,
        positive=True,
        min_value=1,
        max_value=100
    ),
    user=foreign_key(user_recipe),
)

location_recipe = Recipe(
    Location,
    name=lambda: fake.word(),
    user=foreign_key(user_recipe),
)
