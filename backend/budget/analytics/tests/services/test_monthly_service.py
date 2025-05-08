import pytest
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.monthly import AnalyticsMonthlyService


@pytest.mark.django_db
def test_get_positive_categories_data(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
):
    """Test get_positive_categories_data function to ensure it works properly."""
    service = AnalyticsMonthlyService(user, year=2025, month=1).get_positive_categories_data()
    assert service == {}

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=january, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=february, category=positive_category2, amount=100)

    service_january = AnalyticsMonthlyService(user, year=2025, month=1).get_positive_categories_data()
    assert service_january["Positive Category 1"] == 200
    assert service_january["Positive Category 2"] == 0

    service_february = AnalyticsMonthlyService(user, year=2025, month=2).get_positive_categories_data()
    assert service_february["Positive Category 1"] == 0
    assert service_february["Positive Category 2"] == 100


@pytest.mark.django_db
def test_get_negative_categories_data(
    user: User,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_negative_categories_data function to ensure it works properly."""
    service = AnalyticsMonthlyService(user, year=2025, month=1).get_negative_categories_data()
    assert service == {}

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    baker.make_recipe(negative_transaction_recipe, user=user, date=january, category=negative_category1, amount=200)
    baker.make_recipe(negative_transaction_recipe, user=user, date=february, category=negative_category2, amount=100)

    service_january = AnalyticsMonthlyService(user, year=2025, month=1).get_negative_categories_data()
    assert service_january["Negative Category 1"] == 200
    assert service_january["Negative Category 2"] == 0

    service_february = AnalyticsMonthlyService(user, year=2025, month=2).get_negative_categories_data()
    assert service_february["Negative Category 1"] == 0
    assert service_february["Negative Category 2"] == 100


@pytest.mark.django_db
def test_get_neutral_categories_data(
    user: User,
    neutral_category_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test get_neutral_categories_data function to ensure it works properly."""
    service = AnalyticsMonthlyService(user, year=2025, month=1).get_neutral_categories_data()
    assert service == {}

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    neutral_category1 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 1")
    neutral_category2 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 2")
    baker.make_recipe(neutral_transaction_recipe, user=user, date=january, category=neutral_category1, amount=200)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=january, category=neutral_category1, amount=-200)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=february, category=neutral_category2, amount=100)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=february, category=neutral_category2, amount=-100)

    service_january = AnalyticsMonthlyService(user, year=2025, month=1).get_neutral_categories_data()
    assert service_january["Neutral Category 1"] == 0
    assert service_january["Neutral Category 2"] == 0

    service_february = AnalyticsMonthlyService(user, year=2025, month=2).get_neutral_categories_data()
    assert service_february["Neutral Category 1"] == 0
    assert service_february["Neutral Category 2"] == 0


@pytest.mark.django_db
def test_get_balance(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test get_balance function to ensure it works properly."""
    service = AnalyticsMonthlyService(user, year=2025, month=1).get_balance()
    assert service == {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "balance": 0,
    }

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    baker.make_recipe(positive_transaction_recipe, user=user, date=january, amount=200)
    baker.make_recipe(negative_transaction_recipe, user=user, date=january, amount=100)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=january, amount=10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=january, amount=-10)
    baker.make_recipe(positive_transaction_recipe, user=user, date=february, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=february, amount=50)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=february, amount=10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=february, amount=-10)

    service_january = AnalyticsMonthlyService(user, year=2025, month=1).get_balance()
    assert service_january["positive"] == 200
    assert service_january["negative"] == 100
    assert service_january["neutral"] == 0
    assert service_january["balance"] == 100

    service_february = AnalyticsMonthlyService(user, year=2025, month=2).get_balance()
    assert service_february["positive"] == 100
    assert service_february["negative"] == 50
    assert service_february["neutral"] == 0
    assert service_february["balance"] == 50
