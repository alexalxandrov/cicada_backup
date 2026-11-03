"""Attempt to decode the runic cipher as a Vigenère cipher over 21 runes.

The algorithm:

1.  Treat the 21 runes as an ordered alphabet (sorted by Unicode code point).
2.  For a given key length L, split the ciphertext into L columns.
3.  For each column, try all 21 possible shifts.  For each shift produce a decoded
    string (letters a‑z).  Use the same segmentation score as in the hill‑climb
    script to evaluate the decoded string.
4.  Choose the shift that maximises the score for that column.
5.  Concatenate the decoded columns (interleaving them) to produce the full
    plaintext.

The script tests key lengths from 2 to 6 and prints the best score and
corresponding plaintext for each length.
"""

import itertools
from wordfreq import zipf_frequency, top_n_list
from collections import defaultdict

# Load ciphertext
cipher_path = 'WORK/page17/runic_chars2.txt'
with open(cipher_path, 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

# Define rune alphabet order
UNICODE_ORDER = sorted(set(CIPHER))
INDEX_MAP = {r: i for i, r in enumerate(UNICODE_ORDER)}
ALPHABET_SIZE = len(UNICODE_ORDER)

# 21‑letter alphabet based on most common English letters
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

def decode_with_shifts(key_len: int):
    # Split into columns
    columns = ['' for _ in range(key_len)]
    for idx, ch in enumerate(CIPHER):
        columns[idx % key_len] += ch
    best_key_shifts = []
    decoded_cols = []
    for col in columns:
        best_col_score = -1e9
        best_shift = 0
        best_decoded = ''
        for shift in range(ALPHABET_SIZE):
            decoded = []
            for rune in col:
                rune_idx = INDEX_MAP[rune]
                # shift back
                letter_idx = (rune_idx - shift) % ALPHABET_SIZE
                # map to a 21‑letter alphabet
                letter = EN_21[letter_idx % 21]
                decoded.append(letter)
            decoded_str = ''.join(decoded)
            score = seg_score(decoded_str)
            if score > best_col_score:
                best_col_score = score
                best_shift = shift
                best_decoded = decoded_str
        best_key_shifts.append(best_shift)
        decoded_cols.append(best_decoded)
    # Interleave decoded columns to form plaintext
    plaintext = []
    for i in range(len(CIPHER)):
        col_idx = i % key_len
        pos_in_col = i // key_len
        if pos_in_col < len(decoded_cols[col_idx]):
            plaintext.append(decoded_cols[col_idx][pos_in_col])
    plaintext = ''.join(plaintext)
    total_score = seg_score(plaintext)
    return key_len, best_key_shifts, total_score, plaintext

if __name__ == '__main__':
    # Test key lengths from 2 up to 12.  The original script tested only up to 6.
    # Increasing the range may uncover a longer period key if the cipher is
    # Vigenère‑style with a larger key.  The loop now goes to 12 inclusive.
    for key_len in range(2, 13):
        klen, shifts, score, plain = decode_with_shifts(key_len)
        print(f'Key length {klen}: score {score:.1f}')
        print('Key shifts:', shifts)
        print('Plaintext sample:', plain[:200])
        print('-' * 40)