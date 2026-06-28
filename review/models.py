from django.db import models
from accounts.models import User
from services_app.models import ProviderProfile
from bookings.models import Booking


class Review(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_reviews"
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="provider_reviews"
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} → {self.provider.user.username} ({self.rating}/5)"