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
## 7. Affine cipher brute‑force (21‑letter alphabet)
* Script: :file:`affine_analysis.py`
* Output file: :file:`affine_output.txt`
* Best key (a,b): **(19, 9)**
* Best score: **550.50**
* Decoded sample (first 200 chars):
```
muccmtcacsplrucrrlaocpftmctculttfmuroforltttcorfclacllruspllssdutrfraurspyfffsfcycrbfumvtfaltbcsbccfatobrsrafoousotahohtbtafhlctolstfpflfccottotfortpfclllftorroolbpobfcrofoooltroototoclmtfooooflcfotot
```
\t* Verdict: Still gibberish; affine mapping alone does not produce intelligible English.
## 8. Composite Vigenère (2‑letter key) + Caesar (0‑20) search
\t* Script: :file:`vigenere_caesar_combo.py`
\t* Output file: :file:`vigenere_caesar_output.txt`
\t* Best composite score: **519.06**
\t* Best Vigenère key (shifts): **(2, 5)**
\t* Best Caesar shift: **0**
\t* Decoded sample (first 200 chars):
\t```
\tatsoaasesmmnutsdunobslbaaonoinnabvidtgtdranasbugsnoornutglrngmltndbdotummubgbmbofourbtasngonnrsmcosgoatrumuebbttgbnewbwacaogwnsatngablbnbosbnatabbuamgsnrnbatdubtncltrboubbbtbraubtatatorvngtbtbbnsgtata
\t```
\t* Verdict: Still gibberish; composite approach did not solve the cipher.
## 11. Planned KenLM 5‑gram scorer for hill‑climb
* Rationale: The segmented word‑frequency scorer tends to over‑penalise
  legitimate words that do not appear in the top‑20 k word list.  A 5‑gram
  language model (e.g., KenLM) will better capture English n‑gram
  statistics and may allow the hill‑climb to escape local optima.
* Next steps:
  1. Build a KenLM 5‑gram model from the 1‑M‑word Common Crawl
     dataset (or use an existing pre‑trained model).
  2. Replace the `seg_score` function in `hillclimb26.py` with a
     `kenlm_score` that returns the log‑probability of the decoded
     text.  Normalize by text length to compare across runs.
  3. Re‑run `hillclimb26.py` with the new scorer and record the
     best score, mapping and decoded sample.
  4. If improvement is observed, test the same approach on the
     `guided_hillclimb26.py` and `vigenere_caesar_len3.py` outputs.
* Estimated time: ~30 min to build the model locally, plus 10 min to
  rerun the hill‑climb.
* Script: :file:`guided_hillclimb26.py`
* Output file: :file:`guided_hillclimb26_output.txt`
* Initial score from Caesar mapping: **468.96**
* Best score after guided hill‑climb: **468.96** (no improvement)
* Best mapping: same as the pure Caesar mapping (see output file)
* Decoded sample (first 200 chars):
```
beaabtavaudirearrivpadftbataeittfberpfpritttaprfaivaiireudiiuusetrfrverudcfffufacarhfebntfvithauhaafvtphrurvfppeuptvlplthtvfliatpiutfdfifaapttptfprtdfaiiiftprrppihdphfarpfpppitrpptptpaibtfppppfiafptpt
```
* Verdict: No improvement over the initial Caesar‑based hill‑climb.
## 6. Caesar shift brute‑force (21‑letter alphabet)
* Script: :file:`vigenere_caesar_len3.py`
* Output file: :file:`vigenere_caesar_len3_output.txt`
* Best composite score: **520.11**
* Best Vigenère key (shifts): **(3, 2, 5)**
* Best Caesar shift: **0**
* Decoded sample (first 200 chars):
```
atsoaasesmmnutsdunobslbaaonoinnabvidtgtdranasbugsnoornutglrngmltndbdotummubgbmbofourbtasngonnrsmcosgoatrumuebbttgbnewbwacaogwnsatngablbnbosbnatabbuamgsnrnbatdubtncltrboubbbtbraubtatatorvngtbtbbnsgtata
```
* Verdict: Still gibberish; composite approach did not solve the cipher.
## 6. Caesar shift brute‑force (21‑letter alphabet)
* Script: :file:`caesar_analysis.py`
* Output file: :file:`caesar_output.txt`
* Best shift: **15**
* Best score: **468.96**
* Best mapping: `{'ᚠ': 'f', 'ᚢ': 'g', 'ᚣ': 'y', 'ᚦ': 'p', 'ᚱ': 'b', 'ᚷ': 'v', 'ᚻ': 'e', 'ᚾ': 't', 'ᛁ': 'a', 'ᛄ': 'o', 'ᛈ': 'i', 'ᛉ': 'n', 'ᛋ': 's', 'ᛒ': 'h', 'ᛗ': 'r', 'ᛚ': 'd', 'ᛝ': 'l', 'ᛞ': 'c', 'ᛟ': 'u', 'ᛠ': 'm', 'ᛡ': 'w'}`
* Decoded sample (first 200 chars):
```
beaabtavaudirearrivpadftbataeittfberpfpritttaprfaivaiireudiiuusetrfrverudcfffufacarhfebntfvithauhaafvtphrurvfppeuptvlplthtvfliatpiutfdfifaapttptfprtdfaiiiftprrppihdphfarpfpppitrpptptpaibtfppppfiafptpt
```
* Verdict: Still gibberish; the mapping does not reveal coherent English.
## 5. Hill‑climb mono‑alphabetic mapping (26‑letter alphabet, 5 restarts, 20k steps)
* Script: :file:`hillclimb26.py`
* Settings: RESTARTS=5, STEPS=20,000
* Output file: :file:`hillclimb26_output.txt` (redirected)
* Best score: **645.33**
* Best mapping: `{'ᚦ': 'i', 'ᚾ': 's', 'ᚠ': 'a', 'ᛁ': 'p', 'ᛈ': 'm', 'ᛗ': 't', 'ᚷ': 'h', 'ᚻ': 'c', 'ᛟ': 'r', 'ᛒ': 'o', 'ᚱ': 'u', 'ᛚ': 'f', 'ᛝ': 'd', 'ᛋ': 'q', 'ᛞ': 'b', 'ᛠ': 'e', 'ᚢ': 'l', 'ᛡ': 'g', 'ᛄ': 'n', 'ᛉ': 'k', 'ᚣ': 'j'}`
* Decoded sample (first 200 chars):
```
ucppusphprfmtcpttmhipfasupspcmssauctiaitmssspitapmhpmmtcrfmmrrqcstathctrfbaaarapbptoacuksahmsoproppahsiotrthaiicrishdidsoshadmpsimrsafamappissisaitsfapmmmasittiimofioaptiaiiimstiisisipmusaiiiiampaisis
```
* Verdict: Still gibberish; mapping likely far from correct. Further experiments needed.