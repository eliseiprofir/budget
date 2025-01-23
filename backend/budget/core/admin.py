from django.contrib import admin

from core.models import Bucket
from core.models import Location


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "allocation_percentage")
    list_filter = ("is_removed",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Bucket Information",
            {
                "fields": (
                    "name",
                    "user",
                    "allocation_percentage",
                    "is_removed",
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


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("is_removed",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Location Information",
            {
                "fields": (
                    "name",
                    "user",
                    "is_removed",
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
