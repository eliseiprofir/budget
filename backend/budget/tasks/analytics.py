from celery import shared_task
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone

from accounts.models import User
from analytics.services.current import AnalyticsCurrentService
from analytics.services.monthly import AnalyticsMonthlyService
from analytics.services.yearly import AnalyticsYearlyService
from analytics.services.historical import AnalyticsHistoricalService


@shared_task
def generate_current_report(user_id):
    """Generate current analytics report asynchronously and store in cache."""
    try:
        user = User.objects.get(id=user_id)
        service = AnalyticsCurrentService(user)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache_key = f"current_report_{user_id}"

        print(f"Saving report to cache with key: {cache_key}")
        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)
        print(f"Report saved successfully for user {user_id}")

        return {
            "status": "success",
            "message": "Current report generated successfully.",
            "user_id": user_id,
            "cache_key": cache_key,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating current report: {str(e)}",
            "user_id": user_id,
        }


@shared_task
def generate_monthly_report(user_id, year, month):
    """Generate monthly analytics report asynchronously and store in cache."""
    try:
        user = User.objects.get(id=user_id)
        service = AnalyticsMonthlyService(user, year, month)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache_key = f"monthly_report_{user_id}_{year}_{month}"
        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

        return {
            "status": "success",
            "message": "Monthly report generated successfully.",
            "user_id": user_id,
            "year": year,
            "month": month,
            "cache_key": cache_key,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating monthly report: {str(e)}",
            "user_id": user_id,
            "year": year,
            "month": month,
        }


@shared_task
def generate_yearly_report(user_id, year):
    """Generate yearly analytics report asynchronously and store in cache."""
    try:
        user = User.objects.get(id=user_id)
        service = AnalyticsYearlyService(user, year)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache_key = f"yearly_report_{user_id}_{year}"
        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

        return {
            "status": "success",
            "message": "Yearly report generated successfully.",
            "user_id": user_id,
            "year": year,
            "cache_key": cache_key,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating yearly report: {str(e)}",
            "user_id": user_id,
            "year": year,
        }


@shared_task
def generate_historical_report(user_id):
    """Generate historical analytics report asynchronously and store in cache."""
    try:
        user = User.objects.get(id=user_id)
        service = AnalyticsHistoricalService(user)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache_key = f"historical_report_{user_id}"
        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

        return {
            "status": "success",
            "message": "Historical report generated successfully.",
            "user_id": user_id,
            "cache_key": cache_key,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating historical report: {str(e)}",
            "user_id": user_id,
        }
