from database.local_db import salvar_dados_seguros, carregar_dados_seguros

class NotasController:
    def __init__(self, view):
        self.view = view
        self.bloco_selecionado = {"id": None}

    def obter_dados(self):
        dados = carregar_dados_seguros("cofre_notas")
        return dados or {}

    def obter_lista_notas(self):
        return self.obter_dados().get("notas", [])

    def salvar_bloco(self, titulo, texto, cor, emoji="📝"):
        if not titulo:
            return False
        
        dados_salvos = self.obter_dados()
        blocos_dados = dados_salvos.get("notas", [])
        
        if self.bloco_selecionado["id"] is None:
            novo_id = max([b["id"] for b in blocos_dados]) + 1 if blocos_dados else 1
            blocos_dados.append({
                "id": novo_id,
                "titulo": titulo,
                "texto": texto,
                "cor": cor,
                "emoji": emoji
            })
        else:
            for b in blocos_dados:
                if b["id"] == self.bloco_selecionado["id"]:
                    b["titulo"] = titulo
                    b["texto"] = texto
                    b["cor"] = cor
        
        dados_salvos["notas"] = blocos_dados
        salvar_dados_seguros("cofre_notas", dados_salvos)
        self.limpar_selecao()
        return True

    def excluir_bloco(self, bloco_id):
        dados_salvos = self.obter_dados()
        blocos_dados = dados_salvos.get("notas", [])
        
        blocos_filtrados = [b for b in blocos_dados if b["id"] != bloco_id]
        dados_salvos["notas"] = blocos_filtrados
        salvar_dados_seguros("cofre_notas", dados_salvos)
        
        if self.bloco_selecionado["id"] == bloco_id:
            self.limpar_selecao()

    def mover_bloco(self, index, direcao):
        dados_salvos = self.obter_dados()
        blocos_dados = dados_salvos.get("notas", [])
        
        if direcao == "esquerda" and index > 0:
            blocos_dados[index], blocos_dados[index - 1] = blocos_dados[index - 1], blocos_dados[index]
        elif direcao == "direita" and index < len(blocos_dados) - 1:
            blocos_dados[index], blocos_dados[index + 1] = blocos_dados[index + 1], blocos_dados[index]
            
        dados_salvos["notas"] = blocos_dados
        salvar_dados_seguros("cofre_notas", dados_salvos)

    def selecionar_bloco(self, bloco):
        self.bloco_selecionado["id"] = bloco["id"]

    def limpar_selecao(self):
        self.bloco_selecionado["id"] = None

    def obter_cor_texto(self, cor_hex):
        if not cor_hex or cor_hex == "transparent":
            return "#FFFFFF"
        hex_limpo = cor_hex.lstrip('#')
        if len(hex_limpo) == 3:
            hex_limpo = "".join([c*2 for c in hex_limpo])
        try:
            r = int(hex_limpo[0:2], 16)
            g = int(hex_limpo[2:4], 16)
            b = int(hex_limpo[4:6], 16)
            luminancia = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return "#FFFFFF" if luminancia < 0.5 else "#0B0B0C"
        except ValueError:
            return "#FFFFFF"