from django.urls import path
from . import views
urlpatterns=[
    path("welcom/",view=views.hello),
    
    # Authentication
    path("register/",view=views.register),
    path("login/",view=views.login),

    # Customer Profile
    path("customer/profile/create/",view=views.create_customerprofile),
    path("customer/profile/",view=views.view_customer_profile),
    path("customer/profile/edit/",view=views.edit_customer_profile),

    # Dashboards
    path("customer-dashboard/",view=views.customer_dashboard),
    path("provider-dashboard/",view=views.provider_dashboard),
    path("admin/dashboard/",views.admin_dashboard),

    # Provider Management by Admin
    path("admin/providers/<int:id>/block/", views.block_provider),
    path("admin/providers/<int:id>/unblock/", views.unblock_provider),
   
]