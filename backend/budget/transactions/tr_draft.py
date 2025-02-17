# from decimal import Decimal
# from django.core.exceptions import ValidationError
#
# class Transaction(UUIDModel):
#     """Model to store transaction entry/type information"""
#
#     class SplitMethod:
#         """Choices for income split method"""
#         SINGLE_BUCKET = "SINGLE"
#         SPLIT_BY_ALLOCATION = "SPLIT"
#
#         CHOICES = (
#             (SINGLE_BUCKET, "Single Bucket"),
#             (SPLIT_BY_ALLOCATION, "Split by Allocation"),
#         )
#
#     # Existing fields...
#
#     # Add new field for income transactions only
#     split_method = models.CharField(
#         max_length=20,
#         choices=SplitMethod.CHOICES,
#         null=True,
#         blank=True,
#         help_text="Method to split income across buckets (only for income transactions)",
#     )
#
#     def clean(self):
#         """Validate model"""
#         super().clean()
#
#         # Validate split_method only for income transactions
#         if self.amount > 0:  # Income transaction
#             if not self.split_method:
#                 raise ValidationError("Split method is required for income transactions")
#
#             if self.split_method == self.SplitMethod.SINGLE_BUCKET and not self.bucket:
#                 raise ValidationError("Bucket is required when using single bucket method")
#
#             if self.split_method == self.SplitMethod.SPLIT_BY_ALLOCATION:
#                 # Verify user has complete bucket allocation
#                 if not Bucket.is_allocation_complete(self.user):
#                     raise ValidationError("Cannot split income - bucket allocations must sum to 100%")
#                 self.bucket = None  # Clear bucket selection when splitting
#
#     def save(self, *args, **kwargs):
#         """Override save to handle income splitting"""
#         self.full_clean()
#
#         # First save the main transaction
#         super().save(*args, **kwargs)
#
#         # Handle income splitting if needed
#         if self.amount > 0 and self.split_method == self.SplitMethod.SPLIT_BY_ALLOCATION:
#             self._split_income()
#
#     def _split_income(self):
#         """Split income into multiple transactions based on bucket allocations"""
#         # Get all user's buckets
#         buckets = Bucket.available_objects.filter(user=self.user)
#
#         # Delete any existing split transactions
#         Transaction.objects.filter(
#             parent_transaction=self,
#         ).delete()
#
#         # Create new split transactions
#         for bucket in buckets:
#             if bucket.allocation_percentage > 0:
#                 split_amount = (self.amount * bucket.allocation_percentage / 100).quantize(Decimal('0.01'))
#
#                 Transaction.objects.create(
#                     user=self.user,
#                     description=f"Split from {self.description} ({bucket.allocation_percentage}%)",
#                     category=self.category,
#                     date=self.date,
#                     amount=split_amount,
#                     location=self.location,
#                     bucket=bucket,
#                     parent_transaction=self,
#                     split_method=None  # Prevent recursive splitting
#                 )
#
#     # Add fields for split transactions
#     parent_transaction = models.ForeignKey(
#         'self',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='split_transactions'
#     )