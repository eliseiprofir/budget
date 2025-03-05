import pytest
from model_bakery import baker

from accounts.models import User
from analytics.services.current import AnalyticsCurrentService

@pytest.mark.django_db
def test_get_balance(
    user: User,
    positive_transaction_recipe: str,
    negative_transaction_recipe: str,
):
    """Test basic calculations for the current service."""

    baker.make_recipe(
        positive_transaction_recipe,
        amount=100,
        user=user,
    )
    baker.make_recipe(
        negative_transaction_recipe,
        amount=25,
        user=user,
    )

    service = AnalyticsCurrentService(user)

    balance = service.get_balance()
    assert balance['positive'] == 100
    assert balance['negative'] == 25
    assert balance['balance'] == 75

# @pytest.mark.django_db
# def test_current_service_locations_analysis(user):
#     """
#     Test pentru analiza pe locații.
#     """
#     # Creează locații
#     location1 = baker.make_recipe('core.tests.baker_recipes.location_recipe', user=user, name='Bank')
#     location2 = baker.make_recipe('core.tests.baker_recipes.location_recipe', user=user, name='Cash')
#
#     # Tranzacții pentru locația Bank
#     baker.make_recipe(
#         'transactions.tests.baker_recipes.transaction_recipe',
#         user=user,
#         location=location1,
#         amount=decimal.Decimal('100.00'),
#         category__transaction_type__sign='POSITIVE',
#         _quantity=3
#     )
#
#     # Tranzacții pentru locația Cash
#     baker.make_recipe(
#         'transactions.tests.baker_recipes.transaction_recipe',
#         user=user,
#         location=location2,
#         amount=decimal.Decimal('50.00'),
#         category__transaction_type__sign='NEGATIVE',
#         _quantity=2
#     )
#
#     # Inițializează serviciul
#     service = AnalyticsCurrentService(user)
#
#     # Testează analiza pe locații
#     locations_data = service.get_locations_data()
#
#     assert locations_data['Bank'] == decimal.Decimal('300.00')
#     assert locations_data['Cash'] == decimal.Decimal('-100.00')
#     assert locations_data['total'] == decimal.Decimal('200.00')
#
# @pytest.mark.django_db
# def test_current_service_buckets_analysis(user):
#     """
#     Test pentru analiza pe bucket-uri.
#     """
#     # Creează bucket-uri
#     bucket1 = baker.make_recipe('core.tests.baker_recipes.bucket_recipe', user=user, name='Personal')
#     bucket2 = baker.make_recipe('core.tests.baker_recipes.bucket_recipe', user=user, name='Business')
#
#     # Tranzacții pentru bucket-ul Personal
#     baker.make_recipe(
#         'transactions.tests.baker_recipes.transaction_recipe',
#         user=user,
#         bucket=bucket1,
#         amount=decimal.Decimal('100.00'),
#         category__transaction_type__sign='POSITIVE',
#         _quantity=3
#     )
#
#     # Tranzacții pentru bucket-ul Business
#     baker.make_recipe(
#         'transactions.tests.baker_recipes.transaction_recipe',
#         user=user,
#         bucket=bucket2,
#         amount=decimal.Decimal('50.00'),
#         category__transaction_type__sign='NEGATIVE',
#         _quantity=2
#     )
#
#     # Inițializează serviciul
#     service = AnalyticsCurrentService(user)
#
#     # Testează analiza pe bucket-uri
#     buckets_data = service.get_buckets_data()
#
#     assert buckets_data['Personal'] == decimal.Decimal('300.00')
#     assert buckets_data['Business'] == decimal.Decimal('-100.00')
#     assert buckets_data['total'] == decimal.Decimal('200.00')
#
# @pytest.mark.django_db
# def test_current_service_no_transactions(user):
#     """
#     Test pentru serviciul de analiză fără tranzacții.
#     """
#     # Inițializează serviciul pentru un utilizator fără tranzacții
#     service = AnalyticsCurrentService(user)
#
#     # Testează metodele principale
#     balance = service.get_balance()
#     locations_data = service.get_locations_data()
#     buckets_data = service.get_buckets_data()
#     summary = service.get_summary()
#
#     # Verifică că totul este zero
#     assert balance['positive'] == decimal.Decimal('0')
#     assert balance['negative'] == decimal.Decimal('0')
#     assert balance['balance'] == decimal.Decimal('0')
#
#     assert locations_data['total'] == decimal.Decimal('0')
#     assert buckets_data['total'] == decimal.Decimal('0')
#
#     assert summary['balance']['positive'] == decimal.Decimal('0')
#     assert summary['balance']['negative'] == decimal.Decimal('0')
#     assert summary['balance']['balance'] == decimal.Decimal('0')