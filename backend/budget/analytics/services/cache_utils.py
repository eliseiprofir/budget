from django.core.cache import cache
from django.utils import timezone
from django.conf import settings

from tasks.analytics import generate_current_report
from tasks.analytics import generate_monthly_report
from tasks.analytics import generate_yearly_report
from tasks.analytics import generate_historical_report

from analytics.services.current import AnalyticsCurrentService
from analytics.services.monthly import AnalyticsMonthlyService
from analytics.services.yearly import AnalyticsYearlyService
from analytics.services.historical import AnalyticsHistoricalService


def get_or_generate_current_report(user):
    cache_key = f"current_report_{user.id}"
    report_data = cache.get(cache_key)

    if report_data is None:
        generate_current_report.delay(user.id)

        service = AnalyticsCurrentService(user)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def get_or_generate_monthly_report(user, year, month):
    cache_key = f"monthly_report_{user.id}_{year}_{month}"
    report_data = cache.get(cache_key)

    if report_data is None:
        generate_monthly_report.delay(user.id, year, month)

        service = AnalyticsMonthlyService(user, year, month)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def get_or_generate_yearly_report(user, year):
    cache_key = f"yearly_report_{user.id}_{year}"
    report_data = cache.get(cache_key)

    if report_data is None:
        generate_yearly_report.delay(user.id, year)

        service = AnalyticsYearlyService(user, year)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def get_or_generate_historical_report(user):
    cache_key = f"historical_report_{user.id}"
    report_data = cache.get(cache_key)

    if report_data is None:
        generate_historical_report.delay(user.id)

        service = AnalyticsHistoricalService(user)
        report_data = service.get_summary()
        report_data["generated_at"] = timezone.now().isoformat()

        cache.set(cache_key, report_data, timeout=settings.CACHE_TTL)

    return report_data


def invalidate_user_cache(user):
    cache.delete(f"current_report_{user.id}")
    cache.delete(f"historical_report_{user.id}")

    years_back = 5
    current_year = timezone.now().year
    for year in range(current_year - years_back, current_year + 1):
        cache.delete(f"yearly_report_{user.id}_{year}")

        for month in range(1, 13):
            cache.delete(f"monthly_report_{user.id}_{year}_{month}")
