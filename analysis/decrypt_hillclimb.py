#!/usr/bin/env python3
"""Decode Liber Primus page 17 using the hill‑climb mapping from earlier.

The mapping was discovered by a hill‑climb search that produced a score of 651.32.
It maps 21 runes to letters of the English alphabet.
"""

import pathlib

RUNE_FILE = pathlib.Path('analysis/runes_page17.txt')
TEXT = RUNE_FILE.read_text(encoding='utf-8')
RUNES = [c for c in TEXT if ord(c) > 127 and not c.isspace() and c not in "-/\u0026%$\n\r§"]

MAPPING = {
    'ᚦ': 't', 'ᚾ': 'a', 'ᚠ': 's', 'ᛁ': 'm', 'ᛈ': 'i', 'ᛗ': 'o',
    'ᚷ': 'n', 'ᚻ': 'e', 'ᛟ': 'r', 'ᛒ': 'f', 'ᚱ': 'b', 'ᛚ': 'u',
    'ᛝ': 'd', 'ᛋ': 'h', 'ᛞ': 'p', 'ᛠ': 'l', 'ᚢ': 'v', 'ᛡ': 'g',
    'ᛄ': 'c', 'ᛉ': 'y', 'ᚣ': 'w'
}

decoded = []
for c in RUNES:
    decoded.append(MAPPING.get(c, '?'))

output = ''.join(decoded)
out_file = pathlib.Path('analysis/page17_decrypted_hillclimb.txt')
out_file.write_text(output, encoding='utf-8')
print(output[:500])