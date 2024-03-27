import random
from django.core.management.base import BaseCommand
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Rotate users pin'

    def handle(self, *args, **options):
        profiles = UserProfile.objects.all()
        for profile in profiles:
            profile.pin = random.randint(1000, 9999)
        updated = UserProfile.objects.bulk_update(profiles, ['pin'])
        # bulk_update returns None for Django <= 4.0.
        # The value `updated` will be useful when we upgrade.
        self.stdout.write(self.style.SUCCESS(f'Found {profiles.count()} users. Updated {updated} users'))
