import flet as ft #type: ignore

# Lista temporária na memória para guardar os eventos enquanto o app está aberto
EVENTOS_TEMPORARIOS = []

def eventos_views(page: ft.Page):
    """Gera a interface visual da tela de Eventos no estilo Premium Minimalista Ultra-Responsivo."""
    
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        # Preto Absoluto
    BG_CARD = "#161618"             # Grafite Escuro
    PRATA_BORDA = "#2D2D30"         # Prata Escuro para linhas discretas
    PRATA_TEXTO = "#A1A1AA"         # Prata para labels secundárias
    BRANCO_PURO = "#FFFFFF"         # Branco Puro para títulos e destaque

    # --- CAMPOS DE ENTRADA PREMIUM (Largura Máxima Adaptável) ---
    txt_titulo = ft.TextField(
        label="Título do Evento", 
        max_length=40,
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        text_size=14,
        border_radius=8
    )
    
    txt_data = ft.TextField(
        label="Data (DD/MM/AAAA)", 
        hint_text="Ex: 15/06/2026",
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        hint_style=ft.TextStyle(color="#4B5563"),
        bgcolor="#141416",
        text_size=14,
        border_radius=8
    )

    txt_descricao = ft.TextField(
        label="Descrição / Detalhes do Compromisso", 
        multiline=True,
        min_lines=3,
        max_lines=4,
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        text_size=14,
        border_radius=8
    )
    
    # Lista visual usando animações nativas de transição de estado
    lista_eventos_ui = ft.Column(spacing=10, animate_opacity=250)

    def deletar_evento(ev_dados):
        """Remove o evento da lista com efeito visual rápido."""
        EVENTOS_TEMPORARIOS.remove(ev_dados)
        atualizar_lista_na_tela()
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Compromisso removido do registro.", color=BRANCO_PURO), 
            bgcolor="#252529"
        )
        page.snack_bar.open = True
        page.update()

    def atualizar_lista_na_tela():
        """Limpa a tela e redesenha a lista aplicando curvas de animação EASE."""
        lista_eventos_ui.controls.clear()
        
        if not EVENTOS_TEMPORARIOS:
            lista_eventos_ui.controls.append(
                ft.Container(
                    content=ft.Text("Nenhum evento agendado no registro.", color=PRATA_TEXTO, size=13, italic=True),
                    alignment=ft.alignment.center,
                    padding=25
                )
            )
        else:
            for ev in EVENTOS_TEMPORARIOS:
                # Estrutura do card com suporte a interações premium
                card_evento = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Row([
                                ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color=BRANCO_PURO, size=16),
                                ft.Text(ev["titulo"], weight=ft.FontWeight.W_600, color=BRANCO_PURO, size=13)
                            ], spacing=8, expand=True),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE_ROUNDED,
                                icon_color=PRATA_TEXTO,
                                icon_size=16,
                                padding=4,
                                tooltip="Deletar Registro",
                                on_click=lambda e, dados=ev: deletar_evento(dados)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Divider(color=PRATA_BORDA, height=2),
                        
                        ft.Text(
                            ev["descricao"] if ev["descricao"] else "Sem especificações adicionais.", 
                            color=PRATA_TEXTO, 
                            size=12
                        ),
                        ft.Container(
                            content=ft.Text(f"Agendado para: {ev['data']}", size=11, color=BRANCO_PURO, weight=ft.FontWeight.W_500),
                            alignment=ft.alignment.bottom_right
                        )
                    ], spacing=6),
                    bgcolor=BG_CARD,
                    padding=14,
                    border_radius=10,
                    border=ft.border.all(1, PRATA_BORDA),
                    animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                )
                lista_eventos_ui.controls.append(card_evento)
                
        if lista_eventos_ui.page:
            lista_eventos_ui.update()

    def cadastrar_evento_click(e):
        """Valida, limpa os campos e injeta o evento com segurança contra travamentos."""
        if not txt_titulo.value or not txt_data.value:
            page.snack_bar = ft.SnackBar(ft.Text("Erro operacional: Título e Data são obrigatórios."), bgcolor="#451A03")
            page.snack_bar.open = True
            page.update()
            return
        
        # Insere no topo da lista para destacar o último adicionado
        EVENTOS_TEMPORARIOS.insert(0, {
            "titulo": txt_titulo.value,
            "data": txt_data.value,
            "descricao": txt_descricao.value
        })
        
        txt_titulo.value = ""
        txt_descricao.value = ""
        txt_data.value = ""
        
        # Desfoca os campos para ocultar o teclado mobile automaticamente após salvar
        txt_titulo.focus()
        txt_titulo.blur()
        
        atualizar_lista_na_tela()
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Novo evento encriptado com sucesso.", color=BRANCO_PURO), 
            bgcolor=BG_CARD
        )
        page.snack_bar.open = True
        page.update()

    # Renderiza os dados iniciais salvos em memória
    atualizar_lista_na_tela()

    # --- FOLHA DE ESTILO CONTAINER RESPONSIVO CORRIGIDA (Sem max_width) ---
    conteudo_responsivo = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Text("REGISTRAR COMPROMISSO", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                ft.Container(height=8),
                txt_titulo,
                ft.Container(height=6),
                txt_data,
                ft.Container(height=6),
                txt_descricao,
                ft.Container(height=10),
                
                # Botão Principal Interativo (Estilo Sólido Branco)
                ft.Container(
                    content=ft.Text("Adicionar Evento", weight=ft.FontWeight.W_600, color=BG_PRINCIPAL, size=13),
                    alignment=ft.alignment.center,
                    height=46,
                    bgcolor=BRANCO_PURO,
                    border_radius=8,
                    on_click=cadastrar_evento_click,
                ),
                
                ft.Container(height=16),
                ft.Divider(color=PRATA_BORDA, height=1),
                ft.Container(height=16),
                
                ft.Text("CRONOGRAMA AGENDADO", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                ft.Container(height=8),
                lista_eventos_ui,
                
                # Padding tático inferior para que nenhuma barra de navegação mobile corte o conteúdo
                ft.Container(height=50)
            ],
            spacing=0,
        ),
        padding=16,
        expand=True,
        width=420, # Define a largura ideal estável para mobile e PC sem estourar
        alignment=ft.alignment.top_center
    )

    return ft.View(
        route="/eventos",
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text("CENTRAL DE EVENTOS", weight=ft.FontWeight.W_700, size=13, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL,
                center_title=True,
                elevation=0,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, 
                    icon_color=PRATA_TEXTO, 
                    icon_size=15, 
                    on_click=lambda _: page.go("/home")
                )
            ),
            ft.Divider(color=PRATA_BORDA, height=1),
            # Alinha o conteúdo responsivo centralizado na tela inteira
            ft.Row(
                controls=[conteudo_responsivo],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ],
        padding=0
    )