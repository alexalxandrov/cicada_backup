"""Common classical cipher implementations.

This package contains lightweight, pure‑Python implementations of
the most frequently encountered classical ciphers:

* :mod:`caesar` – fixed‑shift substitution cipher.
* :mod:`vigenere` – key‑based shift cipher.
* :mod:`substitution` – arbitrary substitution mapping.
* :mod:`transposition` – columnar transposition.

Each module exposes two functions – ``encrypt`` and ``decrypt`` – that
operate on Unicode strings and preserve case, whitespace and punctuation.
The implementations are intentionally straightforward to make them easy
to understand and extend.
"""

__all__ = [
    "caesar",
    "vigenere",
    "substitution",
    "transposition",
]
