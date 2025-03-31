import pytest
from django.contrib.auth import get_user_model
from core.management.commands.createdefaultsuperuser import DEFAULT_EMAIL
from accounts.models import User
from core.models import Location
from core.models import Bucket
from transactions.models import TransactionType
from transactions.models import Category
from transactions.models import Transaction

User = get_user_model()


@pytest.mark.django_db
def test_createdefaultsuperuser_command(defaultsuperuser):
    user = defaultsuperuser
    assert user is not None
    assert user.is_superuser
    assert user.email == DEFAULT_EMAIL


@pytest.mark.django_db
def test_seed_command(seed):
    """Test that seed command creates the correct number of entries"""
    seed_count = seed

    user_count = User.all_objects.filter(is_superuser=False).count()
    location_count = Location.all_objects.count()
    bucket_count = Bucket.all_objects.count()
    transaction_type_count = TransactionType.all_objects.count()
    category_count = Category.all_objects.count()
    transaction_count = Transaction.objects.count()

    total_count = (
        user_count +
        location_count +
        bucket_count +
        transaction_type_count +
        category_count +
        transaction_count
    )

    assert total_count == seed_count


@pytest.mark.django_db
def test_clear_command(clear):
    """Test that clear command removes all non-superuser entries"""
    clear_count = clear

    user_count = User.all_objects.filter(is_superuser=False).count()
    location_count = Location.all_objects.count()
    bucket_count = Bucket.all_objects.count()
    transaction_type_count = TransactionType.all_objects.count()
    category_count = Category.all_objects.count()
    transaction_count = Transaction.objects.count()

    total_count = (
        user_count +
        location_count +
        bucket_count +
        transaction_type_count +
        category_count +
        transaction_count
    )

    assert total_count == clear_count
    assert total_count == 0
