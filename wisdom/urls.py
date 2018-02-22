from django.contrib import admin
from django.urls import path, include

from wisdom import views
urlpatterns = [
    path('get/notifications', views.get_notifications, name="get_notifications"),
    path('get/service/all', views.get_service_all, name="get_service_all"),
    path('get/service/<int:id>', views.get_service, name="get_service"),
    # path('get/reviews/<int:service_id>', views.get_reviews, name="get_reviews"),
    path('post/review', views.post_review, name="post_review"),

    path('', views.Index.as_view(), name='index')
]