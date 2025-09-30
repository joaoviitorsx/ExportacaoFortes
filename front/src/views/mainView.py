import flet as ft
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.fsRoute import FsRoute

def MainView(page: ft.Page, id: int):
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

    def fileSelected(filenames):
        nonlocal selected_files
        selected_files = filenames
        btnProcessar.disabled = False
        btnProcessar.text = "Processar Arquivo"
        btnDownload.visible = False
        page.update()
        notificacao(page, "Arquivo selecionado", ", ".join(filenames), tipo="info")

    def resetarView():
        page.go(f"/main?empresa={id}")

    def processar(e):
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

        save_dialog = ft.FilePicker(on_result=salvarArquivo)
        page.overlay.append(save_dialog)
        page.update()
        save_dialog.save_file(
            file_name="Exportacao Fortes.fs", allowed_extensions=["fs"]
        )

    def salvarArquivo(result: ft.FilePickerResultEvent):
        if result.path:
            resposta = FsRoute.processarFs(
                empresa_id=id,
                arquivos=selected_files,
                output_path=result.path,
            )

            if resposta["status"] == "ok":
                uploaderCard.updateProgress(100, "Concluído!")
                notificacao(page, "Sucesso!", resposta["mensagem"], tipo="sucesso")
                btnDownload.visible = True
                btnProcessar.disabled = False
                btnProcessar.text = "Processar Novamente"
            else:
                uploaderCard.updateProgress(0, "Erro no processamento")
                notificacao(page, "Erro", resposta["mensagem"], tipo="erro")
                btnProcessar.disabled = False

            page.update()

    btnProcessar.on_click = processar
    btn_voltar = ActionButton("Voltar", icon=ft.Icons.ARROW_BACK, color=ft.Colors.BLUE_600)
    btn_voltar.on_click = lambda e: page.go("/")

    return ft.View(
        route=f"/main?empresa={id}",
        controls=[
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [btn_voltar],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.padding.only(bottom=10),
                    ),

                    Header(),
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
        ],
    )