from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permission import Iscustomer,Isprovider
from services_app.models import ProviderProfile
from .models import Booking ,FavoriteProvider
from .serializer import BookingSerializer,FavoriteProviderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, Iscustomer])
def create_booking(request):

    try:
        provider = ProviderProfile.objects.get(
            id=request.data.get("provider")
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider not found."
        })

    serializer = BookingSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save(
            customer=request.user,
            provider=provider
        )
        return Response({
            "message": "Booking created successfully."
        })

    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated, Iscustomer])
def view_my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    )

    serializer = BookingSerializer(
        bookings,
        many=True
    )

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, Iscustomer])
def cancel_booking(request, id):

    try:
        booking = Booking.objects.get(
            id=id,
            customer=request.user
        )
    except Booking.DoesNotExist:
        return Response({
            "message": "Booking not found."
        })

    booking.status = "cancelled"
    booking.save()

    return Response({
        "message": "Booking cancelled successfully."
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, Isprovider])
def view_booking_requests(request):

    provider = ProviderProfile.objects.get(
        user=request.user
    )

    bookings = Booking.objects.filter(
        provider=provider
    )

    serializer = BookingSerializer(
        bookings,
        many=True
    )

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, Isprovider])
def accept_booking(request, id):

    provider = ProviderProfile.objects.get(
        user=request.user
    )

    try:
        booking = Booking.objects.get(
            id=id,
            provider=provider
        )
    except Booking.DoesNotExist:
        return Response({
            "message": "Booking not found."
        })

    booking.status = "accepted"
    booking.save()

    return Response({
        "message": "Booking accepted."
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated, Isprovider])
def complete_booking(request, id):

    provider = ProviderProfile.objects.get(
        user=request.user
    )

    try:
        booking = Booking.objects.get(
            id=id,
            provider=provider
        )
    except Booking.DoesNotExist:
        return Response({
            "message": "Booking not found."
        })

    booking.status = "completed"
    booking.save()

    return Response({
        "message": "Booking completed."
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated, Iscustomer])
def add_favorite_provider(request):

    try:
        provider = ProviderProfile.objects.get(
            id=request.data.get("provider")
        )
    except ProviderProfile.DoesNotExist:
        return Response({
            "message": "Provider not found."
        })

    if FavoriteProvider.objects.filter(
        customer=request.user,
        provider=provider
    ).exists():
        return Response({
            "message": "Provider already added to favorites."
        })

    FavoriteProvider.objects.create(
        customer=request.user,
        provider=provider
    )

    return Response({
        "message": "Provider added to favorites."
    })



@api_view(['GET'])
@permission_classes([IsAuthenticated, Iscustomer])
def view_favorite_providers(request):

    favorites = FavoriteProvider.objects.filter(
        customer=request.user
    )

    serializer = FavoriteProviderSerializer(
        favorites,
        many=True
    )

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, Iscustomer])
def remove_favorite_provider(request, id):

    try:
        favorite = FavoriteProvider.objects.get(
            id=id,
            customer=request.user
        )
    except FavoriteProvider.DoesNotExist:
        return Response({
            "message": "Favorite provider not found."
        })

    favorite.delete()

    return Response({
        "message": "Provider removed from favorites."
    })