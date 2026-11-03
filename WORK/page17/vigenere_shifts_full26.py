"""Vigenère decryption attempt over 26‑letter alphabet.

This script is similar to :mod:`vigenere_shifts` but assumes that the 21
distinct runes can be mapped to the full 26‑letter English alphabet.  The
mapping is chosen by taking the rune index modulo 26 and then using a
frequency‑ordered list of the 26 letters.  This provides a larger key
space and may reveal a stronger match if the original cipher used a full
alphabet.
"""

import itertools
from wordfreq import zipf_frequency, top_n_list
from collections import defaultdict

# Load ciphertext
cipher_path = 'WORK/page17/runic_chars2.txt'
with open(cipher_path, 'r', encoding='utf-8') as f:
    CIPHER = f.read().strip()

# Define rune alphabet order (Unicode order of unique runes)
UNICODE_ORDER = sorted(set(CIPHER))
INDEX_MAP = {r: i for i, r in enumerate(UNICODE_ORDER)}
ALPHABET_SIZE = len(UNICODE_ORDER)  # 21

# 26‑letter alphabet sorted by frequency in English
EN_26 = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm',
        'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'x', 'q', 'z', 'j']

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
                letter_idx = (rune_idx - shift) % ALPHABET_SIZE
                # Map to 26‑letter alphabet using modulo 26
                letter = EN_26[letter_idx % 26]
                decoded.append(letter)
            decoded_str = ''.join(decoded)
            score = seg_score(decoded_str)
            if score > best_col_score:
                best_col_score = score
                best_shift = shift
                best_decoded = decoded_str
        best_key_shifts.append(best_shift)
        decoded_cols.append(best_decoded)
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
    for key_len in range(2, 13):
        klen, shifts, score, plain = decode_with_shifts(key_len)
        print(f'Key length {klen}: score {score:.1f}')
        print('Key shifts:', shifts)
        print('Plaintext sample:', plain[:200])
        print('-' * 40)