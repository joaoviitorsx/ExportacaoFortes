import flet as ft
from ..components.header import Header
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.empresaRoute import EmpresaRoute
from ..components.card import Card
from ..utils.cnpjFormatador import formatarCnpj


def CadastroView(page: ft.Page) -> ft.View:
    page.title = "Cadastro de Empresa"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    empresa_dados = {}

    cnpj_input = ft.TextField(
        label="Digite o CNPJ",
        width=400,
        height=50,
        border_radius=12,
        filled=True,
        fill_color=ft.Colors.WHITE,
    )

    def formataInput(e):
        valor = cnpj_input.value or ""
        cnpj_input.value = formatarCnpj(valor)
        page.update()

    cnpj_input.on_change = formataInput

    btn_salvar = ActionButton("Salvar", icon=ft.Icons.SAVE, color="primary", disabled=True)
    btn_voltar = ActionButton("Voltar", icon=ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_600)

    info_card = ft.Container(
        bgcolor=ft.Colors.GREY_50,
        border_radius=8,
        padding=15,
        content=None,
        visible=False,
        border=ft.border.all(1, ft.Colors.GREY_300)
    )

    def buscar_empresa(e):
        nonlocal empresa_dados
        cnpj = cnpj_input.value.strip()

        info_card.visible = False
        info_card.content = None
        btn_salvar.disabled = True
        page.update()

        if not cnpj:
            notificacao(page, "Erro", "Digite um CNPJ válido.", tipo="erro")
            return

        try:
            empresa_dados = EmpresaRoute.buscarCnpj(cnpj)

            if not empresa_dados:
                notificacao(page, "Erro", "Empresa não encontrada.", tipo="erro")
            else:
                info_card.content = ft.Column(
                    [
                        ft.Text(
                            f"Razão Social: {empresa_dados.get('razao_social', '-')}",
                            weight=ft.FontWeight.BOLD,
                            size=16,
                        ),
                        ft.Row([
                            ft.Text("CNPJ:", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{empresa_dados.get('cnpj', '-')}")
                        ]),
                        ft.Row([
                            ft.Text(f"UF:", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{empresa_dados.get('uf', '-')}"),
                        ]),
                        ft.Row([
                            ft.Text(f"Optante Simples:", weight=ft.FontWeight.BOLD),
                            ft.Text(f"{'Sim' if empresa_dados.get('simples') else 'Não'}")
                        ]),
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                )
                info_card.visible = True
                btn_salvar.disabled = False
                notificacao(page, "Sucesso", "Dados encontrados!", tipo="sucesso")

            page.update()

        except Exception as ex:
            notificacao(page, "Erro", str(ex), tipo="erro")

    def salvar(e):
        if not empresa_dados:
            notificacao(page, "Erro", "Nenhuma empresa carregada.", tipo="erro")
            return

        try:
            EmpresaRoute.cadastrarEmpresa(empresa_dados)
            notificacao(page, "Sucesso", "Empresa cadastrada com sucesso!", tipo="sucesso")
            page.go("/")
        except Exception as ex:
            notificacao(page, "Erro", str(ex), tipo="erro")

    def voltar(e):
        page.go("/")

    cnpj_input.on_submit = buscar_empresa
    cnpj_input.suffix = ft.IconButton(icon=ft.Icons.SEARCH, on_click=buscar_empresa)
    btn_salvar.on_click = salvar
    btn_voltar.on_click = voltar

    conteudo = ft.Column(
        [
            ft.Text(
                "Cadastrar nova empresa",
                size=20,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            cnpj_input,
            info_card,
            ft.Row(
                [btn_salvar, btn_voltar],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    card = Card(
        title="Cadastro de Empresa",
        content=conteudo,
        icon=ft.Icons.ADD_BUSINESS,
        width=500,
        height=420
    )

    return ft.View(
        route="/cadastro",
        controls=[
            ft.Column(
                [
                    ft.Container(height=64),
                    ft.Container(content=card, alignment=ft.alignment.center, expand=True),
                    Header.footer(),
                ],
                spacing=17,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
    )
