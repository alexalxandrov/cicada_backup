"""Caesar cipher implementation.

The Caesar cipher shifts every alphabetic character by a fixed amount.
The implementation is case‑preserving and leaves non‑alphabetic
characters unchanged.

Example
-------
>>> from ciphers.caesar import encrypt, decrypt
>>> encrypt("Hello, World!", shift=3)
'Khoor, Zruog!'
>>> decrypt("Khoor, Zruog!", shift=3)
'Hello, World!'
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from typing import Iterable

ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_UPPER = string.ascii_uppercase


def _shift_char(c: str, shift: int) -> str:
    if c in ALPHABET_LOWER:
        return ALPHABET_LOWER[(ALPHABET_LOWER.index(c) + shift) % 26]
    if c in ALPHABET_UPPER:
        return ALPHABET_UPPER[(ALPHABET_UPPER.index(c) + shift) % 26]
    return c


def encrypt(text: str, shift: int) -> str:
    """Encrypt ``text`` with a Caesar shift.

    Parameters
    ----------
    text: str
        Plaintext to encrypt.
    shift: int
        Number of positions to shift; positive values shift forward.
    """
    return "".join(_shift_char(ch, shift) for ch in text)


def decrypt(text: str, shift: int) -> str:
    """Decrypt ``text`` that was encrypted with a Caesar shift.

    The decryption simply applies a negative shift.
    """
    return encrypt(text, -shift)
