from rest_framework import serializers
from .models import User ,CustomerProfile
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = "__all__"
