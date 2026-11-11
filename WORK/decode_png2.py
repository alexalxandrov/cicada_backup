import sys, zlib, struct, pathlib
png_path='./осталось/17/XOR.png'
if not pathlib.Path(png_path).exists():
    print('PNG not found')
    sys.exit(1)
with open(png_path,'rb') as f:
    data=f.read()
# parse IHDR
offset=8
width=None
height=None
while offset < len(data):
    length=struct.unpack('>I',data[offset:offset+4])[0]
    chunk_type=data[offset+4:offset+8]
    chunk_data=data[offset+8:offset+8+length]
    if chunk_type==b'IHDR':
        width,height,bitdepth,ctype,compression,filter_method,interlace = struct.unpack('>IIBBBBB',chunk_data)
        break
    offset+=12+length
rowbytes=width*3
# collect IDAT
offset=8
idat_chunks=[]
while offset < len(data):
    length=struct.unpack('>I',data[offset:offset+4])[0]
    chunk_type=data[offset+4:offset+8]
    chunk_data=data[offset+8:offset+8+length]
    if chunk_type==b'IDAT':
        idat_chunks.append(chunk_data)
    offset+=12+length
idat_bytes=b''.join(idat_chunks)
raw=zlib.decompress(idat_bytes)
# strip filter
pixels=[]
for i in range(0,len(raw),rowbytes+1):
    pixels.append(raw[i+1:i+1+rowbytes])
raw_pixels=b''.join(pixels)
# XOR
xor_bytes=bytes([b^0x21 for b in raw_pixels])
with open('temp.7z','wb') as f:
    f.write(xor_bytes)
print('Wrote temp.7z',len(xor_bytes))
