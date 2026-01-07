import flet as ft
from ..components.header import Header
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.empresaRoute import EmpresaRoute
from ..components.card import Card
from ..utils.cnpjFormatador import formatarCnpj
from ..components.reconnectIndicator import ReconnectIndicator
from back.src.utils.connectionMonitor import get_connection_monitor

def CadastroView(page: ft.Page) -> ft.View:
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    empresa_dados = {}
    is_reconnecting = False
    connection_monitor = get_connection_monitor()
    
    # Indicador de reconexão
    reconnect_indicator = ReconnectIndicator()

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

    btn_salvar = ActionButton(
        "Salvar", 
        icon=ft.Icons.SAVE, 
        color=ft.Colors.GREY_400,
        disabled=True
    )
    btn_voltar = ActionButton("Voltar", icon=ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_600)
    
    async def start_reconnection_monitor():
        """Inicia o monitoramento de reconexão"""
        nonlocal is_reconnecting
        
        if is_reconnecting:
            print("[DEBUG] Monitoramento já está em andamento (cadastro)")
            return
        
        print("[DEBUG] Iniciando monitoramento de reconexão no cadastro...")
        is_reconnecting = True
        reconnect_indicator.visible = True
        page.update()
        
        attempt_count = [0]
        
        def test_connection():
            """Testa a conexão tentando buscar empresas"""
            print("[DEBUG] Testando conexão no cadastro...")
            result = EmpresaRoute.listarEmpresas()
            is_ok = not (isinstance(result, dict) and "erro" in result)
            print(f"[DEBUG] Resultado do teste: {is_ok}")
            return is_ok
        
        def on_retry(attempt: int):
            print(f"[DEBUG] on_retry (cadastro) - tentativa {attempt}")
            attempt_count[0] = attempt
            reconnect_indicator.content.controls[1].value = f"Tentando reconectar... (tentativa {attempt})"
            page.update()
        
        def on_connected():
            nonlocal is_reconnecting
            print("[DEBUG] on_connected (cadastro) chamado!")
            is_reconnecting = False
            reconnect_indicator.visible = False
            notificacao(page, "Conexão Restabelecida", "Conectado com sucesso! Você já pode usar o sistema.", tipo="sucesso", duracao=4)
            page.update()
        
        await connection_monitor.monitor_and_retry(
            test_function=test_connection,
            on_connected=on_connected,
            on_retry=on_retry
        )
        
        print("[DEBUG] Monitoramento finalizado no cadastro")

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
            
            # Verificar se houve erro de conexão
            if isinstance(empresa_dados, dict) and "erro" in empresa_dados:
                if empresa_dados["erro"] == "vpn":
                    notificacao(page, "Erro de Conexão", empresa_dados["mensagem"], tipo="erro", duracao=6)
                    # Iniciar monitoramento de reconexão
                    page.run_task(start_reconnection_monitor)
                else:
                    notificacao(page, "Erro", empresa_dados["mensagem"], tipo="erro")
                return

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

        try:
            resultado = EmpresaRoute.cadastrarEmpresa(empresa_dados)
            
            # Verificar se houve erro de conexão
            if isinstance(resultado, dict) and "erro" in resultado:
                if resultado["erro"] == "vpn":
                    notificacao(page, "Erro de Conexão", resultado["mensagem"], tipo="erro", duracao=6)
                    # Iniciar monitoramento de reconexão
                    page.run_task(start_reconnection_monitor)
                elif resultado["erro"] == "geral":
                    notificacao(page, "Erro", resultado["mensagem"], tipo="erro")
                return
            
            if resultado and resultado.get("status") == "erro":
                notificacao(page, "Info", resultado.get("mensagem", "Empresa já cadastrada."), tipo="info")
            elif resultado and resultado.get("status") == "ok":
                tipo = resultado.get("tipo", "empresa")
                msg = f"Empresa cadastrada como {tipo.upper()}!"
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
            reconnect_indicator,  # Indicador de reconexão
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