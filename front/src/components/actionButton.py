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
                    ft.ControlState.DISABLED: ft.colors.GREY_400,
                },
                color={
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                    ft.ControlState.DISABLED: ft.colors.BLACK87,
                },
                padding=ft.padding.symmetric(horizontal=12, vertical=12),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

    def getBg(self, color: str):
        cores = {
            "primary": ft.colors.BLUE_600,
            "success": ft.colors.GREEN_600,
            "secondary": ft.colors.GREY_600,
            "danger": ft.colors.RED_600,
        }
        return cores.get(color, ft.colors.BLUE_600)
