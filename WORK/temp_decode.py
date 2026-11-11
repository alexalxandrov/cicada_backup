import sys, zlib, struct, pathlib

png_path = pathlib.Path('./осталось/17/XOR.png')
with open(png_path, 'rb') as f:
    data = f.read()

# PNG signature
if data[:8] != b'\x89PNG\r\n\x1a\n':
    print('invalid signature')
    sys.exit(1)

# Parse IHDR to get width, height
idx = 8
while idx < len(data):
    length = struct.unpack('!I', data[idx:idx+4])[0]
    chunk_type = data[idx+4:idx+8].decode()
    chunk_data = data[idx+8:idx+8+length]
    if chunk_type == 'IHDR':
        width, height, bit_depth, color_type, comp, filt, interlace = struct.unpack('!IIBBBBB', chunk_data)
        break
    idx += 12 + length

# Now decompress IDAT
idx = 8
pixels = bytearray()
while idx < len(data):
    length = struct.unpack('!I', data[idx:idx+4])[0]
    chunk_type = data[idx+4:idx+8].decode()
    chunk_data = data[idx+8:idx+8+length]
    if chunk_type == 'IDAT':
        pixels += zlib.decompress(chunk_data)
    if chunk_type == 'IEND':
        break
    idx += 12 + length

# Remove filter bytes
row_bytes = width * 3  # assuming RGB (color_type 2)
plain = bytearray()
ptr = 0
for _ in range(height):
    ptr += 1  # skip filter byte
    plain += pixels[ptr:ptr+row_bytes]
    ptr += row_bytes

# XOR with 0x21
key = 0x21
plain = bytearray([b ^ key for b in plain])

with open('temp.7z', 'wb') as f:
    f.write(plain)

print('Wrote temp.7z, size', len(plain))
