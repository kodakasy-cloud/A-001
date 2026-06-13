import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Recupera a chave do arquivo .env
CHAVE = os.getenv("CHAVE_CRIPTOGRAFIA")
if not CHAVE:
    raise ValueError("A chave de criptografia não foi encontrada no arquivo .env!")

fernet = Fernet(CHAVE.encode())

def criptografar_dados(dados: dict) -> bytes:
    """Transforma um dicionário em string JSON e criptografa."""
    json_string = json.dumps(dados)
    dados_criptografados = fernet.encrypt(json_string.encode('utf-8'))
    return dados_criptografados

def descriptografar_dados(dados_criptografados: bytes) -> dict:
    """Descriptografa os dados e os transforma de volta em dicionário."""
    try:
        json_string = fernet.decrypt(dados_criptografados).decode('utf-8')
        return json.loads(json_string)
    except Exception as e:
        print(f"Erro ao descriptografar: {e}")
        return {}