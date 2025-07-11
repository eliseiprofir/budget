from django.db.models import QuerySet


class CategoryQuerySet(QuerySet):
    """Custom queryset for the Category model."""

    def filter_by_user(self, user):
        """User can see only his categories."""
        if not user.is_authenticated:
            return self.none()
        return self.filter(user=user).select_related("user")


class TransactionQuerySet(QuerySet):
    """Custom queryset for the Transaction model."""

    def filter_by_user(self, user):
        """User can see only his transactions."""
        if not user.is_authenticated:
            return self.none()
        return self.filter(user=user).select_related("category", "location", "bucket", "user")
