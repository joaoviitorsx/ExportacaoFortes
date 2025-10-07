import os
import flet as ft

from ..components.card import Card
from ..routes.fsRoute import FsRoute
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao

def MainView(page: ft.Page, id: int, nome_empresa: str):
    page.title = "Exportação SPED → Fortes Fiscal"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    btnProcessar = ActionButton(
        "Processar Arquivo", icon=ft.Icons.PLAY_ARROW, disabled=True, color="primary"
    )
    btnDownload = ActionButton(
        "Baixar Arquivo .fs", icon=ft.Icons.DOWNLOAD, visible=False, color="success"
    )

    uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))
    selected_files = []
    processado_ok = False

    def fileSelected(filenames):
        nonlocal selected_files, processado_ok
        selected_files = filenames
        processado_ok = False
        btnProcessar.disabled = False
        btnProcessar.text = "Processar Arquivo"
        btnDownload.visible = False
        page.update()

        nomes_arquivos = [os.path.basename(path) for path in filenames]
        notificacao(page, "Arquivo selecionado", ", ".join(nomes_arquivos), tipo="info")

    def resetarView():
        nonlocal selected_files, processado_ok, uploaderCard
        selected_files = []
        processado_ok = False
        btnProcessar.disabled = True
        btnProcessar.text = "Processar Arquivo"
        btnDownload.visible = False
        
        uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))
        main_column.controls[3] = uploaderCard
        
        page.update()

    def processar(e):
        nonlocal processado_ok
        if btnProcessar.text == "Processar Novamente":
            resetarView()
            return

        if not selected_files:
            notificacao(page, "Erro", "Nenhum arquivo selecionado.", tipo="erro")
            return

        btnProcessar.disabled = True
        uploaderCard.disableRefresh()
        uploaderCard.showProgress(True)
        page.update()

        resposta = FsRoute.processarFs(
            empresa_id=id,
            arquivos=selected_files,
            output_path=None,
        )

        if resposta["status"] == "ok":
            for etapa in resposta.get("etapas", []):
                uploaderCard.updateProgress(etapa["percent"], etapa["mensagem"])
                page.update()
            btnDownload.visible = True
            btnProcessar.disabled = False
            btnProcessar.text = "Processar Novamente"
            processado_ok = True
            notificacao(page, "Sucesso!", resposta["mensagem"], tipo="sucesso")
        else:
            uploaderCard.updateProgress(0, "Erro no processamento")
            notificacao(page, "Erro", resposta["mensagem"], tipo="erro")
            btnProcessar.disabled = False
            processado_ok = False

        page.update()

    def escolherLocal(e):
        if not processado_ok:
            notificacao(page, "Erro", "Você precisa processar antes de baixar.", tipo="erro")
            return
        
        uploaderCard.showProgress(False)
        uploaderCard.showDownloadProgress(True)
        notificacao(page, "Aguarde", "Escolha o local para salvar o arquivo .fs", tipo="info")
        page.update()

        save_dialog = ft.FilePicker(on_result=salvarArquivo)
        page.overlay.append(save_dialog)
        page.update()
        save_dialog.save_file(
            file_name="Exportacao Fortes.fs", allowed_extensions=["fs"]
        )

    def salvarArquivo(result: ft.FilePickerResultEvent):
        uploaderCard.showDownloadProgress(False)
        if result.path:
            resposta = FsRoute.baixarFs(
                empresa_id=id,
                arquivos=selected_files,
                output_path=result.path,
            )

            if resposta["status"] == "ok":
                uploaderCard.finishDownloadProgress()
                notificacao(page, "Download pronto!", f"Arquivo salvo em {result.path}", tipo="sucesso")
            else:
                notificacao(page, "Erro", resposta["mensagem"], tipo="erro")

            page.update()

    card_empresa = Card(
        title=None,
        content=ft.Row(
            [
                ft.Text(f"Empresa: ", size=13, color=ft.Colors.GREY_700),
                ft.Text(f"{nome_empresa}", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Text(f"(ID: {id})", size=12, color=ft.Colors.GREY_500),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
        ),
        icon=None,
        height=None,
    )

    btnProcessar.on_click = processar
    btnDownload.on_click = escolherLocal

    btn_voltar = ActionButton("Voltar", color=ft.Colors.BLUE_600)
    btn_voltar.on_click = lambda e: page.go("/")

    main_column = ft.Column(
        [
            ft.Container(
                content=ft.Row([btn_voltar], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.only(bottom=10),
            ),
            Header(),
            card_empresa,
            uploaderCard,
             ft.Row(
                [btnProcessar, btnDownload],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            Header.footer(),
            ],
            spacing=17,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
    
    return ft.View(
        route=f"/main?empresa={id}",
        controls=[main_column],
    )
