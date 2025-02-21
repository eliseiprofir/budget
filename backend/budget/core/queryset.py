from django.db.models import QuerySet


class BucketQuerySet(QuerySet):
    """Custom queryset for the Bucket model."""

    def filter_by_user(self, user):
        """Regular user can see his own buckets only. Superusers can see them all."""

        if not user.is_authenticated:
            return self.none()
        if user.is_superuser:
            return self
        return self.filter(user=user)
