# import pytest
# from rest_framework.test import APIClient
# from model_bakery import baker
# from django.urls import reverse
#
# @pytest.mark.django_db
# def test_analytics_current_view(user):
#     """
#     Test pentru view-ul de analiză curentă.
#     """
#     # Creează tranzacții pentru utilizator
#     baker.make_recipe(
#         'transactions.tests.baker_recipes.transaction_recipe',
#         user=user,
#         amount=decimal.Decimal('100.00'),
#         category__transaction_type__sign='POSITIVE',
#         _quantity=3
#     )
#
#     baker.make_recipe(
#         'transactions.tests.baker_recipes.transaction_recipe',
#         user=user,
#         amount=decimal.Decimal('50.00'),
#         category__transaction_type__sign='NEGATIVE',
#         _quantity=2
#     )
#
#     # Configurează clientul API
#     client = APIClient()
#     client.force_authenticate(user=user)
#
#     # Accesează view-ul de analiză curentă
#     url = reverse('analytics-current-list')  # Asigură-te că url-ul este corect
#     response = client.get(url)
#
#     # Verifică răspunsul
#     assert response.status_code == 200
#
#     # Verifică structura datelor
#     data = response.json()
#     assert 'balance' in data
#     assert 'locations' in data
#     assert 'buckets' in data
#
#     # Verifică valorile detaliate ale soldului
#     assert data['balance']['positive'] == '300.00'
#     assert data['balance']['negative'] == '100.00'
#     assert data['balance']['balance'] == '200.00'
#
# @pytest.mark.django_db
# def test_analytics_current_view_unauthorized():
#     """
#     Test pentru accesarea view-ului fără autentificare.
#     """
#     client = APIClient()
#
#     url = reverse('analytics-current-list')  # Asigură-te că url-ul este corect
#     response = client.get(url)
#
#     # Verifică că utilizatorul neautentificat primește 401 Unauthorized
#     assert response.status_code == 401
#
# @pytest.mark.django_db
# def test_analytics_current_view_no_transactions(user):
#     """
#     Test pentru view-ul de analiză fără tranzacții.
#     """
#     client = APIClient()
#     client.force_authenticate(user=user)
#
#     url = reverse('analytics-current-list')  # Asigură-te că url-ul este corect
#     response = client.get(url)
#
#     # Verifică răspunsul pentru utilizator fără tranzacții
#     assert response.status_code == 200
#
#     data = response.json()
#     assert data['balance']['positive'] == '0.00'
#     assert data['balance']['negative'] == '0.00'
#     assert data['balance']['balance'] == '0.00'