"""Columnar transposition cipher.

The columnar transposition cipher writes the plaintext into a grid
with a number of columns equal to the key length and then reads the
columns in key‑order.  The implementation below uses a simple
numeric key consisting of distinct digits (e.g. ``"3142"``).  The key
specifies the order in which columns are read.

The implementation preserves case and non‑alphabetic characters.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List


def _validate_key(key: str) -> List[int]:
    """Validate that ``key`` is a permutation of digits starting at 1.

    Returns the key as a list of integers.
    """
    digits = [int(ch) for ch in key if ch.isdigit()]
    if sorted(digits) != list(range(1, len(digits) + 1)):
        raise ValueError("key must be a permutation of 1..n without duplicates")
    return digits


def encrypt(text: str, key: str) -> str:
    """Encrypt ``text`` with a columnar transposition cipher.

    Parameters
    ----------
    text: str
        Plaintext to encrypt.
    key: str
        Numeric key that defines the column order.
    """
    cols = _validate_key(key)
    ncol = len(cols)
    nrow = math.ceil(len(text) / ncol)
    # Pad with spaces to fill the grid
    padded = text.ljust(nrow * ncol)
    grid = [padded[i * ncol : (i + 1) * ncol] for i in range(nrow)]
    # Read columns in key order
    result = []
    for col_index in sorted(range(ncol), key=lambda i: cols[i]):
        for row in grid:
            result.append(row[col_index])
    return "".join(result).rstrip()


def decrypt(text: str, key: str) -> str:
    """Decrypt ``text`` that was encrypted with a columnar transposition."""
    cols = _validate_key(key)
    ncol = len(cols)
    nrow = math.ceil(len(text) / ncol)
    # Number of cells in the grid
    total = nrow * ncol
    # Pad ciphertext to full grid
    padded = text.ljust(total)
    # Determine column lengths (they all equal when padded)
    col_lengths = [nrow] * ncol
    # Split ciphertext into columns according to key order
    columns = {}
    idx = 0
    for col_index in sorted(range(ncol), key=lambda i: cols[i]):
        columns[col_index] = padded[idx : idx + col_lengths[col_index]]
        idx += col_lengths[col_index]
    # Reconstruct rows
    rows = ["".join(columns[i][j] for i in range(ncol)) for j in range(nrow)]
    return "".join(rows).rstrip()
