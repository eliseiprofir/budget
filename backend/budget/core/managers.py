from model_utils.managers import SoftDeletableManager

from .queryset import BucketQuerySet

class BucketManager(SoftDeletableManager.from_queryset(BucketQuerySet)):
    """Bucket manager."""
    pass
