import pytest
from model_bakery import baker
from django.utils.timezone import make_aware
from datetime import datetime

from accounts.models import User
from transactions.models import Transaction
from analytics.services.base import AnalyticsBaseService


@pytest.mark.django_db
def test_get_positive_categories(
    user: User,
    positive_category_recipe: str,
):
    """Test get_positive_categories function to ensure it works properly."""
    baker.make_recipe(positive_category_recipe, _quantity=3, user=user)
    service = AnalyticsBaseService.get_positive_categories(user)
    assert service.count() == 3


@pytest.mark.django_db
def test_get_negative_categories(
    user: User,
    negative_category_recipe: str,
):
    """Test get_negative_categories function to ensure it works properly."""
    baker.make_recipe(negative_category_recipe, _quantity=2, user=user)
    service = AnalyticsBaseService.get_negative_categories(user)
    assert service.count() == 2


@pytest.mark.django_db
def test_get_positive_transactions(
    user: User,
    positive_transaction_recipe: str,
):
    """Test get_positive_transactions function to ensure it works properly."""
    baker.make_recipe(positive_transaction_recipe, _quantity=3, user=user)
    service = AnalyticsBaseService.get_positive_transactions(user)
    assert service.count() == 3


@pytest.mark.django_db
def test_get_negative_transactions(
    user: User,
    negative_transaction_recipe: str,
):
    """Test get_negative_transactions function to ensure it works properly."""
    baker.make_recipe(negative_transaction_recipe, _quantity=2, user=user)
    service = AnalyticsBaseService.get_negative_transactions(user)
    assert service.count() == 2


@pytest.mark.django_db
def test_sum_transactions(
    user: User,
    transaction_recipe: str,
):
    """Test sum_transactions function to ensure it works properly."""
    baker.make_recipe(transaction_recipe, _quantity=5, user=user)
    transactions = Transaction.objects.all()
    service = AnalyticsBaseService.sum_transactions(transactions)
    assert service == sum([transaction.amount for transaction in transactions])


@pytest.mark.django_db
def test_get_balance_for_queryset(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_balance_for_queryset function to ensure it works properly."""
    baker.make_recipe(positive_transaction_recipe, amount=100, user=user)
    baker.make_recipe(negative_transaction_recipe, amount=50, user=user)
    transactions = Transaction.objects.all()

    service = AnalyticsBaseService(user).get_balance_for_queryset(transactions)
    assert service == {
        "positive": 100,
        "negative": 50,
        "balance": 50,
    }


@pytest.mark.django_db
def test_get_transactions_by_month(
    user: User,
    transaction_recipe: str,
):
    """Test get_transactions_by_month function to ensure it works properly."""
    date_january = make_aware(datetime(2025, 1, 1))
    date_february = make_aware(datetime(2025, 2, 1))
    baker.make_recipe(transaction_recipe, date=date_january, _quantity=3, user=user)
    baker.make_recipe(transaction_recipe, date=date_february, _quantity=2, user=user)
    service_january = AnalyticsBaseService(user).get_transactions_by_month(1, 2025)
    service_february = AnalyticsBaseService(user).get_transactions_by_month(2, 2025)
    service_march = AnalyticsBaseService(user).get_transactions_by_month(3, 2025)

    assert service_january.count() == 3
    assert service_february.count() == 2
    assert service_march.count() == 0


@pytest.mark.django_db
def test_get_transactions_by_year(
    user: User,
    transaction_recipe: str,
):
    """Test get_transactions_by_year function to ensure it works properly."""
    date_2024 = make_aware(datetime(2024, 1, 1))
    date_2025 = make_aware(datetime(2025, 1, 1))
    baker.make_recipe(transaction_recipe, date=date_2024, _quantity=3, user=user)
    baker.make_recipe(transaction_recipe, date=date_2025, _quantity=2, user=user)
    service_2024 = AnalyticsBaseService(user).get_transactions_by_year(2024)
    service_2025 = AnalyticsBaseService(user).get_transactions_by_year(2025)
    service_2026 = AnalyticsBaseService(user).get_transactions_by_year(2026)

    assert service_2024.count() == 3
    assert service_2025.count() == 2
    assert service_2026.count() == 0
