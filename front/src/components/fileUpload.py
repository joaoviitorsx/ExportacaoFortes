import flet as ft
from ..components.card import Card
from ..components.progressBar import ProgressBar


class UploadCard(Card):
    def __init__(self, on_file_selected=None):
        self.on_file_selected = on_file_selected

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

        # Texto que exibirá os nomes dos arquivos selecionados
        self.selected_files_text = ft.Text(
            "Nenhum arquivo selecionado",
            size=12,
            color=ft.Colors.GREY_700,
            italic=True,
        )

        # FilePicker
        self.file_picker = ft.FilePicker(on_result=self._on_files_picked)

        # Área de upload
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
                    self.selected_files_text,  # exibe os nomes dos arquivos
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

        upload_area.on_click = lambda _: self.file_picker.pick_files(
            allow_multiple=True,  # agora permite múltiplos arquivos
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
        )

        # ProgressBar
        self.progress = ProgressBar()
        self.progress.visible = False

        # Conteúdo do card
        content = ft.Column(
            [subtitle, description, upload_area, self.file_picker, self.progress],
            spacing=12,
        )

        super().__init__(title="Upload do Arquivo", content=content)

    # --- Métodos auxiliares ---
    def _on_files_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            filenames = [f.name for f in e.files]

            if len(filenames) == 1:
                display_text = filenames[0]
            else:
                primeiros = filenames[:3]
                restantes = len(filenames) - 3
                display_text = ", ".join(primeiros)
                if restantes > 0:
                    display_text += f" … mais {restantes} arquivo(s) selecionado(s)"

            self.selected_files_text.value = display_text
            self.update()

            # callback externo
            if self.on_file_selected:
                self.on_file_selected(filenames)
        else:
            self.selected_files_text.value = "Nenhum arquivo selecionado"
            self.update()

    def show_progress(self, visible=True):
        self.progress.visible = visible
        self.update()

    def update_progress(self, percent: int, message: str):
        self.progress.set_progress(percent, message)
        self.show_progress(True)
        self.update()
