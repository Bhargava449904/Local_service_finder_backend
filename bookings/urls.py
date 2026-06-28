from django.urls import path
from . import views
urlpatterns=[
    # Bookings
    path("bookings/create/", views.create_booking),
    path("bookings/", views.view_my_bookings),
    path("bookings/<int:id>/cancel/", views.cancel_booking),

    # Provider Bookings
    path("provider/bookings/", views.view_booking_requests),
    path("provider/bookings/<int:id>/accept/", views.accept_booking),
    path("provider/bookings/<int:id>/complete/", views.complete_booking),

    # Favorite Providers
    path("favorites/", views.view_favorite_providers),
    path("favorites/add/", views.add_favorite_provider),
    path("favorites/<int:id>/remove/", views.remove_favorite_provider),
]