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
        page.update()
        notificacao(page, "Arquivo selecionado", filename, tipo="info")

    uploader_card = UploadCard(on_file_selected=file_selected)

    def processar(e):
        btn_processar.disabled = True
        page.update()

        uploader_card.show_progress(True)

        etapas = ["Lendo registros C100…", "Gerando PNM…", "Finalizando…"]
        for step, msg in enumerate(etapas, start=1):
            time.sleep(1.2)
            uploader_card.update_progress(step * 30, msg)
            notificacao(page, "Processando", msg, tipo="info", duracao=2)
            page.update()

        uploader_card.update_progress(100, "Concluído!")
        notificacao(page, "Sucesso!", "Arquivo .fs gerado com sucesso.", tipo="sucesso")
        btn_download.visible = True
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
            ],
            spacing=40,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
