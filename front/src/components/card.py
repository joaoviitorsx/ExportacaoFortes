import flet as ft

class Card(ft.Container):
    def __init__(self, title: str, content: ft.Control, icon: str = None, width: int = None, height: int = None):
        super().__init__(
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            padding=20,
            margin=ft.margin.only(top=12, bottom=2, right=8, left=8),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.with_opacity(0.12, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            expand=False,
            width=width,
            height=height,
        )

        controls = []
        if title:
            if icon:
                controls.append(
                    ft.Row(
                        [
                            ft.Icon(icon, size=20, color=ft.colors.BLUE_600),
                            ft.Text(
                                title,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLACK87,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                )
            else:
                controls.append(
                    ft.Text(
                        title,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLACK87,
                    )
                )
            controls.append(ft.Divider(height=15, color=ft.colors.TRANSPARENT))

        controls.append(content)

        self.content = ft.Column(
            controls=controls,
            spacing=12,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
