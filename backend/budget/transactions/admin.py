from django.contrib import admin

from transactions.models import TransactionType
from transactions.models import Category
from transactions.models import Transaction


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "sign", "user")
    list_filter = ("name", "sign", "user")
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "transaction_type", "user")
    list_filter = ("name", "transaction_type", "user")
    search_fields = ("name", "transaction_type", "user")
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


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("description", "transaction_type", "category", "date", "amount", "location", "bucket", "split_income", "parent_transaction", "user")
    list_filter = ("user", "date", "category", "location", "bucket")
    search_fields = ("description", "category__name", "date", "location__name", "bucket__name", "user__email")
    ordering = ("-date",)
    readonly_fields = ()
    fieldsets = (
        (
            "Transaction Information",
            {
                "fields": (
                    "description",
                    "category",
                    "date",
                    "amount",
                    "location",
                    "bucket",
                    "split_income",
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
