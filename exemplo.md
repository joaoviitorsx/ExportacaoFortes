import os
import flet as ft
from flet import FilePickerResultEvent
from src.Components.notificao import notificacao
from src.Controllers.exportarController import ExportarController
from src.Utils.ambiente import is_linux

def baixarAction(page: ft.Page, empresa_id: int, mes, ano, empresa_nome, file_picker: ft.FilePicker, refs: dict):
    print(f"🔍 [DEBUG] baixarAction chamado - empresa_id: {empresa_id}, mes: {mes}, ano: {ano}")
    print("🚀 Iniciando download...")
    
    meses = {
        "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
        "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
        "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
    }

    if not mes or not ano:
        notificacao(page, "Período não informado", "Selecione o mês e ano antes de prosseguir.", tipo="alerta")
        return

    mes_num = meses.get(mes)
    if not mes_num:
        notificacao(page, "Mês inválido", "Selecione um mês válido.", tipo="erro")
        return

    periodo = f"{mes_num}/{ano}"
    nomeArquivo = f"Tributação_{empresa_nome}_{periodo.replace('/', '-')}.xlsx"

    async def processar_exportacao(caminho):
        """Processa a exportação da planilha"""
        progress = refs.get("download_progress")
        if progress and progress.current:
            progress.current.visible = True
            progress.current.value = None
            progress.current.update()

        try:
            notificacao(page, "Processando", "Gerando planilha, aguarde...", tipo="info")
            
            resultado = await ExportarController.exportarPlanilha(page, empresa_id, periodo, caminho)

            if resultado["status"] == "ok":
                def abrir_planilha(e):
                    try:
                        if os.name == 'nt':  # Windows
                            os.startfile(resultado["caminho_arquivo"])
                        else:  # Linux/Mac
                            import subprocess
                            subprocess.run(['xdg-open', resultado["caminho_arquivo"]], check=False)
                    except Exception as ex:
                        notificacao(page, "Erro", "Não foi possível abrir o arquivo automaticamente.", tipo="erro")
                    dialog.open = False
                    page.update()

                def fechar_dialog(e):
                    dialog.open = False
                    page.update()

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Exportação concluída"),
                    content=ft.Text(
                        f"Planilha exportada com sucesso!\n"
                        f"Deseja abrir o arquivo agora?"
                    ),
                    actions=[
                        ft.TextButton("Abrir", on_click=abrir_planilha),
                        ft.TextButton("Fechar", on_click=fechar_dialog)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                page.overlay.append(dialog)
                page.dialog = dialog
                dialog.open = True
                page.update()

            elif resultado["status"] == "vazio":
                notificacao(page, "Sem dados", resultado["mensagem"], tipo="alerta")
            else:
                notificacao(page, "Erro", resultado["mensagem"], tipo="erro")
                
        except Exception as ex:
            import traceback
            traceback.print_exc()
            notificacao(page, "Erro", f"Erro inesperado: {str(ex)}", tipo="erro")
        finally:
            if progress and progress.current:
                progress.current.visible = False
                progress.current.update()
    
    def processar_caminho_manual(caminho, dialog):
        """Processa caminho informado manualmente (fallback Linux)"""
        if not caminho or not caminho.strip():
            notificacao(page, "Aviso", "Nenhum caminho informado.", tipo="aviso")
            return
        
        caminho = caminho.strip()
        
        # Adicionar extensão se não tiver
        if not caminho.lower().endswith('.xlsx'):
            caminho += '.xlsx'
        
        # Verificar se diretório existe
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            notificacao(page, "Erro", "Diretório não encontrado.", tipo="erro")
            return
        
        dialog.open = False
        page.update()
        
        async def wrapper():
            await processar_exportacao(caminho)
        
        page.run_task(wrapper)
    
    def abrir_fallback_linux():
        """Dialog para informar caminho de salvamento manualmente no Linux"""
        print("🐧 [DEBUG] Usando fallback manual para Linux (Download)")
        
        try:
            print("✅ [DEBUG] Criando componentes do dialog...")
            campo_caminho = ft.TextField(
                label="Caminho COMPLETO onde salvar (incluindo nome do arquivo)",
                hint_text=f"/home/usuario/Downloads/{nomeArquivo}",
                value=f"/home/usuario/Downloads/{nomeArquivo}",
                helper_text="⚠️ A extensão .xlsx será adicionada automaticamente",
                autofocus=True,
                width=550
            )
        
            def confirmar(e):
                print(f"🔘 [DEBUG] Botão Confirmar clicado - valor: {campo_caminho.value}")
                processar_caminho_manual(campo_caminho.value, dialog)
        
            def fechar(e):
                print("🔘 [DEBUG] Botão Fechar clicado")
                dialog.open = False
                page.update()
        
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Salvar Planilha (Linux)", weight=ft.FontWeight.BOLD),
                content=ft.Container(
                    width=550,
                    content=ft.Column([
                        ft.Text("O seletor de arquivos não está disponível no Wayland."),
                        ft.Text("Por favor, informe o caminho completo onde salvar:", size=12),
                        ft.Container(height=10),
                        campo_caminho,
                    ], tight=True, spacing=5)
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar),
                    ft.ElevatedButton("Salvar", on_click=confirmar)
                ]
            )
            print("✅ [DEBUG] Dialog criado")
        
            page.overlay.append(dialog)
            print("✅ [DEBUG] Dialog adicionado ao overlay")
            page.dialog = dialog
            print("✅ [DEBUG] Dialog atribuído ao page")
            dialog.open = True
            print("✅ [DEBUG] Dialog.open = True")
            page.update()
            print("✅ [DEBUG] page.update() executado - Dialog deve estar visível")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao criar dialog: {e}")
            import traceback
            traceback.print_exc()
    
    # Detectar sistema e usar abordagem apropriada
    if is_linux():
        print("🐧 [DEBUG] Sistema Linux detectado - usando fallback manual para download")
        abrir_fallback_linux()
    else:
        # Windows/Mac: usar FilePicker normal
        print("🪟 [DEBUG] Sistema Windows/Mac - usando FilePicker nativo para download")
        
        def on_save(e: FilePickerResultEvent):
            if not e.path:
                return
            
            caminho = e.path if e.path.lower().endswith(".xlsx") else e.path + ".xlsx"
            
            async def wrapper():
                await processar_exportacao(caminho)
            
            page.run_task(wrapper)

        file_picker.on_result = on_save
        file_picker.save_file(
            dialog_title="Salvar planilha de exportação",
            file_name=nomeArquivo,
            allowed_extensions=["xlsx"]
        )