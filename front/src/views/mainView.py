import os
import threading
import flet as ft
from urllib.parse import urlparse, unquote
from front.src.utils.formtador import normalizarEmpresa

from ..components.card import Card
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..components.reconnectIndicator import ReconnectIndicator
from ..routes.fsRoute import FsRoute
from ..utils.ambiente import is_linux
from ..utils.cnpjFormatador import formatarCnpj
from ..utils.filePicker import save_file_with_fallback


def MainView(page: ft.Page, id: int, nome_empresa: str, empresa_cnpj: str) -> ft.View:
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    selected_files = []
    processado_ok = False

    uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))

    btnProcessar = ActionButton("Processar Arquivo", icon=ft.Icons.PLAY_ARROW, disabled=True)
    btnDownload = ActionButton("Baixar Arquivo .fs", icon=ft.Icons.DOWNLOAD, visible=False)

    def normalizarPathRetornadoPicker(path_raw: str) -> str:
        path_limpo = str(path_raw).strip().strip('"').strip("'")

        if path_limpo.lower().startswith("file://"):
            parsed = urlparse(path_limpo)
            uri_path = unquote(parsed.path or "")
            if os.name == "nt" and uri_path.startswith("/") and len(uri_path) > 2 and uri_path[2] == ":":
                uri_path = uri_path[1:]
            if uri_path:
                path_limpo = uri_path

        return path_limpo

    def normalizarCaminhoSaida(path_raw: str) -> str:
        if not path_raw:
            raise ValueError("Caminho de saída inválido.")

        path = normalizarPathRetornadoPicker(path_raw)
        path = os.path.abspath(os.path.expanduser(path))

        if os.path.isdir(path):
            path = os.path.join(path, "Exportacao_Fortes.fs")

        if not path.lower().endswith(".fs"):
            path = f"{path}.fs"

        dir_name = os.path.dirname(path) or "."
        if not os.path.isdir(dir_name):
            raise ValueError("Diretório inválido ou inexistente.")

        return path

    def extrairCaminhoDownload(result: ft.FilePickerResultEvent | None) -> str | None:
        if result is None:
            return None

        path = getattr(result, "path", None)
        if path:
            return path

        files = getattr(result, "files", None) or []
        if files:
            arquivo = files[0]
            file_path = getattr(arquivo, "path", None)
            if file_path:
                return file_path

        return None

    def resetarView():
        nonlocal selected_files, processado_ok
        selected_files = []
        processado_ok = False
        uploaderCard.showUpload()
        btnProcessar.text = "Processar Arquivo"
        btnProcessar.icon = ft.Icons.PLAY_ARROW
        btnProcessar.disabled = True
        btnDownload.visible = False
        page.update()

    def fileSelected(filenames):
        nonlocal selected_files, processado_ok
        selected_files = filenames
        processado_ok = False
        btnProcessar.disabled = False
        btnDownload.visible = False
        page.update()

    def processar(e):
        nonlocal processado_ok

        if processado_ok:
            resetarView()
            return

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
                btnDownload.disabled = False
                btnDownload.on_click = escolherLocal
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
        print("[DEBUG] Clique no botão 'Baixar Arquivo .fs'")
        if not processado_ok:
            notificacao(page, "Erro", "Processamento necessário.", tipo="erro")
            return

        upload_picker = uploaderCard.file_picker

        def restaurarPickerUpload():
            upload_picker.on_result = uploaderCard.filesPicked

        def abrirFallbackSalvar():
            restaurarPickerUpload()
            abrirModalSalvarLinux()

        upload_picker.on_result = salvarArquivo
        save_file_with_fallback(
            page=page,
            on_result=salvarArquivo,
            file_name="Exportacao_Fortes.fs",
            allowed_extensions=["fs"],
            dialog_title="Salvar arquivo de exportação (.fs)",
            fallback_open_manual=abrirFallbackSalvar if is_linux() else None,
            picker=upload_picker,
        )

    def salvarArquivo(result: ft.FilePickerResultEvent):
        uploaderCard.file_picker.on_result = uploaderCard.filesPicked
        path_raw = extrairCaminhoDownload(result)
        print(f"[DEBUG] Resultado seletor recebido: path={getattr(result, 'path', None)}")

        if not path_raw:
            notificacao(page, "Aviso", "Download cancelado.", tipo="info")
            return

        try:
            path = normalizarCaminhoSaida(path_raw)
        except ValueError as e:
            notificacao(page, "Erro", str(e), tipo="erro")
            return

        iniciarDownload(path)

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

            try:
                path = normalizarCaminhoSaida(path_raw)
            except ValueError as e:
                campo.error_text = str(e)
                page.update()
                return

            campo.error_text = None
            iniciarDownload(path)

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
        print(f"[DEBUG] Iniciando geração FS em: {path}")
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

    nome_display, cnpj_display = normalizarEmpresa(nome_empresa, empresa_cnpj)

    empresaCard = Card(
        title="Empresa Selecionada",
        icon=ft.Icons.BUSINESS,
        content=ft.Column(
            [
                ft.Text(nome_display or "", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Text(f"CNPJ: {formatarCnpj(cnpj_display)}", size=13, color=ft.Colors.GREY_700, visible=bool(cnpj_display)),
            ],
            spacing=6,
        ),
    )

    main_column = ft.Column(
        [
            Header(),
            empresaCard,
            uploaderCard,
            ft.Row([btnProcessar, btnDownload], alignment=ft.MainAxisAlignment.CENTER),
            Header.footer(),
        ],
        spacing=20,
        expand=True,
    )

    return ft.View(route=f"/main?empresa={id}", controls=[main_column])
