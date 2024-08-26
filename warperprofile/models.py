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

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.user.following.count()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['user__username']


