import pytest
from django.contrib.auth import get_user_model
from core.management.commands.createdefaultsuperuser import DEFAULT_EMAIL

User = get_user_model()


@pytest.mark.django_db
def test_createdefaultsuperuser_command(defaultsuperuser):
    user = defaultsuperuser
    assert user is not None
    assert user.is_superuser
    assert user.email == DEFAULT_EMAIL
