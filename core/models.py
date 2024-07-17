from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)
    
    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    
    def __str__(self):
        return self.user.username
    
    def follow(self,user):
        self.followers.add(user)
        
    def unfollow(self, user):
        self.followers.remove(user)
        
    def is_following(self, user):
        return self.followers.filter(pk=user.pk).exists()
    
    @property
    def follower_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.user.following.count()