"""Analytics views."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from transactions.models import Transaction, TransactionType
from rest_framework.exceptions import ValidationError
from datetime import datetime


class AnalyticsViewSet(viewsets.ViewSet):
    """ViewSet for analytics endpoints."""

    permission_classes = [IsAuthenticated]

    def _validate_date_params(self, year, month=None):
        """Validate date parameters."""
        try:
            year = int(year)
            if month:
                month = int(month)
                if not (1 <= month <= 12):
                    raise ValidationError({"month": "Month must be between 1 and 12"})
            if not (1900 <= year <= datetime.now().year):
                raise ValidationError({"year": "Invalid year"})
        except (TypeError, ValueError):
            raise ValidationError({"error": "Invalid date parameters"})
        return year, month

    def get_monthly_report(self, request, year, month):
        """Get monthly report with income and expenses by category."""
        # Validate parameters
        year, month = self._validate_date_params(year, month)

        # Get base queryset for user
        transactions = Transaction.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        )

        # Get income categories
        income_transactions = transactions.filter(
            category__transaction_type__sign=TransactionType.Sign.POSITIVE
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Get expense categories
        expense_transactions = transactions.filter(
            category__transaction_type__sign=TransactionType.Sign.NEGATIVE
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Calculate totals
        total_income = sum(t['total'] for t in income_transactions)
        total_expenses = sum(t['total'] for t in expense_transactions)
        balance = total_income - total_expenses

        return Response({
            'income_categories': income_transactions,
            'expense_categories': expense_transactions,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance
        })



    def get_yearly_report(self, request, year):
        """Get yearly report with income and expenses by month."""
        user = request.user
        
        # Get all transactions for the specified year
        transactions = Transaction.objects.filter(
            user=user,
            date__year=year
        )

        # Get monthly income
        monthly_income = transactions.filter(
            category__transaction_type__sign=TransactionType.Sign.POSITIVE
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')

        # Get monthly expenses
        monthly_expenses = transactions.filter(
            category__transaction_type__sign=TransactionType.Sign.NEGATIVE
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')

        # Calculate yearly totals
        total_income = sum(m['total'] for m in monthly_income)
        total_expenses = sum(m['total'] for m in monthly_expenses)
        balance = total_income - total_expenses

        return Response({
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance
        })

    def get_historical_report(self, request):
        """Get historical report with income and expenses by year."""
        user = request.user
        
        # Get all transactions
        transactions = Transaction.objects.filter(user=user)

        # Get yearly income
        yearly_income = transactions.filter(
            category__transaction_type__sign=TransactionType.Sign.POSITIVE
        ).annotate(
            year=TruncYear('date')
        ).values('year').annotate(
            total=Sum('amount')
        ).order_by('year')

        # Get yearly expenses
        yearly_expenses = transactions.filter(
            category__transaction_type__sign=TransactionType.Sign.NEGATIVE
        ).annotate(
            year=TruncYear('date')
        ).values('year').annotate(
            total=Sum('amount')
        ).order_by('year')

        # Calculate historical totals
        total_income = sum(y['total'] for y in yearly_income)
        total_expenses = sum(y['total'] for y in yearly_expenses)
        balance = total_income - total_expenses

        return Response({
            'yearly_income': yearly_income,
            'yearly_expenses': yearly_expenses,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance
        })

    def get_current_status(self, request):
        """Get current status with total money in locations and buckets."""
        user = request.user

        # Get location totals
        location_totals = Transaction.objects.filter(
            user=user
        ).values('location__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Get bucket totals
        bucket_totals = Transaction.objects.filter(
            user=user
        ).values('bucket__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        return Response({
            'location_totals': location_totals,
            'bucket_totals': bucket_totals
        })

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """Get monthly report."""
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        if not year or not month:
            raise ValidationError({
                "error": "Both year and month parameters are required"
            })

        return self.get_monthly_report(request, year, month)

    # @action(detail=False, methods=['get'])
    # def monthly(self, request):
    #     """Get monthly report."""
    #     year = request.query_params.get('year')
    #     month = request.query_params.get('month')
    #     return self.get_monthly_report(request, year, month)

    @action(detail=False, methods=['get'])
    def yearly(self, request):
        """Get yearly report."""
        year = request.query_params.get('year')
        return self.get_yearly_report(request, year)

    @action(detail=False, methods=['get'])
    def historical(self, request):
        """Get historical report."""
        return self.get_historical_report(request)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current status."""
        return self.get_current_status(request)
