from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Integracoes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    hubspot_access_token = models.CharField(max_length=500)
