import flet as ft #type: ignore
import asyncio

def login_view(page: ft.Page):
    
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        
    BG_CARD = "#161618"             
    PRATA_BORDA = "#2D2D30"         
    PRATA_TEXTO = "#A1A1AA"         
    BRANCO_PURO = "#FFFFFF"         
    VERMELHO_ERRO = "#EF4444"       

    txt_senha = ft.TextField(
        label="Digite sua senha",
        password=True,
        can_reveal_password=True,
        width=280,                  
        text_align=ft.TextAlign.CENTER,
        color=BRANCO_PURO,
        cursor_color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        bgcolor="#1C1C1E",
    )
    
    lbl_erro = ft.Text(value="", color=VERMELHO_ERRO, size=13, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)
    
    def btn_teclado_virtual(e):
        valor_botao = e.control.data
        if valor_botao == "limpar":
            txt_senha.value = "" 
        elif valor_botao == "apagar":
            txt_senha.value = txt_senha.value[:-1] 
        else:
            if len(txt_senha.value) < 6:
                txt_senha.value += valor_botao
        page.update()
        
    async def verificar_senha(e):
        senha_correta = "" 
        
        if txt_senha.value == senha_correta:
            lbl_erro.value = ""
            
            conteudo_login.content = ft.Column(
                controls=[
                    ft.ProgressRing(width=40, height=40, stroke_width=3, color=BRANCO_PURO),
                    ft.Container(height=15),
                    ft.Text("Autenticando ambiente...", color=PRATA_TEXTO, size=14, weight=ft.FontWeight.W_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            page.update()
            
            await asyncio.sleep(1.5)
            page.go("/home") 
        else:
            lbl_erro.value = "Senha incorreta! Tente novamente."
            page.update()

    def alternar_teclado(e):
        container_teclado.visible = not container_teclado.visible
        btn_mostrar_teclado.text = "Ocultar Teclado Virtual" if container_teclado.visible else "Usar Teclado Virtual"
        page.update()

    botoes = []
    for i in range(1, 10):
        botoes.append(
            ft.Container(
                content=ft.Text(str(i), size=18, weight=ft.FontWeight.BOLD, color=BRANCO_PURO),
                alignment=ft.alignment.center,
                shape=ft.BoxShape.CIRCLE,
                border=ft.border.all(1, PRATA_BORDA),
                bgcolor="#1C1C1E",
                data=str(i),
                on_click=btn_teclado_virtual,
                width=50, # Reduzido ligeiramente para Androids menores
                height=50,
            )
        )
    
    botoes.append(
        ft.Container(
            content=ft.Icon(ft.Icons.CLEAR, color=PRATA_TEXTO, size=20),
            alignment=ft.alignment.center,
            shape=ft.BoxShape.CIRCLE,
            data="limpar",
            on_click=btn_teclado_virtual,
            width=50,
            height=50,
        )
    )
    
    botoes.append(
        ft.Container(
            content=ft.Text("0", size=18, weight=ft.FontWeight.BOLD, color=BRANCO_PURO),
            alignment=ft.alignment.center,
            shape=ft.BoxShape.CIRCLE,
            border=ft.border.all(1, PRATA_BORDA),
            bgcolor="#1C1C1E",
            data="0",
            on_click=btn_teclado_virtual,
            width=50,
            height=50,
        )
    )
    
    botoes.append(
        ft.Container(
            content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED, color=PRATA_TEXTO, size=18),
            alignment=ft.alignment.center,
            shape=ft.BoxShape.CIRCLE,
            data="apagar",
            on_click=btn_teclado_virtual,
            width=50,
            height=50,
        )
    )

    grid_teclado = ft.GridView(
        controls=botoes,
        runs_count=3,
        max_extent=55,  
        child_aspect_ratio=1.0,  
        spacing=10,
        run_spacing=10,
        width=190, # Mais estreito para evitar overflow lateral
        height=250,
    )

    container_teclado = ft.Container(
        content=grid_teclado,
        visible=False, 
        margin=ft.margin.only(top=5, bottom=5)
    )

    btn_mostrar_teclado = ft.TextButton(
        text="Usar Teclado Virtual",
        icon=ft.Icons.KEYBOARD_OUTLINED,
        style=ft.ButtonStyle(color=PRATA_TEXTO),
        on_click=alternar_teclado
    )

    # --- CORREÇÃO DO BUG (Layout com Scroll Interno) ---
    # Usar ft.ListView garante que o Android consiga rolar os elementos se o teclado físico/nativo subir
    layout_scrollavel = ft.ListView(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.LOCK_PERSON_OUTLINED, size=36, color=BRANCO_PURO),
                            alignment=ft.alignment.center,
                            width=70,
                            height=70,
                            border_radius=35,
                            border=ft.border.all(1, PRATA_BORDA),
                            bgcolor="#1C1C1E"
                        ),
                        ft.Container(height=5),
                        ft.Text("Acesso Restrito", size=22, weight=ft.FontWeight.W_700, color=BRANCO_PURO),
                        ft.Text("Insira suas credenciais de segurança", size=13, color=PRATA_TEXTO, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=10),
                        txt_senha,
                        lbl_erro,
                        btn_mostrar_teclado, 
                        container_teclado,   
                        ft.Container(height=5),
                        
                        ft.Container(
                            content=ft.Text("Entrar", weight=ft.FontWeight.W_600, color=BG_PRINCIPAL, size=14),
                            alignment=ft.alignment.center,
                            height=46,
                            width=280,
                            bgcolor=BRANCO_PURO,
                            border_radius=8,
                            on_click=verificar_senha,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=20, bottom=40) # Margem extra no fundo para não cobrir o botão entrar
            )
        ],
        expand=True,
    )

    conteudo_login = ft.AnimatedSwitcher(
        content=layout_scrollavel,
        transition=ft.AnimatedSwitcherTransition.SCALE,  
        duration=300,  
    )

    return ft.View(
        route="/login",
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text("AUTENTICAÇÃO", weight=ft.FontWeight.W_700, size=13, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL,
                center_title=True,
                automatically_imply_leading=False,
                elevation=0,
            ),
            ft.Divider(color=PRATA_BORDA, height=1),
            ft.Container(
                content=conteudo_login,
                alignment=ft.alignment.center,  
                expand=True,
                padding=10
            )
        ],
        padding=0
    )