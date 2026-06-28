from django.db.models import Avg
from .models import Review


def update_provider_rating(provider):

    reviews = Review.objects.filter(provider=provider)

    total_reviews = reviews.count()

    if total_reviews == 0:
        average_rating = 0
    else:
        average_rating = reviews.aggregate(
            Avg("rating")
        )["rating__avg"]

    provider.average_rating = round(average_rating, 1)
    provider.total_reviews = total_reviews
    provider.save()