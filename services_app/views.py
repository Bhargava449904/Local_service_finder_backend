from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ServiceCategory,ProviderProfile,ProviderGallery
from review.models import Review
from review.serializer import ReviewSerializer
import cloudinary.uploader
from accounts.permission import Isadmin,Iscustomer,Isprovider
from .serializers import ServiceCategorySerializer,ProviderProfileSerializer,ProviderGallerySerializer,ViewProviderSerializer
from math import radians, sin, cos, sqrt, atan2


@api_view(['POST'])
@permission_classes([IsAuthenticated, Isadmin])
def create_service_category(request):
    serializer = ServiceCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Service category created successfully."
        })

    return Response(serializer.errors)


@api_view(['GET'])
def view_service_categories(request):
    categories = ServiceCategory.objects.all()
    serializer = ServiceCategorySerializer(
        categories,
        many=True
    )

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, Isprovider])
def create_provider_profile(request):

    if ProviderProfile.objects.filter(user=request.user).exists():
        return Response({
            "message": "Provider profile already exists."
        })

    profile_image = request.FILES.get("profile_image")

    image_url = None

    if profile_image:
        upload_result = cloudinary.uploader.upload(profile_image)
        image_url = upload_result["secure_url"]

    serializer = ProviderProfileSerializer(
        data={
            "category": request.data.get("category"),
            "phone": request.data.get("phone"),
            "experience": request.data.get("experience"),
            "description": request.data.get("description"),
            "latitude": request.data.get("latitude"),
            "longitude": request.data.get("longitude"),
            "profile_image": image_url,
            "service_radius": request.data.get("service_radius"),
        }
    )

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({
            "message": "Provider profile created successfully."
        })

    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated, Isprovider])
def view_provider_profile(request):

    try:
        provider = ProviderProfile.objects.get(
            user=request.user
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider profile not found."
        })

    serializer = ProviderProfileSerializer(provider)

    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated, Isprovider])
def edit_provider_profile(request):

    try:
        provider = ProviderProfile.objects.get(
            user=request.user
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider profile not found."
        })

    data = request.data.copy()

    profile_image = request.FILES.get("profile_image")

    if profile_image:
        upload_result = cloudinary.uploader.upload(profile_image)
        data["profile_image"] = upload_result["secure_url"]

    serializer = ProviderProfileSerializer(
        provider,
        data=data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Provider profile updated successfully."
        })

    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([IsAuthenticated, Isprovider])
def upload_provider_gallery(request):

    try:
        provider = ProviderProfile.objects.get(
            user=request.user
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider profile not found."
        })

    image = request.FILES.get("image")

    if not image:
        return Response({
            "message": "Image is required."
        })

    upload_result = cloudinary.uploader.upload(image)

    serializer = ProviderGallerySerializer(
        data={
            "image_url": upload_result["secure_url"]
        }
    )

    if serializer.is_valid():
        serializer.save(provider=provider)
        return Response({
            "message": "Gallery image uploaded successfully."
        })

    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated, Isprovider])
def view_provider_gallery(request):

    try:
        provider = ProviderProfile.objects.get(
            user=request.user
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider profile not found."
        })

    gallery = ProviderGallery.objects.filter(
        provider=provider
    )

    serializer = ProviderGallerySerializer(
        gallery,
        many=True
    )

    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated, Isprovider])
def delete_provider_gallery(request, id):

    try:
        provider = ProviderProfile.objects.get(
            user=request.user
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider profile not found."
        })

    try:
        gallery = ProviderGallery.objects.get(
            id=id,
            provider=provider
        )
    except ProviderGallery.DoesNotExist:
        return Response({
            "message": "Gallery image not found."
        })

    gallery.delete()

    return Response({
        "message": "Gallery image deleted successfully."
    })

# =================================================================================

@api_view(['GET'])
def view_all_providers(request):

    providers = ProviderProfile.objects.filter(
        verified=True,
        available=True
    )

    serializer = ViewProviderSerializer(
        providers,
        many=True
    )

    return Response(serializer.data)
@api_view(['GET'])
def search_provider_by_category(request, id):

    providers = ProviderProfile.objects.filter(
        category=id,
        verified=True,
        available=True
    )

    serializer = ViewProviderSerializer(
        providers,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def provider_details(request, id):

    try:
        provider = ProviderProfile.objects.get(
            id=id,
            verified=True
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider not found."
        })

    provider_serializer = ViewProviderSerializer(provider)

    gallery = ProviderGallery.objects.filter(
        provider=provider
    )

    gallery_serializer = ProviderGallerySerializer(
        gallery,
        many=True
    )

    reviews = Review.objects.filter(
        provider=provider
    )

    review_serializer = ReviewSerializer(
        reviews,
        many=True
    )

    return Response({
        "provider": provider_serializer.data,
        "gallery": gallery_serializer.data,
        "reviews": review_serializer.data
    })


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2 +
        cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


@api_view(['GET'])
def nearby_providers(request):

    customer_lat = request.GET.get("lat")
    customer_lon = request.GET.get("lon")

    providers = ProviderProfile.objects.filter(
        verified=True,
        available=True
    )

    nearby = []

    for provider in providers:

        distance = calculate_distance(
            customer_lat,
            customer_lon,
            provider.latitude,
            provider.longitude
        )

        if distance <= provider.service_radius:

            serializer = ViewProviderSerializer(provider)

            data = serializer.data
            data["distance"] = round(distance, 2)

            nearby.append(data)

    nearby.sort(key=lambda x: x["distance"])

    return Response(nearby)






@api_view(['PUT'])
@permission_classes([IsAuthenticated, Isadmin])
def verify_provider(request, id):

    try:
        provider = ProviderProfile.objects.get(id=id)
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider not found."
        })

    provider.verified = True
    provider.save()

    return Response({
        "message": "Provider verified successfully."
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, Isadmin])
def admin_view_providers(request):

    providers = ProviderProfile.objects.all()

    serializer = ViewProviderSerializer(
        providers,
        many=True
    )

    return Response(serializer.data)