import sys
import os
import flet as ft  # type: ignore

# Garante que a pasta raiz do projeto seja vista pelo Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- IMPORTS DAS VIEWS (Sem duplicatas) ---
from views.login_view import login_view
from views.home_view import home_view
from views.modules.notas.notas_views import cofre_views
from views.modules.finances.finance_views import finance_views
from views.modules.eventos.eventos_views import eventos_views
from views.modules.settings.settings_view import settings_view


def main(page: ft.Page):

    # --- CONFIGURAÇÃO PADRÃO DAS PÁGINAS ---
    page.title = "Nother"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.icon = "icone.png"  # Força a janela do Windows a carregar o ícone
    page.icon = "icone.png"
    
    # Sistema de dimensionamento responsivo / Mobile simulado
    if "--mobile" in sys.argv:
        page.window.width = 360        # Largura de celular padrão
        page.window.height = 640       # Altura de celular padrão
        page.window.resizable = False  # Trava o tamanho para testar responsividade
        print("📱 Modo Mobile Ativado: 360x640")
    else:
        page.window.width = 600        # Mantém proporção compacta por padrão
        page.window.height = 900
        page.window.resizable = True

    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- GERENCIADOR DE ROTAS ---
    def route_change(e):
        page.views.clear()

        # Rota de Login / Inicial
        if page.route == "/" or page.route == "/login":
            page.views.append(login_view(page))

        # Rota da Home
        elif page.route == "/home":
            page.views.append(home_view(page))

        # Rota do Cofre / Notas
        elif page.route == "/notas":
            page.views.append(cofre_views(page))
            
        # Rota de Finanças
        elif page.route == "/finance":
            page.views.append(finance_views(page))
        
        # Rota de Eventos
        elif page.route == "/eventos":
            page.views.append(eventos_views(page))
            
        # Rota de Configurações
        elif page.route == "/settings":
            page.views.append(
                ft.View(
                    route="/settings",
                    bgcolor="#0B0B0C",  # BG_PRINCIPAL
                    padding=0,
                    scroll=ft.ScrollMode.ADAPTIVE,  # Libera a rolagem nativa perfeitamente
                    navigation_bar=home_view(page).navigation_bar, 
                    controls=[
                        ft.AppBar(
                            title=ft.Text("CONFIGURAÇÕES", weight=ft.FontWeight.W_700, size=14, color="#FFFFFF"),
                            bgcolor="#0B0B0C",
                            center_title=True,
                            automatically_imply_leading=False,
                            elevation=0,
                        ),
                        ft.Divider(color="#2D2D30", height=1),
                        settings_view(page)  # Injeta o conteúdo estruturado das configurações
                    ]
                )
            ) 
            
        page.update()

    # --- HISTÓRICO DE NAVEGAÇÃO (Botão Voltar Nativo) ---
    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        
    page.on_route_change = route_change
    page.on_route_view_pop = view_pop

    # Executa a rota inicial do app
    page.go("/")


if __name__ == "__main__":
    # Descobre dinamicamente onde o main.py está e aponta para a pasta assets vizinha a ele
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_assets = os.path.join(caminho_atual, "assets") # Se a pasta assets estiver dentro de 'src' junto com o main.py
    
    # Se a sua pasta assets estiver fora de 'src' (na raiz A-001), use a linha abaixo no lugar:
    # pasta_assets = os.path.join(os.path.dirname(caminho_atual), "assets")

    ft.app(target=main, assets_dir=pasta_assets)