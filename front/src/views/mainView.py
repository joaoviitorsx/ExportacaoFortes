import os
import threading
import flet as ft

from ..components.card import Card
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..components.reconnectIndicator import ReconnectIndicator
from ..routes.fsRoute import FsRoute
from ..utils.ambiente import is_linux


def MainView(page: ft.Page, id: int, nome_empresa: str, empresa_cnpj: str) -> ft.View:
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    selected_files = []
    processado_ok = False

    uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))

    btnProcessar = ActionButton("Processar Arquivo", icon=ft.Icons.PLAY_ARROW, disabled=True)
    btnDownload = ActionButton("Baixar Arquivo .fs", icon=ft.Icons.DOWNLOAD, visible=False)

    def fileSelected(filenames):
        nonlocal selected_files, processado_ok
        selected_files = filenames
        processado_ok = False
        btnProcessar.disabled = False
        btnDownload.visible = False
        page.update()

    def processar(e):
        nonlocal processado_ok

        if not selected_files:
            notificacao(page, "Erro", "Nenhum arquivo selecionado.", tipo="erro")
            return

        btnProcessar.disabled = True
        uploaderCard.disableRefresh()
        uploaderCard.showProgress(True)
        page.update()

        def executar():
            nonlocal processado_ok
            resposta = FsRoute.processarFs(
                empresa_id=id,
                arquivos=selected_files,
                output_path=None,
                progress_callback=uploaderCard.updateProgress,
            )

            if resposta["status"] == "ok":
                processado_ok = True
                btnDownload.visible = True
                btnProcessar.text = "Processar Novamente"
                btnProcessar.icon = ft.Icons.REFRESH
                btnProcessar.disabled = False
                notificacao(page, "Sucesso", resposta["mensagem"], tipo="sucesso")
            else:
                uploaderCard.showUpload()
                btnProcessar.disabled = False
                notificacao(page, "Erro", resposta["mensagem"], tipo="erro")

            page.update()

        threading.Thread(target=executar, daemon=True).start()

    def escolherLocal(e):
        if not processado_ok:
            notificacao(page, "Erro", "Processamento necessário.", tipo="erro")
            return

        if is_linux():
            abrirModalSalvarLinux()
        else:
            picker = ft.FilePicker(on_result=salvarArquivo)
            page.overlay.append(picker)
            picker.save_file(file_name="Exportacao_Fortes.fs")

    def salvarArquivo(result: ft.FilePickerResultEvent):
        if result.path:
            iniciarDownload(result.path)

    def abrirModalSalvarLinux():
        campo = ft.TextField(
            label="Salvar como",
            hint_text="/home/usuario/Exportacao_Fortes.fs",
            autofocus=True,
        )

        def confirmar(e):
            path_raw = campo.value.strip()

            if not path_raw:
                campo.error_text = "Informe o caminho para salvar o arquivo"
                page.update()
                return

            path = os.path.expanduser(path_raw)

            if os.path.isdir(path):
                path = os.path.join(path, "Exportacao_Fortes.fs")

            if not path.lower().endswith(".fs"):
                path = f"{path}.fs"

            dir_name = os.path.dirname(path)
            if not os.path.isdir(dir_name):
                campo.error_text = "Diretório inválido ou inexistente"
                page.update()
                return

            campo.error_text = None
            iniciarDownload(os.path.abspath(path))

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Salvar arquivo"),
            content=campo,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fecharDialog()),
                ft.ElevatedButton("Salvar", on_click=confirmar),
            ],
        )

        if dialog not in page.overlay:
            page.overlay.append(dialog)
        page.dialog = dialog
        dialog.open = True
        page.update()

    def fecharDialog():
        if page.dialog:
            page.dialog.open = False
        page.update()

    def iniciarDownload(path):
        fecharDialog()
        uploaderCard.showDownloadProgress(True)

        def executar():
            resposta = FsRoute.baixarFs(
                empresa_id=id,
                arquivos=selected_files,
                output_path=path,
                progress_callback=None,
            )

            if resposta["status"] == "ok":
                uploaderCard.finishDownloadProgress()
                notificacao(page, "Sucesso", f"Arquivo salvo em {path}", tipo="sucesso")
            else:
                uploaderCard.showUpload()
                notificacao(page, "Erro", resposta["mensagem"], tipo="erro")

            page.update()

        threading.Thread(target=executar, daemon=True).start()

    btnProcessar.on_click = processar
    btnDownload.on_click = escolherLocal

    main_column = ft.Column(
        [
            Header(),
            uploaderCard,
            ft.Row([btnProcessar, btnDownload], alignment=ft.MainAxisAlignment.CENTER),
            Header.footer(),
        ],
        spacing=20,
        expand=True,
    )

    return ft.View(route=f"/main?empresa={id}", controls=[main_column])
