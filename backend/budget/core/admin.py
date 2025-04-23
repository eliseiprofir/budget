from django.contrib import admin

from core.models import Bucket
from core.models import Location


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ("name", "allocation_percentage", "allocation_status", "is_removed", "user")
    list_filter = ("is_removed", "user")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("allocation_status",)
    fieldsets = (
        (
            "Bucket Information",
            {
                "fields": (
                    "name",
                    "allocation_percentage",
                    "allocation_status",
                    "is_removed",
                    "user",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (),
            },
        ),
    )

    def get_queryset(self, request):
        return Bucket.all_objects.all()

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_removed", "user")
    list_filter = ("is_removed", "user")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Location Information",
            {
                "fields": (
                    "name",
                    "is_removed",
                    "user",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": (),
            },
        ),
    )

    def get_queryset(self, request):
        return Location.all_objects.all()
