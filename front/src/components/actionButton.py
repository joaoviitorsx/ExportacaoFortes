import flet as ft

class ActionButton(ft.ElevatedButton):
    def __init__(self, text, icon=None, disabled=False, visible=True, color="primary", on_click=None):
        super().__init__(
            text=text,
            icon=icon,
            disabled=disabled,
            visible=visible,
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: self.getBg(color),
                    ft.ControlState.DISABLED: ft.Colors.GREY_400,
                },
                color={
                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                    ft.ControlState.DISABLED: ft.Colors.BLACK87,
                },
                padding=ft.padding.symmetric(horizontal=18, vertical=18),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

    def getBg(self, color: str):
        cores = {
            "primary": ft.Colors.BLUE_600,
            "success": ft.Colors.GREEN_600,
            "secondary": ft.Colors.GREY_600,
            "danger": ft.Colors.RED_600,
        }
        return cores.get(color, ft.Colors.BLUE_600)
