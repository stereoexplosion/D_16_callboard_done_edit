from django.contrib.auth.models import User
from django.db import models


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    code_create_time = models.DateTimeField(auto_now_add=True)

