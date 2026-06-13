import flet as ft # type: ignore

def cofre_views(page: ft.Page):
    
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        # Preto Absoluto
    BG_CARD = "#161618"             # Grafite Escuro
    PRATA_BORDA = "#2D2D30"         # Prata Escuro para linhas discretas
    PRATA_TEXTO = "#A1A1AA"         # Prata para labels secundárias
    BRANCO_PURO = "#FFFFFF"         # Branco Puro para títulos e destaque
    VERMELHO_DESTRUTIVO = "#EF4444" # Vermelho para exclusão

    # --- ESTADO TEMPORÁRIO DOS BLOCOS ---
    blocos_dados = [
        {"id": 1, "titulo": "Exemplo", "texto": "Exemplo ✈️", "cor": "#1C1C1E", "emoji": "✈️"},
    ]
    
    bloco_selecionado = {"id": None}

    def obter_cor_texto(cor_hex):
        if not cor_hex or cor_hex == "transparent":
            return BRANCO_PURO
        hex_limpo = cor_hex.lstrip('#')
        if len(hex_limpo) == 3:
            hex_limpo = "".join([c*2 for c in hex_limpo])
        try:
            r = int(hex_limpo[0:2], 16)
            g = int(hex_limpo[2:4], 16)
            b = int(hex_limpo[4:6], 16)
            luminancia = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return BRANCO_PURO if luminancia < 0.5 else BG_PRINCIPAL
        except ValueError:
            return BRANCO_PURO

    # --- CONTROLADORES INPUT PREMIUM ---
    txt_titulo = ft.TextField(
        label="Título do Bloco", 
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        text_size=14,
        border_radius=8,
    )
    
    txt_conteudo = ft.TextField(
        label="Escreva sua nota secreta aqui...",
        multiline=True,
        min_lines=4,
        max_lines=6,
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        text_size=14,
        border_radius=8,
    )
    
    cor_selecionada = ft.Text("#1C1C1E", visible=False)

    def voltar_home(e):
        page.go("/home")

    def selecionar_cor(e):
        cor_hex = e.control.data
        cor_selecionada.value = cor_hex
        txt_conteudo.bgcolor = cor_hex
        txt_conteudo.color = obter_cor_texto(cor_hex)
        
        # Feedback interativo: atualiza as bordas dos círculos de cor
        for item in linha_cores.controls:
            item.border = ft.border.all(2, BRANCO_PURO if item.data == cor_hex else PRATA_BORDA)
            
        page.update()

    def adicionar_emoji(e):
        txt_conteudo.value = (txt_conteudo.value or "") + e.control.data
        txt_conteudo.update()

    def salvar_bloco(e):
        if not txt_titulo.value:
            return
        
        if bloco_selecionado["id"] is None:
            novo_id = max([b["id"] for b in blocos_dados]) + 1 if blocos_dados else 1
            blocos_dados.append({
                "id": novo_id,
                "titulo": txt_titulo.value,
                "texto": txt_conteudo.value,
                "cor": cor_selecionada.value,
                "emoji": "📝"
            })
        else:
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
        
        # Feedback visual de seleção na paleta
        for item in linha_cores.controls:
            item.border = ft.border.all(2, BRANCO_PURO if item.data == bloco["cor"] else PRATA_BORDA)
            
        page.update()

    def excluir_bloco(bloco_id):
        nonlocal blocos_dados
        blocos_dados = [b for b in blocos_dados if b["id"] != bloco_id]
        if bloco_selecionado["id"] == bloco_id:
            limpar_formulario()
        renderizar_blocos()

    def mover_bloco(index, direcao):
        if direcao == "esquerda" and index > 0:
            blocos_dados[index], blocos_dados[index - 1] = blocos_dados[index - 1], blocos_dados[index]
        elif direcao == "direita" and index < len(blocos_dados) - 1:
            blocos_dados[index], blocos_dados[index + 1] = blocos_dados[index + 1], blocos_dados[index]
        renderizar_blocos()

    def limpar_formulario():
        bloco_selecionado["id"] = None
        txt_titulo.value = ""
        txt_conteudo.value = ""
        txt_conteudo.bgcolor = "#141416"
        txt_conteudo.color = BRANCO_PURO
        cor_selecionada.value = "#1C1C1E"
        for item in linha_cores.controls:
            item.border = ft.border.all(1, PRATA_BORDA)
        page.update()

    # --- COMPONENTES VISUAIS PREMIUM ---
    linha_blocos = ft.Row(wrap=False, scroll=ft.ScrollMode.ALWAYS, spacing=12)

    def renderizar_blocos():
        linha_blocos.controls.clear()
        
        for i, b in enumerate(blocos_dados):
            cor_do_texto = obter_cor_texto(b["cor"])
            cor_setas = PRATA_TEXTO if cor_do_texto == BRANCO_PURO else BG_PRINCIPAL
            
            linha_blocos.controls.append(
                ft.Container(
                    content=ft.Column([
                        # Cabeçalho do Card
                        ft.Row([
                            ft.Row([
                                ft.Text(b["emoji"], size=13), 
                                ft.Text(b["titulo"], weight=ft.FontWeight.W_600, max_lines=1, color=cor_do_texto, size=11)
                            ], expand=True, spacing=4),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED, 
                                icon_color=VERMELHO_DESTRUTIVO, 
                                icon_size=15, 
                                padding=2,
                                on_click=lambda e, b_id=b["id"]: excluir_bloco(b_id)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
                        
                        # Corpo do Texto Interativo
                        ft.GestureDetector(
                            content=ft.Container(
                                content=ft.Text(b["texto"], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, size=11, color=cor_do_texto),
                                height=38,
                                alignment=ft.alignment.top_left
                            ),
                            on_tap=lambda e, bloco=b: carregar_bloco(bloco)
                        ),
                        
                        # Rodapé com Navegadores
                        ft.Row([
                            ft.Row([
                                ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED, icon_color=cor_setas, icon_size=16, disabled=(i == 0), padding=2, on_click=lambda e, idx=i: mover_bloco(idx, "esquerda")),
                                ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED, icon_color=cor_setas, icon_size=16, disabled=(i == len(blocos_dados) - 1), padding=2, on_click=lambda e, idx=i: mover_bloco(idx, "direita")),
                            ], spacing=0),
                            ft.IconButton(ft.Icons.OPEN_IN_NEW_ROUNDED, icon_color=cor_setas, icon_size=13, on_click=lambda e, bloco=b: carregar_bloco(bloco))
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=2, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    width=145,
                    height=125,
                    bgcolor=b["cor"],
                    border_radius=12,
                    padding=8,
                    border=ft.border.all(1, PRATA_BORDA),
                    animate=ft.Animation(250, ft.AnimationCurve.DECELERATE), # Animação de entrada suave
                )
            )
        if linha_blocos.page:
            linha_blocos.update()

    # Seletor de Cores - Escala Corporativa Monocromática com feedback tátil
    cores_disponiveis = ["#121214", "#1C1C1E", "#252529", "#2C2C30", "#3A3A3C", "#48484A", "#A1A1AA", "#FFFFFF"]
    linha_cores = ft.Row([
        ft.Container(
            width=28, height=28, bgcolor=cor, border_radius=14, data=cor, on_click=selecionar_cor,
            border=ft.border.all(1, PRATA_BORDA),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
        ) for cor in cores_disponiveis
    ], wrap=True, spacing=8)

    # Emojis estruturados em containers consistentes para toque Mobile
    emojis = ["🔐", "💼", "💡", "🎯", "📝", "🚀", "💎", "🔋"]
    linha_emojis = ft.Row([
        ft.Container(
            content=ft.Text(emj, size=15),
            alignment=ft.alignment.center,
            width=38,
            height=38,
            bgcolor="#1C1C1E",
            border_radius=8,
            border=ft.border.all(1, PRATA_BORDA),
            data=emj,
            on_click=adicionar_emoji
        ) for emj in emojis
    ], scroll=ft.ScrollMode.ALWAYS, spacing=8)

    renderizar_blocos()

    # --- ENGENHARIA DE LAYOUT (ANTI-BUG MOBILE) ---
    return ft.View(
        route="/cofre",
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text("Notas", weight=ft.FontWeight.W_700, size=13, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL,
                center_title=True,
                elevation=0,
                leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color=PRATA_TEXTO, icon_size=15, on_click=voltar_home)
            ),
            ft.Divider(color=PRATA_BORDA, height=1),
            
            # O uso do Container com ListView impede falhas de layout no Android ao subir o teclado
            ft.Container(
                content=ft.ListView(
                    controls=[
                        # Seção 1
                        ft.Text("CONTEÚDOS ENCRIPTADOS", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                        ft.Container(height=4),
                        linha_blocos,
                        
                        ft.Container(height=12),
                        ft.Divider(color=PRATA_BORDA, height=1),
                        ft.Container(height=12),
                        
                        # Seção 2: Inputs com espaçamento confortável para touch
                        ft.Text("COMPILADOR DE ENTRADA", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                        ft.Container(height=6),
                        txt_titulo,
                        ft.Container(height=6),
                        txt_conteudo,
                        
                        ft.Container(height=10),
                        ft.Text("Injetar Elemento Rápido", size=10, color=PRATA_TEXTO, weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        linha_emojis,
                        
                        ft.Container(height=10),
                        ft.Text("Identidade do Contêiner (Offset)", size=10, color=PRATA_TEXTO, weight=ft.FontWeight.W_600),
                        ft.Container(height=4),
                        linha_cores,
                        
                        ft.Container(height=20),
                        
                        # Ações com botões grandes e fáceis de clicar no Mobile
                        ft.Row([
                            ft.TextButton(
                                text="Limpar Painel", 
                                icon=ft.Icons.REFRESH_ROUNDED, 
                                style=ft.ButtonStyle(color=PRATA_TEXTO),
                                on_click=lambda e: limpar_formulario()
                            ),
                            ft.Container(
                                content=ft.Text("Salvar Nota", weight=ft.FontWeight.W_600, color=BG_PRINCIPAL, size=13),
                                alignment=ft.alignment.center,
                                height=44,
                                width=140,
                                bgcolor=BRANCO_PURO,
                                border_radius=8,
                                on_click=salvar_bloco,
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        # Margem de segurança extra para o scroll do teclado no Android
                        ft.Container(height=40)
                    ],
                ),
                padding=14,
                expand=True
            )
        ],
        padding=0
    )