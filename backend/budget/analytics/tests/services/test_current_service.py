import pytest
from model_bakery import baker

from accounts.models import User
from analytics.services.current import AnalyticsCurrentService

@pytest.mark.django_db
def test_get_location_data(
    user: User,
    location_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_location_data function to ensure it works properly."""
    service = AnalyticsCurrentService(user).get_locations_data()
    assert service == {"total": 0}

    location1 = baker.make_recipe(location_recipe, user=user, name="Location 1")
    location2 = baker.make_recipe(location_recipe, user=user, name="Location 2")
    baker.make_recipe(positive_transaction_recipe, user=user, location=location1, amount=100)
    baker.make_recipe(positive_transaction_recipe, user=user, location=location2, amount=300)
    baker.make_recipe(negative_transaction_recipe, user=user, location=location1, amount=50)
    baker.make_recipe(negative_transaction_recipe, user=user, location=location2, amount=150)

    service = AnalyticsCurrentService(user).get_locations_data()
    assert service["total"] == 200
    assert service["Location 1"] == 50
    assert service["Location 2"] == 150

@pytest.mark.django_db
def test_get_buckets_data(
    user: User,
    bucket_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_buckets_data function to ensure it works properly."""
    service = AnalyticsCurrentService(user).get_buckets_data()
    assert service == {"total": 0}

    bucket1 = baker.make_recipe(bucket_recipe, user=user, name="Bucket 1", allocation_percentage=50)
    bucket2 = baker.make_recipe(bucket_recipe, user=user, name="Bucket 2", allocation_percentage=50)
    baker.make_recipe(positive_transaction_recipe, user=user, bucket=bucket1, amount=100)
    baker.make_recipe(positive_transaction_recipe, user=user, bucket=bucket2, amount=300)
    baker.make_recipe(negative_transaction_recipe, user=user, bucket=bucket1, amount=50)
    baker.make_recipe(negative_transaction_recipe, user=user, bucket=bucket2, amount=150)

    service = AnalyticsCurrentService(user).get_buckets_data()
    assert service["total"] == 200
    assert service["Bucket 1"] == 50
    assert service["Bucket 2"] == 150

@pytest.mark.django_db
def test_get_balance(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_balance function to ensure it works properly."""
    service = AnalyticsCurrentService(user).get_balance()
    assert service == {
        "positive": 0,
        "negative": 0,
        "balance": 0,
    }

    baker.make_recipe(positive_transaction_recipe, amount=100, user=user)
    baker.make_recipe(negative_transaction_recipe, amount=25, user=user)

    service = AnalyticsCurrentService(user).get_balance()
    assert service["positive"] == 100
    assert service["negative"] == 25
    assert service["balance"] == 75

@pytest.mark.django_db
def test_get_summary(
    user: User,
    location_recipe: str,
    bucket_recipe: str,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test get_summary function to ensure it works properly."""
    service = AnalyticsCurrentService(user).get_summary()
    assert service == {
        "locations": {"total": 0},
        "buckets": {"total": 0},
        "balance": {
            "positive": 0,
            "negative": 0,
            "balance": 0,
        },
    }

    location1 = baker.make_recipe(location_recipe, user=user, name="Location 1")
    location2 = baker.make_recipe(location_recipe, user=user, name="Location 2")
    bucket1 = baker.make_recipe(bucket_recipe, user=user, name="Bucket 1", allocation_percentage=50)
    bucket2 = baker.make_recipe(bucket_recipe, user=user, name="Bucket 2", allocation_percentage=50)
    baker.make_recipe(positive_transaction_recipe, user=user, bucket=bucket1, location=location1, amount=100)
    baker.make_recipe(positive_transaction_recipe, user=user, bucket=bucket2, location=location2, amount=300)
    baker.make_recipe(negative_transaction_recipe, user=user, bucket=bucket1, location=location1, amount=50)
    baker.make_recipe(negative_transaction_recipe, user=user, bucket=bucket2, location=location2, amount=150)

    service = AnalyticsCurrentService(user).get_summary()
    assert service["locations"]["total"] == 200
    assert service["locations"]["Location 1"] == 50
    assert service["locations"]["Location 2"] == 150
    assert service["buckets"]["total"] == 200
    assert service["buckets"]["Bucket 1"] == 50
    assert service["buckets"]["Bucket 2"] == 150
    assert service["balance"]["positive"] == 400
    assert service["balance"]["negative"] == 200
    assert service["balance"]["balance"] == 200
