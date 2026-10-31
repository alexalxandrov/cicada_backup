"""Quick test harness for the extended hill‑climb algorithm.

Runs the :py:mod:`hillclimb_more` logic with a reduced number of steps to
allow experimentation in the CI environment.
"""

import random, math
from wordfreq import zipf_frequency, top_n_list
from collections import defaultdict

# Load ciphertext and rune alphabet
with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()
RUNIC_CHARS = sorted(set(CIPHER))

EN_21 = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v']
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

def decode(mapping: dict) -> str:
    return ''.join(mapping.get(c, c) for c in CIPHER)

with open('WORK/page17/runic_freq.txt', 'r', encoding='utf-8') as f:
    freq_lines = f.read().strip().splitlines()
rune_freq = [line.split() for line in freq_lines[3:]]
rune_order = [r for r, _ in sorted(rune_freq, key=lambda x: int(x[1]), reverse=True)]
init_map = {rune: EN_21[i] for i, rune in enumerate(rune_order)}

best_mapping = init_map.copy()
best_score = seg_score(decode(best_mapping))
print('initial score', best_score)

RESTARTS = 1
STEPS = 100_000
for restart in range(RESTARTS):
    mapping = init_map.copy()
    T = 1.0
    for step in range(STEPS):
        a, b = random.sample(RUNIC_CHARS, 2)
        mapping[a], mapping[b] = mapping[b], mapping[a]
        new_score = seg_score(decode(mapping))
        if new_score > best_score or math.exp((new_score - best_score) / T) > random.random():
            best_score = new_score
            best_mapping = mapping.copy()
        else:
            mapping[a], mapping[b] = mapping[b], mapping[a]
        T *= 0.9995
        if step % 10_000 == 0:
            print(f'restart {restart}, step {step}, best {best_score}')
    if seg_score(decode(mapping)) > best_score:
        best_score = seg_score(decode(mapping))
        best_mapping = mapping.copy()

print('\n--- Result ---')
print('best score', best_score)
print('best mapping', best_mapping)
print('decoded sample:', decode(best_mapping)[:200])