import sys, zlib, struct, pathlib
png_path='./осталось/17/XOR.png'
if not pathlib.Path(png_path).exists():
    print('PNG not found')
    sys.exit(1)
with open(png_path,'rb') as f:
    data=f.read()
# PNG signature
sig=data[:8]
assert sig==b'\x89PNG\r\n\x1a\n'
# parse chunks
offset=8
idat_chunks=[]
while offset < len(data):
    length=struct.unpack('>I',data[offset:offset+4])[0]
    chunk_type=data[offset+4:offset+8]
    chunk_data=data[offset+8:offset+8+length]
    # crc = data[offset+8+length:offset+12+length]
    if chunk_type==b'IDAT':
        idat_chunks.append(chunk_data)
    offset+=12+length
idat_bytes=b''.join(idat_chunks)
# decompress
try:
    decompressed=zlib.decompress(idat_bytes)
except Exception as e:
    print('zlib decompress error:', e)
    sys.exit(1)
# XOR
xor_data=bytes([b^0x21 for b in decompressed])
with open('temp.7z','wb') as f:
    f.write(xor_data)
print('written temp.7z',len(xor_data))
