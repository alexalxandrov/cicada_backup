"""Utility functions for brute‑forcing classical ciphers.

The module contains helpers that try all possible keys for simple
ciphers and attempt to guess the correct decryption based on a
wordlist.

The current implementation supports:

* Caesar – all 25 possible shifts.
* Vigenère – key lengths 1‑5 with alphabetic keys.

The helper :func:`find_best_candidate` uses a very lightweight
English word frequency list bundled in ``/usr/share/dict/words`` or
fallback to a small built‑in list if the system dictionary is not
available.
"""

from __future__ import annotations

import itertools
import string
from pathlib import Path
from typing import Iterable, List, Tuple

from ciphers.caesar import decrypt as caesar_decrypt
from ciphers.vigenere import decrypt as vigenere_decrypt
import re

# ---------------------------------------------------------------------------
# Helper for loading a word list
# ---------------------------------------------------------------------------
def _load_wordlist() -> List[str]:
    # Prefer the system dictionary; if unavailable, use a tiny fallback
    dict_path = Path("/usr/share/dict/words")
    if dict_path.exists():
        return [w.strip().lower() for w in dict_path.read_text().splitlines() if w.strip()]
    return ["the", "and", "of", "to", "a", "in", "that", "is", "was", "it"]

WORDLIST = set(_load_wordlist())


def _text_score(text: str) -> int:
    """Return a score based on the number of dictionary words.

    The function splits the text on non‑alphabetic characters and
    counts how many resulting tokens are present in :data:`WORDLIST`.
    """
    tokens = [t.lower() for t in re.split(r"[^A-Za-z]+", text) if t]
    return sum(1 for t in tokens if t in WORDLIST)


def brute_caesar(ciphertext: str) -> List[Tuple[int, str]]:
    """Return all possible Caesar decryptions.

    The return value is a list of tuples ``(shift, plaintext)``.
    """
    return [(shift, caesar_decrypt(ciphertext, shift)) for shift in range(1, 26)]


def brute_vigenere(ciphertext: str, max_key_len: int = 5) -> List[Tuple[str, str]]:
    """Try all alphabetic keys up to ``max_key_len``.

    The function returns a list of ``(key, plaintext)`` tuples.
    """
    alphabet = string.ascii_lowercase
    results: List[Tuple[str, str]] = []
    for length in range(1, max_key_len + 1):
        for key_tuple in itertools.product(alphabet, repeat=length):
            key = "".join(key_tuple)
            results.append((key, vigenere_decrypt(ciphertext, key)))
    return results


def find_best_candidate(decryptions: Iterable[Tuple[str, str]]) -> Tuple[str, str, int]:
    """Pick the best candidate based on wordlist match count.

    Returns ``(key, plaintext, score)``.  The ``key`` is a string for
    Caesar (the shift number) or the actual Vigenère key.
    """
    best = None
    best_score = -1
    for key, text in decryptions:
        score = _text_score(text)
        if score > best_score:
            best_score = score
            best = (key, text, score)
    if best is None:
        raise RuntimeError("no decryptions to evaluate")
    return best
