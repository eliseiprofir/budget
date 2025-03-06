import pytest
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.yearly import AnalyticsYearlyService

@pytest.mark.django_db
def test_get_positive_categories_by_month(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
):
    """Test get_positive_categories_by_month function to ensure it works properly."""
    service = AnalyticsYearlyService(user, year=2025).get_positive_categories_by_month(month=1)
    assert service == {}

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=january, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=february, category=positive_category2, amount=100)

    service_january = AnalyticsYearlyService(user, year=2025).get_positive_categories_by_month(month=1)
    assert service_january["Positive Category 1"] == 200
    assert service_january["Positive Category 2"] == 0

    service_february = AnalyticsYearlyService(user, year=2025).get_positive_categories_by_month(month=2)
    assert service_february["Positive Category 1"] == 0
    assert service_february["Positive Category 2"] == 100

@pytest.mark.django_db
def test_get_negative_categories_by_month(
    user: User,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_negative_categories_by_month function to ensure it works properly."""
    service = AnalyticsYearlyService(user, year=2025).get_negative_categories_by_month(month=1)
    assert service == {}

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    baker.make_recipe(negative_transaction_recipe, user=user, date=january, category=negative_category1, amount=200)
    baker.make_recipe(negative_transaction_recipe, user=user, date=february, category=negative_category2, amount=100)

    service_january = AnalyticsYearlyService(user, year=2025).get_negative_categories_by_month(month=1)
    assert service_january["Negative Category 1"] == 200
    assert service_january["Negative Category 2"] == 0

    service_february = AnalyticsYearlyService(user, year=2025).get_negative_categories_by_month(month=2)
    assert service_february["Negative Category 1"] == 0
    assert service_february["Negative Category 2"] == 100

@pytest.mark.django_db
def test_get_balance_by_month(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_balance_by_month function to ensure it works properly."""
    service = AnalyticsYearlyService(user, year=2025).get_balance_by_month(month=1)
    assert service == {
        "positive": 0,
        "negative": 0,
        "balance": 0,
    }

    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))

    baker.make_recipe(positive_transaction_recipe, user=user, date=january, amount=200)
    baker.make_recipe(negative_transaction_recipe, user=user, date=january, amount=100)
    baker.make_recipe(positive_transaction_recipe, user=user, date=february, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=february, amount=50)

    service_january = AnalyticsYearlyService(user, year=2025).get_balance_by_month(month=1)
    assert service_january["positive"] == 200
    assert service_january["negative"] == 100
    assert service_january["balance"] == 100

    service_february = AnalyticsYearlyService(user, year=2025).get_balance_by_month(month=2)
    assert service_february["positive"] == 100
    assert service_february["negative"] == 50
    assert service_february["balance"] == 50

@pytest.mark.django_db
def test_get_year_data_by_month(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_year_data_by_month function to ensure it works properly."""
    january = make_aware(datetime(2025, 1, 1))
    february = make_aware(datetime(2025, 2, 1))
    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=january, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=february, category=positive_category2, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=january, category=negative_category1, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=february, category=negative_category2, amount=50)

    service = AnalyticsYearlyService(user, year=2025).get_year_data_by_month()
    monthly_data = {}
    for month in range(1, 13):
        data = {
            "positive_categories": AnalyticsYearlyService(user, year=2025).get_positive_categories_by_month(month),
            "negative_categories": AnalyticsYearlyService(user, year=2025).get_negative_categories_by_month(month),
            "balance": AnalyticsYearlyService(user, year=2025).get_balance_by_month(month),
        }
        monthly_data[str(month)] = data

    assert service == monthly_data

@pytest.mark.django_db
def test_get_year_summary(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_year_summary function to ensure it works properly."""
    year_2025 = make_aware(datetime(2025, 1, 1))
    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, category=positive_category2, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, category=negative_category1, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, category=negative_category2, amount=50)

    service = AnalyticsYearlyService(user, year=2025).get_year_summary()

    year_summary = {
        "positive_categories": {},
        "negative_categories": {},
        "balance": {}
    }

    positive_categories = AnalyticsYearlyService(user, year=2025).get_positive_categories()
    negative_categories = AnalyticsYearlyService(user, year=2025).get_negative_categories()
    year_transactions = AnalyticsYearlyService(user, year=2025).get_transactions_by_year(2025)

    for category in positive_categories:
        year_category_transactions = year_transactions.filter(category=category)
        year_summary["positive_categories"][category.name] = AnalyticsYearlyService.sum_transactions(year_category_transactions)

    for category in negative_categories:
        year_category_transactions = year_transactions.filter(category=category)
        year_summary["negative_categories"][category.name] = AnalyticsYearlyService.sum_transactions(year_category_transactions)

    year_summary["balance"] = AnalyticsYearlyService(user, year=2025).get_balance_for_queryset(year_transactions)

    assert service == year_summary
