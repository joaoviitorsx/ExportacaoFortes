import flet as ft
from ..components.card import Card
from ..components.progressBar import ProgressBar

class UploadArea(ft.Container):
    def __init__(self, on_pick):
        super().__init__(
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
            on_click=on_pick,
        )

class SelectedFilesCard(Card):
    def __init__(self, filenames, on_back):
        if len(filenames) == 1:
            display_text = filenames[0]
        else:
            primeiros = filenames[:3]
            restantes = len(filenames) - 3
            display_text = "\n".join(primeiros)
            if restantes > 0:
                display_text += f"\n … mais {restantes} arquivo(s) selecionado(s)"

        content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.FILE_PRESENT, size=30, color=ft.Colors.GREEN_600),
                        ft.Text("Arquivos Selecionados", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Voltar",
                            on_click=on_back,
                            icon_color=ft.Colors.BLUE_600,
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

        self.file_picker = ft.FilePicker(on_result=self.filesPicked)
        self.upload_area = UploadArea(self._pick_files)
        self.progress = ProgressBar()
        self.progress.visible = False

        self.content_column = ft.Column(
            [
                ft.Text("Selecionar Arquivo SPED", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Text("Selecione um arquivo .txt do SPED para processamento", size=13, color=ft.Colors.GREY_600),
                self.upload_area,
                self.file_picker,
                self.progress,
            ],
            spacing=12,
        )

        super().__init__(title="Upload do Arquivo", content=self.content_column)

    def _pick_files(self, _):
        self.file_picker.pick_files(
            allow_multiple=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
        )

    def filesPicked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_files = [f.name for f in e.files]
            self.showFiles()
            if self.on_file_selected:
                self.on_file_selected(self.selected_files)
        else:
            self.selected_files = []
            self.showUpload()

    def showFiles(self):
        self.content_column.controls[2] = SelectedFilesCard(self.selected_files, self.showUpload)
        self.update()

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