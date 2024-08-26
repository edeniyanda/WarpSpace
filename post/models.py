from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500, help_text="Share your thoughts with the galaxy.")
    image = models.ImageField(upload_to='post_images/', blank=True, help_text="Add a visual")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    reposts = models.ManyToManyField(User, related_name='reposted_posts', blank=True)

    def like_count(self):
        return self.likes.count()

    def repost_count(self):
        return self.reposts.count()

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


