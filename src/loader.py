import json
from pathlib import Path

import pandas as pd

from config import FINAL_REPORT_FILE, PROCESS_ID_FILE, RAW_DIR


def ensure_directories() -> None:
    """
    Garante que as pastas de dados existam antes de salvar os arquivos.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)


def save_json(data, file_path: Path) -> None:
    """
    Salva dados em JSON com indentação e codificação UTF-8.

    O parâmetro ensure_ascii=False preserva caracteres especiais,
    como acentos e cedilha.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_process_id(process_id: str) -> None:
    """
    Salva o process_id utilizado para geração dos relatórios.
    """
    with open(PROCESS_ID_FILE, "w", encoding="utf-8") as file:
        file.write(process_id)


def save_final_report(df_final: pd.DataFrame) -> None:
    """
    Salva o arquivo final em CSV, com codificação UTF-8.
    """
    df_final.to_csv(
        FINAL_REPORT_FILE,
        index=False,
        encoding="utf-8",
    )