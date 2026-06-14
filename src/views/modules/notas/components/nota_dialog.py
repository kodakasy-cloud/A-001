import flet as ft

class NotaForm(ft.Column):
    def __init__(self, prata_borda, prata_texto, branco_puro, bg_principal, on_salvar, on_limpar, on_cor_mudou):
        super().__init__()
        self.prata_borda = prata_borda
        self.prata_texto = prata_texto
        self.branco_puro = branco_puro
        self.bg_principal = bg_principal
        self.on_salvar = on_salvar
        self.on_limpar = on_limpar
        self.on_cor_mudou = on_cor_mudou
        self.spacing = 14  # Espaçamento consistente

        # Inputs de Texto Refinados (Visual iOS/Modern Dark)
        self.txt_titulo = ft.TextField(
            label="Título do Bloco", 
            border_color=prata_borda, 
            focused_border_color=branco_puro,
            color=branco_puro, 
            label_style=ft.TextStyle(color=prata_texto, size=12), 
            bgcolor="#141416",
            text_size=14, 
            border_radius=10,
            content_padding=14,
            cursor_color=branco_puro,
        )
        self.txt_conteudo = ft.TextField(
            label="Escreva sua nota secreta aqui...", 
            multiline=True, 
            min_lines=4, 
            max_lines=6,
            border_color=prata_borda, 
            focused_border_color=branco_puro, 
            color=branco_puro,
            label_style=ft.TextStyle(color=prata_texto, size=12), 
            bgcolor="#141416", 
            text_size=14, 
            border_radius=10,
            content_padding=14,
            cursor_color=branco_puro,
        )
        
        self.cor_selecionada = ft.Text("#1C1C1E", visible=False)

# Seletor de Cores - CORRIGIDO (Removido mouse_cursor do Container)
        cores_disponiveis = ["#121214", "#1C1C1E", "#252529", "#2C2C30", "#3A3A3C", "#48484A", "#A1A1AA", "#FFFFFF"]
        self.linha_cores = ft.Row([
            ft.Container(
                width=32, 
                height=32, 
                bgcolor=cor, 
                border_radius=16, 
                data=cor, 
                on_click=self.selecionar_cor,
                border=ft.border.all(1, prata_borda), 
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            ) for cor in cores_disponiveis
        ], wrap=True, spacing=10)

        # Seletor de Emojis - CORRIGIDO (Removido mouse_cursor do Container)
        emojis = ["🔐", "💼", "💡", "🎯", "📝", "🚀", "💎", "🔋"]
        self.linha_emojis = ft.Row([
            ft.Container(
                content=ft.Text(emj, size=16), 
                alignment=ft.alignment.center, 
                width=42, 
                height=42,
                bgcolor="#141416", 
                border_radius=10, 
                border=ft.border.all(1, prata_borda), 
                data=emj,
                on_click=self.adicionar_emoji,
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
            ) for emj in emojis
        ], scroll=ft.ScrollMode.ALWAYS, spacing=10)

        self.btn_salvar = ft.Container(
                    content=ft.Text("Salvar Nota", weight=ft.FontWeight.W_600, color=bg_principal, size=13),
                    alignment=ft.alignment.center, 
                    height=46, 
                    width=150, 
                    bgcolor=branco_puro, 
                    border_radius=10,
                    on_click=self.on_salvar,
                    animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT)
                )

        # Montando a estrutura visual com mais respiro
        self.controls = [
            ft.Text(
                "COMPILADOR DE ENTRADA", 
                size=10, 
                weight=ft.FontWeight.W_800, 
                color=prata_texto, 
                style=ft.TextStyle(letter_spacing=1.5) # 👈 Movido para cá
            ),
            self.txt_titulo,
            self.txt_conteudo,
            
            ft.Column([
                ft.Text("Injetar Elemento Rápido", size=11, color=prata_texto, weight=ft.FontWeight.W_600),
                self.linha_emojis,
            ], spacing=6),
            
            ft.Column([
                ft.Text("Identidade do Contêiner", size=11, color=prata_texto, weight=ft.FontWeight.W_600),
                self.linha_cores,
            ], spacing=6),
            
            ft.Container(height=4), # Espaçador
            
            ft.Row([
                ft.TextButton(
                    text="Limpar Painel", 
                    icon=ft.Icons.REFRESH_ROUNDED, 
                    style=ft.ButtonStyle(
                        color=prata_texto,
                        overlay_color=ft.Colors.with_opacity(0.05, branco_puro)
                    ), 
                    on_click=self.on_limpar
                ),
                self.btn_salvar,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]

    def selecionar_cor(self, e):
        cor_hex = e.control.data
        self.cor_selecionada.value = cor_hex
        self.txt_conteudo.bgcolor = cor_hex
        self.txt_conteudo.color = self.on_cor_mudou(cor_hex)
        
        # Anima a borda selecionada de forma muito mais visível e elegante
        for item in self.linha_cores.controls:
            if item.data == cor_hex:
                item.border = ft.border.all(2, self.branco_puro)
                item.scale = 1.1
            else:
                item.border = ft.border.all(1, self.prata_borda)
                item.scale = 1.0
        self.update()

    def adicionar_emoji(self, e):
        self.txt_conteudo.value = (self.txt_conteudo.value or "") + e.control.data
        # Efeito rápido de feedback no clique do emoji
        e.control.scale = 0.9
        e.control.update()
        e.control.scale = 1.0
        self.txt_conteudo.update()
        e.control.update()

    def limpar_campos(self):
        self.txt_titulo.value = ""
        self.txt_conteudo.value = ""
        self.txt_conteudo.bgcolor = "#141416"
        self.txt_conteudo.color = self.branco_puro
        self.cor_selecionada.value = "#1C1C1E"
        for item in self.linha_cores.controls:
            item.border = ft.border.all(1, self.prata_borda)
            item.scale = 1.0
        self.update()

    def preencher_campos(self, titulo, texto, cor, cor_texto):
        self.txt_titulo.value = titulo
        self.txt_conteudo.value = texto
        self.txt_conteudo.bgcolor = cor
        self.txt_conteudo.color = cor_texto
        self.cor_selecionada.value = cor
        for item in self.linha_cores.controls:
            if item.data == cor:
                item.border = ft.border.all(2, self.branco_puro)
                item.scale = 1.1
            else:
                item.border = ft.border.all(1, self.prata_borda)
                item.scale = 1.0
        self.update()