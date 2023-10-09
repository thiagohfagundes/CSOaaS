from django.shortcuts import render, redirect
from .forms import UploadCSVForm
import pandas as pd

# Create your views here.
def analises(request):
    return render(request, 'index.html', {

    })

def segmentacao(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_csv = request.FILES['arquivo_csv']
            df = pd.read_csv(arquivo_csv)
            request.session['df_json'] = df.to_json()
            return redirect('tratamento')
    else:
        form = UploadCSVForm()

    return render(request, 'analises/segmentacao.html', {
        'form': form
    })


def tratamento(request):
    df_json = request.session.get('df_json')

    if df_json:
        df = pd.read_json(df_json)
        colunas = df.columns
    else:
        redirect('segmentacao')

    return render(request, 'analises/tratamento.html', {
        "colunas": colunas,
        "dados": df,
    })