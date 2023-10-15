from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def usuarios(request):
    return render(request, 'registration/usuarios.html')

class MeuUsuario(CreateView):
    model = Perfil
    template_name = 'registration/criar_usuarios.html'
    fields = '__all__'

class EditarUsuario(UpdateView):
    model = Perfil
    template_name = 'registration/editar_usuarios.html'

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registrar.html'

class EditarPerfil(generic.UpdateView):
    form_class = UserChangeForm
    success_url = reverse_lazy('index')
    template_name = 'registration/editar_perfil.html'

    def get_object(self):
        return self.request.user
