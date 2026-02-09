import os
import flet as ft

from ..components.card import Card
from ..components.progressBar import ProgressBar, DownloadProgressBar
from ..utils.ambiente import is_linux


class UploadArea(ft.Container):
    def __init__(self, on_pick):
        super().__init__(
            content=ft.Column(
                [
                    ft.Icon(name=ft.Icons.UPLOAD_FILE, size=40, color=ft.Colors.BLUE_GREY),
                    ft.Text(
                        "Clique para selecionar",
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
            on_click=on_pick,
        )


class SelectedFilesCard(Card):
    def __init__(self, filenames, on_back):
        primeiros = filenames[:3]
        restantes = len(filenames) - 3

        self.refreshButton = ft.IconButton(
            icon=ft.Icons.REFRESH,
            tooltip="Voltar",
            on_click=on_back,
            icon_color=ft.Colors.BLUE_600,
        )

        content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(
                            name=ft.Icons.FILE_PRESENT,
                            size=30,
                            color=ft.Colors.GREEN_600,
                        ),
                        ft.Text(
                            "Arquivos Selecionados",
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK87,
                        ),
                        ft.Container(
                            content=self.refreshButton,
                            width=40,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text(
                                nome,
                                size=13,
                                color=ft.Colors.GREY_700,
                                selectable=True,
                            )
                            for nome in primeiros
                        ]
                        + (
                            [
                                ft.Text(
                                    f"… mais {restantes} arquivo(s) selecionado(s)",
                                    size=13,
                                    color=ft.Colors.GREY_700,
                                    selectable=True,
                                )
                            ]
                            if restantes > 0
                            else []
                        ),
                        spacing=5,
                    ),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                ),
            ],
            spacing=16,
        )

        super().__init__(title=None, content=content)


class UploadCard(Card):
    def __init__(self, on_file_selected=None):
        self.on_file_selected = on_file_selected
        self.selected_files = []
        self.selected_paths = []
        self.files_card = None

        self.file_picker = ft.FilePicker(on_result=self.filesPicked)
        self.upload_area = UploadArea(self._pick_files)

        self.progress = ProgressBar()
        self.download_progress = DownloadProgressBar()

        self.main_content = ft.Column(
            [
                ft.Text(
                    "Selecionar Arquivo SPED",
                    size=15,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Selecione um arquivo .txt do SPED para processamento",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                self.upload_area,
            ],
            spacing=12,
        )

        self.content_column = ft.Column(
            [self.main_content, self.file_picker],
            spacing=12,
        )

        super().__init__(
            title="Upload do Arquivo",
            content=self.content_column,
            icon=ft.Icons.INSERT_DRIVE_FILE_ROUNDED,
        )

    # =========================
    # UPLOAD
    # =========================

    def _pick_files(self, e):
        if not self.page and e and hasattr(e, "page"):
            self.page = e.page

        if is_linux():
            self._open_path_modal()
        else:
            self.file_picker.pick_files(
                allow_multiple=True,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["txt"],
            )

    def filesPicked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_files = [f.name for f in e.files]
            self.selected_paths = [f.path for f in e.files]
            self.showFiles()

            if self.on_file_selected:
                self.on_file_selected(self.selected_paths)
        else:
            self.showUpload()

    # =========================
    # MODAL LINUX
    # =========================

    def _open_path_modal(self):
        if not self.page and self.upload_area.page:
            self.page = self.upload_area.page

        self.path_field = ft.TextField(
            label="Caminho do arquivo SPED (.txt)",
            hint_text="/home/usuario/arquivo.txt",
            autofocus=True,
        )

        self.path_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Selecionar arquivo (Linux)"),
            content=self.path_field,
            actions=[
                ft.TextButton("Cancelar", on_click=self._close_dialog),
                ft.ElevatedButton("Confirmar", on_click=self._confirm_path),
            ],
        )

        if self.path_dialog not in self.page.overlay:
            self.page.overlay.append(self.path_dialog)
        self.page.dialog = self.path_dialog
        self.path_dialog.open = True
        self.page.update()

    def _confirm_path(self, e):
        path = os.path.expanduser(self.path_field.value.strip())

        if not path:
            self.path_field.error_text = "Informe o caminho do arquivo .txt"
            self.page.update()
            return

        if not path.lower().endswith(".txt"):
            self.path_field.error_text = "O arquivo deve ter extensão .txt"
            self.page.update()
            return

        if not os.path.isfile(path):
            self.path_field.error_text = "Arquivo não encontrado"
            self.page.update()
            return

        self.path_field.error_text = None
        self._close_dialog()

        normalized_path = os.path.abspath(path)
        self.selected_files = [os.path.basename(normalized_path)]
        self.selected_paths = [normalized_path]
        self.showFiles()

        if self.on_file_selected:
            self.on_file_selected(self.selected_paths)

    def _close_dialog(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
        self.page.update()

    # =========================
    # UI STATES
    # =========================

    def showFiles(self):
        self.files_card = SelectedFilesCard(self.selected_files, self.showUpload)
        self.main_content.controls = [
            ft.Text("Selecionar Arquivo SPED", size=15, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Arquivos selecionados com sucesso",
                size=13,
                color=ft.Colors.GREY_600,
            ),
            self.files_card,
        ]
        self.update()

    def disableRefresh(self):
        if self.files_card:
            self.files_card.refreshButton.disabled = True
            self.files_card.refreshButton.visible = False
            self.update()

    def showUpload(self, e=None):
        self.selected_files = []
        self.selected_paths = []
        self.main_content.controls = [
            ft.Text("Selecionar Arquivo SPED", size=15, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Selecione um arquivo .txt do SPED para processamento",
                size=13,
                color=ft.Colors.GREY_600,
            ),
            self.upload_area,
        ]
        self.update()

    # =========================
    # PROGRESS
    # =========================

    def showProgress(self, visible=True):
        if visible:
            self.progress = ProgressBar()
            self.main_content.controls = [
                ft.Text("Processando Arquivo", size=15, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Aguarde enquanto processamos o arquivo",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                self.progress,
            ]
            self.update()

    def updateProgress(self, percent: int, message: str):
        self.progress.bar.value = percent / 100
        self.progress.status.value = f"{message} ({percent}%)"
        self.update()

    # =========================
    # DOWNLOAD
    # =========================

    def showDownloadProgress(self, visible=True):
        if visible:
            self.download_progress = DownloadProgressBar()
            self.main_content.controls = [
                ft.Text("Gerando Arquivo .fs", size=15, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Aguarde enquanto geramos o arquivo",
                    size=13,
                    color=ft.Colors.GREY_600,
                ),
                self.download_progress,
            ]
            self.update()
            self.download_progress.start()
        else:
            self.showFiles()

    def finishDownloadProgress(self):
        self.download_progress.finish()
        self.update()
