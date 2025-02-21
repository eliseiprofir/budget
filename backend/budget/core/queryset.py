from django.db.models import QuerySet


class LocationQuerySet(QuerySet):
    """Custom queryset for the Location model."""

    def filter_by_user(self, user):
        """Regular user can see his own locations only. Superusers can see them all."""
        if not user.is_authenticated:
            return self.none()
        if user.is_superuser:
            return self.all()
        return self.filter(user=user)


class BucketQuerySet(QuerySet):
    """Custom queryset for the Bucket model."""

    def filter_by_user(self, user):
        """Regular user can see his own buckets only. Superusers can see them all."""
        if not user.is_authenticated:
            return self.none()
        if user.is_superuser:
            return self.all()
        return self.filter(user=user)
