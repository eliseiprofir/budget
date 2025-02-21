from model_utils.managers import SoftDeletableManager

from .queryset import BucketQuerySet
from .queryset import LocationQuerySet


class LocationManager(SoftDeletableManager.from_queryset(LocationQuerySet)):
    """Location manager."""
    pass


class BucketManager(SoftDeletableManager.from_queryset(BucketQuerySet)):
    """Bucket manager."""
    pass
