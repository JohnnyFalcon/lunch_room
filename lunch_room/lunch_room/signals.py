from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def add_user_to_customer_group(sender, instance, created, **kwargs):
    if created:
        try:
            customer_group = Group.objects.get(name='customer')
            instance.groups.add(customer_group)
        except Group.DoesNotExist:
            pass