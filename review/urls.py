from django.urls import path
from . import views
urlpatterns=[
    # Reviews
    path("reviews/create/", views.create_review),
    path("reviews/", views.view_my_reviews),
    path("reviews/provider/<int:id>/", views.view_provider_reviews),
    path("reviews/<int:id>/delete/", views.delete_review),
]