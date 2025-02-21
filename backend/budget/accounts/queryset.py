from django.db.models import QuerySet


class UserQuerySet(QuerySet):
    """Custom queryset for the User model."""

    def filter_by_user(self, user):
        """Return only the users that the given user can see."""
        if not user:
            return self.none()
        if user.is_superuser:
            return self.all()
        return self.filter(id=user.id)
