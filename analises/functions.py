import requests
import pandas as pd

# ------------------ Hubspot ---------------------- #

# Função responsável por trocar o code pelo acess token com a Hubspot
def trocacodigo(client_id, client_secret, redirect_uri, code):
    token_url = "https://api.hubapi.com/oauth/v1/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
    else:
        print("Erro ao obter o Access Token. Código de status:", response.status_code)
        print(response.text)
    return access_token

# Função responsável por puxar todos os pipes do Hubspot
def identificapipes(tipopipe, access_token):
    # Define a URL do endpoint de busca de pipelines de tickets
    url = f"https://api.hubapi.com/crm/v3/pipelines/{tipopipe}"

    # Define os parâmetros da query string da requisição
    params = {
        "includeInactive": "false"
    }

    # Faz a requisição GET para o endpoint da API do Hubspot
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, params=params)

    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        # Extrai a lista de pipelines da resposta da API e imprime na tela os nomes e IDs de cada pipeline
        pipes = response.json().get("results")
    else:
        # Imprime uma mensagem de erro caso a requisição não tenha sido bem sucedida
        print(f"Erro ao buscar os pipelines: {response.status_code} - {response.text}")

    return pipes

def identificapropriedades(access_token, tipo_pipe):
    # Define a URL do endpoint de busca de propriedades de tickets
    url = f"https://api.hubapi.com/crm/v3/properties/{tipo_pipe}"

    # Define os parâmetros da query string da requisição, testar sem isso
    params = {
        "limit": 100
    }

    # Faz a requisição GET para o endpoint da API do Hubspot
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, params=params)

    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        # Extrai a lista de propriedades da resposta da API e imprime na tela
        properties = response.json().get("results")
    else:
        # Imprime uma mensagem de erro caso a requisição não tenha sido bem sucedida
        print(f"Erro ao buscar as propriedades: {response.status_code} - {response.text}")

    return properties

def consulta_etapas_pipeline(access_token, object_type, id_pipeline):
    # Faça a requisição para obter as etapas do pipeline
    url = f'https://api.hubapi.com/crm/v3/pipelines/{object_type}/{id_pipeline}/stages'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    stages_pipeline = response.json()['results']
    return stages_pipeline

def consulta_proprietarios(access_token):
    url = "https://api.hubapi.com/owners/v2/owners"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    df = pd.DataFrame(response.json())
    owners = df.loc[:, ['ownerId', 'firstName', 'lastName', 'email']]
    owners['identificacao'] = owners['email'] + ' - ' + owners['firstName'] + ' ' + owners['lastName']
    return owners

# Não está funcionando corretamente, corrigir
def informacoes_conta(access_token):
    account_info_url = 'https://api.hubapi.com/oauth/v1/access-tokens/account-info'

    # Cabeçalho de autenticação com o access token
    headers = {'Authorization': f'Bearer {access_token}'}

    # Faça a solicitação GET para obter informações da conta
    response = requests.get(account_info_url, headers=headers)

    if response.status_code == 200:
        account_info = response.json()
        print(account_info)
        return account_info
    else:
        print(f"Erro ao obter informações da conta. Código de status: {response.status_code}")
        print(response.text)

