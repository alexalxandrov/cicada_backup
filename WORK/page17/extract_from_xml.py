import xml.etree.ElementTree as ET

XML_PATH = 'WORK/16_17_docx/word/document.xml'
OUTPUT_PATH = 'WORK/page17/runic_chars_from_xml.txt'

def main():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    runic_text = []
    for t in root.findall('.//w:t', ns):
        for ch in t.text or '':
            if 'ᚠ' <= ch <= '᛿':
                runic_text.append(ch)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(''.join(runic_text))
    print(f'Extracted {len(runic_text)} runes to {OUTPUT_PATH}')


if __name__ == '__main__':
    main()