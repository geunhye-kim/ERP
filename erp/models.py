from django.db import models
from accounts.models import UserModel
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Product(models.Model):
    class Meta:
        db_table = "my_product"

    product_code = models.CharField(max_length=10)
    product_name = models.CharField(max_length=20)
    product_sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    product_size = models.CharField(choices=product_sizes, max_length=1)
    product_price = models.IntegerField()
    product_desc = models.TextField()
    product_quantity = models.IntegerField(default=0)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, default=1)


class Inbound(models.Model):
    class Meta:
        db_table = "my_inbound"

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inbound")
    inbound_quantity = models.IntegerField(default=0)
    inbound_date = models.DateTimeField(auto_now_add=True)


class Outbound(models.Model):
    class Meta:
        db_table = "my_outbound"

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="outbound")
    outbound_quantity = models.IntegerField(default=0)
    outbound_date = models.DateTimeField(auto_now_add=True)
