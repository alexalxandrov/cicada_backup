"""Simple bigram frequency analysis for the runic ciphertext.

This script prints the 20 most frequent 2‑character sequences (bigrams)
from the runic message stored in :data:`WORK/page17/runic_chars2.txt`.
The output is written to :data:`WORK/page17/bigram_output.txt`.
"""

from collections import Counter

cipher_path = 'WORK/page17/runic_chars2.txt'
with open(cipher_path, 'r', encoding='utf-8') as f:
    text = f.read().strip()

bigrams = Counter([text[i:i+2] for i in range(len(text)-1)])
top_bigrams = bigrams.most_common(20)

out_path = 'WORK/page17/bigram_output.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    for bigram, freq in top_bigrams:
        f.write(f'{bigram}\t{freq}\n')