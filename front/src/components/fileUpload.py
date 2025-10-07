import flet as ft
from ..components.card import Card
from ..components.progressBar import ProgressBar, DownloadProgressBar

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
                        ft.Icon(name=ft.Icons.FILE_PRESENT, size=30, color=ft.Colors.GREEN_600),
                        ft.Text("Arquivos Selecionados", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
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
                            ft.Text(nome, size=13, color=ft.Colors.GREY_700, selectable=True)
                            for nome in primeiros
                        ] +
                        (
                            [ft.Text(f"… mais {restantes} arquivo(s) selecionado(s)", size=13, color=ft.Colors.GREY_700, selectable=True)]
                            if restantes > 0 else []
                        ),
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=5,
                        run_spacing=0,
                    ),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    expand=True,
                )
            ],
            spacing=16
        )
        super().__init__(title=None, content=content)

class UploadCard(Card):
    def __init__(self, on_file_selected=None):
        self.on_file_selected = on_file_selected
        self.selected_files = []
        self.selected_path = []
        self.files_card = None

        self.file_picker = ft.FilePicker(on_result=self.filesPicked)
        self.upload_area = UploadArea(self._pick_files)
        self.progress = ProgressBar()
        self.progress.visible = False

        self.download_progress = DownloadProgressBar()
        self.download_progress.visible = False

        self.content_column = ft.Column(
            [
                ft.Text("Selecionar Arquivo SPED", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Text("Selecione um arquivo .txt do SPED para processamento", size=13, color=ft.Colors.GREY_600),
                self.upload_area,
                self.file_picker,
                self.progress,
                self.download_progress,
            ],
            spacing=12,
        )

        super().__init__(title="Upload do Arquivo", content=self.content_column, icon=ft.Icons.INSERT_DRIVE_FILE_ROUNDED)

    def _pick_files(self, _):
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
            self.selected_files = []
            self.selected_paths = []
            self.showUpload()

    def showFiles(self):
        self.files_card = SelectedFilesCard(self.selected_files, self.showUpload)
        self.content_column.controls[2] = self.files_card
        self.update()

    def disableRefresh(self):
        if self.files_card and self.files_card.refreshButton:
            self.files_card.refreshButton.disabled = True
            self.files_card.refreshButton.visible = False
            self.files_card.refreshButton.update()

    def showUpload(self, _=None):
        self.selected_files = []
        self.content_column.controls[2] = self.upload_area
        self.update()

    def showProgress(self, visible=True):
        self.progress.visible = visible
        self.update()

    def updateProgress(self, percent: int, message: str):
        self.progress.set_progress(percent, message)
        self.showProgress(True)
        self.update()

    def showDownloadProgress(self, visible=True):
        self.download_progress.visible = visible
        if visible:
            self.download_progress.start()
        self.update()

    def updateDownloadProgress(self, percent: int, message: str):
        self.download_progress.set_progress(percent, message)
        self.showDownloadProgress(True)
        self.update()

    def finishDownloadProgress(self):
        self.download_progress.finish()
        self.update()