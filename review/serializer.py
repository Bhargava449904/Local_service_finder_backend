from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        exclude = (
            "customer",
            "provider",
            "created_at",
        )