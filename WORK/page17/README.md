# Runic Text Extraction – Page 17

This folder contains the artefacts and scripts used to extract the runic
characters from the original Word document (`16_17.docx`) and to perform a
first‑pass OCR on the page image.  The goal is to produce a clean list of
runic glyphs that can be used for further cryptographic analysis.

## Workflow

1. **XML extraction**
   * The Word file was unzipped to `WORK/16_17_docx`.  The text is stored in
     `WORK/16_17_docx/word/document.xml` which is UTF‑8 encoded.
   * All characters in the Unicode range U+16A0–U+16FF were extracted with a short
     Python script (`extract_from_xml.py`).  The result is
     `WORK/page17/runic_chars_from_xml.txt` (same content as the manually
     extracted `runic_chars2.txt`).
   * The script also produces a positional mapping of each rune to the XML
     element (`map_positions.py`).  The mapping is saved in
     `WORK/page17/runic_positions.tsv`.
2. **Frequency analysis**
   * A quick frequency table was generated from the extracted runes (see
     `runic_freq.txt`).
3. **OCR attempts**
   * `tesseract` was run on the original JPEG (`17.jpg`) and the PNG exported
     from Word (`decoded_image.png`).
   * The OCR output for the JPEG is stored in `eng_output.txt` – the text is
     largely gibberish because the runes are not part of the trained language
     models.
   * The PNG produced no OCR output and logged errors.
   * These OCR files are kept for reference but are not considered reliable
     for extracting the runic content.
4. **Substitution cipher attempt**
   * A simple hill‑climbing search was performed to map runes to Latin
     letters.  The best mapping found in a single run is listed in the
     script `hillclimb.py` and the decoded sample is printed to the
     console.  The result is still largely incoherent, indicating that a
     more sophisticated model or a different cipher is needed.

## Results

```text
Total runes: 271
Unique runes: 21
Frequency sorted:
ᚦ 47
ᚾ 43
ᚠ 29
ᛁ 25
ᛈ 22
ᛗ 22
ᚷ 14
ᚻ 12
ᛟ 12
ᛒ 12
ᚱ 8
ᛚ 8
ᛝ 3
ᛋ 2
ᛞ 2
ᛠ 2
ᚢ 2
ᛡ 2
ᛄ 2
ᛉ 1
ᚣ 1
```

## Next steps

* Build a positional mapping of runes to the XML `\u003cw:t\u003e` elements to
  understand their order in the text.
* Compare the extracted list to the OCR output to identify any
  discrepancies or missing glyphs.
* Begin simple frequency‑based cryptanalysis (e.g., test substitution
  hypothesis against known runic alphabets).

---
Author: Cline
Date: 2026‑10‑29
``` 
