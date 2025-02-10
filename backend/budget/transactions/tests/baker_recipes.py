from faker import Faker
from model_bakery.recipe import Recipe
from model_bakery.recipe import foreign_key

from core.tests.baker_recipes import bucket_recipe
from transactions.models import TransactionType
from transactions.models import Category

__all__ = ["transaction_type_recipe", "category_recipe"]

fake = Faker()

transaction_type_recipe = Recipe(
    TransactionType,
    name=lambda: fake.word(),
)

category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    bucket=foreign_key(bucket_recipe),
)
