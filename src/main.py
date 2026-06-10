import sys
import flet as ft  # type: ignore

from views.login_view import login_view
from views.home_view import home_view
from views.modules.cofre_views import cofre_views
from views.modules.finance_views import finance_views
from views.modules.eventos_views import eventos_views


def main(page: ft.Page):

    # CONFIGURAÇÃO PADRÃO DAS PÁGINAS
    page.title = "Nother Segury"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Verifica se o app foi iniciado em modo mobile
    if "--mobile" in sys.argv:
        page.window.width = 360        # Largura de celular antigo
        page.window.height = 640       # Altura de celular antigo
        page.window.resizable = False  # Trava o tamanho para testar responsividade
        print("📱 Modo Mobile Ativado: 360x640")
    else:
        page.window.width = 360       # Tamanho desktop padrão
        page.window.height = 640
        page.window.resizable = True

    page.window.center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # FUNÇÃO QUE MUDA TELA
    def route_change(e):  # O Flet passa um evento para o on_route_change
        page.views.clear()

        # Rota de Login
        if page.route == "/" or page.route == "/login":
            page.views.append(login_view(page))

        # Rota da Home
        elif page.route == "/home":
            page.views.append(home_view(page))

        # Rota do Cofre
        elif page.route == "/notas":
            page.views.append(cofre_views(page))
            
        elif page.route == "/finance":
            page.views.append(finance_views(page))
        
        elif page.route == "/eventos":
            page.views.append(eventos_views(page))
            
        page.update()

    def view_pop(e):  # O Flet passa um evento para o on_route_view_pop
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        
    page.on_route_change = route_change
    page.on_route_view_pop = view_pop

    # DEFINIR ROTA INICIAL E VAI PARA ELA
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)