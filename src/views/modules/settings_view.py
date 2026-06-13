# src/views/modules/settings_views.py
import flet as ft # type: ignore

def settings_view(page: ft.Page):
    """
    Retorna o container/componente completo e estilizado da tela de 
    Configurações com design Premium Dark e Scroll 100% funcional.
    """
    # --- PALETA PREMIUM ---
    BG_CARD = "#161618"             
    PRATA_BORDA = "#2D2D30"         
    PRATA_TEXTO = "#A1A1AA"         
    BRANCO_PURO = "#FFFFFF"         
    CORTESIA_VERDE = "#34D399"      

    # --- HELPERS (MANTIDOS IGUAIS) ---
    def criar_opcao_item(sub_texto, icone, action_icon=ft.Icons.CHEVRON_RIGHT_ROUNDED):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(icone, color=PRATA_TEXTO, size=20),
                    ft.Text(sub_texto, size=14, color=BRANCO_PURO, weight=ft.FontWeight.W_400)
                ], spacing=12),
                ft.Icon(action_icon, color=PRATA_TEXTO, size=18)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=14, horizontal=16),
            border=ft.border.all(1, PRATA_BORDA),
            border_radius=12,
            bgcolor="#1F1F23",
            on_click=lambda e: None
        )

    def criar_switch_item(sub_texto, icone, valor_inicial=False):
        return ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Icon(icone, color=PRATA_TEXTO, size=20),
                    ft.Text(sub_texto, size=14, color=BRANCO_PURO, weight=ft.FontWeight.W_400)
                ], spacing=12),
                ft.Switch(
                    value=valor_inicial,
                    active_color=CORTESIA_VERDE,
                    track_color=PRATA_BORDA,
                    thumb_color=BRANCO_PURO
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(vertical=10, horizontal=16),
            border=ft.border.all(1, PRATA_BORDA),
            border_radius=12,
            bgcolor="#1F1F23"
        )

    # --- LISTA DE CONTROLES (CONTEÚDO ROLÁVEL) ---
    conteudo_configuracoes = [
        # Cabeçalho da View
        ft.Row(
            controls=[
                ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=24, color=BRANCO_PURO),
                ft.Text("Ajustes & Preferências", size=20, weight=ft.FontWeight.W_700, color=BRANCO_PURO),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        ),
        ft.Divider(color=PRATA_BORDA, height=1),
        ft.Container(height=5),

        # SEÇÃO 1: PERFIL & CONTA
        ft.Text("CONTA E ASSINATURA", size=11, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
        criar_opcao_item("Detalhes do Perfil", ft.Icons.PERSON_OUTLINED),
        criar_opcao_item("Plano Atual (Prime)", ft.Icons.MONETIZATION_ON_OUTLINED),
        ft.Container(height=10),

        # SEÇÃO 2: SEGURANÇA AVANÇADA
        ft.Text("SEGURANÇA E PRIVACIDADE", size=11, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
        criar_opcao_item("Alterar Senha de Acesso", ft.Icons.LOCK_RESET_ROUNDED),
        criar_switch_item("Autenticação Biométrica", ft.Icons.FINGERPRINT_ROUNDED, valor_inicial=True),
        criar_opcao_item("Gerenciar Chaves de Criptografia", ft.Icons.KEY_ROUNDED),
        ft.Container(height=10),

        # SEÇÃO 3: CUSTOMIZAÇÃO DO APP
        ft.Text("INTERFACE E PREFERÊNCIAS", size=11, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
        criar_switch_item("Modo Escuro Forçado", ft.Icons.DARK_MODE_OUTLINED, valor_inicial=True),
        criar_switch_item("Notificações Push", ft.Icons.NOTIFICATIONS_NONE_ROUNDED, valor_inicial=False),
        criar_opcao_item("Idioma do Sistema", ft.Icons.LANGUAGE_ROUNDED),
        ft.Container(height=10),

        # SEÇÃO 4: BACKUP E ARMAZENAMENTO
        ft.Text("DADOS LOCAIS", size=11, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
        criar_opcao_item("Exportar Banco de Dados (Backup)", ft.Icons.DOWNLOAD_ROUNDED),
        criar_opcao_item("Limpar Cache Local", ft.Icons.DELETE_OUTLINE_ROUNDED),
        ft.Container(height=10),

        # SEÇÃO 5: SOBRE O APP
        ft.Text("SUPORTE & INFORMAÇÕES", size=11, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
        criar_opcao_item("Central de Ajuda", ft.Icons.HELP_OUTLINE_ROUNDED),
        criar_opcao_item("Termos de Privacidade", ft.Icons.PRIVACY_TIP_ROUNDED), 
        
        # Rodapé sutil de Versão
        ft.Container(height=15),
        ft.Row(
            [ft.Text("MY LIFE PRIME v0.1 • Criptografia de Ponta", size=10, color=PRATA_TEXTO)],
            alignment=ft.MainAxisAlignment.CENTER
        )
    ]

# --- RETORNO CORRIGIDO (O SCROLL AGORA É GERENCIADO PELA VIEW PAI NO MAIN) ---
    return ft.Container(
        content=ft.Column(
            controls=conteudo_configuracoes,
            spacing=10,
            tight=True, # Faz a coluna ocupar apenas o tamanho necessário dos itens
        ),
        padding=24,
        bgcolor=BG_CARD,
        border_radius=24,
        border=ft.border.all(1, PRATA_BORDA),
        margin=20,
        # Removemos os 'expand=True' daqui de dentro para não quebrar a física do scroll
    )