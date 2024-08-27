from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from post.models import Post
from faker import Faker
import random
import os
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Create random posts for existing users in the database'

    def handle(self, *args, **kwargs):
        fake = Faker()
        max_posts_per_user = 3  # Maximum number of posts per user

        # Fetch all users
        users = User.objects.all()

        for user in users:
            # Create a random number of posts for each user
            num_posts = random.randint(1, max_posts_per_user)
            for _ in range(num_posts):
                content = fake.text(max_nb_chars=500)
                post = Post.objects.create(
                    user=user,
                    content=content,
                )
                
                # Optionally, add a random image to some posts
                if random.choice([True, False]):
                    post.image = self.get_random_image()
                    post.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created random posts for {users.count()} users.'))

    def get_random_image(self):
        """ Returns a random image from a predefined folder """
        images_folder = os.path.join(settings.BASE_DIR, 'randomphotos')
        if os.path.exists(images_folder):
            image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]
            if image_files:
                return os.path.join('post_images', random.choice(image_files))
        return None
