from django.contrib import admin
from django.urls import path, include

from wisdom import views
urlpatterns = [
    path('api/get/notifications', views.get_notifications, name="get_notifications"),
    path('api/get/service/all', views.get_service_all, name="get_service_all"),
    path('api/get/service/<int:id>', views.get_service, name="get_service"),
    # path('get/reviews/<int:service_id>', views.get_reviews, name="get_reviews"),
    path('api/post/review', views.post_review, name="post_review"),
    path('api/location/get', views.get_nearest_locations, name="get_nearest_locations"),
    path('api/location/<slug:slug>/get', views.get_nearest_locations_service, name="get_nearest_location_service"),

    path('initiatives/<slug:slug>', views.ServiceDetails.as_view(), name="service_details"),
    path('<slug:initiative_slug>', views.InitiativeServiceList.as_view(), name="initiative_service_list"),
    path('', views.Index.as_view(), name='index')
]