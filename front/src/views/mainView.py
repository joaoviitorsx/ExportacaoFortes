import os
import re
import asyncio
from queue import Empty, Queue
import flet as ft
from front.src.utils.formtador import normalizarEmpresa

from ..components.card import Card
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao
from ..components.reconnectIndicator import ReconnectIndicator
from ..routes.fsRoute import FsRoute
from ..utils.cnpjFormatador import formatarCnpj


def MainView(page: ft.Page, id: int, nome_empresa: str, empresa_cnpj: str) -> ft.View:
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    selected_files = []
    processado_ok = False
    processando = False
    modo_botao = "processar"
    nome_display, cnpj_display = normalizarEmpresa(nome_empresa, empresa_cnpj)

    uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))

    btnProcessar = ActionButton("Processar Arquivo", icon=ft.Icons.PLAY_ARROW, disabled=True)

    def voltarParaEmpresas(e):
        page.go("/")

    def sanitizarNomeArquivo(texto: str) -> str:
        nome = (texto or "").strip()
        if not nome:
            return "Empresa"
        nome = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "", nome)
        nome = re.sub(r"\s+", " ", nome).strip().strip(".")
        return nome or "Empresa"

    def extrairFilialCnpj(cnpj: str) -> str:
        digitos = "".join(ch for ch in str(cnpj or "") if ch.isdigit())
        if len(digitos) == 14:
            filial_quatro = digitos[8:12]
            if filial_quatro.isdigit():
                return f"{int(filial_quatro) % 100:02d}"
        return "00"

    def construirNomeArquivoFs() -> str:
        razao = sanitizarNomeArquivo(nome_display or nome_empresa)
        filial = extrairFilialCnpj(cnpj_display)
        return f"ExportacaoFortes-{razao}-{filial}.fs"

    def construirCaminhoSaidaAutomatico(arquivos: list[str]) -> str:
        if not arquivos:
            raise ValueError("Nenhum arquivo SPED selecionado.")

        primeiro_arquivo = os.path.abspath(os.path.expanduser(arquivos[0]))
        diretorio_saida = os.path.dirname(primeiro_arquivo) or "."

        if not os.path.isdir(diretorio_saida):
            raise ValueError("Diretório do arquivo SPED não encontrado.")

        return os.path.join(diretorio_saida, construirNomeArquivoFs())

    def definirModoBotaoProcessar():
        nonlocal modo_botao
        modo_botao = "processar"
        btnProcessar.text = "Processar Arquivo"
        btnProcessar.icon = ft.Icons.PLAY_ARROW
        btnProcessar.disabled = not bool(selected_files)

    def definirModoBotaoResetar():
        nonlocal modo_botao
        modo_botao = "resetar"
        btnProcessar.text = "Processar Novamente"
        btnProcessar.icon = ft.Icons.REFRESH
        btnProcessar.disabled = False

    def resetarView():
        nonlocal selected_files, processado_ok, processando, modo_botao
        selected_files = []
        processado_ok = False
        processando = False
        modo_botao = "processar"
        uploaderCard.showUpload(_silent=True)
        btnProcessar.text = "Processar Arquivo"
        btnProcessar.icon = ft.Icons.PLAY_ARROW
        btnProcessar.disabled = True
        page.update()

    def fileSelected(filenames):
        nonlocal selected_files, processado_ok
        selected_files = list(filenames or [])
        processado_ok = False
        if not processando:
            definirModoBotaoProcessar()
        page.update()

    def aplicarProgressoPendente(fila_progresso: Queue):
        while True:
            try:
                percent, message = fila_progresso.get_nowait()
            except Empty:
                break

            try:
                percent_norm = int(percent)
            except Exception:
                percent_norm = 0

            percent_norm = max(0, min(100, percent_norm))
            uploaderCard.updateProgress(percent_norm, str(message))

    async def executarProcessamentoAsync(arquivos_processamento: list[str]):
        nonlocal processado_ok, processando
        fila_progresso = Queue()

        def progress_callback(percent: int, message: str):
            fila_progresso.put((percent, message))

        try:
            loop = asyncio.get_running_loop()
            future_processamento = loop.run_in_executor(
                None,
                lambda: FsRoute.processarFs(
                    empresa_id=id,
                    arquivos=arquivos_processamento,
                    output_path=None,
                    progress_callback=progress_callback,
                ),
            )

            while not future_processamento.done():
                aplicarProgressoPendente(fila_progresso)
                await asyncio.sleep(0.08)

            aplicarProgressoPendente(fila_progresso)
            resposta = await future_processamento

            if resposta["status"] != "ok":
                uploaderCard.showUpload(_silent=True)
                definirModoBotaoProcessar()
                notificacao(page, "Erro", resposta["mensagem"], tipo="erro")
                return

            try:
                caminho_saida = construirCaminhoSaidaAutomatico(arquivos_processamento)
            except ValueError as error_path:
                uploaderCard.showUpload(_silent=True)
                definirModoBotaoProcessar()
                notificacao(page, "Erro", str(error_path), tipo="erro")
                return

            uploaderCard.showDownloadProgress(True)
            page.update()

            resposta_download = await loop.run_in_executor(
                None,
                lambda: FsRoute.baixarFs(
                    empresa_id=id,
                    arquivos=arquivos_processamento,
                    output_path=caminho_saida,
                    progress_callback=None,
                ),
            )

            if resposta_download["status"] == "ok":
                processado_ok = True
                uploaderCard.finishDownloadProgress()
                definirModoBotaoResetar()
                notificacao(page, "Sucesso", f"Arquivo salvo em {caminho_saida}", tipo="sucesso")
            else:
                uploaderCard.showUpload(_silent=True)
                definirModoBotaoProcessar()
                notificacao(page, "Erro", resposta_download["mensagem"], tipo="erro")
        except Exception as e:
            uploaderCard.showUpload(_silent=True)
            definirModoBotaoProcessar()
            notificacao(page, "Erro", f"Falha ao processar arquivo: {str(e)}", tipo="erro")
        finally:
            processando = False
            if not processado_ok and modo_botao != "resetar":
                definirModoBotaoProcessar()
            try:
                page.update()
            except Exception as ex:
                print(f"[ERRO] page.update no finally falhou: {ex}")

    def processar(e):
        nonlocal processado_ok, processando

        try:
            if processando:
                return

            if modo_botao == "resetar" or processado_ok:
                resetarView()
                return

            if not selected_files:
                notificacao(page, "Erro", "Nenhum arquivo selecionado.", tipo="erro")
                return

            arquivos_processamento = list(selected_files)
            processando = True
            btnProcessar.disabled = True
            uploaderCard.disableRefresh()
            uploaderCard.showProgress(True)
            uploaderCard.progress.start()
            page.update()
            page.run_task(executarProcessamentoAsync, arquivos_processamento)
        except Exception as ex:
            print(f"[ERRO] Erro no handler processar: {ex}")
            import traceback
            traceback.print_exc()
            processando = False
            page.update()

    definirModoBotaoProcessar()
    btnProcessar.on_click = processar

    empresaCard = Card(
        title="Empresa Selecionada",
        icon=ft.Icons.BUSINESS,
        content=ft.Column(
            [
                ft.Text(nome_display or "", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Text(f"CNPJ: {formatarCnpj(cnpj_display)}", size=13, color=ft.Colors.GREY_700, visible=bool(cnpj_display)),
            ],
            spacing=6,
        ),
    )

    main_column = ft.Column(
        [
            ft.Container(
                alignment=ft.alignment.center_left,
                content=ft.TextButton(
                    "Voltar",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=voltarParaEmpresas,
                ),
            ),
            Header(),
            empresaCard,
            uploaderCard,
            ft.Row([btnProcessar], alignment=ft.MainAxisAlignment.CENTER),
            Header.footer(),
        ],
        spacing=20,
        expand=True,
    )

    return ft.View(route=f"/main?empresa={id}", controls=[main_column])
