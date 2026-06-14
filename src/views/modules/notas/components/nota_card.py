import flet as ft

class NotaCard(ft.Container):
    def __init__(self, bloco, index, total_blocos, cor_texto, cor_setas, on_delete, on_tap, on_move_left, on_move_right, prata_borda):
        self.bloco = bloco 

        super().__init__(
            width=150,
            height=135,
            bgcolor=bloco["cor"],
            border_radius=16, 
            padding=12,
            border=ft.border.all(1, prata_borda),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC),
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            # mouse_cursor removido daqui para evitar o erro de init do Container
        )

        # Efeito de feedback visual "Hover" nativo para Desktop
        self.on_hover = lambda e: self._mudar_escala(e)

        self.content = ft.Column([
            # --- HEADER DO CARD ---
            ft.Row([
                ft.Row([
                    ft.Text(bloco["emoji"], size=14), 
                    ft.Text(
                        bloco["titulo"], 
                        weight=ft.FontWeight.W_600, 
                        max_lines=1, 
                        color=cor_texto, 
                        size=12,
                        overflow=ft.TextOverflow.ELLIPSIS
                    )
                ], expand=True, spacing=6),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED, 
                    icon_color="#EF4444", 
                    icon_size=16, 
                    padding=2,
                    tooltip="Excluir Nota",
                    on_click=on_delete,
                    style=ft.ButtonStyle(overlay_color=ft.Colors.with_opacity(0.1, "#EF4444"))
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=0),
            
            # --- CORPO DO CARD (Texto) ---
            ft.GestureDetector(
                content=ft.Container(
                    content=ft.Text(
                        bloco["texto"], 
                        max_lines=2, 
                        overflow=ft.TextOverflow.ELLIPSIS, 
                        size=11, 
                        color=cor_texto,
                        opacity=0.85 # Leve transparência para dar hierarquia ao texto
                    ),
                    height=42,
                    alignment=ft.alignment.top_left
                ),
                on_tap=on_tap
            ),
            
            # --- ACTIONS DO CARD (Setas e Abrir) ---
            ft.Row([
                ft.Row([
                    ft.IconButton(
                        ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED, 
                        icon_color=cor_setas, 
                        icon_size=18, 
                        disabled=(index == 0), 
                        padding=1, 
                        on_click=on_move_left,
                    ),
                    ft.IconButton(
                        ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED, 
                        icon_color=cor_setas, 
                        icon_size=18, 
                        disabled=(index == total_blocos - 1), 
                        padding=1, 
                        on_click=on_move_right,
                    ),
                ], spacing=0),
                ft.IconButton(
                    icon=ft.Icons.OPEN_IN_NEW_ROUNDED, 
                    icon_color=cor_setas, 
                    icon_size=14, 
                    padding=4,
                    on_click=on_tap
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=0, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def _mudar_escala(self, e):
        # Cria um leve efeito de profundidade ao passar o mouse no Desktop
        self.scale = 1.03 if e.data == "true" else 1.0
        self.update()