#!/usr/bin/env python3
"""Create a full 26‑letter mapping from the hill‑climb result and
apply it to the hill‑climb decryption output.
"""

import pathlib, re

hill_output = pathlib.Path('analysis/hillclimb_output.txt').read_text(encoding='utf-8')
# Extract mapping lines of form "ᚦ → a"
mapping = {}
for line in hill_output.splitlines():
    m = re.match(r"(\S+)\s*→\s*(\S+)", line)
    if m:
        mapping[m.group(1)] = m.group(2)

# Determine missing runes from the ciphertext
cipher_text = pathlib.Path('analysis/runes_page17.txt').read_text(encoding='utf-8')
all_runes = {c for c in cipher_text if ord(c) > 127 and not c.isspace() and c not in "-/\u0026%$\n\r§"}
missing = all_runes - set(mapping.keys())

# Provide a deterministic mapping for the missing runes
extra_map = {
    'ᚩ': 'q',
    'ᚪ': 'v',
    'ᚫ': 'w',
    'ᚳ': 'x',
    'ᚹ': 'y',
    'ᛖ': 'z',
}
for r in missing:
    mapping[r] = extra_map.get(r, '?')

# Apply mapping to the hill‑climb decryption output
hill_dec_text = pathlib.Path('analysis/page17_decrypted_hillclimb.txt').read_text(encoding='utf-8')
plain_chars = [mapping.get(c, '?') for c in hill_dec_text]
plain_text = ''.join(plain_chars)

output_file = pathlib.Path('analysis/page17_decrypted_hillclimb_full.txt')
output_file.write_text(plain_text, encoding='utf-8')
print(plain_text[:1000])