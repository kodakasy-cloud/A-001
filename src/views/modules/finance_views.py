import flet as ft #type: ignore

# Lista temporária na memória para guardar os valores simulados
FINANCAS_TEMPORARIAS = []

def finance_views(page: ft.Page):
    """Gera a interface visual das finanças no padrão Premium Minimalista e Anti-Bugs."""
    
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        # Preto Absoluto
    BG_CARD = "#161618"             # Grafite Escuro
    PRATA_BORDA = "#2D2D30"         # Prata Escuro para linhas discretas
    PRATA_TEXTO = "#A1A1AA"         # Prata para labels secundárias
    BRANCO_PURO = "#FFFFFF"         # Branco Puro para títulos e destaque
    VERDE_SUCESSO = "#10B981"       # Verde sutil para ganhos
    VERMELHO_ALERTA = "#EF4444"     # Vermelho sutil para gastos

    # --- TEXTOS DO PAINEL DE SALDO ---
    txt_saldo = ft.Text("R$ 0,00", size=26, weight=ft.FontWeight.W_700, color=BRANCO_PURO)
    txt_receitas = ft.Text("Ganho: R$ 0,00", color=VERDE_SUCESSO, size=12, weight=ft.FontWeight.W_500)
    txt_despesas = ft.Text("Gasto: R$ 0,00", color=VERMELHO_ALERTA, size=12, weight=ft.FontWeight.W_500)

    # --- CAMPOS DE DIGITAÇÃO PREMIUM ---
    txt_valor = ft.TextField(
        label="Valor (R$)", 
        keyboard_type=ft.KeyboardType.NUMBER,
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        text_size=14,
        border_radius=8
    )
    
    txt_categoria = ft.TextField(
        label="Categoria (Ex: Salário, Lanche)", 
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        text_size=14,
        border_radius=8
    )
    
    drop_tipo = ft.Dropdown(
        label="Tipo de Fluxo",
        border_color=PRATA_BORDA,
        focused_border_color=BRANCO_PURO,
        color=BRANCO_PURO,
        label_style=ft.TextStyle(color=PRATA_TEXTO),
        bgcolor="#141416",
        border_radius=8,
        options=[
            ft.dropdown.Option("Receita"),
            ft.dropdown.Option("Despesa"),
        ],
        value="Receita"
    )

    # Coluna interna animada para renderizar o extrato de movimentações
    lista_historico_ui = ft.Column(spacing=8, animate_opacity=200)

    def deletar_movimentacao(item):
        """Remove um lançamento do fluxo e recalcula o painel."""
        FINANCAS_TEMPORARIAS.remove(item)
        calcular_e_atualizar_painel()
        
        page.snack_bar = ft.SnackBar(ft.Text("Registro financeiro removido.", color=BRANCO_PURO), bgcolor=BG_CARD)
        page.snack_bar.open = True
        page.update()

    def calcular_e_atualizar_painel():
        """Faz os cálculos matemáticos e atualiza o balanço e a lista histórica."""
        total_receitas = 0.0
        total_despesas = 0.0

        # Limpa o histórico visual para reconstrução
        lista_historico_ui.controls.clear()

        # Calcula e reconstrói o extrato de trás para frente (mais recente primeiro)
        for item in reversed(FINANCAS_TEMPORARIAS):
            eh_receita = item["tipo"] == "Receita"
            cor_indicador = VERDE_SUCESSO if eh_receita else VERMELHO_ALERTA
            simbolo = "+" if eh_receita else "-"

            if eh_receita:
                total_receitas += item["valor"]
            else:
                total_despesas += item["valor"]

            # Injeta o card do histórico formatado
            lista_historico_ui.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(
                                ft.Icons.ARROW_UPWARD_ROUNDED if eh_receita else ft.Icons.ARROW_DOWNWARD_ROUNDED, 
                                color=cor_indicador, 
                                size=16
                            ),
                            ft.Column([
                                ft.Text(item["categoria"], weight=ft.FontWeight.W_600, color=BRANCO_PURO, size=13),
                                ft.Text(item["tipo"], color=PRATA_TEXTO, size=11),
                            ], spacing=1)
                        ], spacing=10, expand=True),
                        
                        ft.Row([
                            ft.Text(f"{simbolo} R$ {item['valor']:.2f}", color=cor_indicador, weight=ft.FontWeight.W_600, size=13),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=PRATA_TEXTO,
                                icon_size=16,
                                padding=4,
                                on_click=lambda e, i=item: deletar_movimentacao(i)
                            )
                        ], spacing=6)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=BG_CARD,
                    padding=10,
                    border_radius=8,
                    border=ft.border.all(1, PRATA_BORDA)
                )
            )

        saldo_final = total_receitas - total_despesas

        # Atualiza painel numérico principal
        txt_receitas.value = f"Ganho: R$ {total_receitas:.2f}"
        txt_despesas.value = f"Gasto: R$ {total_despesas:.2f}"
        txt_saldo.value = f"R$ {saldo_final:.2f}"
        txt_saldo.color = VERDE_SUCESSO if saldo_final >= 0 else VERMELHO_ALERTA
        
        if not FINANCAS_TEMPORARIAS:
            lista_historico_ui.controls.append(
                ft.Container(
                    content=ft.Text("Nenhuma transação registrada no extrato.", color=PRATA_TEXTO, size=12, italic=True),
                    alignment=ft.alignment.center,
                    padding=15
                )
            )

        if lista_historico_ui.page:
            lista_historico_ui.update()

    def lancar_movimentacao_click(e):
        """Valida as entradas numéricas de forma segura contra falhas de digitação."""
        if not txt_valor.value or not txt_categoria.value:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Insira um Valor e uma Categoria."), bgcolor="#7F1D1D")
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            valor_float = float(txt_valor.value.replace(",", "."))
            if valor_float <= 0:
                raise ValueError
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: O valor inserido deve ser um número positivo."), bgcolor="#7F1D1D")
            page.snack_bar.open = True
            page.update()
            return

        # Guarda dados na memória global
        FINANCAS_TEMPORARIAS.append({
            "tipo": drop_tipo.value,
            "valor": valor_float,
            "categoria": txt_categoria.value
        })

        # Limpeza e reset de foco pós-lançamento (oculta teclado mobile)
        txt_valor.value = ""
        txt_categoria.value = ""
        txt_valor.focus()
        txt_valor.blur()
        
        calcular_e_atualizar_painel()
        
        page.snack_bar = ft.SnackBar(ft.Text("Fluxo de caixa atualizado."), bgcolor=BG_CARD)
        page.snack_bar.open = True
        page.update()

    # Executa o cálculo inicial da view
    calcular_e_atualizar_painel()

    # --- ESTRUTURA DE LAYOUT RESPONSIVA COMPATÍVEL ---
    conteudo_responsivo = ft.Container(
        content=ft.ListView(
            controls=[
                # PAINEL DE BALANÇO CONSOLIDADO
                ft.Text("BALANÇO PATRIMONIAL", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                ft.Container(height=6),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Saldo Líquido Atual:", size=11, color=PRATA_TEXTO),
                        txt_saldo,
                        ft.Container(height=2),
                        ft.Row([txt_receitas, txt_despesas], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=4),
                    bgcolor=BG_CARD,
                    padding=16,
                    border_radius=12,
                    border=ft.border.all(1, PRATA_BORDA)
                ),
                
                ft.Container(height=16),
                ft.Divider(color=PRATA_BORDA, height=1),
                ft.Container(height=16),
                
                # SEÇÃO DE ENTRADAS DE DADOS
                ft.Text("EXECUTAR NOVA MOVIMENTAÇÃO", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                ft.Container(height=8),
                drop_tipo,
                ft.Container(height=6),
                txt_valor,
                ft.Container(height=6),
                txt_categoria,
                ft.Container(height=12),
                
                # Botão Principal Monocromático de Ação Rápida
                ft.Container(
                    content=ft.Text("Injetar Lançamento", weight=ft.FontWeight.W_600, color=BG_PRINCIPAL, size=13),
                    alignment=ft.alignment.center,
                    height=46,
                    bgcolor=BRANCO_PURO,
                    border_radius=8,
                    on_click=lancar_movimentacao_click,
                ),
                
                ft.Container(height=18),
                ft.Divider(color=PRATA_BORDA, height=1),
                ft.Container(height=16),
                
                # EXTRATO EM TEMPO REAL
                ft.Text("HISTÓRICO INTERNO DE TRANSAÇÕES", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                ft.Container(height=8),
                lista_historico_ui,
                
                # Margem de segurança técnica anti-corte do Mobile
                ft.Container(height=50)
            ],
            spacing=0,
        ),
        padding=16,
        expand=True,
        width=420,  # Largura segura ideal para simular tela mobile perfeita ou rodar nativo
        alignment=ft.alignment.top_center
    )

    return ft.View(
        route="/financas",
        bgcolor=BG_PRINCIPAL,
        controls=[
            ft.AppBar(
                title=ft.Text("SISTEMA FINANCEIRO", weight=ft.FontWeight.W_700, size=13, color=BRANCO_PURO),
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
            # Centralizador universal de fluxo
            ft.Row(
                controls=[conteudo_responsivo],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ],
        padding=0
    )