import flet as ft  # type: ignore

def home_view(page: ft.Page):
    
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        
    BG_CARD = "#161618"             
    PRATA_BORDA = "#2D2D30"         
    PRATA_TEXTO = "#A1A1AA"         
    BRANCO_PURO = "#FFFFFF"         
    CORTESIA_VERDE = "#34D399"      

    # --- FUNÇÕES INTERATIVAS & FEEDBACKS ---
    def fazer_login(e):
        page.go("/login")
        
    def mudar_aba(e):
        idx = e.control.selected_index
        if idx == 0:
            page.go("/home")
        elif idx == 1:
            page.go("/notas")  
        elif idx == 2:
            page.go("/finance")
        elif idx == 3:
            page.go("/eventos")
        elif idx == 4:
            page.go("/settings")

    def abrir_status_sistema(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Verificando integridade dos módulos...", color=PRATA_TEXTO, size=12),
            bgcolor="#1A1A1E",
            duration=1500
        )
        page.snack_bar.open = True
        page.update()
        
        status_sheet.open = True
        status_sheet.update()

    def status_card_click(e):
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Módulo operando em conformidade.", color=CORTESIA_VERDE, size=12),
            bgcolor="#161618",
            duration=1000
        )
        page.snack_bar.open = True
        page.update()

    # --- STATUS SHEET (BOTTOM SHEET MOBILE) ---
    status_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=ft.padding.only(top=10, left=20, right=20, bottom=24),
            bgcolor=BG_CARD,
            border=ft.border.only(top=ft.BorderSide(1, PRATA_BORDA)),
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            content=ft.Column(
                controls=[
                    ft.Row([ft.Container(width=32, height=4, bgcolor=PRATA_BORDA, border_radius=2)], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=10),
                    ft.Text("STATUS DO SISTEMA", size=11, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                    ft.Container(height=2),
                    ft.Container(
                        content=ft.Row([
                            ft.Row([ft.Icon(ft.Icons.SHIELD_OUTLINED, color=BRANCO_PURO, size=16), ft.Text("Banco de Dados", size=13, color=BRANCO_PURO, weight=ft.FontWeight.W_500)]),
                            ft.Text("ONLINE", size=10, color=CORTESIA_VERDE, weight=ft.FontWeight.W_700)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=12, border=ft.border.all(1, PRATA_BORDA), border_radius=10, bgcolor="#1F1F23"
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Row([ft.Icon(ft.Icons.KEY_OUTLINED, color=BRANCO_PURO, size=16), ft.Text("Criptografia", size=13, color=BRANCO_PURO, weight=ft.FontWeight.W_500)]),
                            ft.Text("VERIFICADA", size=10, color=CORTESIA_VERDE, weight=ft.FontWeight.W_700)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=12, border=ft.border.all(1, PRATA_BORDA), border_radius=10, bgcolor="#1F1F23"
                    ),
                    ft.Container(height=5),
                    ft.Divider(color=PRATA_BORDA, height=1),
                    ft.Row([
                        ft.Text("MY LIFE PRIME", size=10, color=PRATA_TEXTO, weight=ft.FontWeight.W_600),
                        ft.Text("v0.1", size=10, color=PRATA_TEXTO)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                spacing=8,
                tight=True
            )
        )
    )
    
    page.overlay.append(status_sheet)

    # --- BARRA DE NAVEGAÇÃO INFERIOR ---
    menu_inferior = ft.NavigationBar(
        selected_index=0,
        bgcolor=BG_CARD,
        elevation=0,
        height=60, 
        indicator_color=PRATA_BORDA,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Painel"),
            ft.NavigationBarDestination(icon=ft.Icons.LOCK_OUTLINED, selected_icon=ft.Icons.LOCK, label="Notas"),
            ft.NavigationBarDestination(icon=ft.Icons.PASSWORD_OUTLINED, selected_icon=ft.Icons.PASSWORD_ROUNDED, label="Finanças"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY_OUTLINED, selected_icon=ft.Icons.HISTORY_ROUNDED, label="Eventos"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Ajustes"),
        ],
        on_change=mudar_aba,
    )

    # --- COMPONENTES DO CARD CENTRAL ---
    icone_central = ft.Icon(ft.Icons.LOCK_OUTLINED, size=32, color=BRANCO_PURO)
    texto_titulo = ft.Text("Ambiente Protegido", size=20, weight=ft.FontWeight.W_700, color=BRANCO_PURO)
    texto_sub = ft.Text("Sua conexão está criptografada de ponta a ponta.", color=PRATA_TEXTO, text_align=ft.TextAlign.CENTER, size=12)

    # --- CARD DE STATUS INTERNOS ---
    def criar_item_status(icone, titulo, valor):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icone, color=PRATA_TEXTO, size=14),
                    ft.Column(
                        controls=[
                            ft.Text(titulo, size=9, color=PRATA_TEXTO, weight=ft.FontWeight.W_400),
                            ft.Text(valor, size=11, color=BRANCO_PURO, weight=ft.FontWeight.W_600),
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                spacing=6,
            ),
            bgcolor="#161618",
            padding=ft.padding.symmetric(vertical=8, horizontal=10),
            border_radius=8,
            border=ft.border.all(1, "#27272A"),
            expand=True,
            on_click=status_card_click
        )

    grid_status = ft.Column(
        controls=[
            ft.Row([
                criar_item_status(ft.Icons.SHIELD_OUTLINED, "Status", "Ativo"),
                criar_item_status(ft.Icons.KEY_ROUNDED, "Chave", "AES-256"),
            ], spacing=8),
            ft.Row([
                criar_item_status(ft.Icons.SPEED_ROUNDED, "Latência", "14ms"),
                criar_item_status(ft.Icons.TIMER_OUTLINED, "Sessão", "00:45m"),
            ], spacing=8)
        ],
        spacing=8,
    )

    # --- CARD PRINCIPAL (SUPER COMPACTO E SEGURO) ---
    card_boas_vindas = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(width=6, height=6, bgcolor=ft.Colors.GREEN_400, border_radius=3),
                            ft.Text("SISTEMA OPERACIONAL", size=9, color=ft.Colors.GREEN_400, weight=ft.FontWeight.W_700)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    margin=ft.margin.only(bottom=4)
                ),
                ft.Container(
                    content=icone_central,
                    alignment=ft.alignment.center,
                    width=60,
                    height=60,
                    border_radius=30,
                    border=ft.border.all(1.2, PRATA_BORDA),
                    bgcolor="#1C1C1E"
                ),
                ft.Container(height=4),
                texto_titulo,
                ft.Container(height=1),
                texto_sub,
                ft.Container(height=10),
                
                ft.Divider(color="#27272A", height=1),
                ft.Container(height=6),
                
                grid_status,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=BG_CARD,
        padding=ft.padding.all(16), 
        border_radius=16,
        border=ft.border.all(1, "#27272A"), 
        shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)),
        margin=10, 
        width=310, 
    )

    # --- CONTEÚDO CENTRALIZADO ---
    conteudo_animado = ft.AnimatedSwitcher(
        content=card_boas_vindas,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=400,
        reverse_duration=200,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_BACK
    )

    conteudo_central = ft.Container(
        content=ft.Column(
            controls=[conteudo_animado],
            alignment=ft.MainAxisAlignment.CENTER,       
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        ),
        expand=True,
        bgcolor=BG_PRINCIPAL,
        alignment=ft.alignment.center 
    )

    # --- RETORNO DA VIEW (BOTÃO SAIR NA APPBAR) ---
    return ft.View(
        route="/home",
        navigation_bar=menu_inferior,
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                # [MODIFICADO]: Botão de Sair adicionado nativamente na esquerda (leading)
                leading=ft.IconButton(
                    icon=ft.Icons.LOGOUT_ROUNDED,
                    icon_color=ft.Colors.RED_400,
                    icon_size=20,
                    tooltip="Encerrar Sessão",
                    on_click=fazer_login
                ),
                title=ft.Text("ÁREA SEGURA", weight=ft.FontWeight.W_800, size=12, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL,
                center_title=True,
                automatically_imply_leading=False,
                elevation=0,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINED, 
                        icon_color=PRATA_TEXTO,
                        icon_size=18,
                        tooltip="Status",
                        on_click=abrir_status_sistema
                    ),
                    ft.Container(width=6)
                ]
            ),
            ft.Divider(color="#1C1C1E", height=1),
            conteudo_central
        ],
        padding=0
    )