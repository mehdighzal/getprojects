from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile objects for all users who don\'t have one'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        
        self.stdout.write(f'Found {users_without_profiles.count()} users without profiles')
        
        created_count = 0
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            created_count += 1
            self.stdout.write(f'Created profile for user: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} user profiles')
        )
