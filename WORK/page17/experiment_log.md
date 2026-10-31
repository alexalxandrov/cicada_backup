# Page 17 Decryption Experiments

All experiments were run in the :file:`/Users/oleg/Documents/GitHub/cicada_backup/WORK/page17` directory.  The original runic ciphertext is stored in
``runic_chars2.txt``.  For each experiment the script output was redirected to a
dedicated file.  Below is a summary of the results.

## 1. Vigenère‑style shift search (21‑letter alphabet, key lengths 2‑12)
* Script: :file:`vigenere_shifts.py`
* Output file: :file:`vigenere_output_long.txt`
* Best score: **478.2** (key length 4, shifts `[2, 2, 13, 5]`)
* Plaintext sample (first 200 characters):
+```
aigoangesganuigdurmbsmraasfoirfabawdtbcdrnfasttgsrmorrttgmpnggvtnurdoitmmfrgbgrofstrbiusnbmnncgmcsggoncrugtebtctgtfewtoacnmgwrgatrnabmrnbsgbnncabttambgnrrratutbtreltcroutrbttpautcatncorafgttcbbrggtnca
```
* Verdict: No recognizable English text.

## 2. Vigenère‑style shift search (26‑letter alphabet, key lengths 2‑12)
* Script: :file:`vigenere_shifts_full26.py`
* Output file: :file:`vigenere_output_full26.txt`
* Scores identical to the 21‑letter version (best **478.2** at key 4).
* Plaintext sample unchanged – still gibberish.

## 3. Hill‑climb mono‑alphabetic mapping (21‑letter alphabet)
* Script: :file:`hillclimb21.py`
* Output file: :file:`hillclimb_output.txt`
* Best score: **636.31** with mapping:
+```
{ᚦ: 's', ᚾ: 'a', ᚠ: 't', ᛁ: 'o', ᛈ: 'i', ᛗ: 'r', ᚷ: 'm', ᚻ: 'u', ᛟ: 'p', ᛒ: 'c', ᚱ: 'n', ᛚ: 'h', ᛝ: 'e', ᛋ: 'w', ᛞ: 'f', ᛠ: 'v', ᚢ: 'l', ᛡ: 'd', ᛄ: 'b', ᛉ: 'g', ᚣ: 'y'}
```
* Decoded sample (first 200 characters):
+```
nuoonaomophiruorrimsohtanoaouiaatnurstsriaaaosrtoimoiiruphiippwuartrmurphftttptoforctungatmiacopcootmascrprmtssupsameseacamteioasipathtitoosaasatsrahtoiiitasrrssichsctorstsssiarssasasoinatsssstiotsasa
```
* Verdict: No coherent English.

## 4. Bigram frequency analysis
* Script: :file:`bigram_analysis.py`
* Output file: :file:`bigram_output.txt`
* Top 20 bigrams:
+```
ᚦᚾ	15
ᚦᚦ	14
ᚾᚦ	12
ᚾᚾ	8
ᚾᚠ	6
ᚠᚦ	6
ᚦᛗ	5
ᚠᛁ	5
ᛈᚾ	4
ᛗᚦ	4
ᛁᛈ	4
ᛈᛈ	4
ᚠᚷ	4
ᛁᛁ	3
ᚾᛁ	3
ᛟᛚ	3
ᛁᛗ	3
ᛗᛈ	3
ᚦᛁ	3
ᛚᚠ	3
```
* The most frequent bigram `ᚦᚾ` could correspond to an English digraph like `th` or `sh`.

## Next Steps
1. Expand Vigenère key length range to 12‑15 or 20.
2. Try a different scoring metric (e.g., 5‑gram log‑probability).
3. Explore alternative cipher families (Caesar, affine, simple substitution with full alphabet).
4. Use the bigram analysis to construct a partial mapping and run a guided hill‑climb.

All scripts and data are located in the :file:`WORK/page17` directory.