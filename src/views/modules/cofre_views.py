import flet as ft # type: ignore

def cofre_views(page: ft.Page):
    
    # --- ESTADO TEMPORÁRIO (Simulando um banco de dados) ---
    blocos_dados = [
        {"id": 1, "titulo": "Ideias de Viagem", "texto": "Gramado em Gramado ✈️", "cor": "#FFD1DC", "emoji": "✈️"},
        {"id": 2, "titulo": "Lista de Compras", "texto": "Comprar chocolates 🍫", "cor": "#E8F0FE", "emoji": "🛒"},
    ]
    
    bloco_selecionado = {"id": None}

    # --- FUNÇÃO UTILITÁRIA PARA CONTRASTE DE COR ---
    def obter_cor_texto(cor_hex):
        if not cor_hex or cor_hex == "transparent":
            return "#000000"
        
        hex_limpo = cor_hex.lstrip('#')
        if len(hex_limpo) == 3:
            hex_limpo = "".join([c*2 for c in hex_limpo])
            
        try:
            r = int(hex_limpo[0:2], 16)
            g = int(hex_limpo[2:4], 16)
            b = int(hex_limpo[4:6], 16)
            luminancia = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return "#FFFFFF" if luminancia < 0.5 else "#000000"
        except ValueError:
            return "#000000"

    # --- CONTROLADORES DOS CAMPOS DE TEXTO ---
    txt_titulo = ft.TextField(label="Título do Bloco", border_color="#6200EE")
    txt_conteudo = ft.TextField(
        label="Escreva sua nota aqui...",
        multiline=True,
        min_lines=5,
        max_lines=10,
    )
    
    cor_selecionada = ft.Text("#FFFFFF", visible=False)

    # --- FUNÇÕES DE NAVEGAÇÃO E AÇÃO ---
    def voltar_home(e):
        page.go("/home")

    def selecionar_cor(e):
        cor_hex = e.control.data
        cor_selecionada.value = cor_hex
        txt_conteudo.bgcolor = cor_hex
        txt_conteudo.color = obter_cor_texto(cor_hex)
        if txt_conteudo.page:
            txt_conteudo.update()

    def adicionar_emoji(e):
        txt_conteudo.value = (txt_conteudo.value or "") + e.control.data
        if txt_conteudo.page:
            txt_conteudo.update()

    def salvar_bloco(e):
        if not txt_titulo.value:
            return
        
        if bloco_selecionado["id"] is None:
            # Criar novo bloco
            novo_id = max([b["id"] for b in blocos_dados]) + 1 if blocos_dados else 1
            blocos_dados.append({
                "id": novo_id,
                "titulo": txt_titulo.value,
                "texto": txt_conteudo.value,
                "cor": cor_selecionada.value,
                "emoji": "📝"
            })
        else:
            # Editar bloco existente
            for b in blocos_dados:
                if b["id"] == bloco_selecionado["id"]:
                    b["titulo"] = txt_titulo.value
                    b["texto"] = txt_conteudo.value
                    b["cor"] = cor_selecionada.value
        
        limpar_formulario()
        renderizar_blocos()

    def carregar_bloco(bloco):
        bloco_selecionado["id"] = bloco["id"]
        txt_titulo.value = bloco["titulo"]
        txt_conteudo.value = bloco["texto"]
        txt_conteudo.bgcolor = bloco["cor"]
        txt_conteudo.color = obter_cor_texto(bloco["cor"])
        cor_selecionada.value = bloco["cor"]
        if page:
            page.update()

    def excluir_bloco(bloco_id):
        # Remove o bloco da lista pelo ID
        nonlocal blocos_dados
        blocos_dados = [b for b in blocos_dados if b["id"] != bloco_id]
        if bloco_selecionado["id"] == bloco_id:
            limpar_formulario()
        renderizar_blocos()

    def mover_bloco(index, direcao):
        # Altera a posição do bloco na lista (0 para esquerda, 1 para direita)
        if direcao == "esquerda" and index > 0:
            blocos_dados[index], blocos_dados[index - 1] = blocos_dados[index - 1], blocos_dados[index]
        elif direcao == "direita" and index < len(blocos_dados) - 1:
            blocos_dados[index], blocos_dados[index + 1] = blocos_dados[index + 1], blocos_dados[index]
        renderizar_blocos()

    def limpar_formulario():
        bloco_selecionado["id"] = None
        txt_titulo.value = ""
        txt_conteudo.value = ""
        txt_conteudo.bgcolor = None
        txt_conteudo.color = None
        cor_selecionada.value = "#FFFFFF"
        if page:
            page.update()

    # --- COMPONENTES VISUAIS (WIDGETS) ---
    linha_blocos = ft.Row(wrap=False, scroll=ft.ScrollMode.ALWAYS, spacing=15)

    def renderizar_blocos():
        linha_blocos.controls.clear()
        
        for i, b in enumerate(blocos_dados):
            cor_do_texto = obter_cor_texto(b["cor"])
            
            linha_blocos.controls.append(
                ft.Container(
                    content=ft.Column([
                        # Topo do card: Emoji, Título e botão de Deletar
                        ft.Row([
                            ft.Row([ft.Text(b["emoji"], size=16), ft.Text(b["titulo"], weight="bold", max_lines=1, color=cor_do_texto, size=13)], expand=True, spacing=5),
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red500", icon_size=16, tooltip="Excluir nota", on_click=lambda e, b_id=b["id"]: excluir_bloco(b_id))
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                        
                        # Corpo do texto clicável (para carregar/editar)
                        ft.GestureDetector(
                            content=ft.Container(
                                content=ft.Text(b["texto"], max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, size=12, color=cor_do_texto),
                                height=50,
                                alignment=ft.alignment.top_left
                            ),
                            on_tap=lambda e, bloco=b: carregar_bloco(bloco)
                        ),
                        
                        # Rodapé do Card: Controles para Mover e Editar rápido
                        ft.Row([
                            ft.Row([
                                ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color=cor_do_texto, icon_size=12, disabled=(i == 0), on_click=lambda e, idx=i: mover_bloco(idx, "esquerda")),
                                ft.IconButton(ft.Icons.ARROW_FORWARD_IOS, icon_color=cor_do_texto, icon_size=12, disabled=(i == len(blocos_dados) - 1), on_click=lambda e, idx=i: mover_bloco(idx, "direita")),
                            ], spacing=0),
                            ft.IconButton(ft.Icons.EDIT_NOTE, icon_color=cor_do_texto, icon_size=18, tooltip="Editar no painel", on_click=lambda e, bloco=b: carregar_bloco(bloco))
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=2, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    width=160,
                    height=145,
                    bgcolor=b["cor"],
                    border_radius=12,
                    padding=8,
                    border=ft.border.all(1, "#D3D3D3" if cor_do_texto == "#000000" else "#333333"),
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                )
            )
        if linha_blocos.page:
            linha_blocos.update()

    # Seletor de Cores e Emojis
    cores_disponiveis = ["#FFD1DC", "#E8F0FE", "#D4EDDA", "#FFF3CD", "#E2E3E5", "#FFFFFF", "#1E1E2F", "#000000"]
    linha_cores = ft.Row([
        ft.Container(
            width=30, height=30, bgcolor=cor, border_radius=15, data=cor, on_click=selecionar_cor,
            border=ft.border.all(1, "grey")
        ) for cor in cores_disponiveis
    ])

    emojis = ["❤️", "✨", "🌸", "🍕", "🎈", "🐱", "🚀", "💡"]
    linha_emojis = ft.Row([
        ft.TextButton(text=emj, data=emj, on_click=adicionar_emoji, width=40) for emj in emojis
    ], scroll=ft.ScrollMode.ALWAYS)

    renderizar_blocos()

    # --- LAYOUT PRINCIPAL ---
    return ft.View(
        route="/cofre",
        controls=[
            ft.AppBar(
                title=ft.Text("Meu Cofre de Notas 🔐", weight=ft.FontWeight.W_600),
                bgcolor="surfacevariant",
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=voltar_home)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Seus Blocos de Notas:", size=16, weight=ft.FontWeight.BOLD),
                    linha_blocos,
                    
                    ft.Divider(height=10, color="transparent"),
                    
                    ft.Text("Escrever / Editar Nota:", size=16, weight=ft.FontWeight.BOLD),
                    txt_titulo,
                    
                    ft.Container(
                        content=txt_conteudo,
                        border_radius=8,
                    ),
                    
                    ft.Text("Adicionar Figuras/Emojis rápido:", size=12, color="grey"),
                    linha_emojis,
                    
                    ft.Text("Escolha a cor do bloco:", size=12, color="grey"),
                    linha_cores,
                    
                    ft.Divider(height=10, color="transparent"),
                    
                    ft.Row([
                        ft.ElevatedButton("Novo Bloco", icon=ft.Icons.CLEAR, on_click=lambda e: limpar_formulario()),
                        ft.ElevatedButton("Salvar Nota", icon=ft.Icons.SAVE, bgcolor="#6200EE", color="white", on_click=salvar_bloco),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    
                ], scroll=ft.ScrollMode.ALWAYS),
                padding=20,
                expand=True
            )
        ]
    )