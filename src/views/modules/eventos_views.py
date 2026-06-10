import flet as ft #type: ignore

# Lista temporária na memória para guardar os eventos enquanto o app está aberto
EVENTOS_TEMPORARIOS = []

def eventos_views(page: ft.Page):
    """Gera a interface visual da tela de Eventos sem banco de dados."""
    
    # Campos de entrada de texto
    txt_titulo = ft.TextField(label="Título do Evento", width=300)
    txt_descricao = ft.TextField(label="Descrição / Detalhes", width=300, multiline=True)
    txt_data = ft.TextField(label="Data (DD/MM/AAAA)", width=150, hint_text="Ex: 15/06/2026")
    
    # Lista visual que mostra os eventos na tela
    lista_eventos_ui = ft.ListView(expand=True, spacing=10, padding=20)

    def atualizar_lista_na_tela():
        """Limpa a tela e redesenha a lista com o que está na memória."""
        lista_eventos_ui.controls.clear()
        
        for ev in EVENTOS_TEMPORARIOS:
            lista_eventos_ui.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE),
                    title=ft.Text(ev["titulo"], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"Data: {ev['data']}\n{ev['descricao']}"),
                    is_three_line=True
                )
            )
        page.update()

    def cadastrar_evento_click(e):
        """Pega os dados digitados e joga na lista temporária."""
        if not txt_titulo.value or not txt_data.value:
            page.open(ft.SnackBar(ft.Text("Por favor, preencha o Título e a Data!")))
            return
        
        # Guarda o dicionário na nossa lista na memória
        EVENTOS_TEMPORARIOS.append({
            "titulo": txt_titulo.value,
            "data": txt_data.value,
            "descricao": txt_descricao.value
        })
        
        # Limpa os campos para o próximo input
        txt_titulo.value = ""
        txt_descricao.value = ""
        txt_data.value = ""
        
        # Atualiza o visual
        atualizar_lista_na_tela()
        page.open(ft.SnackBar(ft.Text("Evento adicionado (Temporariamente)!")))

    # Botões de ação
    btn_salvar = ft.ElevatedButton("Adicionar Evento", on_click=cadastrar_evento_click, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    btn_voltar = ft.TextButton("← Voltar para Home", on_click=lambda _: page.go("/home"))

    # Mostra os eventos que já estão na memória ao abrir a tela
    atualizar_lista_na_tela()

    return ft.View(
        route="/eventos",
        controls=[
            btn_voltar,
            ft.Text("📅 Gerenciador de Eventos", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([txt_titulo, txt_data]),
            txt_descricao,
            btn_salvar,
            ft.Divider(),
            ft.Text("Seus Próximos Compromissos:", weight=ft.FontWeight.BOLD),
            lista_eventos_ui
        ]
    )