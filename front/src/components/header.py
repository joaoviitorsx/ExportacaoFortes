import flet as ft
from ...src.utils.path import resourcePath

class Header(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        self.icon = ft.Image(
            src=resourcePath("front/src/assets/icone.png"),
            width=120,
            height=40,
        )

        self.title = ft.Text(
            "Conversor SPED",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK87,
        )

        self.subtitle = ft.Text(
            "Sistema para processamento de arquivos SPED e geração de arquivos .fs",
            size=14,
            color=ft.Colors.GREY_600,
        )

        self.divider = ft.Divider(height=1, color=ft.Colors.GREY_300)
        self.controls = [
            self.icon,
            self.title,
            self.subtitle,
            self.divider,
        ]

    def footer():

        return ft.Container(
            content=ft.Column([
                ft.Divider(color=ft.Colors.GREY_300, opacity=0.3),
                ft.Container(height=16),
                ft.Row([
                    ft.Text(
                        "© 2025 Realize Software. Todos os direitos reservados.",
                        size=12, 
                        color=ft.Colors.GREY_600
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=8),
                ft.Row([
                    ft.Text("Versão 1.0.0", size=10, color=ft.Colors.GREY_500),
                    ft.Text("•", size=10, color=ft.Colors.GREY_400),
                    ft.Text("Suporte: suporte@realize.com.br", size=10, color=ft.Colors.GREY_500),
                ], spacing=8, alignment=ft.MainAxisAlignment.CENTER)
            ]),
            margin=ft.margin.only(top=48)
        )