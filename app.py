import time
import flet as ft
import threading
from front.src.views.mainView import MainView
from front.src.views.empresaView import EmpresaView
from front.src.views.cadastroView import CadastroView
from front.src.utils.path import resourcePath

def loading():
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        bgcolor="#F5F6FA",
        content=ft.Column(
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src=resourcePath("front/src/assets/logo.png"),
                    width=280,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.ProgressRing(
                    width=48,
                    height=48,
                    stroke_width=4,
                    color=ft.Colors.BLUE_600,
                ),
                ft.Text(
                    "Carregando sistema...",
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color=ft.Colors.GREY_700,
                ),
            ],
        ),
    )

def main(page: ft.Page):
    page.title = "Conversor SPED para Fortes Fiscal"
    page.window.width = 680
    page.window.height = 880
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.icon = resourcePath("front/src/assets/icone.ico")

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_600,
            secondary=ft.Colors.PURPLE_500,
            background="#F5F6FA",
        )
    )

    page.controls.clear()
    page.add(loading())
    page.update()

    def route_change(e: ft.RouteChangeEvent):
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

    page.on_route_change = route_change

    def initialize_app():
        # Aqui entram:
        # - conexão com banco
        # - leitura de config
        # - validação de ambiente
        # - preload leve
        
        time.sleep(1)  #so pra simular carregamento
        page.go("/")  # navega para a primeira tela real

    threading.Thread(
        target=initialize_app,
        daemon=True,
    ).start()


if __name__ == "__main__":
    ft.app(target=main)
