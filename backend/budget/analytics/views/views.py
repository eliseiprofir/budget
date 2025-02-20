# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Sum
# from transactions.models import Transaction, TransactionType
# from rest_framework.exceptions import ValidationError
# from datetime import datetime
#
# class AnalyticsViewSet(viewsets.ViewSet):
#     """ViewSet for analytics endpoints."""
#
#     permission_classes = [IsAuthenticated]
#
#     def list(self, request):
#         """
#         Root endpoint that shows available analytics endpoints.
#         """
#         available_endpoints = {
#             'monthly_report': '/api/analytics/monthly/?year=YYYY&month=MM',
#             # Aici vom adăuga celelalte endpoint-uri pe măsură ce le implementăm
#         }
#         return Response(available_endpoints)
#
#     def _validate_date_params(self, year, month=None):
#         """Validate date parameters."""
#         try:
#             year = int(year)
#             if month:
#                 month = int(month)
#                 if not (1 <= month <= 12):
#                     raise ValidationError({"month": "Month must be between 1 and 12"})
#             if not (1900 <= year <= datetime.now().year):
#                 raise ValidationError({"year": "Invalid year"})
#         except (TypeError, ValueError):
#             raise ValidationError({"error": "Invalid date parameters"})
#         return year, month
#
#     @action(detail=False, methods=['get'])
#     def monthly(self, request):
#         """Get monthly report."""
#         year = request.query_params.get('year')
#         month = request.query_params.get('month')
#
#         if not year or not month:
#             raise ValidationError({
#                 "error": "Both year and month parameters are required"
#             })
#
#         year, month = self._validate_date_params(year, month)
#
#         # Get all transactions for the specified month
#         transactions = Transaction.objects.filter(
#             user=request.user,
#             date__year=year,
#             date__month=month
#         )
#
#         # Get income categories
#         income_transactions = transactions.filter(
#             category__transaction_type__sign=TransactionType.Sign.POSITIVE
#         ).values('category__name').annotate(
#             total=Sum('amount')
#         ).order_by('-total')
#
#         # Get expense categories
#         expense_transactions = transactions.filter(
#             category__transaction_type__sign=TransactionType.Sign.NEGATIVE
#         ).values('category__name').annotate(
#             total=Sum('amount')
#         ).order_by('-total')
#
#         # Calculate totals
#         total_income = sum(t['total'] for t in income_transactions)
#         total_expenses = sum(t['total'] for t in expense_transactions)
#         balance = total_income - total_expenses
#
#         return Response({
#             'income_categories': income_transactions,
#             'expense_categories': expense_transactions,
#             'total_income': total_income,
#             'total_expenses': total_expenses,
#             'balance': balance
#         })