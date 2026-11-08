# Page 17 Analysis Summary

## Rune Text (copied from master transcription)
The extracted rune sequence for page 17 is stored in `WORK/analysis/page17_content.txt`.  It contains 273 runes (including punctuation runes).  The text runs from the top of the page up to the closing paragraph delimiter `&`.

## Decryption Scores (from prior automated runs)
| Tool | Best Score | Key / Strategy |
|------|-----------|----------------|
| **Rosetta** | **-6.934** | `INSTAR|atbash` (Atbash first, then Vigenère with keyword INSTAR) |
| **Keyword/Vigenère** | **-6.286** | `ENLIGHTENMENT` (plain Vigenère, no Atbash) |
| **Autokey** | -6.981 | `PILGRIM` (key = PILGRIM, plain autokey Vigenère) |

The Rosetta score is the lowest (most negative) among the three runs, suggesting the *Atbash + Vigenère* strategy with the keyword **INSTAR** is currently the best candidate for page 17.

## Next Steps
1. **Translate runes to letters** using the Gematria‑Primus table (29‑rune ↔ 29‑letter mapping).  The translation tool is available in the external repository `cicada-solvers/GematriaPrimusTool`; the mapping can be reproduced manually if the tool is inaccessible.
2. **Apply Atbash** (reverse mapping) to the transliterated text.
3. **Decrypt with Vigenère** using the keyword `INSTAR`.  The resulting plaintext will be evaluated for linguistic coherence and cross‑checking with known Liber Primus motifs.
4. **Verify against alternative hypotheses** (e.g., `ENLIGHTENMENT` keyword, or running an autokey decryption).  Compare language‑model scores to confirm best fit.
5. **Document results** in `WORK/analysis/page17_decrypted.txt` and update `WORK/STATUS.md` with the new state.

If the Atbash + Vigenère approach fails to produce intelligible plaintext, consider exploring a running‑key or totient‑stream variant, or revisiting the possibility of a *double* Atbash (i.e., Atbash → Vigenère → Atbash).

---

> **Note**: The Gematria‑Primus translator is not present in the local repository; obtaining the mapping requires pulling the external tool or using the online translator at https://www.boxentriq.com/encodings/gematria-primus-translator.
