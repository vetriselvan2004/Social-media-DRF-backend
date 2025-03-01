from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, primary_key=True)
    bio = models.CharField(max_length=500)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    description = models.CharField(max_length=400)
    post_image = models.ImageField(upload_to='posts/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(MyUser, related_name='post_likes', blank=True)

    def get_user_profile_image(self):
        if self.user.profile_image:
            return self.user.profile_image.url  # Returns the URL of the image
        return None  # Or a default image URL