from django.db.models import QuerySet


class UserQuerySet(QuerySet):
    """Custom queryset for the User model."""

    def filter_by_user(self, user):
        """Return the users details."""
        if not user:
            return self.none()
        return self.filter(id=user.id)
