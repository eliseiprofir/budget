from django.contrib import admin

from transactions.models import TransactionType
from transactions.models import Category
from transactions.models import Transaction


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "sign",)
    list_filter = ("name", "sign",)
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("sign",)
    fieldsets = (
        (
            "Transaction Type Information",
            {
                "fields": (
                    "name",
                    "sign",
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "transaction_type")
    list_filter = ("name", "transaction_type")
    search_fields = ("name", "transaction_type")
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Category Information",
            {
                "fields": (
                    "name",
                    "transaction_type",
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


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "description", "transaction_type", "category", "date", "amount", "location", "bucket")
    list_filter = ("user", "date", "transaction_type", "category", "location", "bucket")
    search_fields = ("description", "transaction_type", "category", "date", "location", "bucket")
    ordering = ("-date",)
    readonly_fields = ()
    fieldsets = (
        (
            "Transaction Information",
            {
                "fields": (
                    "user",
                    "description",
                    "transaction_type",
                    "category",
                    "date",
                    "amount",
                    "location",
                    "bucket",
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
