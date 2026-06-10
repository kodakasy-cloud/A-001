import flet as ft #type: ignore

# Listas temporárias para guardar os valores simulados
FINANCAS_TEMPORARIAS = []

def finance_views(page: ft.Page):
    """Gera a interface visual das finanças sem banco de dados."""
    
    # Textos do painel de saldo
    txt_saldo = ft.Text("R$ 0,00", size=24, weight=ft.FontWeight.BOLD)
    txt_receitas = ft.Text("Ganho: R$ 0,00", color=ft.Colors.GREEN)
    txt_despesas = ft.Text("Gasto: R$ 0,00", color=ft.Colors.RED)

    # Campos de digitação
    txt_valor = ft.TextField(label="Valor (R$)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    txt_categoria = ft.TextField(label="Categoria (Ex: Salário, Lanche)", width=200)
    
    drop_tipo = ft.Dropdown(
        label="Tipo",
        width=150,
        options=[
            ft.dropdown.Option("Receita"),
            ft.dropdown.Option("Despesa"),
        ],
        value="Receita"
    )

    def calcular_e_atualizar_painel():
        """Faz as contas matemáticas usando a lista da memória e atualiza a tela."""
        total_receitas = 0.0
        total_despesas = 0.0

        for item in FINANCAS_TEMPORARIAS:
            if item["tipo"] == "Receita":
                total_receitas += item["valor"]
            else:
                total_despesas += item["valor"]

        saldo_final = total_receitas - total_despesas

        # Atualiza os textos na interface
        txt_receitas.value = f"Ganho: R$ {total_receitas:.2f}"
        txt_despesas.value = f"Gasto: R$ {total_despesas:.2f}"
        txt_saldo.value = f"R$ {saldo_final:.2f}"
        
        # Cor do saldo (Verde se positivo, Vermelho se negativo)
        txt_saldo.color = ft.Colors.GREEN if saldo_final >= 0 else ft.Colors.RED
        page.update()

    def lançar_movimentacao_click(e):
        """Pega o valor digitado e adiciona na memória."""
        if not txt_valor.value or not txt_categoria.value:
            page.open(ft.SnackBar(ft.Text("Por favor, preencha o valor e a categoria!")))
            return
        
        try:
            valor_float = float(txt_valor.value.replace(",", "."))
        except ValueError:
            page.open(ft.SnackBar(ft.Text("Digite um número válido!")))
            return

        # Salva na lista do Python
        FINANCAS_TEMPORARIAS.append({
            "tipo": drop_tipo.value,
            "valor": valor_float,
            "categoria": txt_categoria.value
        })

        # Limpa os campos de texto
        txt_valor.value = ""
        txt_categoria.value = ""
        
        # Refaz os cálculos de saldo
        calcular_e_atualizar_painel()
        page.open(ft.SnackBar(ft.Text("Movimentação lançada!")))

    btn_salvar = ft.ElevatedButton("Lançar no Sistema", on_click=lançar_movimentacao_click, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE)
    btn_voltar = ft.TextButton("← Voltar para Home", on_click=lambda _: page.go("/home"))

    # Executa o cálculo inicial para exibir R$ 0,00 zerado
    calcular_e_atualizar_painel()

    return ft.View(
        route="/financas",
        controls=[
            btn_voltar,
            ft.Text("💰 Controle de Finanças Pessoais", style=ft.TextThemeStyle.HEADLINE_MEDIUM, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            # Painel do Saldo
            ft.Container(
                content=ft.Column([
                    ft.Text("Saldo Atual Disponível:", size=14),
                    txt_saldo,
                    ft.Row([txt_receitas, txt_despesas], spacing=30)
                ]),
                padding=20,
                bgcolor="surfacevariant",
                border_radius=10
            ),
            ft.Divider(),
            
            ft.Text("Adicionar Nova Movimentação:", weight=ft.FontWeight.BOLD),
            ft.Row([drop_tipo, txt_valor]),
            txt_categoria,
            ft.Container(height=10),
            btn_salvar
        ]
    )