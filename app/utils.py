"""Fungsi bantu validasi dan sanitasi input."""
import re
from typing import Optional

MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def sanitize_text(value: str) -> str:
    """Hapus karakter kontrol dan rapikan spasi di tepi."""
    return _CONTROL_CHARS.sub("", value).strip()


def validate_title(title) -> Optional[str]:
    """Kembalikan pesan error, atau None jika judul valid."""
    if not isinstance(title, str):
        return "title harus berupa string"
    cleaned = sanitize_text(title)
    if not cleaned:
        return "title tidak boleh kosong"
    if len(cleaned) > MAX_TITLE_LENGTH:
        return f"title maksimal {MAX_TITLE_LENGTH} karakter"
    return None


def validate_description(description) -> Optional[str]:
    """Kembalikan pesan error, atau None jika deskripsi valid."""
    if not isinstance(description, str):
        return "description harus berupa string"
    if len(sanitize_text(description)) > MAX_DESCRIPTION_LENGTH:
        return f"description maksimal {MAX_DESCRIPTION_LENGTH} karakter"
    return None


def parse_bool(value: str) -> Optional[bool]:
    """Ubah query string 'true'/'false' menjadi bool; selain itu None."""
    mapping = {"true": True, "1": True, "false": False, "0": False}
    return mapping.get(str(value).lower())
