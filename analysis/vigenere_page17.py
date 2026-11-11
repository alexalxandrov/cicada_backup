#!/usr/bin/env python3
"""Vigenère analysis on Liber Primus page 17 rune text.

This script copies the rune file from the repository into the WORK directory,
extracts only rune characters, builds a mapping from rune to integer index, and
performs a brute‑force search over key lengths 1..40. For each key length it
tests all possible shifts for each column to find the best decryption according
to chi‑square against English letter frequencies.

The output is the key length with the lowest average chi‑square and the
corresponding key expressed as runes.

The results are printed to stdout and can be redirected to a log file in the
WORK directory.
"""

import pathlib, math

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

# Path to the original rune file in the repository
repo_runes_path = pathlib.Path(
    "GITHUB_REPOS/cicada-solvers__The-Complete-Cicada3301-Archive/2014/Liber Primus/runes in text format.txt"
)

# Working directory where we will copy the file for analysis
work_dir = pathlib.Path("analysis")
work_dir.mkdir(exist_ok=True)

work_runes_path = work_dir / "runes_page17.txt"

# ------------------------------------------------------------
# Copy file to work directory (if not already present)
# ------------------------------------------------------------

if not work_runes_path.exists():
    work_runes_path.write_text(repo_runes_path.read_text(encoding="utf-8"))

# ------------------------------------------------------------
# Load and filter rune characters
# ------------------------------------------------------------

text = work_runes_path.read_text(encoding="utf-8")
# Filter out whitespace and common delimiters; keep only rune characters.
runes = [c for c in text if ord(c) > 127 and not c.isspace() and c not in "-/\u0026%$\n\r§"]

# Build rune to index mapping
unique_runes = sorted(set(runes))
rune_to_idx = {r: i for i, r in enumerate(unique_runes)}
idx_to_rune = {i: r for r, i in rune_to_idx.items()}

# ------------------------------------------------------------
# English letter frequency (normalized) – use only letters that appear
# ------------------------------------------------------------

eng_freq_raw = {
    "E": 12.70,
    "T": 9.06,
    "A": 8.17,
    "O": 7.51,
    "I": 7.04,
    "N": 6.75,
    "S": 6.33,
    "H": 6.09,
    "R": 5.99,
    "D": 4.25,
    "L": 4.03,
    "C": 2.78,
    "U": 2.76,
    "M": 2.41,
    "W": 2.36,
    "F": 2.23,
    "G": 2.02,
    "Y": 1.97,
    "P": 1.93,
    "B": 1.49,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.10,
    "Z": 0.07,
}

# Map to our rune alphabet: use English letter frequencies for the first
# 26 runes (index 0-25). Remaining runes get 0 frequency.
eng_indices = [0.0] * len(unique_runes)
for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    if i < len(eng_indices):
        eng_indices[i] = eng_freq_raw.get(ch, 0.0)
# Normalize to sum to 1.0
total = sum(eng_indices)
if total > 0:
    eng_indices = [f / total for f in eng_indices]

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def chi_square(column):
    """Compute chi‑square for a column of rune indices against
    the expected English distribution."""
    n = len(column)
    observed = [0] * len(unique_runes)
    for idx in column:
        observed[idx] += 1
    chi = 0.0
    for i in range(len(unique_runes)):
        expected = eng_indices[i] * n
        if expected > 0:
            chi += (observed[i] - expected) ** 2 / expected
    return chi

def best_shift_for_column(col):
    """Return the shift value (0..len-1) that minimises chi‑square
    for the given column."""
    best = None
    best_chi = float("inf")
    for shift in range(len(unique_runes)):
        # Decrypt column by shifting backwards
        dec = [(x - shift) % len(unique_runes) for x in col]
        chi = chi_square(dec)
        if chi < best_chi:
            best_chi = chi
            best = shift
    return best, best_chi

def analyse_key_lengths(cipher, max_len=40):
    best_overall = None
    for L in range(1, max_len + 1):
        cols = [[] for _ in range(L)]
        for i, c in enumerate(cipher):
            cols[i % L].append(rune_to_idx[c])
        key_shifts = []
        chi_values = []
        for col in cols:
            shift, chi_val = best_shift_for_column(col)
            key_shifts.append(shift)
            chi_values.append(chi_val)
        avg_chi = sum(chi_values) / L
        if best_overall is None or avg_chi < best_overall[1]:
            best_overall = (L, avg_chi, key_shifts)
    return best_overall

# ------------------------------------------------------------
# Decrypt using the best key and output plaintext
# ------------------------------------------------------------

def decrypt_with_key(cipher, key_shifts):
    """Decrypt the rune cipher using the provided key shifts.
    """
    plain_indices = []
    key_len = len(key_shifts)
    for i, c in enumerate(cipher):
        idx = rune_to_idx[c]
        shift = key_shifts[i % key_len]
        plain_idx = (idx - shift) % len(unique_runes)
        plain_indices.append(plain_idx)
    return ''.join(idx_to_rune[i] for i in plain_indices)

if __name__ == "__main__":
    cipher = runes
    best = analyse_key_lengths(cipher, 40)
    key_shifts = best[2]
    plaintext = decrypt_with_key(cipher, key_shifts)
    output = (
        f"Best key length: {best[0]}\n"
        f"Average chi‑square: {best[1]:.3f}\n"
        f"Best key (runes): {''.join(idx_to_rune[s] for s in key_shifts)}\n"
        f"\nDecrypted text:\n{plaintext}\n"
    )
    print(output)
    # Log to file
    (work_dir / "vigenere_results.txt").write_text(output, encoding="utf-8")
