from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_user = models.PositiveIntegerField(unique=True)
    bio = models.TextField(max_length=500, blank=True, help_text="Tell the galaxy about yourself.")
    profileimg = models.ImageField(
        upload_to='profile_images/', 
        default='default.jpg', 
        help_text="Upload your intergalactic avatar."
    )
    planet = models.CharField(max_length=100, blank=True, help_text="Your home planet.")
    star_system = models.CharField(max_length=100, blank=True, help_text="The star system you belong to.")
    species = models.CharField(max_length=100, blank=True, help_text="Your species.")
    interests = models.CharField(max_length=250, blank=True, help_text="What interests you in the cosmos?")
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def total_followers(self):
        return self.followers.count()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['user__username']


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500, help_text="Share your thoughts with the galaxy.")
    image = models.ImageField(upload_to='post_images/', blank=True, help_text="Add a visual")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"

class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reposted {self.original_post}"
