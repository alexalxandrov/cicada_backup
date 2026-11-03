#!/usr/bin/env python3
"""Hill‑climb mono‑alphabetic mapping with a seed from a Caesar search.

The script reads the best mapping from :file:`caesar_output.txt`, uses it as the
initial key, and performs a hill‑climb with 5 restarts and 200 000 steps (like
``hillclimb26.py``).  This is a guided search that may escape local maxima that
the random restarts miss.
"""

import math, json, random, sys
from wordfreq import zipf_frequency, top_n_list

# Load ciphertext
with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

# Load best Caesar mapping
caesar_map = {}
with open('WORK/page17/caesar_output.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith("{"):
            caesar_map = eval(line)
            break

# Build rune list
RUNIC_CHARS = sorted(set(CIPHER))
EN_26 = [chr(i) for i in range(ord('a'), ord('z')+1)]

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

def decode_with_map(mapping):
    return ''.join(mapping.get(ch, ch) for ch in CIPHER)

RESTARTS = 5
STEPS = 200_000
best_mapping = caesar_map if caesar_map else None
best_score = seg_score(decode_with_map(best_mapping)) if best_mapping else -1e9
print(f"Initial score from Caesar mapping: {best_score}")

for restart in range(RESTARTS):
    # If we have a seed, start from it and perturb; otherwise random
    if best_mapping:
        current_map = best_mapping.copy()
    else:
        current_map = dict(zip(RUNIC_CHARS, EN_26))
        random.shuffle(EN_26)
        current_map = dict(zip(RUNIC_CHARS, EN_26))
        for step in range(STEPS):
            # propose a small change: swap two letters that are currently mapped
            letters = list(set(current_map.values()))
            a, b = random.sample(letters, 2)
        inv_map = {v: k for k, v in current_map.items()}
        i1, i2 = inv_map[a], inv_map[b]
        current_map[i1], current_map[i2] = current_map[i2], current_map[i1]
        decoded = decode_with_map(current_map)
        score = seg_score(decoded)
        if score > best_score:
            best_score = score
            best_mapping = current_map.copy()
            print(f"restart {restart}, step {step}, new best {best_score}")
        # If not better, revert swap
        else:
            current_map[i1], current_map[i2] = current_map[i2], current_map[i1]

# Output
with open('WORK/page17/guided_hillclimb26_output.txt', 'w', encoding='utf-8') as f:
    f.write(f"Best score: {best_score}\n")
    f.write("Best mapping:\n")
    f.write(str(best_mapping) + "\n\n")
    f.write("Decoded sample:\n")
    f.write(decode_with_map(best_mapping)[:200])

print(f"Guided hill‑climb complete. Best score={best_score}")