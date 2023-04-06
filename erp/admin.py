from django.contrib import admin
from .models import Product, Inbound, Outbound

# Register your models here.
admin.site.register(Product)
admin.site.register(Inbound)
admin.site.register(Outbound)