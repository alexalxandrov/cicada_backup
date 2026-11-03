#!/usr/bin/env python3
"""Decrypt Liber Primus page 17 runic text using the Vigenère key from
``analysis/page17_results.txt`` and a simple rune→letter mapping.

The mapping is a best‑guess mapping of runes to Latin letters based on
common rune transliterations.  It may not produce fully intelligible
Latin text, but it allows us to see whether the Vigenère key yields
coherent words.
"""

import pathlib, string, re

# read rune text
runes_text = pathlib.Path('analysis/runes_page17.txt').read_text(encoding='utf-8')
runes = [c for c in runes_text if ord(c) > 127 and not c.isspace() and c not in "-/\u0026%$\n\r§"]

# alphabet order of runes (sorted by Unicode code point)
alphabet = sorted(set(runes))
alphabet_index = {r: i for i, r in enumerate(alphabet)}

# Use the hill‑climb mapping from the previous run for a more accurate
# rune → letter translation.  The mapping is extracted from the
# `analysis/hillclimb_output.txt` file that contains lines such as
# `ᚦ → i`.
hillclimb_mapping_file = pathlib.Path('analysis/hillclimb_output.txt')
hillclimb_mapping = {}
for line in hillclimb_mapping_file.read_text().splitlines():
    m = re.match(r"\s*'(.+?)'\s*→\s*'(.+?)'", line)
    if m:
        hillclimb_mapping[m.group(1)] = m.group(2)

# Additional mapping for runes that did not appear in the hill‑climb
# output but are present in the ciphertext.
extra_map = {
    'ᚩ': 'q',   # unused letter in hillclimb mapping
    'ᚪ': 'v',   # common substitution
    'ᚫ': 'w',   # common substitution
    'ᚳ': 'c',   # choose unused 'c'
    'ᚹ': 'y',   # choose unused 'y'
    'ᛖ': 'z',   # choose unused 'z'
    'ᛏ': 't',   # assign 't' for ᛏ
}

# Combine the two mapping dictionaries, giving priority to the hill‑climb
# mapping where available.
rune_to_letter = {**extra_map, **hillclimb_mapping}

# read key runes from results file
key_line = pathlib.Path('analysis/page17_results.txt').read_text(encoding='utf-8')
key_start = key_line.find('Best key (runes):')
key_runes = key_line[key_start + len('Best key (runes):'):].strip()

# build key shifts using alphabet order
key_shifts = [alphabet_index.get(r, 0) for r in key_runes]

# Vigenère decryption of runes
plain_runes = []
ki = 0
for r in runes:
    if r in alphabet_index:
        shift = key_shifts[ki % len(key_shifts)]
        plain_idx = (alphabet_index[r] - shift) % len(alphabet)
        plain_runes.append(alphabet[plain_idx])
        ki += 1
    else:
        plain_runes.append('?')
# debug: show first 200 runes
print('plain_runes sample:', ''.join(plain_runes[:200]))

# Map plain runes to letters
plain_letters = [rune_to_letter.get(r, '?') for r in plain_runes]
output = ''.join(plain_letters)
output_file = pathlib.Path('analysis/page17_decrypted_vigenere.txt')
output_file.write_text(output, encoding='utf-8')
print(output[:1000])