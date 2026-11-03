"""Hill‑climbing / simulated‑annealing search for a monoalphabetic mapping.

This script is a more robust version of the original hillclimb.py.  It:

* Builds the initial mapping from rune frequencies to the most common English letters.
* Randomly shuffles the English letters for each restart to explore a larger space.
* Uses a simulated‑annealing schedule with 200 000 steps per restart and 5 restarts.
* Evaluates the mapping by segmenting the decoded text with a dynamic‑programming word‑frequency scorer.
* Keeps the best mapping found across all restarts.

The script writes the best score and mapping to stdout.  The final decoded text is also printed.
"""

import random, math
from wordfreq import zipf_frequency, top_n_list

# ---------------------------------------------------------------------------
# Load runic data
# ---------------------------------------------------------------------------
RUNIC_TEXT = open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8').read().strip()
RUNIC_CHARS = sorted(set(RUNIC_TEXT))

# ---------------------------------------------------------------------------
# Helper to decode a mapping
# ---------------------------------------------------------------------------
def decode(mapping: dict) -> str:
    return ''.join(mapping.get(c, c) for c in RUNIC_TEXT)

# ---------------------------------------------------------------------------
# Word‑frequency scoring (segmentation)
# ---------------------------------------------------------------------------
WORD_SET = {w for w in top_n_list('en', 20000) if 2 <= len(w) <= 7}
MAX_LEN = 7

def seg_score(text: str) -> float:
    """Return a score based on the best segmentation of ``text``.

    Uses a dynamic programming approach: at each position the best score up to that
    character is stored, adding the zipf frequency of a dictionary word or
    penalising unknown fragments.
    """
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
                # heavy penalty for unknown word fragment
                score = best[j] - 10.0
            if score > best[i]:
                best[i] = score
    return best[n]

# ---------------------------------------------------------------------------
# Build a mapping from rune frequency to English letter frequency
# ---------------------------------------------------------------------------
freq_lines = open('WORK/page17/runic_freq.txt', 'r', encoding='utf-8').read().strip().splitlines()
# the file contains a header; the data starts after the third line
data = [line.split() for line in freq_lines[3:]]  # each line: rune count
rune_order = [r for r, _ in sorted(data, key=lambda x: int(x[1]), reverse=True)]
eng_order = list('etaoinshrdlcumwfgypbvkjxqz')[:len(rune_order)]

def init_mapping() -> dict:
    """Return a random mapping based on rune frequency order.

    The English letters are shuffled each time to diversify the search.
    """
    shuffled = eng_order.copy()
    random.shuffle(shuffled)
    return dict(zip(rune_order, shuffled))

# ---------------------------------------------------------------------------
# Main search loop
# ---------------------------------------------------------------------------
best_mapping = init_mapping()
best_score = seg_score(decode(best_mapping))
print('initial score', best_score)

# Simulated annealing with multiple restarts
RESTARTS = 5
STEPS = 200_000
for restart in range(RESTARTS):
    mapping = init_mapping()
    T = 1.0
    for step in range(STEPS):
        a, b = random.sample(RUNIC_CHARS, 2)
        mapping[a], mapping[b] = mapping[b], mapping[a]
        new_score = seg_score(decode(mapping))
        if new_score > best_score or math.exp((new_score - best_score) / T) > random.random():
            best_score = new_score
            best_mapping = mapping.copy()
        else:
            # revert the swap
            mapping[a], mapping[b] = mapping[b], mapping[a]
        T *= 0.9995
        if step % 5000 == 0:
            print(f'restart {restart}, step {step}, best {best_score}')
    # Evaluate final mapping of this restart
    final_score = seg_score(decode(mapping))
    if final_score > best_score:
        best_score = final_score
        best_mapping = mapping.copy()
        print(f'  new best after restart {restart}: {best_score}')

print('\n--- Result ---')
print('best score', best_score)
print('best mapping', best_mapping)
print('decoded sample:', decode(best_mapping)[:200])