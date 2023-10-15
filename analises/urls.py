from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.analises, name='index'),
    path('segmentacao/', views.segmentacao, name='segmentacao'),
    path('tratamento/', views.tratamento, name='tratamento'),
    path('<int:pk>/password/', auth_views.PasswordChangeView.as_view(template_name='registration/mudarsenha.html'), name='editarsenha'),
    path('tiposvariaveis/', views.tiposvariaveis, name='tiposvariaveis'),
    path('hubspot/', views.login_hubspot, name = 'hubspot'),
    path('instalado/', views.retorno_hubspot),
    path('vincular/', views.vincular, name='vincular'),
    path('configurar/', views.configurar_opcoes_hubspot, name='configurar'),
    path('confirmar/', views.confirmar, name='confirmar'),
]