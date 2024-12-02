from django.db import models


class Restaurant(models.Model):
    name = models.CharField(verbose_name='Nazwa', max_length=255)
    address = models.CharField(verbose_name='Adres', max_length=255)
    phone = models.CharField(verbose_name='Telefon kontaktowy', max_length=255)


class Meal(models.Model):
    name = models.CharField(verbose_name='Nazwa', max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='meals')