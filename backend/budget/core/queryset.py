from django.db.models import QuerySet


class LocationQuerySet(QuerySet):
    """Custom queryset for the Location model."""

    def filter_by_user(self, user):
        """User can see only his locations."""
        if not user.is_authenticated:
            return self.none()
        return self.filter(user=user).select_related("user")


class BucketQuerySet(QuerySet):
    """Custom queryset for the Bucket model."""

    def filter_by_user(self, user):
        """User can see only his buckets."""
        if not user.is_authenticated:
            return self.none()
        return self.filter(user=user).select_related("user")
