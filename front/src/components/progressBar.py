import flet as ft

class ProgressBar(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.bar = ft.ProgressBar(
            expand=True,
            height=12,
            value=0,
            bgcolor="#E0E0E0",
            border_radius=6,
        )

        self.status = ft.Text(
            "Aguardando processamento...",
            size=14,
            color=ft.Colors.GREY_600,
        )

        self.controls = [
            ft.Container(
                content=self.bar,
                padding=ft.padding.symmetric(horizontal=20),
                expand=True,
            ),
            self.status,
        ]

    def start(self):
        self.bar.value = 0
        self.status.value = "Iniciando..."
        self.update()

    def set_progress(self, percent: int, message: str):
        self.bar.value = percent / 100
        self.status.value = f"{message} ({percent}%)"
        self.update()

    def finish(self):
        self.bar.value = 1
        self.status.value = "Concluído!"
        self.update()


class DownloadProgressBar(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.bar = ft.ProgressBar(
            expand=True,
            height=12,
            color=ft.Colors.BLUE_600,
            bgcolor="#E0E0E0",
            border_radius=6,
            visible=False,
        )

        self.status = ft.Text("", size=14)

        self.controls = [
            ft.Container(
                content=self.bar,
                padding=ft.padding.symmetric(horizontal=20),
                expand=True,
            ),
            self.status,
        ]

    def start(self):
        self.bar.visible = True
        self.bar.value = None  # indeterminada
        self.status.value = "Gerando arquivo .fs..."
        self.status.color = ft.Colors.GREY_700
        self.update()

    def finish(self):
        self.bar.value = 1
        self.status.value = "Arquivo gerado com sucesso!"
        self.status.color = ft.Colors.GREEN_600
        self.update()

    def hide(self):
        self.bar.visible = False
        self.status.value = ""
        self.update()
