from faker import Faker
from model_bakery.recipe import Recipe
from model_bakery.recipe import foreign_key

from core.tests.baker_recipes import bucket_recipe
from transactions.models import Entry
from transactions.models import Category

__all__ = ["entry_recipe", "category_recipe"]

fake = Faker()

entry_recipe = Recipe(
    Entry,
    name=lambda: fake.random_element(
        [
            Entry.Name.EXPENSE,
            Entry.Name.INCOME,
            Entry.Name.TRANSFER,
        ]
    ),
)

category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    bucket=foreign_key(bucket_recipe),
)
