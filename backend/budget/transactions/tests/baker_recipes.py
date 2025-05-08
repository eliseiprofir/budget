from faker import Faker

from django.utils.timezone import make_aware

from model_bakery.recipe import Recipe
from model_bakery.recipe import foreign_key

from accounts.tests.baker_recipes import user_recipe
from core.tests.baker_recipes import bucket_recipe
from core.tests.baker_recipes import location_recipe
from transactions.models import TransactionType
from transactions.models import Category
from transactions.models import Transaction


__all__ = [
    "transaction_type_recipe",
    "category_recipe",
    "transaction_recipe",
    "positive_transaction_type_recipe",
    "positive_category_recipe",
    "positive_transaction_recipe",
    "negative_transaction_type_recipe",
    "negative_category_recipe",
    "negative_transaction_recipe",
    "neutral_transaction_type_recipe",
    "neutral_category_recipe",
    "neutral_transaction_recipe",
]

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
    user=foreign_key(user_recipe),
)

category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    transaction_type=foreign_key(transaction_type_recipe),
    user=foreign_key(user_recipe),
)

transaction_recipe = Recipe(
    Transaction,
    description=lambda: fake.word(),
    category=foreign_key(category_recipe),
    date=lambda: make_aware(fake.date_time()),
    amount=lambda: fake.pydecimal(
        left_digits=2,
        right_digits=2,
        positive=True,
        min_value=1,
        max_value=100
    ),
    location=foreign_key(location_recipe),
    bucket=foreign_key(bucket_recipe),
    user=foreign_key(user_recipe),
)

# Positive transaction type/category/transaction recipes
positive_transaction_type_recipe = Recipe(
    TransactionType,
    sign=lambda: TransactionType.Sign.POSITIVE,
    name=lambda: fake.word(),
    user=foreign_key(user_recipe),
)

positive_category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    transaction_type=foreign_key(positive_transaction_type_recipe),
    user=foreign_key(user_recipe),
)

positive_transaction_recipe = Recipe(
    Transaction,
    description=lambda: fake.word(),
    category=foreign_key(positive_category_recipe),
    date=lambda: make_aware(fake.date_time()),
    amount=lambda: fake.pydecimal(
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=10,
        max_value=1000
    ),
    location=foreign_key(location_recipe),
    bucket=foreign_key(bucket_recipe),
    user=foreign_key(user_recipe),
)

# Negative transaction type/category/transaction recipes
negative_transaction_type_recipe = Recipe(
    TransactionType,
    sign=lambda: TransactionType.Sign.NEGATIVE,
    name=lambda: fake.word(),
    user=foreign_key(user_recipe),
)

negative_category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    transaction_type=foreign_key(negative_transaction_type_recipe),
    user=foreign_key(user_recipe),
)

negative_transaction_recipe = Recipe(
    Transaction,
    description=lambda: fake.word(),
    category=foreign_key(negative_category_recipe),
    date=lambda: make_aware(fake.date_time()),
    amount=lambda: fake.pydecimal(
        left_digits=2,
        right_digits=2,
        positive=True,
        min_value=1,
        max_value=100
    ),
    location=foreign_key(location_recipe),
    bucket=foreign_key(bucket_recipe),
    user=foreign_key(user_recipe),
)

# Neutral transaction type/category/transaction recipes
neutral_transaction_type_recipe = Recipe(
    TransactionType,
    sign=lambda: TransactionType.Sign.NEUTRAL,
    name=lambda: fake.word(),
    user=foreign_key(user_recipe),
)

neutral_category_recipe = Recipe(
    Category,
    name=lambda: fake.word(),
    transaction_type=foreign_key(neutral_transaction_type_recipe),
    user=foreign_key(user_recipe),
)

neutral_transaction_recipe = Recipe(
    Transaction,
    description=lambda: fake.word(),
    category=foreign_key(neutral_category_recipe),
    date=lambda: make_aware(fake.date_time()),
    amount=lambda: 0,
    location=foreign_key(location_recipe),
    bucket=foreign_key(bucket_recipe),
    user=foreign_key(user_recipe),
)
