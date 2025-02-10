from faker import Faker
from model_bakery.recipe import Recipe
from model_bakery.recipe import foreign_key


from transactions.models import TransactionType
from transactions.models import Category

__all__ = ["transaction_type_recipe", "category_recipe"]

fake = Faker()

transaction_type_recipe = Recipe(
    TransactionType,
    sign=lambda: fake.random_element(
        [
            TransactionType.Sign.POSITIVE,
            TransactionType.Sign.NEGATIVE,
            TransactionType.Sign.NEUTRAL,
        ]
    ),
    name=lambda: fake.word(),
)

category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    transaction_type=foreign_key(transaction_type_recipe),
)
