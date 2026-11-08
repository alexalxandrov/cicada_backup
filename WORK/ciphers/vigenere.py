"""Vigenère cipher implementation.

The Vigenère cipher encrypts a message by shifting each alphabetic
character by an amount determined by the corresponding character of a
keyword.  The keyword is repeated to match the length of the
plaintext.

Only the 26‑letter Latin alphabet is supported; the implementation
preserves case and leaves non‑alphabetic characters untouched.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from typing import Iterable

ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_UPPER = string.ascii_uppercase


def _key_shifts(keyword: str) -> Iterable[int]:
    """Yield integer shift values derived from ``keyword``.

    The function normalises the keyword to lower case and maps each
    letter to its 0‑based alphabet index.
    """
    kw = keyword.lower()
    for ch in kw:
        if ch in ALPHABET_LOWER:
            yield ALPHABET_LOWER.index(ch)
        else:
            # Ignore non‑alphabetic characters in the keyword
            yield 0


def _shift_char(c: str, shift: int) -> str:
    if c in ALPHABET_LOWER:
        return ALPHABET_LOWER[(ALPHABET_LOWER.index(c) + shift) % 26]
    if c in ALPHABET_UPPER:
        return ALPHABET_UPPER[(ALPHABET_UPPER.index(c) + shift) % 26]
    return c


def encrypt(text: str, keyword: str) -> str:
    """Encrypt ``text`` using the Vigenère cipher.

    Parameters
    ----------
    text: str
        Plaintext to encrypt.
    keyword: str
        Keyword used for the cipher.
    """
    shifts = list(_key_shifts(keyword))
    if not shifts:
        raise ValueError("keyword must contain at least one alphabetic character")
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            result.append(_shift_char(ch, shifts[ki % len(shifts)]))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)


def decrypt(text: str, keyword: str) -> str:
    """Decrypt ``text`` that was encrypted with the Vigenère cipher."""
    shifts = list(_key_shifts(keyword))
    if not shifts:
        raise ValueError("keyword must contain at least one alphabetic character")
    result = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            result.append(_shift_char(ch, -shifts[ki % len(shifts)]))
            ki += 1
        else:
            result.append(ch)
    return "".join(result)
