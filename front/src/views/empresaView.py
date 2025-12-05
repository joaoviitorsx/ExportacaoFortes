import flet as ft
from ..components.header import Header
from ..components.actionButton import ActionButton
from ..routes.empresaRoute import EmpresaRoute
from ..utils.path import resourcePath
from ..components.card import Card

def EmpresaView(page: ft.Page) -> ft.View:
    #page.title = "Selecionar Empresa"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    empresas = EmpresaRoute.listarEmpresas()

    dropdown = ft.Dropdown(
        label="Empresas cadastradas",
        hint_text="Selecione uma empresa",
        options=[
            ft.dropdown.Option(
                str(e["id"]),
                f'{e["razao_social"]} - {e["cnpj"]}',
                e["cnpj"]
            ) for e in empresas
        ],
        width=350,
        border_radius=12,
        border_color=ft.Colors.GREY_400,
        filled=True,
        fill_color=ft.Colors.WHITE,
    )

    btn_entrar = ActionButton("Entrar", disabled=True, color="primary")
    btn_cadastrar = ActionButton("Cadastrar Empresa", color="success")

    def on_change(e):
        btn_entrar.disabled = dropdown.value is None
        page.update()

    def entrar(e):
        if dropdown.value:
            empresa_id = int(dropdown.value)
            razao_social = ""
            cnpj = ""
            for opt in dropdown.options:
                if opt.key == dropdown.value:
                    razao_social = opt.text
                    break
            page.go(f"/main?empresa={empresa_id}&nome={razao_social.replace(' ', '%20')}&cnpj={cnpj}")

    def cadastrar(e):
        page.go("/cadastro")

    dropdown.on_change = on_change
    btn_entrar.on_click = entrar
    btn_cadastrar.on_click = cadastrar

    conteudo = ft.Column(
        [
            ft.Image(
                src=resourcePath("front/src/assets/logo.png"),
                width=320,
                #height=80,
                fit=ft.ImageFit.CONTAIN,
            ),
            ft.Text(
                "Selecione a empresa",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            dropdown,
            ft.Row(
                [btn_entrar, btn_cadastrar],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=25,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    card = Card(
        title="",
        content=conteudo,
        icon=ft.Icons.BUSINESS,
        width=480,
        height=520, 
    )

    return ft.View(
        route="/",
        controls=[
            ft.Column(
                [
                    ft.Container(
                        content=card,
                        alignment=ft.alignment.center,
                        expand=True,
                    ),
                    #Header.footer(),
                ],
                spacing=15,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
    )
