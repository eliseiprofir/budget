import pytest
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from analytics.services.historical import AnalyticsHistoricalService


@pytest.mark.django_db
def test_get_positive_categories_by_year(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
):
    """Test get_positive_categories_by_year function to ensure it works properly."""
    service = AnalyticsHistoricalService(user).get_positive_categories_by_year(year=2025)
    assert service == {}

    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 2, 1))

    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2026, category=positive_category2, amount=100)

    service_year_2025 = AnalyticsHistoricalService(user).get_positive_categories_by_year(year=2025)
    assert service_year_2025["Positive Category 1"] == 200
    assert service_year_2025["Positive Category 2"] == 0

    service_year_2026 = AnalyticsHistoricalService(user).get_positive_categories_by_year(year=2026)
    assert service_year_2026["Positive Category 1"] == 0
    assert service_year_2026["Positive Category 2"] == 100


@pytest.mark.django_db
def test_get_negative_categories_by_year(
    user: User,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_negative_categories_by_year function to ensure it works properly."""
    service = AnalyticsHistoricalService(user).get_negative_categories_by_year(year=2025)
    assert service == {}

    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 2, 1))

    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, category=negative_category1, amount=200)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2026, category=negative_category2, amount=100)

    service_year_2025 = AnalyticsHistoricalService(user).get_negative_categories_by_year(year=2025)
    assert service_year_2025["Negative Category 1"] == 200
    assert service_year_2025["Negative Category 2"] == 0

    service_year_2026 = AnalyticsHistoricalService(user).get_negative_categories_by_year(year=2026)
    assert service_year_2026["Negative Category 1"] == 0
    assert service_year_2026["Negative Category 2"] == 100


@pytest.mark.django_db
def test_get_neutral_categories_by_year(
    user: User,
    neutral_category_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test get_neutral_categories_by_year function to ensure it works properly."""
    service = AnalyticsHistoricalService(user).get_neutral_categories_by_year(year=2025)
    assert service == {}

    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 2, 1))

    neutral_category1 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 1")
    neutral_category2 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 2")
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, category=neutral_category1, amount=200)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, category=neutral_category1, amount=-200)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, category=neutral_category2, amount=100)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, category=neutral_category2, amount=-100)

    service_year_2025 = AnalyticsHistoricalService(user).get_neutral_categories_by_year(year=2025)
    assert service_year_2025["Neutral Category 1"] == 0
    assert service_year_2025["Neutral Category 2"] == 0

    service_year_2026 = AnalyticsHistoricalService(user).get_neutral_categories_by_year(year=2026)
    assert service_year_2026["Neutral Category 1"] == 0
    assert service_year_2026["Neutral Category 2"] == 0


@pytest.mark.django_db
def test_get_balance_by_year(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test get_balance_by_year function to ensure it works properly."""
    service = AnalyticsHistoricalService(user).get_balance_by_year(year=2025)
    assert service == {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "balance": 0,
    }

    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 2, 1))

    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, amount=200)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, amount=100)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, amount=10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, amount=-10)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2026, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2026, amount=50)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, amount=10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, amount=-10)

    service_year_2025 = AnalyticsHistoricalService(user).get_balance_by_year(year=2025)
    assert service_year_2025["positive"] == 200
    assert service_year_2025["negative"] == 100
    assert service_year_2025["neutral"] == 0
    assert service_year_2025["balance"] == 100

    service_year_2026 = AnalyticsHistoricalService(user).get_balance_by_year(year=2026)
    assert service_year_2026["positive"] == 100
    assert service_year_2026["negative"] == 50
    assert service_year_2026["neutral"] == 0
    assert service_year_2026["balance"] == 50


@pytest.mark.django_db
def test_get_historical_data_by_year(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
    neutral_category_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test get_historical_data_by_year function to ensure it works properly."""
    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 2, 1))
    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    neutral_category1 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 1")
    neutral_category2 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2026, category=positive_category2, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, category=negative_category1, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2026, category=negative_category2, amount=50)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, category=neutral_category1, amount=10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, category=neutral_category1, amount=-10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, category=neutral_category2, amount=20)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, category=neutral_category2, amount=-20)

    service = AnalyticsHistoricalService(user)
    service_data = service.get_historical_data_by_year()
    years = AnalyticsHistoricalService(user).transactions.dates("date", "year").distinct()
    yearly_data = {}
    for year_date in years:
        year = year_date.year
        data = {
            "positive_categories": service.get_positive_categories_by_year(year),
            "negative_categories": service.get_negative_categories_by_year(year),
            "neutral_categories": service.get_neutral_categories_by_year(year),
            "balance": service.get_balance_by_year(year),
        }
        yearly_data[str(year)] = data

    assert service_data == yearly_data


@pytest.mark.django_db
def test_get_historical_summary(
    user: User,
    positive_category_recipe: str,
    positive_transaction_recipe: str,
    negative_category_recipe: str,
    negative_transaction_recipe: str,
    neutral_category_recipe: str,
    neutral_transaction_recipe: str,
):
    """Test get_historical_summary function to ensure it works properly."""
    year_2025 = make_aware(datetime(2025, 1, 1))
    year_2026 = make_aware(datetime(2026, 2, 1))
    positive_category1 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 1")
    positive_category2 = baker.make_recipe(positive_category_recipe, user=user, name="Positive Category 2")
    negative_category1 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 1")
    negative_category2 = baker.make_recipe(negative_category_recipe, user=user, name="Negative Category 2")
    neutral_category1 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 1")
    neutral_category2 = baker.make_recipe(neutral_category_recipe, user=user, name="Neutral Category 2")
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2025, category=positive_category2, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, category=negative_category1, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2025, category=negative_category2, amount=50)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, category=neutral_category1, amount=10)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2025, category=neutral_category1, amount=-10)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2026, category=positive_category1, amount=200)
    baker.make_recipe(positive_transaction_recipe, user=user, date=year_2026, category=positive_category2, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2026, category=negative_category1, amount=100)
    baker.make_recipe(negative_transaction_recipe, user=user, date=year_2026, category=negative_category2, amount=50)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, category=neutral_category2, amount=20)
    baker.make_recipe(neutral_transaction_recipe, user=user, date=year_2026, category=neutral_category2, amount=-20)

    service = AnalyticsHistoricalService(user)
    service_data = service.get_historical_summary()

    historical_summary = {
        "positive_categories": {},
        "negative_categories": {},
        "neutral_categories": {},
        "balance": {}
    }

    positive_categories = service.get_positive_categories()
    negative_categories = service.get_negative_categories()
    neutral_categories = service.get_neutral_categories()
    transactions = service.transactions

    for category in positive_categories:
        year_category_transactions = transactions.filter(category=category)
        historical_summary["positive_categories"][category.name] = AnalyticsHistoricalService.sum_transactions(year_category_transactions)

    for category in negative_categories:
        year_category_transactions = transactions.filter(category=category)
        historical_summary["negative_categories"][category.name] = AnalyticsHistoricalService.sum_transactions(year_category_transactions)

    for category in neutral_categories:
        year_category_transactions = transactions.filter(category=category)
        historical_summary["neutral_categories"][category.name] = AnalyticsHistoricalService.sum_transactions(year_category_transactions)

    historical_summary["balance"] = service.get_balance_for_queryset(transactions)

    assert service_data == historical_summary
