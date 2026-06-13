import os
import shutil

def limpar_pycache(diretorio_inicial="."):
    print(f"Iniciando a limpeza a partir de: {os.path.abspath(diretorio_inicial)}\n")
    
    contador_pastas = 0
    contador_arquivos = 0

    # os.walk navega por todas as pastas e subpastas
    for raiz, diretorios, arquivos in os.walk(diretorio_inicial, topdown=False):
        
        # 1. Remover pastas __pycache__
        for diretorio in diretorios:
            if diretorio == "__pycache__":
                caminho_completo = os.path.join(raiz, diretorio)
                try:
                    shutil.rmtree(caminho_completo)
                    print(f"[PASTA APAGADA] {caminho_completo}")
                    contador_pastas += 1
                except Exception as e:
                    print(f"[ERRO] Não foi possível apagar {caminho_completo}: {e}")

        # 2. Remover arquivos .pyc ou .pyo isolados (caso existam fora do __pycache__)
        for arquivo in arquivos:
            if arquivo.endswith(".pyc") or arquivo.endswith(".pyo"):
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    os.remove(caminho_completo)
                    print(f"[ARQUIVO APAGADO] {caminho_completo}")
                    contador_arquivos += 1
                except Exception as e:
                    print(f"[ERRO] Não foi possível apagar {caminho_completo}: {e}")

    print("\n" + "="*30)
    print("Limpeza concluída com sucesso!")
    print(f"Total de pastas __pycache__ removidas: {contador_pastas}")
    print(f"Total de arquivos .pyc/.pyo removidos: {contador_arquivos}")
    print("="*30)

if __name__ == "__main__":
    # Executa a limpeza na pasta atual
    limpar_pycache()