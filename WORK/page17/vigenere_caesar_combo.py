#!/usr/bin/env python3
"""Search composite cipher: Vigenère (key length 2) + Caesar (shift 0‑20) over 21‑letter alphabet.

The script enumerates all 2‑letter keys (21^2 = 441) for the 21‑letter
alphabet.  For each key it applies a Vigenère decryption (shifting the
ciphertext backwards by the key values), then performs a Caesar shift search
on the resulting text.  The best combination is reported.
"""

import math, itertools
from wordfreq import zipf_frequency, top_n_list

# Load ciphertext
with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

RUNIC_CHARS = sorted(set(CIPHER))
EN_21 = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v']
index_map = {r: i for i, r in enumerate(RUNIC_CHARS)}

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

# Caesar search on a given text
def caesar_search(text):
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
best_combo = None
best_details = None

# Enumerate 2‑letter keys (shifts)
for k1, k2 in itertools.product(range(21), repeat=2):
    # Decrypt with Vigenère (shifts subtract)
    decoded = []
    for i, ch in enumerate(CIPHER):
        if ch in index_map:
            c = index_map[ch]
            shift = k1 if i % 2 == 0 else k2
            p = (c - shift) % 21
            decoded.append(EN_21[p])
        else:
            decoded.append(ch)
    decoded_text = ''.join(decoded)
    score_vig, shift_c, decoded_c = caesar_search(decoded_text)
    if score_vig > best_overall:
        best_overall = score_vig
        best_combo = (k1, k2, shift_c)
        best_details = decoded_c
        print(f"New best: key={k1},{k2} shift={shift_c} score={score_vig}")

with open('WORK/page17/vigenere_caesar_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Best composite score: {best_overall}\n")
    f.write(f"Best Vigenère key (shifts): {best_combo[:2]}\n")
    f.write(f"Best Caesar shift: {best_combo[2]}\n")
    f.write("Decoded sample:\n")
    f.write(best_details[:200])

print(f"Composite search complete. Best score={best_overall}")