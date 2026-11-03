#!/usr/bin/env python3
"""Brute‑force Caesar shift over the 21‑letter rune alphabet.

The script reads the ciphertext from :file:`runic_chars2.txt`, applies all possible
shifts to the 21‑letter alphabet (``RUNIC_CHARS``), and evaluates the
resulting plaintext with the same segmented word‑frequency score used in
``hillclimb21.py``.  The best shift and its score are written to
``caesar_output.txt``.
"""

import sys, math
from wordfreq import zipf_frequency, top_n_list

# Load ciphertext
with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

RUNIC_CHARS = sorted(set(CIPHER))
EN_21 = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v']

# Word set for scoring
WORD_SET = {w for w in top_n_list('en', 20000) if 2 <= len(w) <= 7}
MAX_LEN = 7

def seg_score(text: str) -> float:
    n = len(text)
    best = [-1e9] * (n + 1)
    best[0] = 0.0
    for i in range(1, n + 1):
        for l in range(1, MAX_LEN + 1):
            j = i - l
            if j < 0:
                break
            w = text[j:i]
            if w in WORD_SET:
                score = best[j] + zipf_frequency(w, 'en')
            else:
                score = best[j] - 10.0
            if score > best[i]:
                best[i] = score
    return best[n]

# Generate mapping for each shift
best_shift = None
best_score = -1e9
for shift in range(len(EN_21)):
    mapping = {rune: EN_21[(i + shift) % len(EN_21)] for i, rune in enumerate(RUNIC_CHARS)}
    decoded = ''.join(mapping.get(c, c) for c in CIPHER)
    score = seg_score(decoded)
    if score > best_score:
        best_score = score
        best_shift = shift
        best_text = decoded

with open('WORK/page17/caesar_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Best shift: {best_shift}\n")
    f.write(f"Best score: {best_score}\n")
    f.write("Best mapping:\n")
    mapping = {rune: EN_21[(i + best_shift) % len(EN_21)] for i, rune in enumerate(RUNIC_CHARS)}
    f.write(str(mapping) + "\n\n")
    f.write("Decoded sample:\n")
    f.write(best_text[:200])

print(f"Caesar search complete. Best shift={best_shift}, score={best_score}")