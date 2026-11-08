# Classical Cipher Library

This sub‑project provides a minimal, pure‑Python implementation of
common classical ciphers:

* **Caesar** – simple shift cipher.
* **Vigenère** – key‑based shift cipher.
* **Substitution** – arbitrary mapping of the 26‑letter Latin alphabet.
* **Transposition** – columnar transposition with a numeric key.

Each module exposes an ``encrypt`` and ``decrypt`` function that
operate on Unicode strings and preserve non‑alphabetic characters.

The implementation is intentionally straightforward so it can be
used as a teaching aid or for quick experimentation.

## Usage

```python
from ciphers.caesar import encrypt as caesar_encrypt
from ciphers.vigenere import encrypt as vigenere_encrypt

print(caesar_encrypt("Hello", shift=3))  # Khoor
print(vigenere_encrypt("Hello", keyword="KEY"))  # Rijvs
```

Feel free to extend or modify the implementations as needed.
