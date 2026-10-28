#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
████████████████████████████████████████████████████████████████████████
██  ULTIMATE DECODER v4.0 — txt.txt ANALYZER                          ██
██  Все методы криптоанализа + визуализация + эвристики              ██
██  Вывод ТОЛЬКО в консоль | Чтение ТОЛЬКО txt.txt                   ██
████████████████████████████████████████████████████████████████████████
"""

import re
import sys
import math
import string
import base64
import zlib
from collections import Counter, defaultdict
from itertools import cycle, islice
from typing import List, Tuple, Optional

# Проверка наличия PIL для визуализации
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL не найден. Визуализация будет пропущена.")
    print("   Установите: pip install pillow\n")

# ════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════
FILE_PATH = 'txt.txt'
OUTPUT_IMAGE = 'decoded_image.png'
VERBOSE = True
MAX_PREVIEW = 300

def log(msg: str, level: str = "INFO"):
    prefix = {"INFO": "ℹ", "SUCCESS": "✓", "ERROR": "✗", "DEBUG": "•", "WARN": "⚠"}
    print(f"[{prefix.get(level, '?')}] {msg}")

def banner(text: str):
    print("\n" + "═" * 78)
    print(f"  🔍 {text}")
    print("═" * 78)

# ════════════════════════════════════════════════════════════════════
# LOAD & PREPROCESS
# ════════════════════════════════════════════════════════════════════
banner("ЗАГРУЗКА И ПРЕД-ОБРАБОТКА")

with open(FILE_PATH, 'r', encoding='utf-8', errors='replace') as f:
    RAW = f.read()

log(f"Размер файла: {len(RAW):,} символов", "SUCCESS")
log(f"Строк: {RAW.count(chr(10)) + 1:,}")
log(f"Точек: {RAW.count('.'):,} ({RAW.count('.')/len(RAW)*100:.2f}%)")
log(f"Пробелов: {RAW.count(' '):,}")

# Извлечение блоков: 8 символов, разделённые пробелом
def parse_blocks(text: str) -> List[Tuple[int, int, str]]:
    blocks = []
    for line_idx, line in enumerate(text.strip().split('\n')):
        parts = line.split(' ')
        for block_idx, part in enumerate(parts):
            if part.strip():
                block = part[:8].ljust(8, '.')
                blocks.append((line_idx, block_idx, block))
    return blocks

BLOCKS = parse_blocks(RAW)
log(f"Извлечено блоков: {len(BLOCKS):,}", "SUCCESS")
log(f"Уникальных блоков: {len(set(b[2] for b in BLOCKS)):,}")

# ════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════
def block_to_byte(block: str, mode: str = 'dot0') -> int:
    if mode == 'dot0':
        val = 0
        for i, c in enumerate(block[:8]):
            if c != '.':
                val |= (1 << (7 - i))
        return val
    return 0

def byte_to_char(b: int) -> str:
    return chr(b) if 32 <= b <= 126 else '?'

def english_score(text: str) -> float:
    common = 'etaoin shrdlu'
    if not text: return 0
    return sum(1 for c in text.lower() if c in common) / len(text)

def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

# ════════════════════════════════════════════════════════════════════
# DATA EXTRACTION
# ════════════════════════════════════════════════════════════════════
bytes_bitmask = [block_to_byte(b[2]) for b in BLOCKS]
signal_bytes = [b for b in bytes_bitmask if b != 0]

# Извлечение чисел и триплетов
num_pattern = re.compile(r'\.(\d{3})\.(\d{3})')
num_pairs = num_pattern.findall(RAW)
all_numbers = []
for n1, n2 in num_pairs:
    try:
        all_numbers.append(int(n1))
        all_numbers.append(int(n2))
    except:
        pass

triplet_pattern = re.compile(r'\.([A-Z]{3})\.([A-Z]{3})')
triplet_pairs = triplet_pattern.findall(RAW)
all_triplets = [t for pair in triplet_pairs for t in pair]

# ════════════════════════════════════════════════════════════════════
# МЕТОД 1: XOR БРУТ-ФОРС
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 1: XOR БРУТ-ФОРС")

best_key, best_score, best_text = None, -1, ""
for key in range(256):
    decoded = bytes([b ^ key for b in signal_bytes[:2000]])
    text = decoded.decode('ascii', errors='ignore')
    score = english_score(text)
    if score > best_score:
        best_score, best_key, best_text = score, key, text[:100]

if best_key:
    log(f"Лучший XOR-ключ: {best_key} (0x{best_key:02x}), оценка: {best_score:.3f}", "SUCCESS")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 2: ПОЗИЦИОННОЕ КОДИРОВАНИЕ
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 2: ПОЗИЦИОННОЕ КОДИРОВАНИЕ")

pos_decoded = []
for _, _, block in BLOCKS:
    for pos, c in enumerate(block[:8]):
        if c.isalpha():
            base = ord(c.lower()) - ord('a')
            shifted = (base + pos) % 26
            pos_decoded.append(chr(ord('A') + shifted))
            break
log(f"Символов через позицию: {len(pos_decoded):,}")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 3: КЛЮЧ ИЗ ТРИПЛЕТОВ
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 3: КЛЮЧ ИЗ ТРИПЛЕТОВ")

def triplet_to_key(pairs, length=256):
    key = []
    for t1, t2 in pairs:
        if len(t1) >= 1 and len(t2) >= 1:
            diff = (ord(t2[0]) - ord(t1[0])) % 26
            key.append(65 + diff)
            if len(key) >= length:
                break
    return bytes(key or [65] * length)

triplet_key = triplet_to_key(triplet_pairs)
xor_triplet = []
for i, b in enumerate(signal_bytes[:MAX_PREVIEW]):
    k = triplet_key[i % len(triplet_key)] if triplet_key else 65
    dec = b ^ k
    xor_triplet.append(byte_to_char(dec))
print(f"XOR с триплет-ключом: {''.join(xor_triplet)[:100]}")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 4: ЧИСЛА → СИМВОЛЫ (OCT/HEX/ASCII)
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 4: ЧИСЛА → СИМВОЛЫ")

def interpret_numbers(pairs, method: str) -> str:
    result = []
    for n1, n2 in pairs[:100]:
        for n in [n1, n2]:
            try:
                if method == 'ascii':
                    val = int(n)
                    if 32 <= val <= 126:
                        result.append(chr(val))
                elif method == 'octal':
                    val = int(n, 8)
                    if 32 <= val <= 126:
                        result.append(chr(val))
                elif method == 'hex':
                    val = int(n, 16)
                    if 32 <= val <= 126:
                        result.append(chr(val))
            except:
                pass
    return ''.join(result)

for method in ['ascii', 'octal', 'hex']:
    decoded = interpret_numbers(num_pairs, method)
    if decoded:
        print(f"  {method:6s}: {decoded[:50]}")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 5: АНАЛИЗ ТРИПЛЕТОВ
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 5: АНАЛИЗ ТРИПЛЕТОВ")

log(f"Найдено пар триплетов: {len(triplet_pairs):,}")
unique_triplets = set(all_triplets)
log(f"Уникальных триплетов: {len(unique_triplets)}")

print("\nПервые 30 триплетов в порядке появления:")
for i, t in enumerate(all_triplets[:30]):
    if i % 6 == 0: print()
    print(f"  {t}", end="")
print()

# ════════════════════════════════════════════════════════════════════
# МЕТОД 6: ПОВТОРЯЮЩИЕСЯ ТРИПЛЕТЫ (AAA, BBB...)
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 6: ПОВТОРЯЮЩИЕСЯ ТРИПЛЕТЫ")

repeating = [t for t in unique_triplets if len(set(t)) == 1]
log(f"Найдено повторяющихся триплетов: {len(repeating)}")
if repeating:
    print("Примеры:", '  '.join(sorted(repeating)[:15]))

# ════════════════════════════════════════════════════════════════════
# МЕТОД 7: ТРИПЛЕТЫ → ЧИСЛА (A=1, B=2...)
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 7: ТРИПЛЕТЫ → ЧИСЛА")

print("\nДекодирование первых 20 триплетов:")
for t in all_triplets[:20]:
    nums = [ord(c) - ord('A') + 1 for c in t]
    print(f"  {t} → {nums} (сумма={sum(nums)})")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 8: КООРДИНАТНАЯ ВИЗУАЛИЗАЦИЯ
# ════════════════════════════════════════════════════════════════════
banner("МЕТОД 8: КООРДИНАТНАЯ ВИЗУАЛИЗАЦИЯ")

if num_pairs:
    coords = [(int(n1) % 80, int(n2) % 30) for n1, n2 in num_pairs[:500]]
    grid = [['·' for _ in range(80)] for _ in range(30)]
    for x, y in coords:
        if 0 <= x < 80 and 0 <= y < 30:
            grid[y][x] = '█'
    
    print("Координатная карта (30×80) из числовых пар:")
    print("   " + "─" * 70)
    for row in grid:
        print("   " + ''.join(row))
    print("   " + "─" * 70)

# ════════════════════════════════════════════════════════════════════
# МЕТОД 9: ВИЗУАЛИЗАЦИЯ КАК ИЗОБРАЖЕНИЕ
# ════════════════════════════════════════════════════════════════════
banner("🎨 ВИЗУАЛИЗАЦИЯ КАК ИЗОБРАЖЕНИЕ")

if PIL_AVAILABLE:
    IMG_WIDTH, IMG_HEIGHT = 1024, 1024
    TOTAL_PIXELS = IMG_WIDTH * IMG_HEIGHT
    
    log(f"Создание изображения {IMG_WIDTH}x{IMG_HEIGHT}...", "INFO")
    
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (0, 0, 0))
    pixels = img.load()
    
    signal_blocks = [b[2] for b in BLOCKS if b[2] != '........']
    log(f"Сигнальных блоков для визуализации: {len(signal_blocks):,}", "SUCCESS")
    
    def block_to_color(block: str) -> Tuple[int, int, int]:
        upper = sum(1 for c in block if c.isupper())
        lower = sum(1 for c in block if c.islower())
        digit = sum(1 for c in block if c.isdigit())
        special = sum(1 for c in block if not c.isalnum() and c != '.')
        
        r = min(255, upper * 50 + special * 30)
        g = min(255, lower * 50 + digit * 30)
        b = min(255, (upper + lower) * 25 + special * 40)
        return (r, g, b)
    
    for idx, block in enumerate(signal_blocks[:TOTAL_PIXELS]):
        x = idx % IMG_WIDTH
        y = idx // IMG_WIDTH
        if y >= IMG_HEIGHT: break
        pixels[x, y] = block_to_color(block)
    
    img.save(OUTPUT_IMAGE)
    log(f"✓ Изображение сохранено: {OUTPUT_IMAGE}", "SUCCESS")
    log(f"Заполнено пикселей: {min(len(signal_blocks), TOTAL_PIXELS):,} из {TOTAL_PIXELS:,}")
    
    # Мини-превью
    print("\n   Мини-превью (символьное представление):")
    print("   " + "─" * 70)
    preview_chars = []
    for block in signal_blocks[:1400]:
        preview_chars.append('█' if block != '........' else '·')
    
    for row in range(0, 1400, 70):
        print("   " + ''.join(preview_chars[row:row+70]))
    print("   " + "─" * 70)
else:
    log("PIL не доступен. Пропускаем создание изображения.", "WARN")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 10: ЭНТРОПИЯ И СТАТИСТИКА
# ════════════════════════════════════════════════════════════════════
banner("📊 ЭНТРОПИЯ И СТАТИСТИКА")

def calculate_entropy(data: bytes) -> float:
    """Рассчитывает энтропию Шеннона для байтовых данных"""
    if not data:
        return 0.0
    from collections import Counter
    import math
    freq = Counter(data)
    length = len(data)
    return -sum((count / length) * math.log2(count / length) 
                for count in freq.values() if count > 0)

entropy = calculate_entropy(bytes(signal_bytes))
log(f"Энтропия сигнальных байт: {entropy:.4f} бит/символ")

if entropy > 7.5:
    print("   ⚠ Высокая энтропия → возможно, зашифровано или сжато")
elif entropy < 4:
    print("   ✓ Низкая энтропия → возможно, текст или структурированные данные")

# Биграммы
signal_chars = [c for b in BLOCKS for c in b[2] if c not in '. ']
bigrams = Counter(''.join(pair) for pair in zip(signal_chars, signal_chars[1:]))
print("\nТоп-10 биграмм:")
for bg, cnt in bigrams.most_common(10):
    print(f"  {bg}: {cnt}")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 11: МАТЕМАТИЧЕСКИЕ ПАТТЕРНЫ
# ════════════════════════════════════════════════════════════════════
banner("🔢 МАТЕМАТИЧЕСКИЕ ПАТТЕРНЫ")

primes_found = [n for n in set(all_numbers) if is_prime(n)]
log(f"Уникальных чисел: {len(set(all_numbers))}")
log(f"Простых чисел среди них: {len(primes_found)}")
if primes_found:
    print(f"Простые: {primes_found[:15]}")

# Проверка градиента +111
print("\nПроверка градиента +111:")
sorted_nums = sorted(set(all_numbers))
for i in range(len(sorted_nums)-1):
    if sorted_nums[i+1] - sorted_nums[i] == 111:
        print(f"  {sorted_nums[i]} → {sorted_nums[i+1]} = +111 ✓")

# ════════════════════════════════════════════════════════════════════
# МЕТОД 12: ИЗВЛЕЧЕНИЕ СООБЩЕНИЯ
# ════════════════════════════════════════════════════════════════════
banner("📝 ИЗВЛЕЧЕНИЕ СООБЩЕНИЯ")

# Первые буквы триплетов
first_letters = ''.join(t[0] for t in all_triplets if t)
print(f"Первые буквы триплетов: {first_letters[:100]}...")

# Последние буквы
last_letters = ''.join(t[-1] for t in all_triplets if t)
print(f"Последние буквы триплетов: {last_letters[:100]}...")

# ════════════════════════════════════════════════════════════════════
# ФИНАЛЬНЫЙ ОТЧЁТ
# ════════════════════════════════════════════════════════════════════
banner("🎯 ИТОГОВЫЙ ОТЧЁТ")

print("""
╔══════════════════════════════════════════════════════════════════════╗
║  📊 ОБЩАЯ СТАТИСТИКА:                                               ║
║  • Всего блоков:           {:>10,}                                  ║
║  • Сигнальных байт:          {:>10,} ({:.1f}%)                     ║
║  • Уникальных блоков:        {:>10,}                                  ║
║  • Энтропия:                 {:>10.4f} бит/символ                   ║
║                                                                    ║
║  🔑 ПАРАМЕТРЫ ДЕКОДИРОВАНИЯ:                                       ║
║  • Лучший XOR-ключ:          {:>10} (0x{:02x})                    ║
║  • Триплет-ключ:             {:>10} байт                            ║
║  • Числовых пар:             {:>10,}                                  ║
║  • Простых чисел:            {:>10,}                                  ║
║                                                                    ║
║  🎨 ВИЗУАЛИЗАЦИЯ:                                                  ║
║  • Изображение:              {:>10}                                  ║
║  • Размер:                   {:>10}                                  ║
║                                                                    ║
║  🚀 РЕКОМЕНДАЦИИ:                                                  ║
║  1. Откройте {} и ищите паттерны/текст                    ║
║  2. Проверьте простые числа на соответствие ключам                ║
║  3. Попробуйте комбинацию: позиционный декод + XOR                ║
║  4. Ищите сигнатуры форматов в декодированных данных              ║
║  5. Проверьте координатную карту на наличие форм                  ║
╚══════════════════════════════════════════════════════════════════════╝
""".format(
    len(BLOCKS),
    len(signal_bytes), len(signal_bytes)/len(BLOCKS)*100,
    len(set(b[2] for b in BLOCKS)),
    entropy,
    best_key if best_key else 'N/A', best_key if best_key else 0,
    len(triplet_key),
    len(num_pairs),
    len(primes_found),
    OUTPUT_IMAGE if PIL_AVAILABLE else 'Не создано',
    f"{IMG_WIDTH}x{IMG_HEIGHT}" if PIL_AVAILABLE else 'N/A',
    OUTPUT_IMAGE
))

print("\n✅ АНАЛИЗ ЗАВЕРШЁН | Удачи в расшифровке! 🔐✨\n")