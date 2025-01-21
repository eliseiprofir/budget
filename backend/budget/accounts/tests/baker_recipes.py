from faker import Faker
from model_bakery.recipe import Recipe
from accounts.models import User

__all__ = ["user_recipe"]

fake = Faker()

user_recipe = Recipe(
    User,
    full_name=lambda: fake.name(),
    email=lambda: fake.email(),
    password=lambda: fake.password(),
)
