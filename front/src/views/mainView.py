import os
import asyncio
import flet as ft
import threading

from ..components.card import Card
from ..routes.fsRoute import FsRoute
from ..components.header import Header
from ..components.fileUpload import UploadCard
from ..components.actionButton import ActionButton
from ..components.notificacao import notificacao

def MainView(page: ft.Page, id: int, nome_empresa: str, empresa_cnpj: str) -> ft.View:
    #page.title = "Exportação SPED → Fortes Fiscal"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#F5F6FA"
    page.padding = 30

    btnProcessar = ActionButton(
        "Processar Arquivo", icon=ft.icons.PLAY_ARROW, disabled=True, color="primary"
    )
    btnDownload = ActionButton(
        "Baixar Arquivo .fs", icon=ft.icons.DOWNLOAD, visible=False, color="success"
    )

    uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))
    selected_files = []
    processado_ok = False

    def fileSelected(filenames):
        nonlocal selected_files, processado_ok
        selected_files = filenames
        processado_ok = False
        btnProcessar.disabled = False
        btnProcessar.text = "Processar Arquivo"
        btnDownload.visible = False
        page.update()

        nomes_arquivos = [os.path.basename(path) for path in filenames]
        notificacao(page, "Arquivo selecionado", ", ".join(nomes_arquivos), tipo="info")

    def resetarView():
        nonlocal selected_files, processado_ok, uploaderCard
        selected_files = []
        processado_ok = False
        btnProcessar.disabled = True
        btnProcessar.text = "Processar Arquivo"
        btnDownload.visible = False
        uploaderCard = UploadCard(on_file_selected=lambda f: fileSelected(f))
        main_column.controls[3] = uploaderCard
        page.update()

    def processar(e):
        nonlocal processado_ok

        if btnProcessar.text == "Processar Novamente":
            resetarView()
            btnProcessar.icon = ft.icons.PLAY_ARROW
            page.update()
            return

        if not selected_files:
            notificacao(page, "Erro", "Nenhum arquivo selecionado.", tipo="erro")
            return

        btnProcessar.disabled = True
        uploaderCard.disableRefresh()
        uploaderCard.showProgress(True)
        page.update()
        
        def atualizar_progresso(percent: int, mensagem: str):
            try:
                uploaderCard.updateProgress(percent, mensagem)
                page.update()  # Força atualização da página
            except Exception as e:
                print(f"[ERRO] Falha ao atualizar progresso: {e}")

        def executarThread():
            nonlocal processado_ok
            try:
                resposta = FsRoute.processarFs(
                    empresa_id=id,
                    arquivos=selected_files,
                    output_path=None,
                    progress_callback=atualizar_progresso
                )

                if resposta["status"] == "ok":
                    btnDownload.visible = True
                    btnProcessar.disabled = False
                    btnProcessar.text = "Processar Novamente"
                    btnProcessar.icon = ft.icons.REFRESH
                    processado_ok = True
                    notificacao(page, "Sucesso!", resposta["mensagem"], tipo="sucesso")
                else:
                    uploaderCard.showProgress(False)
                    uploaderCard.showFiles()
                    notificacao(page, "Erro de Validação", resposta["mensagem"], tipo="erro")
                    btnProcessar.disabled = False
                    btnProcessar.text = "Processar Arquivo"
                    btnProcessar.icon = ft.icons.PLAY_ARROW
                    processado_ok = False

            except Exception as e:
                uploaderCard.showProgress(False)
                uploaderCard.showFiles()
                notificacao(page, "Erro", f"Erro inesperado: {str(e)}", tipo="erro")
                btnProcessar.disabled = False
                btnProcessar.text = "Processar Arquivo"
                btnProcessar.icon = ft.icons.PLAY_ARROW
                processado_ok = False
            
            finally:
                page.update()

        thread = threading.Thread(target=executarThread, daemon=True)
        thread.start()

    def escolherLocal(e):
        nonlocal processado_ok
        if not processado_ok:
            notificacao(page, "Erro", "Você precisa processar antes de baixar.", tipo="erro")
            return
        
        uploaderCard.showProgress(False)
        
        notificacao(page, "Aguarde", "Escolha o local para salvar o arquivo .fs", tipo="info")
        page.update()

        save_dialog = ft.FilePicker(on_result=salvarArquivo)
        page.overlay.append(save_dialog)
        page.update()
        save_dialog.save_file(
            file_name="Exportacao Fortes.fs", allowed_extensions=["fs"]
        )

    def salvarArquivo(result: ft.FilePickerResultEvent):
        if result.path:
            uploaderCard.showDownloadProgress(True)
            notificacao(page, "Gerando arquivo", "O arquivo está sendo gerado...", tipo="info")
            page.update()
            
            def executarDownload():
                try:
                    resposta = FsRoute.baixarFs(
                        empresa_id=id,
                        arquivos=selected_files,
                        output_path=result.path,
                        progress_callback=None
                    )

                    if resposta["status"] == "ok":
                        uploaderCard.finishDownloadProgress()
                        notificacao(page, "Download pronto!", f"Arquivo salvo em {result.path}", tipo="sucesso")
                    else:
                        uploaderCard.showDownloadProgress(False)
                        notificacao(page, "Erro", resposta["mensagem"], tipo="erro")
                except Exception as e:
                    uploaderCard.showDownloadProgress(False)
                    notificacao(page, "Erro", f"Erro ao gerar arquivo: {str(e)}", tipo="erro")
                
                page.update()
            
            thread = threading.Thread(target=executarDownload, daemon=True)
            thread.start()
        else:
            uploaderCard.showDownloadProgress(False)
            notificacao(page, "Cancelado", "Download cancelado pelo usuário", tipo="info")
            page.update()

    card_empresa = Card(
        title=None,
        content=ft.Row(
            [
                ft.Text(f"(ID: {id})", size=12, color=ft.colors.GREY_500),
                ft.Text(f"Empresa: ", size=13, color=ft.colors.GREY_700),
                ft.Text(
                    f"{nome_empresa}",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE_700,
                    expand=True               
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            run_spacing=2,                   
            expand=True                      
        ),
        icon=None,
        height=None,
    )

    btnProcessar.on_click = processar
    btnDownload.on_click = escolherLocal

    btn_voltar = ActionButton("Voltar", icon=ft.icons.ARROW_BACK, color="primary")
    btn_voltar.on_click = lambda e: page.go("/")

    main_column = ft.Column(
        [
            ft.Container(
                content=ft.Row([btn_voltar], alignment=ft.MainAxisAlignment.START),
                padding=ft.padding.only(top=0, bottom=15),
            ),
            Header(),
            card_empresa,
            uploaderCard,
            ft.Row(
                [btnProcessar, btnDownload],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            Header.footer(),
        ],
        spacing=17,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    
    return ft.View(
        route=f"/main?empresa={id}",
        controls=[main_column],
    )