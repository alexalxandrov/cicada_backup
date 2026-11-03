#!/usr/bin/env python3
"""Brute‑force affine cipher over the 21‑letter rune alphabet.

The script tries all pairs (a, b) where ``a`` is coprime to 21 and ``b`` in
0‑20.  It decrypts the ciphertext from :file:`runic_chars2.txt` using the
formula ``p = a⁻¹ * (c - b) mod 21`` where ``c`` is the ciphertext index.
The resulting plaintext is scored with the same segmented word‑frequency
metric that the 21‑letter hill‑climb uses.
The best score, key pair and decoded sample are written to
``affine_output.txt``.
"""

import math
from wordfreq import zipf_frequency, top_n_list

# Load ciphertext
with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

RUNIC_CHARS = sorted(set(CIPHER))
EN_21 = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v']

# Build mapping from rune to index
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

# Find modular inverses for a
def modinv(a, mod):
    a = a % mod
    for x in range(1, mod):
        if (a * x) % mod == 1:
            return x
    return None

coprime_as = [a for a in range(1, 21) if math.gcd(a, 21) == 1]
best_score = -1e9
best_key = None
best_text = ''

for a in coprime_as:
    inv_a = modinv(a, 21)
    for b in range(21):
        decoded = []
        for ch in CIPHER:
            if ch in index_map:
                c = index_map[ch]
                p = (inv_a * (c - b)) % 21
                decoded.append(EN_21[p])
            else:
                decoded.append(ch)
        decoded_text = ''.join(decoded)
        score = seg_score(decoded_text)
        if score > best_score:
            best_score = score
            best_key = (a, b)
            best_text = decoded_text

with open('WORK/page17/affine_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Best key (a,b): {best_key}\n")
    f.write(f"Best score: {best_score}\n")
    f.write("Decoded sample:\n")
    f.write(best_text[:200])

print(f"Affine search complete. Best key={best_key}, score={best_score}")