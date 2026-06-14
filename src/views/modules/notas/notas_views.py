import flet as ft
from .controllers.notas_controllers import NotasController
from .components.nota_card import NotaCard
from .components.nota_dialog import NotaForm

def cofre_views(page: ft.Page):
    # --- PALETA DE CORES PREMIUM ---
    BG_PRINCIPAL = "#0B0B0C"        
    BG_CARD = "#161618"             
    PRATA_BORDA = "#2D2D30"         
    PRATA_TEXTO = "#A1A1AA"         
    BRANCO_PURO = "#FFFFFF"         

    controller = NotasController(view=None) # Instanciado inicialmente sem amarração direta
    linha_blocos = ft.Row(wrap=False, scroll=ft.ScrollMode.ALWAYS, spacing=12)

    def voltar_home(e):
        page.go("/home")

    def disparar_salvar(e):
        sucesso = controller.salvar_bloco(
            titulo=form.txt_titulo.value,
            texto=form.txt_conteudo.value,
            cor=form.cor_selecionada.value
        )
        if sucesso:
            form.limpar_campos()
            renderizar_blocos()

    def disparar_limpar(e):
        controller.limpar_selecao()
        form.limpar_campos()

    def disparar_carregar(bloco):
        controller.selecionar_bloco(bloco)
        cor_texto = controller.obter_cor_texto(bloco["cor"])
        form.preencher_campos(bloco["titulo"], bloco["texto"], bloco["cor"], cor_texto)

    def disparar_excluir(bloco_id):
        controller.excluir_bloco(bloco_id)
        if controller.bloco_selecionado["id"] is None:
            form.limpar_campos()
        renderizar_blocos()

    def disparar_mover(index, direcao):
        controller.mover_bloco(index, direcao)
        renderizar_blocos()

    def renderizar_blocos():
        linha_blocos.controls.clear()
        blocos_dados = controller.obter_lista_notas()
        
        for i, b in enumerate(blocos_dados):
            cor_do_texto = controller.obter_cor_texto(b["cor"])
            cor_setas = PRATA_TEXTO if cor_do_texto == BRANCO_PURO else BG_PRINCIPAL
            
            card = NotaCard(
                bloco=b, index=i, total_blocos=len(blocos_dados),
                cor_texto=cor_do_texto, cor_setas=cor_setas, prata_borda=PRATA_BORDA,
                on_delete=lambda e, b_id=b["id"]: disparar_excluir(b_id),
                on_tap=lambda e, bloco=b: disparar_carregar(bloco),
                on_move_left=lambda e, idx=i: disparar_mover(idx, "esquerda"),
                on_move_right=lambda e, idx=i: disparar_mover(idx, "direita")
            )
            linha_blocos.controls.append(card)
            
        if linha_blocos.page:
            linha_blocos.update()

    # Criação do Formulário Isolado
    form = NotaForm(
        prata_borda=PRATA_BORDA, 
        prata_texto=PRATA_TEXTO,  # 👈 Corrigido para bater com a classe NotaForm
        branco_puro=BRANCO_PURO, 
        bg_principal=BG_PRINCIPAL,
        on_salvar=disparar_salvar, 
        on_limpar=disparar_limpar, 
        on_cor_mudou=controller.obter_cor_texto
    )

    # Vincula a view de volta no controlador caso precise futuramente
    controller.view = page 

    # Carga inicial dos cartões
    renderizar_blocos()

    return ft.View(
        route="/cofre",
        bgcolor=BG_PRINCIPAL,
        padding=0,
        controls=[
            ft.AppBar(
                title=ft.Text("Notas", weight=ft.FontWeight.W_700, size=13, color=BRANCO_PURO),
                bgcolor=BG_PRINCIPAL, center_title=True, elevation=0,
                leading=ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color=PRATA_TEXTO, icon_size=15, on_click=voltar_home)
            ),
            ft.Divider(color=PRATA_BORDA, height=1),
            ft.Container(
                content=ft.ListView(
                    controls=[
                        ft.Text("CONTEÚDOS ENCRIPTADOS", size=10, weight=ft.FontWeight.W_700, color=PRATA_TEXTO),
                        ft.Container(height=4),
                        linha_blocos,
                        ft.Container(height=12),
                        ft.Divider(color=PRATA_BORDA, height=1),
                        ft.Container(height=12),
                        form, # Inserção do componente de formulário completo
                        ft.Container(height=40)
                    ],
                ),
                padding=14,
                expand=True
            )
        ]
    )