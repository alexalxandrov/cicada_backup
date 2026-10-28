# -*- coding: utf-8 -*-
"""
Расшифровка второго слоя страницы 17 Liber Primus.
Гипотеза: ключ = "SENECAEST" (индексы по Gematria Primus) применяется к остатку после "SENECA EST".
Методы: сложение/вычитание (циклически) и автоключ.
"""

# Таблица Gematria Primus (индекс -> латиница, как в документе)
index_to_latin = {
    0: 'F', 1: 'U', 2: 'TH', 3: 'O', 4: 'R', 5: 'C', 6: 'G', 7: 'W',
    8: 'H', 9: 'N', 10: 'I', 11: 'J', 12: 'EO', 13: 'P', 14: 'X', 15: 'S',
    16: 'T', 17: 'B', 18: 'E', 19: 'M', 20: 'L', 21: 'NG', 22: 'OE', 23: 'D',
    24: 'A', 25: 'AE', 26: 'Y', 27: 'IA', 28: 'EA'
}

# Обратный словарь для преобразования латиницы (диграфов) в индекс
# Для простоты зададим соответствие вручную, но можно построить из index_to_latin
latin_to_index = {v: k for k, v in index_to_latin.items()}

# Ключ "SENECAEST" в индексах
key_word = "SENECAEST"
key_indices = [latin_to_index[ch] for ch in key_word]  # S=15, E=18, N=9, E=18, C=5, A=24, E=18, S=15, T=16

# Остаток после "SENECA EST" в виде латинской строки (диграфы сохранены)
# Взято из вашего вывода: "MOEAHNGNGAAEAEUOEAEHNGBBAECUCXSIBTHIAXWIWBOBNGHWNGAEBBNGHBSEASNGSEAEIABBBSICBGHAENGEANGSBBIACIBNGOEABAESECISIBIEABCIBBBBBEEAEOAHBIBISNGAEHBBBBBBSXAIBIAEAEBBAIABBICEOAEIABBBGTBIBBDHCNGBIABMIANG"
remainder_latin = "MOEAHNGNGAAEAEUOEAEHNGBBAECUCXSIBTHIAXWIWBOBNGHWNGAEBBNGHBSEASNGSEAEIABBBSICBGHAENGEANGSBBIACIBNGOEABAESECISIBIEABCIBBBBBEEAEOAHBIBISNGAEHBBBBBBSXAIBIAEAEBBAIABBICEOAEIABBBGTBIBBDHCNGBIABMIANG"

# Преобразуем остаток в список индексов, разбивая по диграфам
def latin_string_to_indices(s):
    idx = 0
    indices = []
    while idx < len(s):
        # Проверяем двухсимвольные диграфы
        if idx+1 < len(s) and s[idx:idx+2] in latin_to_index:
            indices.append(latin_to_index[s[idx:idx+2]])
            idx += 2
        else:
            # Однобуквенный символ
            indices.append(latin_to_index[s[idx]])
            idx += 1
    return indices

remainder_indices = latin_string_to_indices(remainder_latin)
print(f"Длина остатка (в рунах/диграфах): {len(remainder_indices)}")

# Функции расшифровки
def decrypt_vigenere(cipher, key, mode='add'):
    """mode: 'add' (C + K) или 'sub' (C - K)"""
    res = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        if mode == 'add':
            r = (c + k) % 29
        else:  # sub
            r = (c - k) % 29
        res.append(r)
    return res

def decrypt_autokey(cipher, key, mode='add'):
    """Автоключ: сначала ключ, затем расшифрованный текст как ключ."""
    res = []
    key_stream = list(key)
    for i, c in enumerate(cipher):
        k = key_stream[i]
        if mode == 'add':
            r = (c + k) % 29
        else:
            r = (c - k) % 29
        res.append(r)
        key_stream.append(r)  # расшифрованный текст становится частью ключа
    return res

# Режимы для проверки
modes = [
    ("Сложение (циклический ключ)", lambda c, k: decrypt_vigenere(c, k, 'add')),
    ("Вычитание (циклический ключ)", lambda c, k: decrypt_vigenere(c, k, 'sub')),
    ("Сложение (автоключ)", lambda c, k: decrypt_autokey(c, k, 'add')),
    ("Вычитание (автоключ)", lambda c, k: decrypt_autokey(c, k, 'sub')),
]

print("\n" + "="*80)
print("Расшифровка остатка ключом 'SENECAEST'")
print("="*80)

for mode_name, func in modes:
    result_indices = func(remainder_indices, key_indices)
    result_latin = ''.join(index_to_latin[i] for i in result_indices)
    print(f"\n--- {mode_name} ---")
    # Выводим первые 200 символов для оценки
    print(result_latin[:200] + ("..." if len(result_latin) > 200 else ""))

# Дополнительно: проверка с обратным порядком остатка (гипотеза крестов)
print("\n" + "="*80)
print("Остаток в обратном порядке + вычитание (циклический ключ)")
print("="*80)
rev_remainder = remainder_indices[::-1]
rev_result = decrypt_vigenere(rev_remainder, key_indices, 'sub')
rev_latin = ''.join(index_to_latin[i] for i in rev_result)
print(rev_latin[:200] + ("..." if len(rev_latin) > 200 else ""))

# Проверка с красным текстом как ключом (две группы, объединяем)
# Красный текст: ᚾᛗᚠᛗᚷᚻᛗᛟᛚ и ᛞᚠᚠᚠᛟ
red_runes1 = "ᚾᛗᚠᛗᚷᚻᛗᛟᛚ"
red_runes2 = "ᛞᚠᚠᚠᛟ"
# Таблица руна -> индекс (из предыдущих данных)
runes_to_index = {
    'ᚠ':0, 'ᚢ':1, 'ᚦ':2, 'ᚩ':3, 'ᚱ':4, 'ᚳ':5, 'ᚷ':6, 'ᚹ':7,
    'ᚻ':8, 'ᚾ':9, 'ᛁ':10, 'ᛄ':11, 'ᛇ':12, 'ᛈ':13, 'ᛉ':14,
    'ᛋ':15, 'ᛏ':16, 'ᛒ':17, 'ᛖ':18, 'ᛗ':19, 'ᛚ':20, 'ᛝ':21,
    'ᛟ':22, 'ᛞ':23, 'ᚪ':24, 'ᚫ':25, 'ᚣ':26, 'ᛡ':27, 'ᛠ':28
}
red_indices = [runes_to_index[r] for r in red_runes1 + red_runes2]  # объединяем
print("\n" + "="*80)
print("Красный текст как ключ (вычитание, циклический)")
print("="*80)
red_result = decrypt_vigenere(remainder_indices, red_indices, 'sub')
red_latin = ''.join(index_to_latin[i] for i in red_result)
print(red_latin[:200] + ("..." if len(red_latin) > 200 else ""))

# Вывод для самопроверки: ключ "SENECAEST" в индексах
print("\nКлюч 'SENECAEST' в индексах:", key_indices)
print("Длина ключа:", len(key_indices))