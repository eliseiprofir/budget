from django.contrib import admin

from transactions.models import Entry
from transactions.models import Category


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Entry Information",
            {
                "fields": (
                    "name",
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "bucket")
    list_filter = ("name", "bucket")
    search_fields = ("name", "bucket")
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Category Information",
            {
                "fields": (
                    "name",
                    "bucket",
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
