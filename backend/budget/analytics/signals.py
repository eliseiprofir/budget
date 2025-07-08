from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from core.models import Location
from core.models import Bucket
from transactions.models import Category
from transactions.models import Transaction
from analytics.services.cache_utils import invalidate_user_analytics_cache

@receiver(post_save, sender=Location)
def invalidate_cache_on_location_save(sender, instance, **kwargs):
    """Invalidate cache when a location is saved."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_delete, sender=Location)
def invalidate_cache_on_location_delete(sender, instance, **kwargs):
    """Invalidate cache when a location is deleted."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_save, sender=Bucket)
def invalidate_cache_on_bucket_save(sender, instance, **kwargs):
    """Invalidate cache when a bucket is saved."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_delete, sender=Bucket)
def invalidate_cache_on_bucket_delete(sender, instance, **kwargs):
    """Invalidate cache when a bucket is deleted."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_save, sender=Category)
def invalidate_cache_on_category_save(sender, instance, **kwargs):
    """Invalidate cache when a category is saved."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_delete, sender=Category)
def invalidate_cache_on_category_delete(sender, instance, **kwargs):
    """Invalidate cache when a category is deleted."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_save, sender=Transaction)
def invalidate_cache_on_transaction_save(sender, instance, **kwargs):
    """Invalidate cache when a transaction is saved."""
    invalidate_user_analytics_cache(instance.user)

@receiver(post_delete, sender=Transaction)
def invalidate_cache_on_transaction_delete(sender, instance, **kwargs):
    """Invalidate cache when a transaction is deleted."""
    invalidate_user_analytics_cache(instance.user)
