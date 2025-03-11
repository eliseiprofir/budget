from django.core.cache import cache
from django.utils import timezone

from tasks.analytics import generate_current_report
from tasks.analytics import generate_monthly_report
from tasks.analytics import generate_yearly_report
from tasks.analytics import generate_historical_report


def get_or_generate_current_report(user):
    """Get current report from cache or generate it asynchronously if not available."""
    cache_key = f"current_report_{user.id}"
    report_data = cache.get(cache_key)
    
    if report_data is None:
        generate_current_report.delay(user.id)
        return None
    
    return report_data


def get_or_generate_monthly_report(user, year, month):
    """Get monthly report from cache or generate it asynchronously if not available."""
    cache_key = f"monthly_report_{user.id}_{year}_{month}"
    report_data = cache.get(cache_key)
    
    if report_data is None:
        generate_monthly_report.delay(user.id, year, month)
        return None
    
    return report_data


def get_or_generate_yearly_report(user, year):
    """Get yearly report from cache or generate it asynchronously if not available."""
    cache_key = f"yearly_report_{user.id}_{year}"
    report_data = cache.get(cache_key)
    
    if report_data is None:
        generate_yearly_report.delay(user.id, year)
        return None
    
    return report_data


def get_or_generate_historical_report(user):
    """Get historical report from cache or generate it asynchronously if not available."""
    cache_key = f"historical_report_{user.id}"
    report_data = cache.get(cache_key)
    
    if report_data is None:
        generate_historical_report.delay(user.id)
        return None
    
    return report_data


def invalidate_user_cache(user):
    """Invalidate all cache entries for a user."""
    cache.delete(f"current_report_{user.id}")
    cache.delete(f"historical_report_{user.id}")

    years_back = 5
    current_year = timezone.now().year
    for year in range(current_year - years_back, current_year + 1):
        cache.delete(f"yearly_report_{user.id}_{year}")

        for month in range(1, 13):
            cache.delete(f"monthly_report_{user.id}_{year}_{month}")
