import flet as ft

class ActionButton(ft.ElevatedButton):
    def __init__(
        self,
        text: str,
        icon: str | None = None,
        disabled: bool = False,
        visible: bool = True,
        color: str = "primary",
    ):
        colors = {
            "primary": ft.Colors.BLUE_600,
            "success": ft.Colors.GREEN_600,
            "danger": ft.Colors.RED_600,
            "secondary": ft.Colors.GREY_700,
        }

        super().__init__(
            text=text,
            icon=icon,
            disabled=disabled,
            visible=visible,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=8)},
                padding={"": 20},
                bgcolor={"": colors.get(color, ft.Colors.BLUE_600)},
                color={"": ft.Colors.WHITE},
            ),
        )
