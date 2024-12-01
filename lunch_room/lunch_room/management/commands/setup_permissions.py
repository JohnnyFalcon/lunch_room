from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    """
     Command to create three default groups: admin, manager, and customer.
    """

    def handle(self, *args, **kwargs):
        try:
            admin_group, _ = Group.objects.get_or_create(name='admin')
            manager_group, _ = Group.objects.get_or_create(name='manager')
            customer_group, _ = Group.objects.get_or_create(name='customer')

            print('Successfully created all groups')

        except Exception as e:
            print(f'Error creating groups: {str(e)}')

