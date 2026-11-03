import sys
from wordfreq import zipf_frequency, top_n_list

def load_mapping():
    # mapping obtained from prior hillclimbing run
    return {
        'ᚠ':'n','ᚢ':'v','ᚣ':'x','ᚦ':'s','ᚱ':'h','ᚷ':'d','ᚻ':'m','ᚾ':'a',
        'ᛁ':'e','ᛄ':'u','ᛈ':'t','ᛉ':'z','ᛋ':'y','ᛒ':'l','ᛗ':'i','ᛚ':'o',
        'ᛝ':'j','ᛞ':'w','ᛟ':'p','ᛠ':'g','ᛡ':'f'
    }

def decode(text, mapping):
    return ''.join(mapping.get(c, c) for c in text)

def segment(text):
    # use words from top 20000
    word_set = {w for w in top_n_list('en', 20000) if 2 <= len(w) <= 7}
    max_len = 7
    n = len(text)
    best = [-1e9] * (n + 1)
    best[0] = 0
    prev = [None] * (n + 1)
    for i in range(1, n + 1):
        for l in range(1, max_len + 1):
            j = i - l
            if j < 0:
                break
            w = text[j:i]
            if w in word_set:
                score = best[j] + zipf_frequency(w, 'en')
                if score > best[i]:
                    best[i] = score
                    prev[i] = (j, w)
    # reconstruct
    seg = []
    idx = n
    while idx > 0 and prev[idx] is not None:
        j, w = prev[idx]
        seg.append(w)
        idx = j
    seg.reverse()
    return ' '.join(seg)


def main():
    with open('WORK/page17/runic_chars2.txt', 'r', encoding='utf-8') as f:
        raw = f.read().strip()
    mapping = load_mapping()
    decoded = decode(raw, mapping)
    seg_text = segment(decoded)
    print('Decoded length:', len(decoded))
    print('Segmented preview:', seg_text[:200])


if __name__ == '__main__':
    main()