import flet as ft
from front.src.views.mainView import MainView
from front.src.views.empresaView import EmpresaView
from front.src.views.cadastroView import CadastroView
from front.src.utils.path import resourcePath


def main(page: ft.Page):
    page.title = "Conversor SPED para Fortes Fiscal"
    page.window.height = 880
    page.window.width = 680
    #page.window.resizable = False
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
            page.views.append(EmpresaView(page))

        elif page.route == "/cadastro":
            page.views.append(CadastroView(page))

        elif page.route.startswith("/main"):
            empresa_id = None
            nome_empresa = ""
            empresa_cnpj = ""
            if "?empresa=" in page.route:
                params = page.route.split("?")[1]
                for param in params.split("&"):
                    if param.startswith("empresa="):
                        empresa_id = int(param.split("=")[1])
                    elif param.startswith("nome="):
                        nome_empresa = param.split("=")[1].replace("%20", " ")
            if empresa_id is not None:
                page.views.append(MainView(page, empresa_id, nome_empresa, empresa_cnpj))
            else:
                page.go("/")

        page.update()

    page.on_route_change = route
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
