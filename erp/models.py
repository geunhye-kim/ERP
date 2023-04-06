from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    class Meta:
        db_table = "my_product"

    product_code = models.CharField(max_length=10)
    product_name = models.CharField(max_length=15)
    product_sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    product_size = models.CharField(choices=product_sizes, max_length=1)
    product_price = models.CharField(max_length=10)
    product_desc = models.TextField()
    product_quantity = models.IntegerField(default=0)


class Inbound(Product):
    inbound_quantity = models.IntegerField(default=0)
    inbound_date = models.DateTimeField(auto_now_add=True)


class Outbound(Product):
    outbound_quantity = models.IntegerField(default=0)
    outbound_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.code
    #
    # def save(self, *args, **kwargs):
