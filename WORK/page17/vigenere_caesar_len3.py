#!/usr/bin/env python3
"""Brute‑force a 3‑letter Vigenère key over the 21‑letter rune alphabet,
followed by a Caesar shift search (0‑20).

The script enumerates all 21^3 = 9261 possible keys.  For each key it
decrypts the ciphertext with the Vigenère formula
``p = (c - k_i) mod 21`` where `k_i` is the key letter for position `i % 3`.
After decryption it performs a full Caesar shift search on the resulting
text using the same segmented word‑frequency scorer as the previous
experiments.

The best composite score, the key and the Caesar shift are written to
``vigenere_caesar_len3_output.txt``.
"""

import itertools
import math
from wordfreq import zipf_frequency, top_n_list

# Load ciphertext
with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

RUNIC_CHARS = sorted(set(CIPHER))
EN_21 = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v']
index_map = {r: i for i, r in enumerate(RUNIC_CHARS)}

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

def caesar_search(text: str):
    best_score = -1e9
    best_shift = None
    best_decoded = ''
    for shift in range(21):
        decoded = []
        for ch in text:
            if ch in index_map:
                c = index_map[ch]
                p = (c - shift) % 21
                decoded.append(EN_21[p])
            else:
                decoded.append(ch)
        decoded_text = ''.join(decoded)
        score = seg_score(decoded_text)
        if score > best_score:
            best_score = score
            best_shift = shift
            best_decoded = decoded_text
    return best_score, best_shift, best_decoded

best_overall = -1e9
best_key = None
best_shift = None
best_decoded = None

for k in itertools.product(range(21), repeat=3):
    # decrypt with Vigenère
    decoded = []
    for i, ch in enumerate(CIPHER):
        if ch in index_map:
            c = index_map[ch]
            shift = k[i % 3]
            p = (c - shift) % 21
            decoded.append(EN_21[p])
        else:
            decoded.append(ch)
    decoded_text = ''.join(decoded)
    score_vig, shift_c, decoded_c = caesar_search(decoded_text)
    if score_vig > best_overall:
        best_overall = score_vig
        best_key = k
        best_shift = shift_c
        best_decoded = decoded_c
        print(f"New best: Vigenère key={k} Caesar shift={shift_c} score={score_vig}")

with open('WORK/page17/vigenere_caesar_len3_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Best composite score: {best_overall}\n")
    f.write(f"Best Vigenère key (shifts): {best_key}\n")
    f.write(f"Best Caesar shift: {best_shift}\n")
    f.write("Decoded sample:\n")
    f.write(best_decoded[:200])

print(f"Length‑3 Vigenère+Caesar search complete. Best score={best_overall}")