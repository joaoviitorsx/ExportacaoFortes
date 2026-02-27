from typing import Callable, Optional

import flet as ft


def _ensure_picker(page: ft.Page, picker: ft.FilePicker) -> ft.FilePicker:
    if picker not in page.overlay:
        page.overlay.append(picker)
    return picker


def save_file_with_fallback(
    page: ft.Page,
    on_result: Callable,
    file_name: str,
    allowed_extensions: Optional[list[str]] = None,
    dialog_title: str = "Salvar arquivo",
    fallback_open_manual: Optional[Callable] = None,
    picker: Optional[ft.FilePicker] = None,
) -> None:
    target = picker or ft.FilePicker()
    target.on_result = on_result

    try:
        _ensure_picker(page, target)
        page.update()
        print(f"[DEBUG] Abrindo seletor para salvar arquivo: {dialog_title}")
        target.save_file(
            file_name=file_name,
            allowed_extensions=allowed_extensions or [],
            dialog_title=dialog_title,
        )
    except Exception as error:
        print(f"[ERRO] Falha ao abrir FilePicker de salvamento: {error}")
        if fallback_open_manual:
            fallback_open_manual()


def pick_files_with_fallback(
    page: ft.Page,
    on_result: Callable,
    allowed_extensions: Optional[list[str]] = None,
    allow_multiple: bool = False,
    dialog_title: str = "Selecionar arquivo",
    fallback_open_manual: Optional[Callable] = None,
    picker: Optional[ft.FilePicker] = None,
) -> None:
    target = picker or ft.FilePicker()
    target.on_result = on_result

    try:
        _ensure_picker(page, target)
        page.update()
        print(f"[DEBUG] Abrindo seletor de arquivos: {dialog_title}")
        target.pick_files(
            allow_multiple=allow_multiple,
            allowed_extensions=allowed_extensions or [],
            dialog_title=dialog_title,
        )
    except Exception as error:
        print(f"[ERRO] Falha ao abrir FilePicker: {error}")
        if fallback_open_manual:
            fallback_open_manual()
