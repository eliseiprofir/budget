import logging

from django.core.cache import cache
from django.utils import timezone
from django.conf import settings

# from tasks.analytics import generate_current_report
# from tasks.analytics import generate_monthly_report
# from tasks.analytics import generate_yearly_report
# from tasks.analytics import generate_historical_report

from django_q.tasks import async_task

from analytics.services.current import AnalyticsCurrentService
from analytics.services.monthly import AnalyticsMonthlyService
from analytics.services.yearly import AnalyticsYearlyService
from analytics.services.historical import AnalyticsHistoricalService

logger = logging.getLogger(__name__)

def safe_cache_get(key, default=None):
    try:
        return cache.get(key, default)
    except Exception as e:
        logger.warning(f"Cache get failed for key {key}: {e}")
        return default

def safe_cache_set(key, value, timeout=None):
    try:
        cache.set(key, value, timeout)
        return True
    except Exception as e:
        logger.warning(f"Cache set failed for key {key}: {e}")
        return False

def safe_cache_delete(key):
    try:
        cache.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Cache delete failed for key {key}: {e}")
        return False


def get_or_generate_current_report(user):
    cache_key = f"current_report_{user.id}"
    report_data = safe_cache_get(cache_key)

    if report_data is None:
        # generate_current_report.delay(user.id)
        async_task("tasks.analytics.generate_current_report", user.id)

        service = AnalyticsCurrentService(user)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        safe_cache_set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def get_or_generate_monthly_report(user, year, month):
    cache_key = f"monthly_report_{user.id}_{year}_{month}"
    report_data = safe_cache_get(cache_key)

    if report_data is None:
        # generate_monthly_report.delay(user.id, year, month)
        async_task("tasks.analytics.generate_monthly_report", user.id, year, month)

        service = AnalyticsMonthlyService(user, year, month)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        safe_cache_set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def get_or_generate_yearly_report(user, year):
    cache_key = f"yearly_report_{user.id}_{year}"
    report_data = safe_cache_get(cache_key)

    if report_data is None:
        # generate_yearly_report.delay(user.id, year)
        async_task("tasks.analytics.generate_yearly_report", user.id, year)

        service = AnalyticsYearlyService(user, year)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        safe_cache_set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def get_or_generate_historical_report(user):
    cache_key = f"historical_report_{user.id}"
    report_data = safe_cache_get(cache_key)

    if report_data is None:
        # generate_historical_report.delay(user.id)
        async_task("tasks.analytics.generate_historical_report", user.id)

        service = AnalyticsHistoricalService(user)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        safe_cache_set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def invalidate_user_analytics_cache(user):
    safe_cache_delete(f"current_report_{user.id}")
    safe_cache_delete(f"historical_report_{user.id}")

    years_back = 5
    current_year = timezone.now().year
    for year in range(current_year - years_back, current_year + 1):
        safe_cache_delete(f"yearly_report_{user.id}_{year}")

        for month in range(1, 13):
            safe_cache_delete(f"monthly_report_{user.id}_{year}_{month}")
