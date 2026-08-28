import re
from pathlib import Path
from typing import Any
from src.dbf_reports.dbf.generic import Generic

def dbf_report_params(filename:str):
    sway = filename.split("_")[0][-3]
    if sway.isdigit():
        return int(sway)
    return 0

def is_df_report(df: int|Path)->bool:
    if isinstance(df, Path):
        df = dbf_report_params(df.stem)
    if df == 1 or df == 4 or df == 5:
        return True
    return False

def get_dbf_row_Class(file: Path):
    dfnum = dbf_report_params(file.stem)
    return Generic

def _clean_string(value: Any) -> str | None:
    if value is None:
        return None
    try:
        s = str(value)
    except Exception:
        return None
    # прибрати control chars
    s = re.sub(r"[\x00-\x1f\x7f]", "", s)
    # trim
    s = s.strip()
    # кілька пробілів -> один
    s = re.sub(r"\s+", " ", s)
    # нижній регістр
    s = s.lower()
    if s == "":
        return None
    return s

