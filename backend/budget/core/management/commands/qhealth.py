from django.core.management.base import BaseCommand
from django.utils import timezone
from django_q.models import Success
from django_q.models import Failure
from django_q.models import Schedule
from django_q.models import OrmQ
import sys

class Command(BaseCommand):
    help = 'Check the health of Django-Q cluster'

    def handle(self, *args, **options):
        # Check if there are active tasks (running workers)
        active_tasks = OrmQ.objects.filter(
            lock__gte=timezone.now() - timezone.timedelta(minutes=10)
        )
        
        if not active_tasks.exists():
            # Check if cluster was recently active by looking at recent successes
            recent_activity = Success.objects.filter(
                stopped__gte=timezone.now() - timezone.timedelta(minutes=30)
            )
            if not recent_activity.exists():
                self.stdout.write(self.style.WARNING('No recent Django-Q activity detected'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Found {active_tasks.count()} active tasks'))
        
        # Check if there are recently failed tasks
        recent_failures = Failure.objects.filter(
            stopped__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        if recent_failures.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {recent_failures.count()} failed tasks in the last 24 hours'
            ))
        
        # Check if scheduled tasks are being executed
        overdue_schedules = Schedule.objects.filter(
            next_run__lt=timezone.now(),
            repeats__gt=0  # Only check recurring schedules
        )
        
        if overdue_schedules.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {overdue_schedules.count()} overdue scheduled tasks'
            ))

        # Check if there are recently successful tasks
        recent_success = Success.objects.filter(
            stopped__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        success_count = recent_success.count()
        if success_count == 0:
            self.stdout.write(self.style.WARNING('No successful tasks in the last 24 hours'))
        else:
            self.stdout.write(self.style.SUCCESS(f'{success_count} successful tasks in the last 24 hours'))
        
        # Summary
        failure_count = recent_failures.count()
        if failure_count == 0 and success_count > 0:
            self.stdout.write(self.style.SUCCESS('✓ Django-Q cluster is healthy'))
            sys.exit(0)
        elif failure_count > success_count:
            self.stdout.write(self.style.ERROR('✗ Django-Q cluster has issues'))
            sys.exit(1)
        else:
            self.stdout.write(self.style.WARNING('⚠ Django-Q cluster status unclear'))
            sys.exit(0)
