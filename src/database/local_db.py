import os
from security.crypto import criptografar_dados, descriptografar_dados

# Define o caminho para a pasta database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def salvar_dados_seguros(nome_arquivo: str, dados: dict):
    """Criptografa os dados e salva em um arquivo dentro da pasta database."""
    if not nome_arquivo.endswith('.json'):
        nome_arquivo += '.json'
        
    caminho_completo = os.path.join(BASE_DIR, nome_arquivo)
    
    # Criptografa o dicionário
    conteudo_criptografado = criptografar_dados(dados)
    
    # Salva o arquivo em modo binário ('wb')
    with open(caminho_completo, 'wb') as arquivo:
        arquivo.write(conteudo_criptografado)

def carregar_dados_seguros(nome_arquivo: str) -> dict:
    """Lê o arquivo criptografado e retorna os dados originais."""
    if not nome_arquivo.endswith('.json'):
        nome_arquivo += '.json'
        
    caminho_completo = os.path.join(BASE_DIR, nome_arquivo)
    
    if not os.path.exists(caminho_completo):
        return {} # Retorna vazio se o arquivo não existir ainda
        
    # Lê o arquivo em modo binário ('rb')
    with open(caminho_completo, 'rb') as arquivo:
        conteudo_criptografado = arquivo.read()
        
    # Descriptografa e retorna
    return descriptografar_dados(conteudo_criptografado)