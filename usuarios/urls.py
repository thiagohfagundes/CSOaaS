from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('registrar/', views.SignUp.as_view(), name="signup"),
    path('perfil/editar', views.EditarPerfil.as_view(), name="editar_perfil"),
    path('perfil/meu_perfil', views.EditarPerfil.as_view(), name="perfil"),
]