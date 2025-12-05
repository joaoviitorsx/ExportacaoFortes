import flet as ft
from ..components.header import Header
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.empresaRoute import EmpresaRoute
from ..components.card import Card
from ..utils.cnpjFormatador import formatarCnpj

def CadastroView(page: ft.Page) -> ft.View:
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

    # Checkbox para indicar se é filial
    is_filial_checkbox = ft.Checkbox(
        label="Esta empresa é filial?",
        value=False,
    )

    # Campo para CNPJ da matriz (inicialmente invisível)
    cnpj_matriz_input = ft.TextField(
        label="CNPJ da Matriz",
        width=400,
        height=50,
        border_radius=12,
        filled=True,
        fill_color=ft.Colors.WHITE,
        visible=False,
        hint_text="Digite o CNPJ da empresa matriz"
    )

    def formataInput(e):
        valor = cnpj_input.value or ""
        cnpj_input.value = formatarCnpj(valor)
        page.update()

    def formataCnpjMatriz(e):
        valor = cnpj_matriz_input.value or ""
        cnpj_matriz_input.value = formatarCnpj(valor)
        page.update()

    def on_filial_change(e):
        # Mostrar/ocultar campo de CNPJ da matriz
        cnpj_matriz_input.visible = is_filial_checkbox.value
        if not is_filial_checkbox.value:
            cnpj_matriz_input.value = ""
        page.update()

    cnpj_input.on_change = formataInput
    cnpj_matriz_input.on_change = formataCnpjMatriz
    is_filial_checkbox.on_change = on_filial_change

    btn_salvar = ActionButton(
        "Salvar", 
        icon=ft.Icons.SAVE, 
        color=ft.Colors.GREY_400,
        disabled=True
    )
    btn_voltar = ActionButton("Voltar", icon=ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_600)

    info_card = ft.Container(
        bgcolor=ft.Colors.GREY_50,
        border_radius=8,
        padding=15,
        content=None,
        visible=False,
        border=ft.border.all(1, ft.Colors.GREY_300),
        animate_opacity=300,
        animate_size=300,
    )

    def buscar_empresa(e):
        nonlocal empresa_dados
        cnpj = cnpj_input.value.strip()

        info_card.visible = False
        info_card.content = None
        btn_salvar.disabled = True
        btn_salvar.bgcolor = ft.Colors.GREY_400
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
                btn_salvar.bgcolor = ft.Colors.GREEN_600
                notificacao(page, "Sucesso", "Dados encontrados!", tipo="sucesso")

            page.update()

        except Exception as ex:
            notificacao(page, "Erro", str(ex), tipo="erro")

    def salvar(e):
        if not empresa_dados:
            notificacao(page, "Erro", "Nenhuma empresa carregada.", tipo="erro")
            return

        # Validar CNPJ da matriz se a empresa for filial
        if is_filial_checkbox.value:
            cnpj_matriz = cnpj_matriz_input.value.strip()
            if not cnpj_matriz:
                notificacao(page, "Erro", "Digite o CNPJ da matriz.", tipo="erro")
                return
            empresa_dados["cnpj_matriz"] = cnpj_matriz.replace(".", "").replace("/", "").replace("-", "")
        else:
            empresa_dados["cnpj_matriz"] = None

        try:
            resultado = EmpresaRoute.cadastrarEmpresa(empresa_dados)
            if resultado and resultado.get("status") == "erro":
                notificacao(page, "Info", resultado.get("mensagem", "Empresa já cadastrada."), tipo="info")
            elif resultado and resultado.get("status") == "ok":
                msg = "Empresa cadastrada com sucesso!"
                notificacao(page, "Sucesso", msg, tipo="sucesso")
                page.go("/")
            else:
                notificacao(page, "Erro", "Erro ao cadastrar empresa.", tipo="erro")
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
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Cadastrar nova empresa",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [cnpj_input],
                        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [info_card],
                        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [is_filial_checkbox],
                        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [cnpj_matriz_input],
                        col={"xs": 12, "sm": 12, "md": 12, "lg": 12, "xl": 12},
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ResponsiveRow(
                [
                    ft.Row(
                        [btn_voltar, btn_salvar],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
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
    )

    return ft.View(
        route="/cadastro",
        controls=[
            ft.Column(
                [
                    ft.Container(height=64),
                    ft.Container(
                        content=card, 
                        alignment=ft.alignment.center, 
                        expand=True,
                        padding=ft.padding.symmetric(vertical=20)
                    ),
                    Header.footer(),
                ],
                spacing=17,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            )
        ],
    )