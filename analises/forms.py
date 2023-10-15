from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class UploadCSVForm(forms.Form):
    arquivo_csv = forms.FileField(label="Importe seu arquivo CSV")
    linha_inicio = forms.CharField(label="Linha de início", max_length=6, required=False)
    linha_final = forms.CharField(label="Linha final", max_length=6, required=False)
    coluna_inicio = forms.CharField(label="Coluna de início", max_length=6, required=False)
    coluna_final = forms.CharField(label="Coluna final", max_length=6, required=False)

class SelecaoColunas(forms.Form):
    def __init__(self, *args, **kwargs):
        opcoes = kwargs.pop('opcoes', None)
        super(SelecaoColunas, self).__init__(*args, **kwargs)

        if opcoes is not None:
            self.fields['colunas'] = forms.MultipleChoiceField(
                choices=[(opcao, opcao) for opcao in opcoes],
                widget=forms.CheckboxSelectMultiple
            )

class SelecaoHubs(forms.Form):
    pipeline = forms.ChoiceField(choices=[])
    propriedade = forms.MultipleChoiceField(choices=[])
    proprietarios = forms.MultipleChoiceField(choices=[])

class SelecaoPropriedades(forms.Form):
    propriedades = forms.MultipleChoiceField(choices=[])