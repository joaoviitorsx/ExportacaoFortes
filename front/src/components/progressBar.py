import flet as ft

class ProgressBar(ft.Column):
    def __init__(self):
        super().__init__(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        self.bar = ft.ProgressBar(width=400, value=0, bgcolor="#ddd")
        self.status = ft.Text("Aguardando processamento...", size=14, color="grey")

        self.steps = ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        self.controls = [self.bar, self.status, self.steps]

    def start(self):
        self.bar.value = 0
        self.status.value = "Iniciando..."
        self.steps.controls.clear()
        self.update()

    def set_progress(self, percent: int, message: str):
        self.bar.value = percent / 100
        self.status.value = message
        self.steps.controls.append(
            ft.Text(f"✔ {message}", size=12, color=ft.colors.GREY_800)
        )
        self.update()

    def finish(self):
        self.bar.value = 1
        self.status.value = "Concluído!"
        self.steps.controls.append(
            ft.Text("✔ Processamento finalizado com sucesso!", size=12, color=ft.colors.GREEN_600)
        )
        self.update()
