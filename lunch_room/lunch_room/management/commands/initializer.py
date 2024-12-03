from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
from lunch_room.models import Restaurant, Meal, OrderGroup


class Command(BaseCommand):
    help = 'Initialize application data including restaurants, meals, users, and groups'

    restaurants_data = [
        {
            'name': 'Pizzeria Napoli',
            'address': 'ul. Krakowska 123, Warszawa',
            'phone': '+48 123 456 789',
            'meals': [
                ('Margherita', '25.00'),
                ('Pepperoni', '32.00'),
                ('Capricciosa', '34.00'),
                ('Quattro Formaggi', '36.00'),
                ('Diavola', '33.00'),
                ('Hawajska', '31.00'),
                ('Vegetariana', '30.00'),
                ('Calzone', '35.00'),
                ('Marinara', '28.00'),
                ('Funghi', '29.00'),
            ]
        },
        {
            'name': 'Burger House',
            'address': 'ul. Długa 45, Warszawa',
            'phone': '+48 987 654 321',
            'meals': [
                ('Classic Burger', '29.00'),
                ('Cheeseburger', '32.00'),
                ('Double Burger', '39.00'),
                ('Chicken Burger', '28.00'),
                ('Vege Burger', '27.00'),
                ('BBQ Burger', '34.00'),
                ('Mexican Burger', '35.00'),
                ('Fish Burger', '31.00'),
                ('Bacon Burger', '33.00'),
                ('Mushroom Burger', '30.00'),
            ]
        },
        {
            'name': 'Asian Fusion',
            'address': 'ul. Nowy Świat 78, Warszawa',
            'phone': '+48 321 654 987',
            'meals': [
                ('Pad Thai', '28.00'),
                ('Sushi Set', '45.00'),
                ('Ramen', '32.00'),
                ('Spring Rolls', '18.00'),
                ('Curry Chicken', '34.00'),
                ('Fried Rice', '26.00'),
                ('Dim Sum', '30.00'),
                ('Peking Duck', '48.00'),
                ('Tom Yum Soup', '25.00'),
                ('Bao Buns', '27.00'),
            ]
        }
    ]

    def create_groups(self):
        """Create default user groups."""
        groups = {}
        group_names = ['admin', 'manager', 'customer']

        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            print(f"{'Created' if created else 'Found'} group: {name}")

        return groups

    def create_users(self):
        """Create default admin users."""
        users = []
        default_password = 'printbox'
        user_emails = ['bob@getprintbox.com', 'stefan@getprintbox.com']

        # Get admin group
        admin_group = Group.objects.get(name='admin')

        for email in user_emails:
            username = email.split('@')[0]
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={
                    'is_active': True,
                    'is_staff': True,
                    'is_superuser': True
                }
            )

            if created:
                user.set_password(default_password)
                user.save()
                print(f"Created new admin user: {email}")
            else:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                print(f"Updated existing user to admin: {email}")

            user.groups.add(admin_group)
            print(f"Added user {email} to admin group")

            users.append(user)

        return users

    def create_restaurants(self):
        """Create restaurants and their meals."""
        for restaurant_data in self.restaurants_data:
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_data['name'],
                defaults={
                    'address': restaurant_data['address'],
                    'phone': restaurant_data['phone']
                }
            )

            print(f"{'Created' if created else 'Found'} restaurant: {restaurant.name}")

            for meal_name, price in restaurant_data['meals']:
                meal, meal_created = Meal.objects.get_or_create(
                    name=meal_name,
                    restaurant=restaurant,
                    defaults={'price': Decimal(price)}
                )

                if meal_created:
                    print(f"Added new meal: {meal_name} to {restaurant.name}")
                else:
                    print(f"Meal {meal_name} already exists in {restaurant.name}")

    def create_order_group(self, users):
        """Create default order group and assign users."""
        order_group, created = OrderGroup.objects.get_or_create(
            name='Default Order Group',
        )

        if created:
            print("Created new order group: Default Order Group")
        else:
            print("Found existing order group: Default Order Group")

        # Add users to the order group
        for user in users:
            order_group.users.add(user)
            print(f"Added user {user.email} to order group")

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                print("Starting data initialization...")

                # Create groups
                groups = self.create_groups()

                # Create admin users
                users = self.create_users()

                # Create restaurants and meals
                self.create_restaurants()

                # Create order group and assign users
                self.create_order_group(users)

                print("\nData initialization completed successfully!")

        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise
