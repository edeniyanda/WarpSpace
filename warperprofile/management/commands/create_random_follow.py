from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Randomly assign followers so each user follows at least 20 others'

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())

        for user in users:
            # Ensure each user follows at least 20 others
            num_follows = random.randint(20, len(users) - 1)
            potential_follows = [u for u in users if u != user]

            # Select random users to follow
            random_follows = random.sample(potential_follows, num_follows)
            for follow in random_follows:
                user.profile.followers.add(follow)

            user.profile.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created random followers for users.'))
