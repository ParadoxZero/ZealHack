from django.contrib import admin

# Register your models here.
from wisdom.models import Service, Location, Rating, Notifications


class LocationInline(admin.StackedInline):
    model = Location


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [LocationInline, ]

admin.site.register(Rating)
admin.site.register(Notifications)
