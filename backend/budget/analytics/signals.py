from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from transactions.models import Transaction
from analytics.services.cache_utils import invalidate_user_cache

@receiver(post_save, sender=Transaction)
def invalidate_cache_on_transaction_save(sender, instance, **kwargs):
    """Invalidate cache when a transaction is saved."""
    invalidate_user_cache(instance.user)

@receiver(post_delete, sender=Transaction)
def invalidate_cache_on_transaction_delete(sender, instance, **kwargs):
    """Invalidate cache when a transaction is deleted."""
    invalidate_user_cache(instance.user)