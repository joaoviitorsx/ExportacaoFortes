import flet as ft

class Header(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.icon = ft.Icon(
            name=ft.Icons.DESCRIPTION_OUTLINED,
            size=40,
            color=ft.Colors.BLUE_600,
        )

        self.title = ft.Text(
            "Processador SPED",
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
