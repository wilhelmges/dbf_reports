import re
from typing import Any

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

