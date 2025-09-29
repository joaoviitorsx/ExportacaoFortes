import flet as ft

class Card(ft.Container):
    def __init__(self, title: str, content: ft.Control):
        super().__init__(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
            margin=ft.margin.only(top=10, bottom=10),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            expand=False,
        )

        title_text = ft.Text(
            title,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK87,
        )

        controls = []
        if title:
            controls.append(
                ft.Text(
                    title,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87,
                )
            )
            controls.append(ft.Divider(height=15, color=ft.Colors.TRANSPARENT))
        controls.append(content)

        self.content = ft.Column(
            controls=controls,
            spacing=12,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
