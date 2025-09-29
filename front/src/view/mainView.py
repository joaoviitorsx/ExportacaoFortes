import time
import flet as ft

from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao


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

    def file_selected(filename):
        btn_processar.disabled = False
        btn_processar.text = "Processar Arquivo"
        btn_download.visible = False
        page.update()
        notificacao(page, "Arquivo selecionado", filename, tipo="info")

    uploader_card = UploadCard(on_file_selected=file_selected)

    def resetarView():
        page.clean()
        MainView(page)

    def processar(e):
        if btn_processar.text == "Processar Novamente":
            resetarView()
            return

        btn_processar.disabled = True
        page.update()

        uploader_card.disableRefresh() 
        uploader_card.showProgress(True)

        etapas = ["Lendo registros C100…", "Gerando PNM…", "Finalizando…"]
        for step, msg in enumerate(etapas, start=1):
            time.sleep(1.2)
            uploader_card.updateProgress(step * 30, msg)
            page.update()

        uploader_card.updateProgress(100, "Concluído!")
        notificacao(page, "Sucesso!", "Arquivo .fs gerado com sucesso.", tipo="sucesso")
        btn_download.visible = True

        btn_processar.disabled = False
        btn_processar.text = "Processar Novamente"
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
