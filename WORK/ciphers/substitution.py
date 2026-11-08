"""Simple substitution cipher.

This module allows the user to define a 1‑to‑1 mapping of the Latin
alphabet.  The mapping can be provided as a 26‑character string where the
character at position *i* maps to the alphabet character with index
*i*.  For example, ``"ZYXWVUTSRQPONMLKJIHGFEDCBA"`` reverses the
alphabet.

Only the 26‑letter Latin alphabet is considered; all other
characters are left unchanged.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from typing import Dict

ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_UPPER = string.ascii_uppercase


def _validate_mapping(mapping: str) -> Dict[str, str]:
    """Validate that ``mapping`` is a 26‑character permutation.

    Returns a dictionary mapping each alphabet letter to its substitute.
    """
    mapping = mapping.lower()
    if len(mapping) != 26 or set(mapping) != set(ALPHABET_LOWER):
        raise ValueError("mapping must be a permutation of the 26 letters")
    return {ALPHABET_LOWER[i]: mapping[i] for i in range(26)}


def _shift_char(c: str, mapping: Dict[str, str]) -> str:
    if c in ALPHABET_LOWER:
        return mapping[c]
    if c in ALPHABET_UPPER:
        return mapping[c.lower()].upper()
    return c


def encrypt(text: str, mapping: str) -> str:
    """Encrypt ``text`` using a substitution mapping."""
    table = _validate_mapping(mapping)
    return "".join(_shift_char(ch, table) for ch in text)


def decrypt(text: str, mapping: str) -> str:
    """Decrypt ``text`` that was encrypted with the provided mapping."""
    # Invert the mapping
    table = _validate_mapping(mapping)
    inverse = {v: k for k, v in table.items()}
    return "".join(_shift_char(ch, inverse) for ch in text)
