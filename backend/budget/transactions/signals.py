from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Transaction

@receiver(pre_save, sender=Transaction)
def update_transaction_type(sender, instance, **kwargs):
    if instance.category:
        instance.transaction_type = str(instance.category.transaction_type)
