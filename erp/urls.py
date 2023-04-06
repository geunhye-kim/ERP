from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.inventory_show, name='inventory'),
    path('productcreate/', views.product_create, name='product-create'),
    path('inboundcreate/', views.inbound_create, name='inbound-create'),
]