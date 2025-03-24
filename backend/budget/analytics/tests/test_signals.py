import pytest
from model_bakery import baker
from django.core.cache import cache


@pytest.mark.django_db
def test_invalidate_cache_on_transaction_save(user_recipe: str, transaction_recipe: str):
    """Test that cache is invalidated when a transaction is saved."""
    user = baker.make_recipe(user_recipe)
    transaction = baker.make_recipe(transaction_recipe, user=user)

    cache_key = f"current_report_{user.id}"
    cache.set(cache_key, {"test": "data"})
    
    assert cache.get(cache_key) is not None
    
    transaction.amount = 1000
    transaction.save()

    assert cache.get(cache_key) is None


@pytest.mark.django_db
def test_invalidate_cache_on_transaction_delete(user_recipe: str, transaction_recipe: str):
    """Test that cache is invalidated when a transaction is deleted."""
    # Setup
    user = baker.make_recipe(user_recipe)
    transaction = baker.make_recipe(transaction_recipe, user=user)
    
    cache_keys = [
        f"current_report_{user.id}",
        f"historical_report_{user.id}",
        f"yearly_report_{user.id}_2024",
        f"monthly_report_{user.id}_2024_1"
    ]
    
    for key in cache_keys:
        cache.set(key, {"test": "data"})
        assert cache.get(key) is not None
    
    transaction.delete()

    for key in cache_keys:
        assert cache.get(key) is None


@pytest.mark.django_db
def test_cache_invalidation_different_users(user_recipe: str, transaction_recipe: str):
    """Test that cache invalidation only affects the correct user."""
    user1 = baker.make_recipe(user_recipe)
    user2 = baker.make_recipe(user_recipe)
    transaction = baker.make_recipe(transaction_recipe, user=user1)
    
    cache.set(f"current_report_{user1.id}", {"test": "user1"})
    cache.set(f"current_report_{user2.id}", {"test": "user2"})
    
    transaction.save()

    assert cache.get(f"current_report_{user1.id}") is None
    assert cache.get(f"current_report_{user2.id}") is not None
