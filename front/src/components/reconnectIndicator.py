import flet as ft

def ReconnectIndicator() -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.ProgressRing(
                    width=16, 
                    height=16, 
                    stroke_width=2, 
                    color=ft.Colors.ORANGE
                ),
                ft.Text(
                    "Tentando reconectar...",
                    size=14,
                    color=ft.Colors.ORANGE,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=10,
        border_radius=8,
        bgcolor=ft.Colors.ORANGE_50,
        visible=False,
        animate_opacity=300,
    )
