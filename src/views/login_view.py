import flet as ft # type: ignore
import asyncio
import hashlib

def login_view(page: ft.Page):
    
    page.client_storage.clear()
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        
    BG_CARD = "#161618"             
    PRATA_BORDA = "#2D2D30"         
    PRATA_TEXTO = "#A1A1AA"         
    BRANCO_PURO = "#FFFFFF"         
    VERMELHO_ERRO = "#EF4444"       
    CORTESIA_VERDE = "#34D399"

    # --- VARIÁVEIS DE ESTADO INTERNAS ---
    senha_gravada = None
    primeiro_acesso = True

    # --- COMPONENTES DE INTERFACE ---
    txt_senha = ft.TextField(
        label="Carregando segurança...",
        password=True,
        can_reveal_password=True,
        width=260,
        text_align=ft.TextAlign.CENTER,
        color=BRANCO_PURO,
        cursor_color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO, size=12),
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        bgcolor="#1C1C1E",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=12,
        disabled=True # Começa desabilitado até o storage responder
    )
    
    lbl_erro = ft.Text(value="", color=VERMELHO_ERRO, size=12, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)
    txt_titulo = ft.Text("Verificando...", size=18, weight=ft.FontWeight.W_700, color=BRANCO_PURO)
    txt_subtitulo = ft.Text("Aguarde um instante", size=12, color=PRATA_TEXTO, text_align=ft.TextAlign.CENTER)
    txt_botao = ft.Text("Entrar", weight=ft.FontWeight.W_600, color=BG_PRINCIPAL, size=13)
    ico_cabecalho = ft.Icon(ft.Icons.LOCK_PERSON_OUTLINED, size=30, color=BRANCO_PURO)

    # --- INICIALIZAÇÃO ASSÍNCRONA DO ESTADO ---
    async def checar_estado_inicial(e=None):
        nonlocal primeiro_acesso, senha_gravada
        # Busca de forma assíncrona e segura usando os recursos do Flet
        senha_gravada = await page.client_storage.get_async("app_master_password")
        primeiro_acesso = senha_gravada is None

        # Atualiza os textos e labels dinamicamente baseados no storage
        txt_senha.label = "Defina sua nova senha" if primeiro_acesso else "Digite a senha numérica"
        txt_senha.disabled = False
        txt_titulo.value = "Configurar Acesso" if primeiro_acesso else "Acesso Restrito"
        txt_subtitulo.value = "Cadastre uma senha de 4 a 12 números" if primeiro_acesso else "Insira suas credenciais de segurança"
        txt_botao.value = "Salvar e Entrar" if primeiro_acesso else "Desbloquear"
        ico_cabecalho.name = ft.Icons.VERIFIED_USER_OUTLINED if primeiro_acesso else ft.Icons.LOCK_PERSON_OUTLINED
        page.update()

    # CORREÇÃO CRÍTICA: Dispara a tarefa assíncrona usando o gerenciador nativo do Flet
    page.run_task(checar_estado_inicial)

    # --- FUNÇÕES LÓGICAS ---
    def btn_teclado_virtual(e):
        if txt_senha.disabled:
            return
        valor_botao = e.control.data
        if valor_botao == "limpar":
            txt_senha.value = "" 
        elif valor_botao == "apagar":
            txt_senha.value = txt_senha.value[:-1] 
        else:
            if len(txt_senha.value) < 12:
                txt_senha.value += valor_botao
        page.update()
        
    async def processar_autenticacao(e):
        nonlocal primeiro_acesso, senha_gravada
        if txt_senha.disabled:
            return

        lbl_erro.value = ""
        
        # Validação inicial dos dígitos
        if not txt_senha.value or not txt_senha.value.isdigit():
            lbl_erro.value = "A senha deve conter apenas números!"
            lbl_erro.color = VERMELHO_ERRO
            page.update()
            return

        # Criptografia via HASH SHA-256
        senha_criptografada = hashlib.sha256(txt_senha.value.encode()).hexdigest()

        # Fluxo de Primeiro Acesso: Registro da senha mestre
        if primeiro_acesso:
            if 4 <= len(txt_senha.value) <= 12:
                # Salva no banco local do dispositivo de forma assíncrona
                await page.client_storage.set_async("app_master_password", senha_criptografada)
                
                lbl_erro.value = "Senha mestre cadastrada com sucesso!"
                lbl_erro.color = CORTESIA_VERDE
                conteudo_login.content = layout_loading
                page.update()
                
                await asyncio.sleep(1.5)
                page.go("/home")
            else:
                lbl_erro.value = "A senha precisa ter entre 4 e 12 dígitos!"
                lbl_erro.color = VERMELHO_ERRO
                page.update()
                
        # Fluxo de Login Tradicional: Compara hashes criptografados
        else:
            if senha_criptografada == senha_gravada:
                conteudo_login.content = layout_loading
                page.update()
                
                await asyncio.sleep(1.2)
                page.go("/home") 
            else:
                lbl_erro.value = "Senha incorreta! Tente novamente."
                lbl_erro.color = VERMELHO_ERRO
                page.update()

    def alternar_teclado(e):
        container_teclado.visible = not container_teclado.visible
        btn_mostrar_teclado.text = "Ocultar Teclado Virtual" if container_teclado.visible else "Usar Teclado Virtual"
        cabecalho_card.visible = not container_teclado.visible if page.height <= 660 else True
        page.update()

    # --- CONSTRUÇÃO DO TECLADO VIRTUAL ---
    botoes = []
    for i in range(1, 10):
        botoes.append(
            ft.Container(
                content=ft.Text(str(i), size=16, weight=ft.FontWeight.BOLD, color=BRANCO_PURO),
                alignment=ft.alignment.center,
                shape=ft.BoxShape.CIRCLE,
                border=ft.border.all(1, PRATA_BORDA),
                bgcolor="#1C1C1E",
                data=str(i),
                on_click=btn_teclado_virtual,
                width=45,
                height=45,
            )
        )
    
    botoes.append(ft.Container(content=ft.Icon(ft.Icons.CLEAR, color=PRATA_TEXTO, size=16), alignment=ft.alignment.center, shape=ft.BoxShape.CIRCLE, data="limpar", on_click=btn_teclado_virtual, width=45, height=45))
    botoes.append(ft.Container(content=ft.Text("0", size=16, weight=ft.FontWeight.BOLD, color=BRANCO_PURO), alignment=ft.alignment.center, shape=ft.BoxShape.CIRCLE, border=ft.border.all(1, PRATA_BORDA), bgcolor="#1C1C1E", data="0", on_click=btn_teclado_virtual, width=45, height=45))
    botoes.append(ft.Container(content=ft.Icon(ft.Icons.BACKSPACE_OUTLINED, color=PRATA_TEXTO, size=16), alignment=ft.alignment.center, shape=ft.BoxShape.CIRCLE, data="apagar", on_click=btn_teclado_virtual, width=45, height=45))

    grid_teclado = ft.GridView(
        controls=botoes, 
        runs_count=3, 
        max_extent=48, 
        child_aspect_ratio=1.0, 
        spacing=8, 
        run_spacing=8, 
        width=160, 
        height=190,
    )

    container_teclado = ft.Container(content=grid_teclado, visible=False, alignment=ft.alignment.center)

    btn_mostrar_teclado = ft.TextButton(
        text="Usar Teclado Virtual",
        icon=ft.Icons.KEYBOARD_OUTLINED,
        style=ft.ButtonStyle(
            color=PRATA_TEXTO, 
            text_style=ft.TextStyle(size=11)
        ),
        on_click=alternar_teclado
    )

    # --- COMPONENTES DINÂMICOS DO CABEÇALHO ---
    cabecalho_card = ft.Column(
        controls=[
            ft.Container(
                content=ico_cabecalho,
                alignment=ft.alignment.center, width=54, height=54, border_radius=27, border=ft.border.all(1, PRATA_BORDA), bgcolor="#1C1C1E"
            ),
            ft.Container(height=2),
            txt_titulo,
            txt_subtitulo,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4
    )

    # --- CARD DE FORMULÁRIO PRINCIPAL ---
    card_login = ft.Container(
        content=ft.Column(
            controls=[
                cabecalho_card,
                ft.Container(height=6),
                txt_senha,
                lbl_erro,
                btn_mostrar_teclado, 
                container_teclado,   
                ft.Container(height=4),
                ft.Container(
                    content=txt_botao,
                    alignment=ft.alignment.center, 
                    height=42, 
                    width=260, 
                    bgcolor=BRANCO_PURO, 
                    border_radius=8, 
                    on_click=processar_autenticacao,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True
        ),
        bgcolor=BG_CARD,
        padding=ft.padding.symmetric(vertical=20, horizontal=16),
        border_radius=16,
        border=ft.border.all(1, "#27272A"),
        width=310,
    )

    # --- LAYOUT DE LOADING ---
    layout_loading = ft.Container(
        content=ft.Column(
            controls=[
                ft.ProgressRing(width=36, height=36, stroke_width=3, color=BRANCO_PURO),
                ft.Container(height=10),
                ft.Text("Processando ambiente criptográfico...", color=PRATA_TEXTO, size=12, weight=ft.FontWeight.W_500)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    conteudo_login = ft.AnimatedSwitcher(
        content=card_login, 
        transition=ft.AnimatedSwitcherTransition.SCALE,  
        duration=300,  
        reverse_duration=150,
        switch_in_curve=ft.AnimationCurve.EASE_OUT
    )

    view_centralizada = ft.Container(
        content=ft.Column(
            controls=[conteudo_login],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        bgcolor=BG_PRINCIPAL,
        alignment=ft.alignment.center
    )

    return ft.View(
        route="/login",
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text("SEGURANÇA CORPORATIVA", weight=ft.FontWeight.W_800, size=11, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL,
                center_title=True,
                automatically_imply_leading=False,
                elevation=0,
            ),
            ft.Divider(color=PRATA_BORDA, height=1),
            view_centralizada
        ],
        padding=0
    )