from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from warperprofile.models import Profile
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with random users and profiles'

    def handle(self, *args, **kwargs):
        fake = Faker()
        number_of_users = 100  # You can change this to generate more or fewer users

        for _ in range(number_of_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name() + str(random.randint(1, 10000))
            email = fake.email()
            password = 'password123'  # Default password for all generated users

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()

                profile = Profile.objects.create(
                    user=user,
                    id_user=user.id,
                    bio=fake.text(max_nb_chars=250),
                    planet=fake.word(),
                    star_system=fake.word(),
                    species=fake.word(),
                    interests=', '.join(fake.words(nb=3))
                )
                profile.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully added {number_of_users} users to the database'))
