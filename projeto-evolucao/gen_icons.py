#!/usr/bin/env python3
"""Gera ícones PWA simples usando apenas stdlib."""
import struct, zlib, os

def png(size):
    """Gera PNG mínimo: fundo #060612 com letra E branca."""
    w = h = size
    # Cada pixel RGB
    bg = (6, 6, 18)
    fg = (255, 255, 255)

    pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            # Desenha um "E" estilizado no centro
            cx = x - w // 2
            cy = y - h // 2
            r = min(w, h) * 0.35
            thickness = r * 0.18
            bar = r * 0.55

            in_circle = (cx**2 + cy**2) <= r**2
            # vertical bar left
            vert = abs(cx + r * 0.15) < thickness and abs(cy) < r * 0.85
            # horizontal bars
            top_bar  = abs(cy + r * 0.6) < thickness and cx > -r * 0.1 and cx < bar
            mid_bar  = abs(cy)           < thickness and cx > -r * 0.1 and cx < bar * 0.75
            bot_bar  = abs(cy - r * 0.6) < thickness and cx > -r * 0.1 and cx < bar

            if vert or top_bar or mid_bar or bot_bar:
                row.extend(fg)
            else:
                row.extend(bg)
        pixels.append(bytes([0] + row))  # filter byte

    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)
    raw = b''.join(pixels)
    idat = chunk(b'IDAT', zlib.compress(raw, 9))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend

os.makedirs('public/icons', exist_ok=True)
for size in [192, 512]:
    data = png(size)
    path = f'public/icons/icon-{size}.png'
    with open(path, 'wb') as f:
        f.write(data)
    print(f'Gerado: {path} ({len(data)} bytes)')

# apple touch icon (180x180)
data = png(180)
with open('public/apple-touch-icon.png', 'wb') as f:
    f.write(data)
print('Gerado: public/apple-touch-icon.png')

# favicon simples 32x32
data = png(32)
with open('public/favicon.ico', 'wb') as f:
    f.write(data)
print('Gerado: public/favicon.ico')
