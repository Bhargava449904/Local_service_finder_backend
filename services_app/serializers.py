from rest_framework import serializers
from .models import (ServiceCategory,ProviderProfile,ProviderGallery)

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"

class ProviderProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderProfile
        fields = "__all__"

class ProviderGallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProviderGallery
        exclude = (
            "provider",
            "uploaded_at",
        )


from rest_framework import serializers
from .models import ProviderProfile


class ViewProviderSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source="user.username", read_only=True)
    service = serializers.CharField(source="category.type_of_service", read_only=True)

    class Meta:
        model = ProviderProfile
        fields = [
            "id",
            "provider_name",
            "service",
            "experience",
            "description",
            "profile_image",
            "average_rating",
            "total_reviews",
            "available",
            "verified", 
        ]