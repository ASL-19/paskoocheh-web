from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gqlauth.models import UserStatus


class Command(BaseCommand):
    help = 'Migrate old users to graphql auth by adding a verified UserStatus'

    def handle(self, *args, **options):

        User = get_user_model()
        for user in User.objects.all():
            UserStatus.objects.get_or_create(user=user)
        update = UserStatus.objects.all().update(verified=True)
        self.stdout.write(self.style.SUCCESS(f'Updated {update} users.'))
