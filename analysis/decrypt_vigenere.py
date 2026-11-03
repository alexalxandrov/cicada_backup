#!/usr/bin/env python3
"""Decrypt Liber Primus page 17 runic ciphertext using the Vigenère key found by
``analysis/vigenere_page17.py``.

The script loads the same rune file, builds the rune alphabet, then applies the
key (shifts are applied backwards, i.e. decryption).  The resulting plaintext
is printed to stdout and written to ``analysis/page17_decrypted.txt``.
"""

import pathlib

REPO_RUNE_PATH = pathlib.Path(
    "GITHUB_REPOS/cicada-solvers__The-Complete-Cicada3301-Archive/2014/Liber Primus/runes in text format.txt"
)
WORK_DIR = pathlib.Path("analysis")
WORK_DIR.mkdir(exist_ok=True)
WORK_RUNE_PATH = WORK_DIR / "runes_page17.txt"
WORK_RUNE_PATH.write_text(REPO_RUNE_PATH.read_text(encoding="utf-8"))

text = WORK_RUNE_PATH.read_text(encoding="utf-8")
# keep only rune characters – the same filtering used in vigenere_page17.py
runes = [c for c in text if ord(c) > 127 and not c.isspace() and c not in "-/\u0026%$\n\r§"]
unique_runes = sorted(set(runes))
rune_to_idx = {r: i for i, r in enumerate(unique_runes)}
idx_to_rune = {i: r for r, i in rune_to_idx.items()}

# Key discovered by analysis script
key_str = "ᚻᛠᚳᚢᛚᛖᛄᚱᛇᛝᛒᛠᚻᛒᚪᛄᛇᛟᛠᛗᚳᛗᚷᚷᛗᚠᚢᚩᛖᛞᚣᛞᚾᚩᛡᚪᛠᛈᚾᚫ"
key = [rune_to_idx[ch] for ch in key_str]
L = len(key)

decoded_letters = []
for i, r in enumerate(runes):
    idx = rune_to_idx[r]
    shift = key[i % L]
    dec_idx = (idx - shift) % len(unique_runes)
    # Map first 26 runes to letters A-Z, others to '?' for safety
    if dec_idx < 26:
        decoded_letters.append(chr(ord('A') + dec_idx))
    else:
        decoded_letters.append('?')

decoded_text = "".join(decoded_letters)
output_path = WORK_DIR / "page17_decrypted.txt"
output_path.write_text(decoded_text, encoding="utf-8")
print(decoded_text[:500])  # show first 500 chars for quick view