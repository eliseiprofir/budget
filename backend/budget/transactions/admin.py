from django.contrib import admin

from transactions.models import Category
from transactions.models import Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sign", "is_removed", "user")
    list_filter = ("sign", "is_removed", "user")
    search_fields = ("name", "sign", "user")
    ordering = ("name",)
    readonly_fields = ()
    fieldsets = (
        (
            "Category Information",
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


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("description", "category", "date", "amount", "location", "bucket", "split_income", "parent_transaction", "user")
    list_filter = ("date", "category", "location", "bucket", "user")
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
                    "parent_transaction",
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
