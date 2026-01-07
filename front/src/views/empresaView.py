import flet as ft
from ..components.header import Header
from ..components.actionButton import ActionButton
from ..routes.empresaRoute import EmpresaRoute
from ..utils.path import resourcePath
from ..components.card import Card
from ..components.notificacao import notificacao
from ..components.reconnectIndicator import ReconnectIndicator
from back.src.utils.connectionMonitor import get_connection_monitor

def EmpresaView(page: ft.Page) -> ft.View:
    #page.title = "Selecionar Empresa"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    # Estado de reconexão
    is_reconnecting = False
    connection_monitor = get_connection_monitor()
    
    # Indicador de reconexão
    reconnect_indicator = ReconnectIndicator()

    empresas = EmpresaRoute.listarEmpresas()
    
    # Verificar se houve erro de conexão
    has_connection_error = isinstance(empresas, dict) and "erro" in empresas
    
    if has_connection_error:
        if empresas["erro"] == "vpn":
            notificacao(page, "Erro de Conexão", empresas["mensagem"], tipo="erro", duracao=6)
        else:
            notificacao(page, "Erro", empresas["mensagem"], tipo="erro", duracao=6)
        empresas = []

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
        disabled=has_connection_error,
    )

    btn_entrar = ActionButton("Entrar", disabled=True, color="primary")
    btn_cadastrar = ActionButton("Cadastrar Empresa", color="success")
    
    def reload_empresas():
        nonlocal empresas
        try:
            print("[DEBUG] Tentando recarregar empresas...")
            empresas_novas = EmpresaRoute.listarEmpresas()
            
            print(f"[DEBUG] Resultado: {type(empresas_novas)}")
            
            # Verificar se conseguiu conectar
            if not (isinstance(empresas_novas, dict) and "erro" in empresas_novas):
                print("[DEBUG] Conexão bem-sucedida! Atualizando interface...")
                empresas = empresas_novas
                
                # Atualizar dropdown
                dropdown.options = [
                    ft.dropdown.Option(
                        str(e["id"]),
                        f'{e["razao_social"]} - {e["cnpj"]}',
                        e["cnpj"]
                    ) for e in empresas
                ]
                dropdown.disabled = False
                
                print("[DEBUG] Empresas recarregadas com sucesso!")
                return True
            else:
                print(f"[DEBUG] Ainda sem conexão: {empresas_novas.get('mensagem', 'Erro desconhecido')}")
            return False
        except Exception as e:
            print(f"[ERRO] Falha ao recarregar empresas: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def start_reconnection_monitor():
        nonlocal is_reconnecting
        
        if is_reconnecting:
            print("[DEBUG] Monitoramento já está em andamento")
            return
        
        print("[DEBUG] Iniciando monitoramento de reconexão na view...")
        is_reconnecting = True
        reconnect_indicator.visible = True
        page.update()
        
        attempt_count = [0]  # Lista para permitir modificação em closure
        
        def on_retry(attempt: int):
            print(f"[DEBUG] on_retry chamado - tentativa {attempt}")
            attempt_count[0] = attempt
            reconnect_indicator.content.controls[1].value = f"Tentando reconectar... (tentativa {attempt})"
            page.update()
        
        def on_connected():
            nonlocal is_reconnecting
            print("[DEBUG] on_connected chamado! Atualizando interface...")
            is_reconnecting = False
            reconnect_indicator.visible = False
            notificacao(page, "Conexão Restabelecida", "Conectado com sucesso! Lista de empresas atualizada.", tipo="sucesso", duracao=4)
            page.update()
        
        await connection_monitor.monitor_and_retry(
            test_function=reload_empresas,
            on_connected=on_connected,
            on_retry=on_retry
        )
        
        print("[DEBUG] Monitoramento finalizado na view")

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
    
    # Se houver erro de conexão, iniciar monitoramento de reconexão
    if has_connection_error:
        page.run_task(start_reconnection_monitor)

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
            reconnect_indicator,  # Indicador de reconexão
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
