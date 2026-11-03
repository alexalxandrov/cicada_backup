import xml.etree.ElementTree as ET

XML_PATH = 'WORK/16_17_docx/word/document.xml'
OUTPUT_PATH = 'WORK/page17/runic_positions.tsv'

def main():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    positions = []
    idx = 0
    for elem in root.findall('.//w:t', ns):
        for ch in elem.text or '':
            if 'ᚠ' <= ch <= '᛿':
                xml_id = elem.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', '')
                positions.append((idx, ch, xml_id))
                idx += 1
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('index\trune\txml_id\n')
        for idx, rune, xml_id in positions:
            f.write(f'{idx}\t{rune}\t{xml_id}\n')
    print(f'Mapped {len(positions)} runes to XML in {OUTPUT_PATH}')


if __name__ == '__main__':
    main()