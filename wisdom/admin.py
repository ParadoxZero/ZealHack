from django.contrib import admin

# Register your models here.
from wisdom.models import Service, Location, Rating, Notifications, ServiceImage


class LocationInline(admin.StackedInline):
    model = Location

class ImageInline(admin.StackedInline):
    model = ServiceImage

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [LocationInline, ImageInline]

admin.site.register(Rating)
admin.site.register(Notifications)
