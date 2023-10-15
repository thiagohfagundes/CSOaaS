from django.shortcuts import render, redirect
from .forms import UploadCSVForm, SelecaoColunas, SelecaoHubs
from django.contrib.auth.decorators import login_required
import pandas as pd
from io import StringIO
from .functions import trocacodigo, identificapipes, identificapropriedades, consulta_proprietarios
from .models import Integracoes
import requests

client_id = '0c545053-e2f4-4365-8b76-bad3aa88a776'
client_secret = '32bc602f-e17d-4a4b-8433-9f1a9ba760cb'
redirect_uri = 'http://localhost:8000/instalado/'
auth_hubspot = f"https://app.hubspot.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=crm.objects.deals.read%20crm.objects.owners.read"

# Create your views here.
def analises(request):

    return render(request, 'index.html', {})

@login_required(login_url='login')
def vincular(request):
    usuario = request.user
    try:
        registro = Integracoes.objects.get(usuario=usuario)
        registro = 'Conta do Hubspot vinculada'
    except Integracoes.DoesNotExist:
        registro = 'Conta não vinculada'
    return render(request, 'vincular_hubspot.html', {
        "registro": registro
    })

def segmentacao(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_csv = request.FILES['arquivo_csv']
            df = pd.read_csv(arquivo_csv)
            if form.cleaned_data["linha_inicio"]:
                linha_inicial = form.cleaned_data["linha_inicio"]
            if form.cleaned_data["linha_final"]:
                linha_final = form.cleaned_data["linha_final"]
            if form.cleaned_data["coluna_inicio"]:
                coluna_inicio = form.cleaned_data["coluna_inicio"]
            if form.cleaned_data["coluna_final"]:
                coluna_final = form.cleaned_data["coluna_final"]

            request.session['df'] = df.to_json()
            return redirect('tratamento')
    else:
        form = UploadCSVForm()

    return render(request, 'analises/segmentacao.html', {
        'form': form
    })

def tratamento(request):
    df_json = request.session.get('df')

    if df_json:
        df = pd.read_json(StringIO(df_json))
        colunas = df.columns
    else:
        redirect('segmentacao')

    if request.method == 'POST':
        form = SelecaoColunas(request.POST, opcoes=colunas)
        if form.is_valid():
            opcoes_selecionadas = form.cleaned_data['colunas']
            df = df[opcoes_selecionadas] #transformar isso em dataframe primeiro
            request.session['df'] = df.to_json()
            return redirect('tiposvariaveis')
    else:
        form = SelecaoColunas(opcoes=colunas)

    return render(request, 'analises/tratamento.html', {
        "colunas": colunas,
        "form": form
    })

def tiposvariaveis(request):
    df_json = request.session.get('df')

    return render(request, 'analises/tiposvariaveis.html')

@login_required(login_url='login')
def login_hubspot(request):
    return redirect(auth_hubspot)

@login_required(login_url='login')
def retorno_hubspot(request):
    code = request.GET.get('code')
    usuario = request.user
    registro, criado = Integracoes.objects.get_or_create(usuario=usuario)

    if criado:
        access_token = trocacodigo(client_id, client_secret, redirect_uri, code)
        registro.hubspot_access_token = access_token
        registro.save()
        mensagem = 'Conta vinculada com sucesso'
    else:
        registro = Integracoes.objects.get(usuario=usuario)
        if registro.hubspot_access_token:
            access_token = registro.hubspot_access_token
        else:
            registro.hubspot_access_token = trocacodigo(client_id, client_secret, redirect_uri, code)
            registro.save()
            mensagem = 'Conta vinculada com sucesso'
        mensagem = 'Conta vinculada com sucesso'

    return render(request, 'conector/hubspot/retornohubspot.html', {
        "mensagem": mensagem,
    })

@login_required(login_url='login')
def configurar_opcoes_hubspot(request):
    usuario = Integracoes.objects.get(usuario=request.user)
    access_token = usuario.hubspot_access_token

    pipelines = identificapipes('deals', access_token)
    proprietarios = consulta_proprietarios(access_token)
    propriedades = identificapropriedades(access_token, 'deals')

    opcoes_pipeline = [item['label'] for item in pipelines]
    opcoes_propriedade = [item['label'] for item in propriedades]
    proprietarios_list = proprietarios['identificacao'].tolist()

    if request.method == 'POST':
        form = SelecaoHubs()
        form.fields['pipeline'].choices = [(label, label) for label in opcoes_pipeline]
        form.fields['propriedade'].choices = [(label, label) for label in opcoes_propriedade]
        form.fields['proprietarios'].choices = [(label, label) for label in proprietarios_list]

        request.session['pipeline'] = form.pipeline
        request.session['propriedade'] = form.propriedade
        request.session['proprietarios'] = form.proprietarios
        return redirect('confirmar')

    else:
        form = SelecaoHubs()
        form.fields['pipeline'].choices = [(label, label) for label in opcoes_pipeline]
        form.fields['propriedade'].choices = [(label, label) for label in opcoes_propriedade]
        form.fields['proprietarios'].choices = [(label, label) for label in proprietarios_list]

    return render(request, 'conector/hubspot/configurar_hubspot.html', {
        "form": form,
    })

@login_required(login_url='login')
def confirmar(request):
    propriedades = request.session.get('propriedade')
    pipeline = request.session.get('pipeline')
    proprietarios = request.session.get('proprietarios')

    return render(request, 'conector/hubspot/confirmar.html', {
        "propriedades": propriedades,
        "pipeline": pipeline,
        "proprietarios": proprietarios
    })
