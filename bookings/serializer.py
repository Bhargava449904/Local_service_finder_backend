from rest_framework import serializers
from .models import Booking,FavoriteProvider


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        exclude = (
            "customer",
            "status",
            "created_at",
            "updated_at",
        )


class FavoriteProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteProvider
        exclude = (
            "customer",
            "created_at",
        )