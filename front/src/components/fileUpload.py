import flet as ft
from ..components.card import Card
from ..components.progressBar import ProgressBar


class UploadCard(Card):
    def __init__(self, on_file_selected=None):
        subtitle = ft.Text(
            "Selecionar Arquivo SPED",
            size=15,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK87,
        )

        description = ft.Text(
            "Selecione um arquivo .txt do SPED para processamento",
            size=13,
            color=ft.Colors.GREY_600,
        )

        file_picker = ft.FilePicker(
            on_result=lambda e: on_file_selected(e.files[0].name) if e.files else None
        )

        upload_area = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.UPLOAD_FILE, size=40, color=ft.Colors.BLUE_GREY),
                    ft.Text(
                        "Clique para selecionar ou arraste o arquivo aqui",
                        size=13,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Apenas arquivos .txt são aceitos",
                        size=11,
                        color=ft.Colors.GREY_500,
                        italic=True,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=8,
            padding=30,
            margin=ft.margin.only(top=10),
            alignment=ft.alignment.center,
        )

        upload_area.on_click = lambda _: file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
        )

        self.progress = ProgressBar()
        self.progress.visible = False

        content = ft.Column(
            [subtitle, description, upload_area, file_picker, self.progress],
            spacing=12,
        )

        super().__init__(title="Upload do Arquivo", content=content)

    def show_progress(self, visible=True):
        self.progress.visible = visible
        self.update()

    def update_progress(self, percent: int, message: str):
        self.progress.set_progress(percent, message)
        self.show_progress(True)
        self.update()
