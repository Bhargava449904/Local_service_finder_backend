from django.urls import path
from . import views
urlpatterns=[
    # Service Categories
    path("categories/", views.view_service_categories),
    path("categories/create/", views.create_service_category),

    # Provider Profile
    path("provider/profile/", views.view_provider_profile),
    path("provider/profile/create/", views.create_provider_profile),
    path("provider/profile/edit/", views.edit_provider_profile),

    # Provider Gallery
    path("provider/gallery/", views.view_provider_gallery),
    path("provider/gallery/upload/", views.upload_provider_gallery),
    path("provider/gallery/<int:id>/delete/", views.delete_provider_gallery),

    # Customer Provider Search
    path("providers/", views.view_all_providers),
    path("providers/category/<int:id>/", views.search_provider_by_category),
    path("providers/nearby/", views.nearby_providers),
    path("providers/<int:id>/", views.provider_details),

    # Admin
    path("admin/providers/", views.admin_view_providers),
    path("admin/providers/<int:id>/verify/", views.verify_provider),
]