from django.db.models import QuerySet


class CategoryQuerySet(QuerySet):
    """Custom queryset for the Category model."""

    def filter_by_user(self, user):
        """Regular user can see his own categories. Superusers can see them all."""
        if not user.is_authenticated:
            return self.none()
        if user.is_superuser:
            return self.all().select_related("user")
        return self.filter(user=user).select_related("user")


class TransactionQuerySet(QuerySet):
    """Custom queryset for the Transaction model."""

    def filter_by_user(self, user):
        """Regular user can see his own transactions. Superusers can see them all."""
        if not user.is_authenticated:
            return self.none()
        if user.is_superuser:
            return self.all().select_related("category", "location", "bucket", "user")
        return self.filter(user=user).select_related("category", "location", "bucket", "user")
