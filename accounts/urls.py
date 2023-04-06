from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='sign-up'),
    path('login/', views.login_view, name='log-in'),
    path('logout/', views.logout_view, name='log-out'),
]