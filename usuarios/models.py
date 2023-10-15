from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=50, null=True, blank=True)
    imagem_de_perfil = models.ImageField(null=True, blank=True, upload_to='imagens/perfil/')
    email = models.EmailField(max_length=254, null=True, blank=True)
    site = models.URLField(max_length=254, null=True, blank=True)
    instagram = models.URLField(max_length=254, null=True, blank=True)
    facebook = models.URLField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.user

