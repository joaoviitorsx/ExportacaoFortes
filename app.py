import flet as ft
from front.src.view.mainView import MainView
from front.src.utils.path import resourcePath


def main(page: ft.Page):
    page.title = "SPED → Fortes Fiscal"
    page.window.height = 820
    page.window.width = 632
    page.resize=False
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.icon = resourcePath("front/src/assets/icone.ico")
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_600,
            secondary=ft.Colors.PURPLE_500,
            background="#F5F6FA",
        )
    )

    MainView(page)


if __name__ == "__main__":
    ft.app(target=main)
