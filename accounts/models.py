#accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    # username = models.CharField(max_length=20, null=False)
    # password = models.CharField(max_length=256, null=False)
    # email = models.EmailField(default='example@example.com')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
