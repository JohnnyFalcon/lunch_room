from django.core.management.base import BaseCommand

from decimal import Decimal

from lunch_room.models import Restaurant, Meal


class Command(BaseCommand):
    help = 'Populate database with sample restaurants and meals'

    def handle(self, *args, **options):
        # Restaurant data
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

        for restaurant_data in restaurants_data:
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_data['name'],
                defaults={
                    'address': restaurant_data['address'],
                    'phone': restaurant_data['phone']
                }
            )

            if created:
                print(f"Created new restaurant: {restaurant.name}")
            else:
                print(f"Found existing restaurant: {restaurant.name}")

            # Create meals for each restaurant
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

        print("\nPopulation completed!")
        print(f"Total restaurants: {Restaurant.objects.count()}")
        print(f"Total meals: {Meal.objects.count()}")