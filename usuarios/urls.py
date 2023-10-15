from django.urls import path
from . import views
from .views import MeuUsuario, EditarUsuario

urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('registrar/', views.SignUp.as_view(), name="signup"),
    path('perfil/editar', views.EditarPerfil.as_view(), name="editar_perfil"),
    path('perfil/meu_perfil', views.EditarPerfil.as_view(), name="perfil"),
    path('usuarios/criar', MeuUsuario.as_view(), name='criar_usuario'),
    path('usuarios/editar', EditarUsuario.as_view(), name='editar_usuario')
]