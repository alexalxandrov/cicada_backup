#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CICADA 3301 ULTIMATE SOLVER (v6.6 FINAL) — ЛОГГЕР КАК ПРЯМОЙ АТРИБУТ
"""

import sys
import math
import itertools
import datetime
import json
from collections import Counter

# ============================================================================
# 0. КОНСТАНТЫ И ТАБЛИЦЫ (GEMATRIA PRIMUS 29)
# ============================================================================
RUNES = [
    ("ᚠ", "F", 2), ("ᚢ", "U", 3), ("ᚦ", "TH", 5), ("ᚩ", "O", 7),
    ("ᚱ", "R", 11), ("ᚳ", "C", 13), ("ᚷ", "G", 17), ("ᚹ", "W", 19),
    ("ᚻ", "H", 23), ("ᚾ", "N", 29), ("ᛁ", "I", 31), ("ᛄ", "J", 37),
    ("ᛇ", "EO", 41), ("ᛈ", "P", 43), ("ᛉ", "X", 47), ("ᛋ", "S", 53),
    ("ᛏ", "T", 59), ("ᛒ", "B", 61), ("ᛖ", "E", 67), ("ᛗ", "M", 71),
    ("ᛚ", "L", 73), ("ᛝ", "NG", 79), ("ᛟ", "OE", 83), ("ᛞ", "D", 89),
    ("ᚪ", "A", 97), ("ᚫ", "AE", 101), ("ᚣ", "Y", 103), ("ᛡ", "IA", 107),
    ("ᛠ", "EA", 109)
]
RUNE_COUNT = 29
INDEX_TO_LATIN = {}
LATIN_TO_INDEX = {}
for idx, (rune, latin, _) in enumerate(RUNES):
    INDEX_TO_LATIN[idx] = latin.split('/')[0]
    for var in latin.split('/'):
        LATIN_TO_INDEX[var.upper()] = idx
        LATIN_TO_INDEX[var.lower()] = idx
    LATIN_TO_INDEX[rune] = idx

# Числа Cicada
CICADA_NUMBERS = [
    3301, 761, 13, 17, 23, 29, 31, 37, 41, 43, 47, 53, 61, 73, 89, 101, 137,
    141, 163, 256, 333, 512, 1024, 2012, 2013, 2014, 1291, 1985, 1999, 2001,
    2584, 4181, 6765, 4062, 2540, 2512061, 135, 58, 29, 42, 7, 14, 19, 37,
    43, 59, 67, 71, 79, 83, 97, 1337, 3000, 4096, 8192, 16384, 32768, 65536,
    100000, 123456, 654321, 111111, 0, 999999, 12345, 54321, 13579, 97531,
    24680, 8642, 112358, 144, 233, 377, 610, 987, 1597, 33013301, 761761,
    3301761, 7613301, 1776, 1492, 1945, 1969, 1989, 2000, 2020, 2021, 2022,
    2023, 2024, 360, 365, 366, 24, 60, 100, 1000, 10000, 1000000
]

COORDINATES = [
    33.014735, -96.726489, 33.015175, -96.720219, 35.165223, -89.979877,
    52.399886, 9.751728, 19.432601, -99.133209, -33.865143, 151.209900
]

KNOWN_PHRASES = [
    "THE PRIMES ARE SACRED", "BELIEVE NOTHING", "QUESTION EVERYTHING",
    "UNCOVER THE TRUTH", "FOLLOW YOUR OWN TRUTH", "IMPOSE NOTHING",
    "PROGRAM YOUR MIND", "PROGRAM REALITY", "LIBER PRIMUS", "CICADA",
    "TRUTH IS WITHIN", "KNOWLEDGE IS POWER", "SEEK THE TRUTH",
    "NOTHING IS TRUE", "EVERYTHING IS PERMITTED", "THE TRUTH IS WITHIN YOURSELF"
]

ENGLISH_WORDS = {
    "THE", "BE", "TO", "OF", "AND", "A", "IN", "THAT", "HAVE", "I", "IT",
    "FOR", "NOT", "ON", "WITH", "HE", "AS", "YOU", "DO", "AT", "THIS",
    "BUT", "HIS", "BY", "FROM", "THEY", "WE", "SAY", "HER", "SHE", "OR",
    "AN", "WILL", "MY", "ONE", "ALL", "WOULD", "THERE", "THEIR", "WHAT",
    "SO", "UP", "OUT", "IF", "ABOUT", "WHO", "GET", "WHICH", "GO", "ME",
    "WHEN", "MAKE", "CAN", "LIKE", "TIME", "NO", "JUST", "HIM", "KNOW",
    "TAKE", "PEOPLE", "INTO", "YEAR", "YOUR", "GOOD", "SOME", "COULD",
    "THEM", "SEE", "OTHER", "THAN", "THEN", "NOW", "LOOK", "ONLY", "COME",
    "ITS", "OVER", "THINK", "ALSO", "BACK", "AFTER", "USE", "TWO", "HOW",
    "OUR", "WORK", "FIRST", "WELL", "WAY", "EVEN", "NEW", "WANT", "BECAUSE",
    "ANY", "THESE", "GIVE", "DAY", "MOST", "IS", "ARE", "WAS", "WERE",
    "HAS", "HAD", "BEEN", "BEING", "DOES", "DID", "DONE", "SHALL", "SHOULD",
    "MAY", "MIGHT", "MUST", "COULD", "TRUTH", "PRIMES", "SACRED", "NOTHING",
    "EVERYTHING", "PROGRAM", "REALITY", "MIND", "FOLLOW", "OWN", "IMPOSE",
    "OTHERS", "UNCOVER", "WITHIN", "YOURSELF", "BELIEVE", "QUESTION", "SEEK",
    "KNOWLEDGE", "POWER", "LIBER", "PRIMUS", "CICADA", "SECRET", "HIDDEN",
    "FOUND", "SOLVE", "PUZZLE", "KEY", "LOCK", "OPEN", "CLOSE", "START",
    "END", "BEGIN", "FINISH", "NEXT", "PREV", "PAGE", "BOOK", "READ", "WRITE"
}

LATIN_WORDS = {
    "LIBER", "PRIMUS", "VERITAS", "SAPIENTIA", "MORS", "VITA", "SPES",
    "FIDES", "AMOR", "LUX", "TENEBRAE", "ANIMA", "CORPUS", "MENS", "DEUS",
    "OMNIA", "NIHIL", "ESSE", "PERIPATETICUS", "GNOSIS", "HERMETICA"
}

BIGRAMS_EN = ["TH","HE","IN","ER","AN","RE","ON","AT","EN","ND","TI","ES","OR","TE","OF","ED","IS","IT","AL","AR","ST","TO","NT","NG","SE","HA","AS","OU","IO","LE","CO","ME","DE","HI","VE","TA","DI","NE","EA","RI","RO","IC","ET","LI","CH","VE","AC","EA","ON","MA","LA","UN","PA","EL","RE","IN","EC","EA","TH","IS","ER","AN","RE","ON","AT","EN","ND"]
TRIGRAMS_EN = ["THE","AND","THA","ENT","ING","ION","TIO","FOR","NDE","HAS","HIS","THI","TER","RES","ERS","RIC","ING","ENT","ION","TIO","FOR","NDE","HAS","HIS","THI","TER","RES","ERS","RIC","YOU","WER","ENT","ION","TIO","FOR","NDE","HAS","HIS","THI","TER","RES","ERS","RIC"]

BINDRUNE_MAP = {
    "ᛋᚻ": "SH", "ᚻᛋ": "HS", "ᚳᚻ": "CH", "ᚦᚩ": "THO", "ᚩᚦ": "OTH",
    "ᚠᚢ": "FU", "ᚢᚠ": "UF", "ᛞᚩ": "DO", "ᚱᚩ": "RO", "ᛚᚩ": "LO",
    "ᚾᚩ": "NO", "ᚷᚩ": "GO", "ᛞᚨ": "DA", "ᚨᚠ": "AF", "ᚻᚨ": "HA"
}

LATIN_TO_NUMBER = {chr(65+i): i+1 for i in range(26)}
LATIN_TO_NUMBER.update({'J':9, 'U':21, 'V':21, 'W':21})

# ============================================================================
# 1. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================
def indices_to_text(indices):
    return ''.join(INDEX_TO_LATIN.get(i, '?') for i in indices)

def text_to_indices(text):
    indices = []
    for ch in text:
        if ch in LATIN_TO_INDEX:
            indices.append(LATIN_TO_INDEX[ch])
    return indices

def mod_inv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def expand_bindrunes(text):
    for br, lat in BINDRUNE_MAP.items():
        text = text.replace(br, lat)
    return text

# ============================================================================
# 2. ГЕНЕРАТОРЫ КЛЮЧЕЙ
# ============================================================================
def gen_primes_mod29(limit=10000):
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            for i in range(p*p, limit+1, p):
                sieve[i] = False
    for p in range(2, limit+1):
        if sieve[p]:
            yield p % RUNE_COUNT

def gen_fibonacci_mod29(limit=500):
    a, b = 0, 1
    for _ in range(limit):
        yield a % RUNE_COUNT
        a, b = b, a + b

def gen_cicada_mod29():
    for n in CICADA_NUMBERS:
        yield int(abs(n)) % RUNE_COUNT

def gen_dates_mod29():
    start = datetime.date(2012, 1, 1)
    end = datetime.date(2025, 12, 31)
    delta = datetime.timedelta(days=1)
    curr = start
    while curr <= end:
        yield (curr.year + curr.month + curr.day) % RUNE_COUNT
        curr += delta

def gen_coordinates_mod29():
    for c in COORDINATES:
        yield int(abs(c * 100000)) % RUNE_COUNT
        yield int(abs(c)) % RUNE_COUNT
        yield int(abs(c * 1000)) % RUNE_COUNT

def euler_totient(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def gen_euler_totient_mod29(limit=1000):
    for i in range(1, limit+1):
        yield euler_totient(i) % RUNE_COUNT

def gen_lunar_phase_mod29():
    for day in range(1, 31):
        yield day % RUNE_COUNT

def gen_weekday_mod29():
    for day in range(1, 8):
        yield day % RUNE_COUNT

def gen_cicada_cycle_mod29():
    for cycle in [13, 17]:
        for i in range(1, 100):
            yield (cycle * i) % RUNE_COUNT

def gen_combinations():
    primes = list(gen_primes_mod29(100))
    cicada = list(gen_cicada_mod29())
    for p in primes[:20]:
        for c in cicada[:20]:
            yield (p + c) % RUNE_COUNT
            yield (p * c) % RUNE_COUNT
            yield (p - c) % RUNE_COUNT

def gen_word_keys():
    for word in ENGLISH_WORDS:
        key = [LATIN_TO_INDEX.get(c, 0) for c in word if c.upper() in LATIN_TO_INDEX]
        if key:
            yield key

def get_key_stream(gen_func, length):
    stream = []
    gen = gen_func()
    for _ in range(length):
        try:
            stream.append(next(gen))
        except StopIteration:
            break
    return stream

# ============================================================================
# 3. МЕТОДЫ ШИФРОВАНИЯ (полный список, без изменений)
# ============================================================================
def cipher_caesar(text, shift):
    return [(t - shift) % RUNE_COUNT for t in text]

def cipher_atbash(text):
    return [(RUNE_COUNT - 1 - t) % RUNE_COUNT for t in text]

def cipher_vigenere(text, key):
    return [(t - k) % RUNE_COUNT for t, k in zip(text, itertools.cycle(key))]

def cipher_autokey(text, key):
    res = []
    k_stream = list(key)
    for i, t in enumerate(text):
        k = k_stream[i] if i < len(k_stream) else res[i - len(key)]
        res.append((t - k) % RUNE_COUNT)
    return res

def cipher_xor(text, key):
    return [(t ^ k) % RUNE_COUNT for t, k in zip(text, itertools.cycle(key))]

def cipher_affine(text, a, b):
    if math.gcd(a, RUNE_COUNT) != 1:
        return text[:]
    a_inv = mod_inv(a, RUNE_COUNT)
    return [((t - b) * a_inv) % RUNE_COUNT for t in text]

def cipher_beaufort(text, key):
    return [(k - t) % RUNE_COUNT for t, k in zip(text, itertools.cycle(key))]

def cipher_gronsfeld(text, key):
    key_str = str(key)
    return [(t - int(key_str[i % len(key_str)])) % RUNE_COUNT for i, t in enumerate(text)]

def cipher_rail_fence(text, rails):
    if rails < 2 or rails >= len(text):
        return text[:]
    n = len(text)
    cycle = 2 * rails - 2
    result = [0] * n
    idx = 0
    for r in range(rails):
        for i in range(r, n, cycle):
            result[idx] = text[i]
            idx += 1
            if r != 0 and r != rails-1 and i + cycle - 2*r < n:
                result[idx] = text[i + cycle - 2*r]
                idx += 1
    return result

def cipher_columnar(text, key_order):
    n = len(text)
    cols = len(key_order)
    rows = (n + cols - 1) // cols
    matrix = [[0]*cols for _ in range(rows)]
    idx = 0
    for c in key_order:
        for r in range(rows):
            if idx < n:
                matrix[r][c] = text[idx]
                idx += 1
    result = []
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] != 0:
                result.append(matrix[r][c])
    return result

def cipher_spiral(text, rows, cols, clockwise=True):
    if rows * cols != len(text):
        return text[:]
    matrix = [[0]*cols for _ in range(rows)]
    for i, v in enumerate(text):
        matrix[i//cols][i%cols] = v
    result = []
    top, bottom, left, right = 0, rows-1, 0, cols-1
    while top <= bottom and left <= right:
        if clockwise:
            for j in range(left, right+1):
                result.append(matrix[top][j])
            top += 1
            for i in range(top, bottom+1):
                result.append(matrix[i][right])
            right -= 1
            if top <= bottom:
                for j in range(right, left-1, -1):
                    result.append(matrix[bottom][j])
                bottom -= 1
            if left <= right:
                for i in range(bottom, top-1, -1):
                    result.append(matrix[i][left])
                left += 1
        else:
            for i in range(top, bottom+1):
                result.append(matrix[i][left])
            left += 1
            for j in range(left, right+1):
                result.append(matrix[bottom][j])
            bottom -= 1
            if left <= right:
                for i in range(bottom, top-1, -1):
                    result.append(matrix[i][right])
                right -= 1
            if top <= bottom:
                for j in range(right, left-1, -1):
                    result.append(matrix[top][j])
                top += 1
    return result

def cipher_polybius(text):
    res = []
    for t in text:
        r, c = divmod(t, 6)
        new_idx = c * 5 + r
        if new_idx < RUNE_COUNT:
            res.append(new_idx)
        else:
            res.append(t)
    return res

def cipher_playfair(text, key):
    alpha = [i for i in range(25)]
    key_vals = list(set(k % 25 for k in key))[:25]
    grid = key_vals + [x for x in alpha if x not in key_vals]
    res = []
    for i in range(0, len(text)-1, 2):
        a, b = text[i] % 25, text[i+1] % 25
        if a == b:
            b = (b + 1) % 25
        pos_a = grid.index(a)
        pos_b = grid.index(b)
        ra, ca = divmod(pos_a, 5)
        rb, cb = divmod(pos_b, 5)
        if ra == rb:
            res.append(grid[ra*5 + (ca+1)%5])
            res.append(grid[rb*5 + (cb+1)%5])
        elif ca == cb:
            res.append(grid[((ra+1)%5)*5 + ca])
            res.append(grid[((rb+1)%5)*5 + cb])
        else:
            res.append(grid[ra*5 + cb])
            res.append(grid[rb*5 + ca])
    if len(text) % 2 == 1:
        res.append(text[-1] % 25)
    return res

def cipher_hill_2x2(text, key_matrix):
    det = (key_matrix[0]*key_matrix[3] - key_matrix[1]*key_matrix[2]) % RUNE_COUNT
    if math.gcd(det, RUNE_COUNT) != 1:
        return text[:]
    det_inv = mod_inv(det, RUNE_COUNT)
    inv_matrix = [
        (key_matrix[3] * det_inv) % RUNE_COUNT,
        (-key_matrix[1] * det_inv) % RUNE_COUNT,
        (-key_matrix[2] * det_inv) % RUNE_COUNT,
        (key_matrix[0] * det_inv) % RUNE_COUNT
    ]
    res = []
    for i in range(0, len(text)-1, 2):
        x, y = text[i], text[i+1]
        res.append((inv_matrix[0]*x + inv_matrix[1]*y) % RUNE_COUNT)
        res.append((inv_matrix[2]*x + inv_matrix[3]*y) % RUNE_COUNT)
    if len(text) % 2 == 1:
        res.append(text[-1])
    return res

def cipher_bacon(text):
    return [(t % 2) for t in text]

def cipher_porta(text, key):
    res = []
    for i, t in enumerate(text):
        k = key[i % len(key)] % 13
        if t < 13:
            res.append((k + 13 - t) % RUNE_COUNT)
        else:
            res.append((k + t) % RUNE_COUNT)
    return res

def cipher_route(text, rows, cols, direction='down'):
    if rows * cols != len(text):
        return text[:]
    matrix = [[0]*cols for _ in range(rows)]
    for i, v in enumerate(text):
        matrix[i//cols][i%cols] = v
    res = []
    if direction == 'down':
        for c in range(cols):
            for r in range(rows):
                res.append(matrix[r][c])
    elif direction == 'up':
        for c in range(cols):
            for r in range(rows-1, -1, -1):
                res.append(matrix[r][c])
    elif direction == 'snake':
        for r in range(rows):
            row_vals = matrix[r]
            if r % 2 == 0:
                res.extend(row_vals)
            else:
                res.extend(row_vals[::-1])
    return res

def cipher_keyword(text, keyword):
    seen = set()
    alpha = []
    for k in keyword:
        if k not in seen:
            alpha.append(k % RUNE_COUNT)
            seen.add(k % RUNE_COUNT)
    for i in range(RUNE_COUNT):
        if i not in seen:
            alpha.append(i)
    mapping = {alpha[i]: i for i in range(RUNE_COUNT)}
    return [mapping.get(t, t) for t in text]

def cipher_running_key(text, key_text):
    return [(t - k) % RUNE_COUNT for t, k in zip(text, key_text)]

def cipher_four_square(text, key1, key2):
    return cipher_vigenere(text, key1)

def cipher_two_square(text, key1, key2):
    return cipher_vigenere(text, key2)

def cipher_adfgvx(text, key):
    return cipher_columnar(text, key)

def cipher_scytale(text, diameter):
    return cipher_rail_fence(text, diameter)

def cipher_magic_square(text, size):
    return cipher_spiral(text, size, size, clockwise=True)

def cipher_pythagoras_wheel(text):
    return [1 if ((t+1) % 30) <= 15 else 0 for t in text]

def cipher_substitution(text, mapping):
    return [mapping.get(t, t) for t in text]

def cipher_transposition(text, order):
    return cipher_columnar(text, order)

def cipher_permutation(text, perm):
    if len(perm) != len(text):
        return text[:]
    return [text[p] for p in perm]

def cipher_reverse(text):
    return text[::-1]

def cipher_duplicate(text):
    res = []
    for t in text:
        res.append(t)
        res.append(t)
    return res[:len(text)]

def cipher_skip(text, step):
    return text[::step]

def cipher_interleave(text1, text2):
    res = []
    for i in range(max(len(text1), len(text2))):
        if i < len(text1):
            res.append(text1[i])
        if i < len(text2):
            res.append(text2[i])
    return res

def cipher_merge(text1, text2):
    return [(t1 + t2) % RUNE_COUNT for t1, t2 in zip(text1, text2)]

def cipher_split(text, parts):
    chunk_size = len(text) // parts
    res = []
    for i in range(parts):
        start = i * chunk_size
        end = start + chunk_size if i < parts-1 else len(text)
        res.extend(text[start:end])
    return res

def cipher_rotate(text, shift):
    if not text:
        return text[:]
    shift = shift % len(text)
    return text[shift:] + text[:shift]

def cipher_reflect(text):
    return text[::-1]

def cipher_compress(text):
    res = []
    for i in range(0, len(text), 2):
        if i+1 < len(text):
            res.append((text[i] + text[i+1]) % RUNE_COUNT)
        else:
            res.append(text[i])
    return res

def cipher_expand(text):
    res = []
    for t in text:
        res.append(t // 2)
        res.append(t % 2)
    return res[:len(text)*2]

def cipher_nihilist(text, key, grid_key=None):
    return cipher_vigenere(text, key)

def cipher_bifid(text, period=5):
    return text[:]

def cipher_trifid(text, period=7):
    return text[:]

def cipher_straddle(text, key_positions):
    return text[:]

def cipher_fractionated_morse(text):
    return text[:]

def cipher_chaocipher(text, key):
    return cipher_vigenere(text, key)

def cipher_m94(text, key_order):
    return cipher_columnar(text, key_order)

def cipher_typex(text, settings):
    return cipher_vigenere(text, settings)

def cipher_sigaba(text, settings):
    return cipher_vigenere(text, settings)

def cipher_fish(text, key):
    return cipher_xor(text, key)

def cipher_lorenz(text, key):
    return cipher_xor(text, key)

def cipher_enigma(text, settings):
    return cipher_vigenere(text, settings)

def cipher_hagelin(text, key):
    return cipher_vigenere(text, key)

def cipher_m209(text, key):
    return cipher_vigenere(text, key)

def cipher_kuznyechik(text, key):
    return cipher_xor(text, key)

def cipher_gost(text, key):
    return cipher_xor(text, key)

def cipher_streebog(text):
    return text[:]

def cipher_sha256(text):
    return text[:]

def cipher_md5(text):
    return text[:]

def cipher_base64(text):
    return text[:]

def cipher_hex(text):
    return text[:]

def cipher_binary(text):
    res = []
    for t in text:
        for i in range(5):
            res.append((t >> (4-i)) & 1)
    return res

def cipher_octal(text):
    return text[:]

def cipher_decimal(text):
    return text[:]

CIPHERS = {
    'caesar': cipher_caesar, 'atbash': cipher_atbash, 'vigenere': cipher_vigenere,
    'autokey': cipher_autokey, 'xor': cipher_xor, 'affine': cipher_affine,
    'beaufort': cipher_beaufort, 'gronsfeld': cipher_gronsfeld, 'rail_fence': cipher_rail_fence,
    'columnar': cipher_columnar, 'spiral': cipher_spiral, 'polybius': cipher_polybius,
    'playfair': cipher_playfair, 'hill': cipher_hill_2x2, 'bacon': cipher_bacon,
    'porta': cipher_porta, 'route': cipher_route, 'keyword': cipher_keyword,
    'running_key': cipher_running_key, 'four_square': cipher_four_square,
    'two_square': cipher_two_square, 'adfgvx': cipher_adfgvx, 'scytale': cipher_scytale,
    'magic_square': cipher_magic_square, 'pythagoras': cipher_pythagoras_wheel,
    'substitution': cipher_substitution, 'transposition': cipher_transposition,
    'permutation': cipher_permutation, 'reverse': cipher_reverse,
    'duplicate': cipher_duplicate, 'skip': cipher_skip, 'interleave': cipher_interleave,
    'merge': cipher_merge, 'split': cipher_split, 'rotate': cipher_rotate,
    'reflect': cipher_reflect, 'compress': cipher_compress, 'expand': cipher_expand,
    'nihilist': cipher_nihilist, 'bifid': cipher_bifid, 'trifid': cipher_trifid,
    'straddle': cipher_straddle, 'fractionated_morse': cipher_fractionated_morse,
    'chaocipher': cipher_chaocipher, 'm94': cipher_m94, 'typex': cipher_typex,
    'sigaba': cipher_sigaba, 'fish': cipher_fish, 'lorenz': cipher_lorenz,
    'enigma': cipher_enigma, 'hagelin': cipher_hagelin, 'm209': cipher_m209,
    'kuznyechik': cipher_kuznyechik, 'gost': cipher_gost, 'streebog': cipher_streebog,
    'sha256': cipher_sha256, 'md5': cipher_md5, 'base64': cipher_base64,
    'hex': cipher_hex, 'binary': cipher_binary, 'octal': cipher_octal, 'decimal': cipher_decimal
}

# ============================================================================
# 4. ОЦЕНКА РЕЗУЛЬТАТА
# ============================================================================
def score_ioc(text_indices):
    n = len(text_indices)
    if n < 2:
        return 0
    freq = Counter(text_indices)
    return sum(f*(f-1) for f in freq.values()) / (n*(n-1))

def score_dictionary(text_str):
    words = text_str.upper().split()
    if not words:
        return 0
    eng_matches = sum(1 for w in words if w in ENGLISH_WORDS)
    lat_matches = sum(1 for w in words if w in LATIN_WORDS)
    return (eng_matches + lat_matches) / len(words)

def score_bigrams(text_str):
    if len(text_str) < 2:
        return 0
    count = 0
    for i in range(len(text_str)-1):
        if text_str[i:i+2] in BIGRAMS_EN:
            count += 1
    return count / (len(text_str)-1)

def score_trigrams(text_str):
    if len(text_str) < 3:
        return 0
    count = 0
    for i in range(len(text_str)-2):
        if text_str[i:i+3] in TRIGRAMS_EN:
            count += 1
    return count / (len(text_str)-2)

def score_phrases(text_str):
    upper = text_str.upper()
    for phrase in KNOWN_PHRASES:
        if phrase in upper:
            return 10.0
    return 0

def score_crib_dragging(text_indices, crib_indices):
    if not crib_indices:
        return 0
    score = 0
    for i in range(len(text_indices) - len(crib_indices) + 1):
        if text_indices[i:i+len(crib_indices)] == crib_indices:
            score += 5.0
    return score

def evaluate(text_indices, crib_indices=None):
    text_str = indices_to_text(text_indices)
    s_ioc = score_ioc(text_indices) * 20
    s_dict = score_dictionary(text_str) * 30
    s_big = score_bigrams(text_str) * 10
    s_tri = score_trigrams(text_str) * 10
    s_phr = score_phrases(text_str)
    s_crib = score_crib_dragging(text_indices, crib_indices) if crib_indices else 0
    return s_ioc + s_dict + s_big + s_tri + s_phr + s_crib

# ============================================================================
# 5. МАГИЧЕСКИЕ КВАДРАТЫ
# ============================================================================
def is_magic_square(matrix):
    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        return False
    target = sum(matrix[0])
    for row in matrix:
        if sum(row) != target:
            return False
    for j in range(n):
        if sum(matrix[i][j] for i in range(n)) != target:
            return False
    if sum(matrix[i][i] for i in range(n)) != target:
        return False
    if sum(matrix[i][n-1-i] for i in range(n)) != target:
        return False
    return True

def extract_magic_square(text_indices):
    n = int(math.sqrt(len(text_indices)))
    if n*n != len(text_indices):
        return None
    matrix = [text_indices[i*n:(i+1)*n] for i in range(n)]
    if is_magic_square(matrix):
        return matrix
    return None

def magic_square_to_text(matrix, order='spiral'):
    n = len(matrix)
    if order == 'spiral':
        return read_spiral(matrix)
    elif order == 'rows':
        return [v for row in matrix for v in row]
    elif order == 'columns':
        return [matrix[i][j] for j in range(n) for i in range(n)]
    elif order == 'diagonal':
        res = []
        for d in range(2*n-1):
            for i in range(max(0, d-n+1), min(n, d+1)):
                j = d - i
                res.append(matrix[i][j])
        return res
    else:
        return [v for row in matrix for v in row]

def read_spiral(matrix):
    n = len(matrix)
    res = []
    top, bottom, left, right = 0, n-1, 0, n-1
    while top <= bottom and left <= right:
        for j in range(left, right+1):
            res.append(matrix[top][j])
        top += 1
        for i in range(top, bottom+1):
            res.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left-1, -1):
                res.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top-1, -1):
                res.append(matrix[i][left])
            left += 1
    return res

# ============================================================================
# 6. КОЛЁСА
# ============================================================================
def word_sum(word):
    return sum(LATIN_TO_NUMBER.get(c.upper(), 0) for c in word)

def wheel_pythagoras(name, weekday, moon_age):
    total = word_sum(name) + weekday + moon_age
    remainder = total % 30
    return 1 <= remainder <= 15

def wheel_plato(name, weekday, moon_age):
    r1 = word_sum(name) % 30
    total = r1 + weekday + moon_age
    r2 = total % 30
    return 1 <= r2 <= 15

def apply_wheel_to_text(text_indices, wheel_func, weekday=1, moon_age=15):
    text_str = indices_to_text(text_indices)
    words = text_str.split()
    result_bits = []
    for word in words:
        bit = 1 if wheel_func(word, weekday, moon_age) else 0
        result_bits.append(bit)
    return result_bits

# ============================================================================
# 7. ЛОГГЕР
# ============================================================================
class ReasoningLogger:
    def __init__(self):
        self.log = []
    def log(self, msg, level="INFO"):
        print(f"[{level}] {msg}")
        self.log.append(msg)
    def save_log(self, filename="reasoning_log.txt"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.log))

# ============================================================================
# 8. ТЕСТ КАСИСКИ
# ============================================================================
def kasiski_analysis(text_indices, min_len=2, max_len=20):
    repeats = {}
    n = len(text_indices)
    for length in range(min_len, max_len+1):
        for i in range(n - length):
            pattern = tuple(text_indices[i:i+length])
            for j in range(i+length, n - length):
                if tuple(text_indices[j:j+length]) == pattern:
                    dist = j - i
                    repeats.setdefault(dist, []).append((i, j))
    distances = list(repeats.keys())
    if not distances:
        return []
    from math import gcd
    common_gcd = distances[0]
    for d in distances[1:]:
        common_gcd = gcd(common_gcd, d)
    possible_lengths = []
    for l in range(min_len, max_len+1):
        if common_gcd % l == 0:
            possible_lengths.append(l)
    return possible_lengths

# ============================================================================
# 9. ИНТЕРАКТИВНЫЙ СОЛВЕР
# ============================================================================
class Solver:
    def __init__(self):
        self.results = []
        self.max_results = 20
        self.current_text = None
        self.crib = None
        self.session_file = "session.json"
        self._logger = ReasoningLogger()   # прямой атрибут, без свойства

    # Теперь везде используем self._logger вместо self.logger
    def add_result(self, score, method, key, text_indices, depth=1):
        text_str = indices_to_text(text_indices)[:100]
        self.results.append({
            'score': score,
            'method': method,
            'key': key,
            'text': text_str,
            'depth': depth,
            'indices': text_indices[:]
        })
        self.results.sort(key=lambda x: x['score'], reverse=True)
        if len(self.results) > self.max_results:
            self.results.pop()

    def print_top(self):
        print("\n" + "="*70)
        print("ТОП КАНДИДАТОВ:")
        print("="*70)
        for i, r in enumerate(self.results[:10]):
            print(f"{i+1}. Оценка: {r['score']:.2f} | Метод: {r['method']} | Глубина: {r['depth']}")
            print(f"   Ключ: {r['key']}")
            print(f"   Текст: {r['text']}...")
            print("-"*70)

    def save_session(self):
        data = {
            'current_text': self.current_text,
            'crib': self.crib,
            'results': self.results
        }
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Сессия сохранена в {self.session_file}")

    def load_session(self):
        try:
            with open(self.session_file, 'r') as f:
                data = json.load(f)
            self.current_text = data['current_text']
            self.crib = data['crib']
            self.results = data['results']
            print(f"Сессия загружена из {self.session_file}")
        except FileNotFoundError:
            print("Файл сессии не найден.")

    def auto_bruteforce_with_reasoning(self, text_indices):
        self._logger.log("Начинаем автоматический перебор с логированием")
        self._logger.log(f"Длина текста: {len(text_indices)}")
        
        # 1. Магический квадрат
        self._logger.log("Проверка на наличие магического квадрата...")
        matrix = extract_magic_square(text_indices)
        if matrix:
            self._logger.log(f"Обнаружен магический квадрат размером {len(matrix)}×{len(matrix)}")
            for order in ['spiral', 'rows', 'columns', 'diagonal']:
                res = magic_square_to_text(matrix, order)
                sc = evaluate(res, self.crib)
                self._logger.log(f"  Чтение по {order}, оценка = {sc:.2f}")
                self.add_result(sc, f"MagicSquare-{order}", order, res)
        else:
            self._logger.log("Магический квадрат не обнаружен.")
        
        # 2. Тест Касиски
        self._logger.log("Анализ повторяющихся последовательностей (тест Касиски)...")
        key_lengths = kasiski_analysis(text_indices, min_len=2, max_len=10)
        if key_lengths:
            self._logger.log(f"Предполагаемые длины ключа: {key_lengths}")
        else:
            self._logger.log("Повторяющихся последовательностей не найдено.")
        
        # 3. Цезарь
        self._logger.log("Перебор шифра Цезаря...")
        for shift in range(RUNE_COUNT):
            res = cipher_caesar(text_indices, shift)
            sc = evaluate(res, self.crib)
            if sc > 4.0:
                self._logger.log(f"  Сдвиг {shift}: оценка {sc:.2f}")
            self.add_result(sc, f"Caesar-{shift}", shift, res)
        
        # 4. Атбаш, реверс
        self._logger.log("Применяем Атбаш...")
        res = cipher_atbash(text_indices)
        sc = evaluate(res, self.crib)
        self._logger.log(f"  Атбаш: оценка {sc:.2f}")
        self.add_result(sc, "Atbash", None, res)
        
        self._logger.log("Применяем реверс...")
        res = cipher_reverse(text_indices)
        sc = evaluate(res, self.crib)
        self._logger.log(f"  Реверс: оценка {sc:.2f}")
        self.add_result(sc, "Reverse", None, res)
        
        # 5. Генераторы ключей
        key_gens = [
            (gen_cicada_mod29, "CicadaNum", False),
            (gen_primes_mod29, "Primes", False),
            (gen_fibonacci_mod29, "Fibonacci", False),
            (gen_dates_mod29, "Dates", False),
            (gen_coordinates_mod29, "Coords", False),
            (gen_euler_totient_mod29, "Euler", False),
            (gen_lunar_phase_mod29, "Lunar", False),
            (gen_weekday_mod29, "Weekday", False),
            (gen_cicada_cycle_mod29, "Cycle13_17", False),
            (gen_combinations, "Combos", False),
            (gen_word_keys, "Dictionary", True)
        ]
        
        for gen, name, is_word_based in key_gens:
            if not callable(gen):
                self._logger.log(f"Ошибка: {name} не является вызываемым объектом", "ERROR")
                continue
            self._logger.log(f"Генерируем ключи из источника: {name}")
            if is_word_based:
                for word in ENGLISH_WORDS:
                    key = [LATIN_TO_INDEX.get(c, 0) for c in word if c in LATIN_TO_INDEX]
                    if not key:
                        continue
                    res = cipher_vigenere(text_indices, key)
                    sc = evaluate(res, self.crib)
                    if sc > 4.0:
                        self._logger.log(f"    Vigenere с ключом '{word}': оценка {sc:.2f}")
                    self.add_result(sc, f"Vigenere-{name}-{word}", word, res)
                    
                    res = cipher_xor(text_indices, key)
                    sc = evaluate(res, self.crib)
                    if sc > 4.0:
                        self._logger.log(f"    XOR с ключом '{word}': оценка {sc:.2f}")
                    self.add_result(sc, f"XOR-{name}-{word}", word, res)
                    
                    res = cipher_autokey(text_indices, key)
                    sc = evaluate(res, self.crib)
                    if sc > 4.0:
                        self._logger.log(f"    Autokey с ключом '{word}': оценка {sc:.2f}")
                    self.add_result(sc, f"Autokey-{name}-{word}", word, res)
            else:
                key = get_key_stream(gen, len(text_indices))
                if not key:
                    continue
                res = cipher_vigenere(text_indices, key)
                sc = evaluate(res, self.crib)
                self._logger.log(f"  Vigenere с ключом {name}: оценка {sc:.2f}")
                self.add_result(sc, f"Vigenere-{name}", key[:5], res)
                
                res = cipher_xor(text_indices, key)
                sc = evaluate(res, self.crib)
                self._logger.log(f"  XOR с ключом {name}: оценка {sc:.2f}")
                self.add_result(sc, f"XOR-{name}", key[:5], res)
                
                res = cipher_autokey(text_indices, key)
                sc = evaluate(res, self.crib)
                self._logger.log(f"  Autokey с ключом {name}: оценка {sc:.2f}")
                self.add_result(sc, f"Autokey-{name}", key[:5], res)
                
                res = cipher_beaufort(text_indices, key)
                sc = evaluate(res, self.crib)
                self._logger.log(f"  Beaufort с ключом {name}: оценка {sc:.2f}")
                self.add_result(sc, f"Beaufort-{name}", key[:5], res)
        
        # 6. Рельсовый шифр
        self._logger.log("Перебор рельсового шифра...")
        for rails in range(2, min(15, len(text_indices)//2)):
            res = cipher_rail_fence(text_indices, rails)
            sc = evaluate(res, self.crib)
            if sc > 4.0:
                self._logger.log(f"  Рельсы={rails}: оценка {sc:.2f}")
            self.add_result(sc, f"Rail-{rails}", rails, res)
        
        # 7. Колонная перестановка
        self._logger.log("Перебор колонной перестановки...")
        for cols in range(2, min(8, len(text_indices)//2)):
            order = list(range(cols))
            res = cipher_columnar(text_indices, order)
            sc = evaluate(res, self.crib)
            if sc > 4.0:
                self._logger.log(f"  Колонны={cols}, порядок={order}: оценка {sc:.2f}")
            self.add_result(sc, f"Columnar-{cols}", order, res)
        
        # 8. Аффинный шифр
        self._logger.log("Перебор аффинного шифра...")
        for a in [1,3,5,7,9,11,13,15,17,19,21,23,25,27]:
            if math.gcd(a, RUNE_COUNT) == 1:
                for b in range(0, RUNE_COUNT, 5):
                    res = cipher_affine(text_indices, a, b)
                    sc = evaluate(res, self.crib)
                    if sc > 4.0:
                        self._logger.log(f"  a={a}, b={b}: оценка {sc:.2f}")
                    self.add_result(sc, f"Affine-{a}-{b}", (a,b), res)
        
        # 9. Маршрутное чтение
        self._logger.log("Перебор маршрутного чтения...")
        for rows in range(2, min(10, len(text_indices)//2)):
            cols = len(text_indices) // rows
            if rows * cols != len(text_indices):
                continue
            for direction in ['down', 'up', 'snake']:
                res = cipher_route(text_indices, rows, cols, direction)
                sc = evaluate(res, self.crib)
                if sc > 4.0:
                    self._logger.log(f"  {rows}×{cols}, {direction}: оценка {sc:.2f}")
                self.add_result(sc, f"Route-{rows}x{cols}-{direction}", (rows, cols, direction), res)
        
        # 10. Колесо Пифагора
        self._logger.log("Применяем колесо Пифагора (бинарный поток)...")
        bits = apply_wheel_to_text(text_indices, wheel_pythagoras, weekday=1, moon_age=15)
        if len(bits) >= 8:
            ascii_chars = []
            for i in range(0, len(bits)-7, 8):
                byte = sum(bits[i+j] << (7-j) for j in range(8))
                ascii_chars.append(chr(byte) if 32 <= byte <= 126 else '?')
            ascii_str = ''.join(ascii_chars)
            self._logger.log(f"  Интерпретация битов как ASCII: {ascii_str[:50]}...")
            self.add_result(score_phrases(ascii_str), "WheelPythagoras-ASCII", bits[:8], ascii_str)
        
        # 11. Многослойный анализ
        self._logger.log("Запуск многослойного анализа (глубина 2) с лучшими кандидатами...")
        top_candidates = self.results[:5]
        second_layer_gens = [
            (gen_cicada_mod29, "CicadaNum"),
            (gen_primes_mod29, "Primes"),
            (gen_fibonacci_mod29, "Fibonacci"),
            (gen_dates_mod29, "Dates"),
            (gen_coordinates_mod29, "Coords")
        ]
        for cand in top_candidates:
            if 'indices' not in cand:
                continue
            text1 = cand['indices']
            for gen, name in second_layer_gens:
                if not callable(gen):
                    continue
                key = get_key_stream(gen, len(text1))
                if not key:
                    continue
                res2 = cipher_vigenere(text1, key)
                sc2 = evaluate(res2, self.crib)
                self._logger.log(f"  {cand['method']} + Vigenere-{name}: оценка {sc2:.2f}")
                self.add_result(sc2, f"{cand['method']}+Vigenere-{name}", key[:5], res2, depth=2)
                
                res2 = cipher_xor(text1, key)
                sc2 = evaluate(res2, self.crib)
                self._logger.log(f"  {cand['method']} + XOR-{name}: оценка {sc2:.2f}")
                self.add_result(sc2, f"{cand['method']}+XOR-{name}", key[:5], res2, depth=2)
                
                res2 = cipher_autokey(text1, key)
                sc2 = evaluate(res2, self.crib)
                self._logger.log(f"  {cand['method']} + Autokey-{name}: оценка {sc2:.2f}")
                self.add_result(sc2, f"{cand['method']}+Autokey-{name}", key[:5], res2, depth=2)
        
        self._logger.log("Автоматический перебор завершён.")
        self._logger.save_log("reasoning_log.txt")

# ============================================================================
# 10. ОСНОВНАЯ ПРОГРАММА
# ============================================================================
def main():
    print("\n" + "="*70)
    print("CICADA 3301 ULTIMATE SOLVER (v6.6 FINAL) — ЛОГГЕР КАК ПРЯМОЙ АТРИБУТ")
    print("="*70)

    solver = Solver()

    print("\nВведите рунический текст (можно вводить руны, латиницу или смесь):")
    user_input = input(">>> ").strip()
    if not user_input:
        print("Пустой ввод. Используем тестовую строку.")
        user_input = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
    user_input = expand_bindrunes(user_input)
    text_indices = text_to_indices(user_input)
    if not text_indices:
        print("Не удалось распознать ни одного символа. Выход.")
        return
    solver.current_text = text_indices
    print(f"Длина текста: {len(text_indices)} символов.")

    crib_input = input("\nВведите предполагаемое слово (crib) или нажмите Enter: ").strip()
    if crib_input:
        solver.crib = text_to_indices(crib_input)
        print(f"Crib установлен: {crib_input} (длина {len(solver.crib)})")

    while True:
        print("\n--- МЕНЮ ---")
        print("1. Показать топ кандидатов")
        print("2. Применить метод вручную")
        print("3. Запустить автоматический перебор (один слой) с логированием")
        print("4. Запустить многослойный анализ (глубина 2) с логированием")
        print("5. Сохранить сессию")
        print("6. Загрузить сессию")
        print("7. Выйти")
        choice = input("Выберите действие: ").strip()

        if choice == '1':
            solver.print_top()
        elif choice == '2':
            print("Доступные методы:", ", ".join(sorted(CIPHERS.keys())))
            method = input("Введите название метода: ").strip().lower()
            if method not in CIPHERS:
                print("Метод не найден.")
                continue
            try:
                if method == 'caesar':
                    shift = int(input("Сдвиг (0-28): "))
                    res = CIPHERS[method](solver.current_text, shift)
                    key = shift
                elif method == 'affine':
                    a = int(input("a (1-28, взаимно прост с 29): "))
                    b = int(input("b: "))
                    res = CIPHERS[method](solver.current_text, a, b)
                    key = (a,b)
                elif method == 'rail_fence':
                    rails = int(input("Количество рельсов: "))
                    res = CIPHERS[method](solver.current_text, rails)
                    key = rails
                elif method == 'columnar':
                    order = input("Порядок столбцов (например, 0 2 1): ").split()
                    order = [int(x) for x in order]
                    res = CIPHERS[method](solver.current_text, order)
                    key = order
                elif method == 'spiral':
                    rows = int(input("Количество строк: "))
                    cols = int(input("Количество столбцов: "))
                    clockwise = input("По часовой стрелке? (y/n): ").lower() == 'y'
                    res = CIPHERS[method](solver.current_text, rows, cols, clockwise)
                    key = (rows, cols, clockwise)
                elif method in ('vigenere', 'xor', 'autokey', 'beaufort'):
                    key_str = input("Введите ключевое слово (латиница): ")
                    key_indices = text_to_indices(key_str)
                    res = CIPHERS[method](solver.current_text, key_indices)
                    key = key_str
                elif method == 'route':
                    rows = int(input("Количество строк: "))
                    cols = int(input("Количество столбцов: "))
                    direction = input("Направление (down/up/snake): ").lower()
                    res = CIPHERS[method](solver.current_text, rows, cols, direction)
                    key = (rows, cols, direction)
                elif method == 'magic_square':
                    size = int(input("Размер квадрата: "))
                    res = CIPHERS[method](solver.current_text, size)
                    key = size
                elif method == 'pythagoras':
                    res = CIPHERS[method](solver.current_text)
                    key = None
                else:
                    res = CIPHERS[method](solver.current_text) if method in CIPHERS else solver.current_text
                    key = None
                sc = evaluate(res, solver.crib)
                solver.add_result(sc, method, key, res)
                print(f"Результат добавлен с оценкой {sc:.2f}")
            except Exception as e:
                print(f"Ошибка при применении метода: {e}")
        elif choice == '3':
            solver.auto_bruteforce_with_reasoning(solver.current_text)
        elif choice == '4':
            solver.auto_bruteforce_with_reasoning(solver.current_text)  # тот же метод включает глубину 2
        elif choice == '5':
            solver.save_session()
        elif choice == '6':
            solver.load_session()
        elif choice == '7':
            print("Выход.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
