import flet as ft
from front.src.views.mainView import MainView
from front.src.views.empresaView import EmpresaView
from front.src.views.cadastroView import CadastroView
from front.src.utils.path import resourcePath


def main(page: ft.Page):
    page.title = "SPED → Fortes Fiscal"
    page.window.height = 832
    page.window.width = 632
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.icon = resourcePath("front/src/assets/icone.ico")
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_600,
            secondary=ft.Colors.PURPLE_500,
            background="#F5F6FA",
        )
    )

    def route(e: ft.RouteChangeEvent):
        page.views.clear()

        if page.route == "/":
            EmpresaView(page)

        elif page.route == "/cadastro":
            CadastroView(page)

        elif page.route.startswith("/main"):
            empresa_id = 1
            if "?empresa=" in page.route:
                empresa_id = int(page.route.split("=")[-1])
            MainView(page, empresa_id)

        page.update()

    page.on_route_change = route
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
