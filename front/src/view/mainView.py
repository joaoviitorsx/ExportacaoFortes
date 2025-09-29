import flet as ft
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..routes.fsRoute import FsRoute

def MainView(page: ft.Page):
    page.title = "Exportação SPED → Fortes Fiscal"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    btn_processar = ActionButton(
        "Processar Arquivo", icon=ft.Icons.PLAY_ARROW, disabled=True, color="primary"
    )
    btn_download = ActionButton(
        "Baixar Arquivo .fs", icon=ft.Icons.DOWNLOAD, visible=False, color="success"
    )

    # arquivos selecionados
    uploader_card = UploadCard(on_file_selected=lambda f: file_selected(f))

    selected_files = []

    def file_selected(filenames):
        nonlocal selected_files
        selected_files = filenames
        btn_processar.disabled = False
        btn_processar.text = "Processar Arquivo"
        btn_download.visible = False
        page.update()
        notificacao(page, "Arquivo selecionado", ", ".join(filenames), tipo="info")

    def resetarView():
        page.clean()
        MainView(page)

    def processar(e):
        if btn_processar.text == "Processar Novamente":
            resetarView()
            return

        if not selected_files:
            notificacao(page, "Erro", "Nenhum arquivo selecionado.", tipo="erro")
            return

        btn_processar.disabled = True
        uploader_card.disableRefresh()
        uploader_card.showProgress(True)
        page.update()

        # aqui o usuário escolhe onde salvar
        save_dialog = ft.FilePicker(on_result=salvarArquivo)
        page.overlay.append(save_dialog)
        page.update()
        save_dialog.save_file(
            file_name="Exportacao_Fortes.fs", allowed_extensions=["fs"]
        )

    def salvarArquivo(result: ft.FilePickerResultEvent):
        if result.path:
            resposta = FsRoute.processarFs(
                empresa_id=1,
                arquivos=selected_files,
                output_path=result.path,
            )

            if resposta["status"] == "ok":
                uploader_card.updateProgress(100, "Concluído!")
                notificacao(page, "Sucesso!", resposta["mensagem"], tipo="sucesso")
                btn_download.visible = True
                btn_processar.disabled = False
                btn_processar.text = "Processar Novamente"
            else:
                uploader_card.updateProgress(0, "Erro no processamento")
                notificacao(page, "Erro", resposta["mensagem"], tipo="erro")
                btn_processar.disabled = False

            page.update()

    btn_processar.on_click = processar

    page.add(
        ft.Column(
            [
                Header(),
                uploader_card,
                ft.Row(
                    [btn_processar, btn_download],
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
    )
