import flet as ft

class ProgressBar(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.bar = ft.ProgressBar(width=620, height=12, value=0, bgcolor="#ddd", border_radius=6)
        self.status = ft.Text("Aguardando processamento...", size=14, color="grey")

        self.controls = [
            self.bar,
            self.status
        ]

    def start(self):
        self.bar.value = 0
        self.status.value = "Iniciando..."
        self.update()

    def set_progress(self, percent: int, message: str):
        self.bar.value = percent / 100
        self.status.value = message
        self.update()

    def finish(self):
        self.bar.value = 1
        self.status.value = "Concluído!"
        self.update()

class DownloadProgressBar(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.bar = ft.ProgressBar(width=620, height=12, value=0, bgcolor="#ddd", border_radius=6)
        self.status = ft.Text("Preparando download...", size=14, color="grey")

        self.controls = [
            self.bar,
            self.status
        ]

    def start(self):
        self.bar.value = 0
        self.status.value = "Gerando o arquivo..."
        self.update()

    def set_progress(self, percent: int, message: str):
        self.bar.value = percent / 100
        self.status.value = message
        self.update()

    def finish(self):
        self.bar.value = 1
        self.status.value = "Arquivo gerado com sucesso!"
        self.update()