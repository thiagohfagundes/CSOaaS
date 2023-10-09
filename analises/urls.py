from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.analises, name='index'),
    path('segmentacao/', views.segmentacao, name='segmentacao'),
    path('tratamento/', views.tratamento, name='tratamento'),
    path('<int:pk>/password/', auth_views.PasswordChangeView.as_view(template_name='registration/mudarsenha.html'), name='editarsenha'),
]