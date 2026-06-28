from django.db import models
from accounts.models import User


class ServiceCategory(models.Model):
    type_of_service = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_of_service
    

class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=10)
    experience = models.PositiveIntegerField()
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    verified = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    profile_image = models.URLField()
    service_radius = models.PositiveIntegerField(default=10)
    average_rating = models.FloatField(default=0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username




class ProviderGallery(models.Model):

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE
    )
    image_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.provider.user.username