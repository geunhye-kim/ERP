from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.inventory_show, name='inventory'),
    path('productcreate/', views.product_create, name='product-create'),
    path('inboundcreate/', views.inbound_create, name='inbound-create'),
    path('inboundlist/<int:id>/', views.inbound_list, name='inbound-list'),
    path('outboundcreate/', views.outbound_create, name='outbound-create'),
    path('outboundlist/<int:id>/', views.outbound_list, name='outbound-list'),
]