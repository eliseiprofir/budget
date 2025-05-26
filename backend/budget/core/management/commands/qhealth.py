from django.core.management.base import BaseCommand
from django.utils import timezone
from django_q.models import Success, Failure, Schedule
from django_q.cluster import Cluster
import sys

class Command(BaseCommand):
    help = 'Check the health of Django-Q cluster'

    def handle(self, *args, **options):
        # Check if there are active clusters
        clusters = Cluster.objects.filter(
            stopped__isnull=True,
            last_heartbeat__gte=timezone.now() - timezone.timedelta(minutes=5)
        )
        
        if not clusters.exists():
            self.stdout.write(self.style.ERROR('No active Django-Q clusters found!'))
            sys.exit(1)
        
        # Check if there are recently failed tasks
        recent_failures = Failure.objects.filter(
            stopped__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        if recent_failures.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {recent_failures.count()} failed tasks in the last 24 hours'
            ))
        
        # Check if scheduled tasks are being executed
        schedules = Schedule.objects.filter(next_run__lt=timezone.now())
        
        if schedules.exists():
            self.stdout.write(self.style.WARNING(
                f'Found {schedules.count()} scheduled tasks that are overdue'
            ))

        # Check if there are recently successful tasks
        recent_success = Success.objects.filter(
            stopped__gte=timezone.now() - timezone.timedelta(hours=24)
        )
        
        if not recent_success.exists():
            self.stdout.write(self.style.WARNING('No successful tasks in the last 24 hours'))
        
        self.stdout.write(self.style.SUCCESS('Django-Q cluster is healthy'))
        sys.exit(0)
