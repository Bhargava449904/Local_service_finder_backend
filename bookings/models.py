from django.db import models
from accounts.models import User
from services_app.models import ProviderProfile


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_bookings"
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="provider_bookings"
    )

    booking_date = models.DateField()

    booking_time = models.TimeField()

    problem_description = models.TextField()

    service_address = models.TextField()

    customer_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    customer_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.customer.username} → {self.provider.user.username}"


class FavoriteProvider(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_providers"
    )

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "provider"],
                name="unique_favorite_provider"
            )
        ]

    def __str__(self):
        return f"{self.customer.username} → {self.provider.user.username}"