import flet as ft  # type: ignore

def home_view(page: ft.Page):
    
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
            page.go("/configuracoes")

    def abrir_status_sistema(e):
        status_sheet.open = True
        status_sheet.update()

    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        
    BG_CARD = "#161618"             
    PRATA_BORDA = "#2D2D30"         
    PRATA_TEXTO = "#A1A1AA"         
    BRANCO_PURO = "#FFFFFF"         
    CORTESIA_VERDE = "#34D399"      

    # --- STATUS SHEET ---
    status_sheet = ft.BottomSheet(
        content=ft.Container(
            padding=ft.padding.only(top=12, left=24, right=24, bottom=32),
            bgcolor=BG_CARD,
            border=ft.border.only(top=ft.BorderSide(1, PRATA_BORDA)),
            border_radius=ft.border_radius.only(top_left=24, top_right=24),
            content=ft.Column(
                controls=[
                    ft.Row([ft.Container(width=36, height=4, bgcolor=PRATA_BORDA, border_radius=2)], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=15),
                    ft.Text("STATUS DO SISTEMA", size=12, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                    ft.Container(height=5),
                    ft.Container(
                        content=ft.Row([
                            ft.Row([ft.Icon(ft.Icons.SHIELD_OUTLINED, color=BRANCO_PURO, size=18), ft.Text("Banco de Dados", size=14, color=BRANCO_PURO, weight=ft.FontWeight.W_500)]),
                            ft.Text("ONLINE", size=11, color=CORTESIA_VERDE, weight=ft.FontWeight.W_700)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=14, border=ft.border.all(1, PRATA_BORDA), border_radius=12, bgcolor="#1F1F23"
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Row([ft.Icon(ft.Icons.KEY_OUTLINED, color=BRANCO_PURO, size=18), ft.Text("Chave de Criptografia", size=14, color=BRANCO_PURO, weight=ft.FontWeight.W_500)]),
                            ft.Text("VERIFICADA", size=11, color=CORTESIA_VERDE, weight=ft.FontWeight.W_700)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=14, border=ft.border.all(1, PRATA_BORDA), border_radius=12, bgcolor="#1F1F23"
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.Row([ft.Icon(ft.Icons.CLOUD_OFF_OUTLINED, color=PRATA_TEXTO, size=18), ft.Text("Nuvem", size=14, color=PRATA_TEXTO, weight=ft.FontWeight.W_500)]),
                            ft.Text("LOCAL", size=11, color=PRATA_TEXTO, weight=ft.FontWeight.W_700)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=14, border=ft.border.all(1, PRATA_BORDA), border_radius=12, bgcolor="#1F1F23"
                    ),
                    ft.Container(height=10),
                    ft.Divider(color=PRATA_BORDA, height=1),
                    ft.Container(height=5),
                    ft.Row([
                        ft.Text("MY LIFE PRIME", size=11, color=PRATA_TEXTO, weight=ft.FontWeight.W_600),
                        ft.Text("v0.1", size=11, color=PRATA_TEXTO)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ],
                spacing=10,
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

    # --- CARD CENTRAL DE BOAS-VINDAS ---
    icone_central = ft.Icon(ft.Icons.LOCK_OUTLINED, size=64, color=BRANCO_PURO)
    texto_titulo = ft.Text("Bem-vindo", size=28, weight=ft.FontWeight.W_700, color=BRANCO_PURO)
    texto_sub = ft.Text("Seu ambiente seguro está pronto e criptografado.", color=PRATA_TEXTO, text_align=ft.TextAlign.CENTER, size=14)

    conteudo_central = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=icone_central,
                                alignment=ft.alignment.center,
                                width=110,
                                height=110,
                                border_radius=55,
                                border=ft.border.all(1.5, PRATA_BORDA),
                                bgcolor="#1C1C1E"
                            ),
                            ft.Container(height=10),
                            texto_titulo,
                            ft.Container(height=2),
                            texto_sub,
                            ft.Container(height=28),
                            ft.Container(
                                content=ft.Text("Encerrar Sessão", weight=ft.FontWeight.W_600, color=BG_PRINCIPAL, size=14),
                                alignment=ft.alignment.center,
                                height=48,
                                width=180,
                                bgcolor=BRANCO_PURO,
                                border_radius=10,
                                on_click=fazer_login,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=BG_CARD,
                    padding=ft.padding.all(32),
                    border_radius=24,
                    border=ft.border.all(1, PRATA_BORDA),
                    shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
                    margin=20, 
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=BG_PRINCIPAL,
    )

    return ft.View(
        route="/home",
        navigation_bar=menu_inferior,
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text("ÁREA SEGURA", weight=ft.FontWeight.W_700, size=14, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL,
                center_title=True,
                automatically_imply_leading=False,
                elevation=0,
                # O argumento 'bottom' que causava o erro foi removido daqui
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.INFO_OUTLINED, 
                        icon_color=PRATA_TEXTO,
                        tooltip="Status",
                        on_click=abrir_status_sistema
                    ),
                    ft.Container(width=8)
                ]
            ),
            # A linha divisória foi movida para cá, logo após o AppBar
            ft.Divider(color=PRATA_BORDA, height=1),
            conteudo_central
        ],
        padding=0
    )