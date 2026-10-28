#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from collections import defaultdict

TYPE_DELAY = 0.006
LINE_DELAY = 0.0015
SHOW_ANIMATION = True

HERE = Path(__file__).resolve().parent

# Можно положить словари рядом со скриптом под любым из этих имен.
# Также поддерживаются переменные окружения WORDPATTERN_EN и WORDPATTERN_RU.
EN_CANDIDATES = [
    Path(os.environ.get("WORDPATTERN_EN", "")) if os.environ.get("WORDPATTERN_EN") else None,
    HERE / "english.txt",
    HERE / "en.txt",
    HERE / "words_en.txt",
    HERE / "en_US.dic",
    HERE / "en_GB.dic",
    Path("/usr/share/dict/words"),
    Path("/usr/share/hunspell/en_US.dic"),
    Path("/usr/share/hunspell/en_GB.dic"),
    Path("/usr/share/myspell/dicts/en_US.dic"),
    Path("/usr/share/myspell/dicts/en_GB.dic"),
]

RU_CANDIDATES = [
    Path(os.environ.get("WORDPATTERN_RU", "")) if os.environ.get("WORDPATTERN_RU") else None,
    HERE / "russian.txt",
    HERE / "ru.txt",
    HERE / "words_ru.txt",
    HERE / "ru_RU.dic",
    Path("/usr/share/dict/russian"),
    Path("/usr/share/hunspell/ru_RU.dic"),
    Path("/usr/share/myspell/dicts/ru_RU.dic"),
]


def clean_candidates(items):
    out = []
    for x in items:
        if x is None:
            continue
        if isinstance(x, Path) and str(x):
            out.append(x)
    return out


def is_wordish(token: str) -> bool:
    return any(ch.isalpha() for ch in token)


def normalize(token: str) -> str:
    return "".join(ch for ch in token if ch.isalpha())


def signature(text: str) -> str:
    text = normalize(text)
    if not text:
        return ""
    mapping = {}
    out = []
    next_code = ord("A")
    for ch in text.casefold():
        if ch not in mapping:
            mapping[ch] = chr(next_code)
            next_code += 1
        out.append(mapping[ch])
    return "".join(out)


def read_words(path: Path) -> list[str]:
    if not path.exists() or not path.is_file():
        return []

    encodings = ("utf-8-sig", "utf-8", "cp1251", "cp866", "latin1")
    lines = None

    for enc in encodings:
        try:
            with path.open("r", encoding=enc, errors="strict") as f:
                lines = f.read().splitlines()
            break
        except Exception:
            pass

    if lines is None:
        return []

    words = []
    is_dic = path.suffix.lower() == ".dic"

    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if is_dic and i == 0 and line.isdigit():
            continue

        token = line.split("/", 1)[0].strip()
        if is_wordish(token):
            words.append(token)

    return words


def unique_keep_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        key = item.casefold()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def load_index(candidates) -> tuple[dict[str, list[str]], list[Path]]:
    used_paths = []
    loaded = []

    for path in clean_candidates(candidates):
        words = read_words(path)
        if words:
            used_paths.append(path)
            loaded.extend(words)

    loaded = unique_keep_order(loaded)

    index: dict[str, list[str]] = defaultdict(list)
    for w in loaded:
        sig = signature(w)
        if sig:
            index[sig].append(w)

    for k in list(index.keys()):
        index[k] = sorted(unique_keep_order(index[k]), key=lambda s: (s.casefold(), s))

    return dict(index), used_paths


def slow_print(text: str, end="\n", delay=TYPE_DELAY):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(end=end, flush=True)


def slow_lines(lines: list[str], delay=LINE_DELAY):
    for line in lines:
        print(line, flush=True)
        if delay:
            time.sleep(delay)


def animate():
    if not SHOW_ANIMATION:
        return
    print("Поиск", end="", flush=True)
    for _ in range(3):
        time.sleep(0.18)
        print(".", end="", flush=True)
    print("\n", flush=True)


def show_header():
    slow_print("╔══════════════════════════════════════════════╗")
    slow_print("║   WORD PATTERN SEARCH / КРИПТОГРАММЫ v2.0   ║")
    slow_print("╚══════════════════════════════════════════════╝")
    print()


def show_sources(label: str, paths: list[Path]):
    if paths:
        slow_print(f"[{label}] Загруженные словари:")
        for p in paths:
            slow_print(f"  • {p}")
    else:
        slow_print(f"[{label}] Словарь не найден.")


def search(index: dict[str, list[str]], query: str) -> list[str]:
    sig = signature(query)
    if not sig:
        return []
    return index.get(sig, [])


def display_results(title: str, results: list[str]):
    slow_print(f"== {title} ==")
    slow_print(f"Найдено: {len(results)}")
    if not results:
        slow_print("  (ничего)")
        return

    if len(results) > 300:
        delay = 0.0
    elif len(results) > 100:
        delay = 0.0008
    else:
        delay = LINE_DELAY

    for i, word in enumerate(results, 1):
        print(f"{i:5d}. {word}", flush=True)
        if delay:
            time.sleep(delay)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(line_buffering=True)
        except Exception:
            pass

    en_index, en_paths = load_index(EN_CANDIDATES)
    ru_index, ru_paths = load_index(RU_CANDIDATES)

    show_header()
    show_sources("EN", en_paths)
    show_sources("RU", ru_paths)
    print()

    if not en_paths and not ru_paths:
        slow_print("Словари не найдены.")
        slow_print("Положи файлы словарей рядом со скриптом или задай переменные окружения:")
        slow_print("  WORDPATTERN_EN=/path/to/english.dic_or_txt")
        slow_print("  WORDPATTERN_RU=/path/to/russian.dic_or_txt")
        slow_print("")
        slow_print("Подходят:")
        slow_print("  English: SCOWL / ESDB / plain word list / Hunspell .dic")
        slow_print("  Russian: Hunspell .dic из LibreOffice dictionaries")
        return 1

    slow_print("Вводи шаблон как слово или как последовательность букв.")
    slow_print("Примеры: ABBA, AAB, HELLO, КОКОС")
    slow_print("Выход: q / quit / exit / Ctrl+C")
    print()

    while True:
        try:
            query = input("Шаблон > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not query:
            continue

        if query.casefold() in {"q", "quit", "exit"}:
            break

        sig = signature(query)
        if not sig:
            slow_print("Нужно ввести хотя бы одну букву.")
            continue

        animate()

        en_results = search(en_index, query)
        ru_results = search(ru_index, query)

        slow_print(f"Шаблон: {sig}")
        print()

        display_results("ENGLISH", en_results)
        print()
        display_results("РУССКИЙ", ru_results)
        print()

        try:
            input("Enter — новый поиск...")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        print()

    slow_print("Готово.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())