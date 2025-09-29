import flet as ft
from .empresaView import EmpresaView
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.empresaRoute import EmpresaRoute

def CadastroView(page: ft.Page):
    page.title = "Cadastro de Empresa"
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    cnpj_input = ft.TextField(label="CNPJ", width=400)

    btn_salvar = ActionButton("Salvar", icon=ft.Icons.SAVE, color="primary")
    btn_voltar = ActionButton("Voltar", icon=ft.Icons.ARROW_BACK, color="secondary")

    def salvar(e):
        cnpj = cnpj_input.value.strip()

        if not cnpj:
            notificacao(page, "Erro", "Preencha todos os campos.", tipo="erro")
            return

        try:
            EmpresaRoute.cadastrar_empresa(cnpj)
            notificacao(page, "Sucesso", "Empresa cadastrada com sucesso!", tipo="sucesso")
            page.clean()
            EmpresaView(page)
        except Exception as ex:
            notificacao(page, "Erro", str(ex), tipo="erro")

    def voltar(e):
        from .empresaView import EmpresaView
        page.clean()
        EmpresaView(page)

    btn_salvar.on_click = salvar
    btn_voltar.on_click = voltar

    page.add(
        ft.Column(
            [
                ft.Text("Cadastrar nova empresa", size=18, weight=ft.FontWeight.BOLD),
                cnpj_input,
                ft.Row([btn_salvar, btn_voltar], spacing=20),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )
