import flet as ft
from .mainView import MainView
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.empresaRoute import EmpresaRoute

def EmpresaView(page: ft.Page):
    page.title = "Selecionar Empresa"
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    empresas = EmpresaRoute.listar_empresas()
    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(e["id"]), e["razao_social"]) for e in empresas],
        width=300,
    )

    btn_entrar = ActionButton("Entrar", icon=ft.Icons.LOGIN, disabled=True, color="primary")
    btn_cadastrar = ActionButton("Cadastrar Empresa", icon=ft.Icons.ADD_BUSINESS, color="success")

    def on_change(e):
        btn_entrar.disabled = dropdown.value is None
        page.update()

    dropdown.on_change = on_change

    def entrar(e):
        if dropdown.value:
            empresa_id = int(dropdown.value)
            page.clean()
            MainView(page, empresa_id=empresa_id)

    def cadastrar(e):
        from .cadastroView import CadastroView
        page.clean()
        CadastroView(page)

    btn_entrar.on_click = entrar
    btn_cadastrar.on_click = cadastrar

    page.add(
        ft.Column(
            [
                ft.Text("Selecione a empresa", size=18, weight=ft.FontWeight.BOLD),
                dropdown,
                ft.Row([btn_entrar, btn_cadastrar], spacing=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )
