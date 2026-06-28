from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .permission import Isadmin,Iscustomer,Isprovider
from rest_framework.permissions import IsAuthenticated 
from .models import User,CustomerProfile
from rest_framework_simplejwt.tokens import RefreshToken
import cloudinary.uploader
from .serializer import CustomerProfileSerializer
from bookings.models import Booking, FavoriteProvider
from review.models import Review
from services_app.models import ProviderProfile
@api_view(['GET'])
def hello(request):
    return Response({"message":"welcome to e-commers project"})

@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    role = request.data.get("role")

    if not username or not email or not password:
        return Response({"message": "All fields are required"})

    if User.objects.filter(email=email).exists():
        return Response({"message": "Email already registered"})

    User.objects.create_user(
        username=username,
        email=email,
        password=password,  # Django hashes automatically
        role=role
    )

    return Response({"message": "User registered successfully"})


@api_view(['POST'])
def login(request):

    email = request.data.get("email")
    password = request.data.get("password")

    try:
        database = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "Invalid credentials"})

    if not database.check_password(password):
        return Response({"message": "Invalid credentials"})

    refresh = RefreshToken.for_user(database)
    refresh["user_id"] = database.id
    refresh["role"] = database.role

    response = Response({
        "message": "Login Success"
    })

    response.set_cookie(
        "access_token",
        str(refresh.access_token),
        httponly=True
    )

    response.set_cookie(
        "refresh_token",
        str(refresh),
        httponly=True
    )

    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated,Iscustomer])
def create_customerprofile(request):
    if CustomerProfile.objects.filter(user=request.user).exists():
        return Response({
            "message": "Profile already exists"
        })
    profile_image=request.FILES.get("profile_image")
    image_url=cloudinary.uploader.upload(profile_image)
    serializer = CustomerProfileSerializer(
        data={
            "user": request.user.id,
            "phone": request.data.get("phone"),
            "profile_image": image_url["secure_url"],
            "address": request.data.get("address"),
            "city": request.data.get("city"),
        }
    )
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Profile created successfully"})
    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated,Iscustomer])
def view_customer_profile(request):

    profile = CustomerProfile.objects.get(
        user=request.user
    )
    return Response({
        "username": profile.user.username,
        "email": profile.user.email,
        "phone": profile.phone,
        "address": profile.address,
        "city": profile.city,
        "profile_image": profile.profile_image
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated,Iscustomer,])
def edit_customer_profile(request):

    try:
        profile = CustomerProfile.objects.get(
            user=request.user
        )
    except CustomerProfile.DoesNotExist:
        return Response({
            "message": "Profile not found"
        })

    serializer = CustomerProfileSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully"
        })

    return Response(serializer.errors)



@api_view(['GET'])
@permission_classes([IsAuthenticated, Iscustomer])
def customer_dashboard(request):

    profile = CustomerProfile.objects.get(
        user=request.user
    )

    active_bookings = Booking.objects.filter(
        customer=request.user,
        status__in=["pending", "accepted", "in_progress"]
    ).count()

    completed_bookings = Booking.objects.filter(
        customer=request.user,
        status="completed"
    ).count()

    favorite_providers = FavoriteProvider.objects.filter(
        customer=request.user
    ).count()

    reviews = Review.objects.filter(
        customer=request.user
    ).count()

    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "profile_image": profile.profile_image,
        "city": profile.city,
        "active_bookings": active_bookings,
        "completed_bookings": completed_bookings,
        "favorite_providers": favorite_providers,
        "reviews_given": reviews
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, Isprovider])
def provider_dashboard(request):

    try:
        provider = ProviderProfile.objects.get(
            user=request.user
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider profile not found."
        })

    pending_bookings = Booking.objects.filter(
        provider=provider,
        status="pending"
    ).count()

    accepted_bookings = Booking.objects.filter(
        provider=provider,
        status="accepted"
    ).count()

    in_progress_bookings = Booking.objects.filter(
        provider=provider,
        status="in_progress"
    ).count()

    completed_bookings = Booking.objects.filter(
        provider=provider,
        status="completed"
    ).count()

    return Response({
        "provider_name": request.user.username,
        "category": provider.category.type_of_service,
        "profile_image": provider.profile_image,
        "experience": provider.experience,
        "available": provider.available,
        "average_rating": provider.average_rating,
        "total_reviews": provider.total_reviews,
        "pending_bookings": pending_bookings,
        "accepted_bookings": accepted_bookings,
        "in_progress_bookings": in_progress_bookings,
        "completed_bookings": completed_bookings
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated, Isadmin])
def block_provider(request, id):

    try:
        provider = ProviderProfile.objects.get(id=id)
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider not found."
        })

    provider.user.is_active = False
    provider.user.save()

    return Response({
        "message": "Provider blocked successfully."
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated, Isadmin])
def unblock_provider(request, id):

    try:
        provider = ProviderProfile.objects.get(id=id)
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider not found."
        })

    provider.user.is_active = True
    provider.user.save()

    return Response({
        "message": "Provider unblocked successfully."
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, Isadmin])
def admin_dashboard(request):

    total_customers = User.objects.filter(
        role="customer"
    ).count()

    total_providers = User.objects.filter(
        role="provider"
    ).count()

    verified_providers = ProviderProfile.objects.filter(
        verified=True
    ).count()

    pending_verification = ProviderProfile.objects.filter(
        verified=False
    ).count()

    total_bookings = Booking.objects.count()

    completed_bookings = Booking.objects.filter(
        status="completed"
    ).count()

    total_reviews = Review.objects.count()

    return Response({
        "total_customers": total_customers,
        "total_providers": total_providers,
        "verified_providers": verified_providers,
        "pending_verification": pending_verification,
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "total_reviews": total_reviews
    })