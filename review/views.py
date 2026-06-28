from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .utils import update_provider_rating
from accounts.permission import Iscustomer
from bookings.models import Booking
from .models import Review
from .serializer import ReviewSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated, Iscustomer])
def create_review(request):

    try:
        booking = Booking.objects.get(
            id=request.data.get("booking"),
            customer=request.user,
            status="completed"
        )
    except Booking.DoesNotExist:
        return Response({
            "message": "Completed booking not found."
        })

    if Review.objects.filter(booking=booking).exists():
        return Response({
            "message": "Review already submitted."
        })

    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save(
            customer=request.user,
            provider=booking.provider
        )

        update_provider_rating(booking.provider)

        return Response({
            "message": "Review added successfully."
        })

    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated, Iscustomer])
def view_my_reviews(request):

    reviews = Review.objects.filter(
        customer=request.user
    )

    serializer = ReviewSerializer(
        reviews,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def view_provider_reviews(request, id):

    reviews = Review.objects.filter(
        provider=id
    )

    serializer = ReviewSerializer(
        reviews,
        many=True
    )

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, Iscustomer])
def delete_review(request, id):

    try:
        review = Review.objects.get(
            id=id,
            customer=request.user
        )
    except Review.DoesNotExist:
        return Response({
            "message": "Review not found."
        })

    provider = review.provider

    review.delete()

    update_provider_rating(provider)

    return Response({
        "message": "Review deleted successfully."
    })