#!/usr/bin/env python3
# Generates minimal placeholder assets locally with no third-party deps.
# Creates 8-bit paletted BMPs, JSON metadata, and simple WAV SFX so CI never breaks.

import os, json, math, wave, struct

ROOT = os.path.dirname(os.path.dirname(__file__))
GFX = os.path.join(ROOT, 'graphics')
AUD = os.path.join(ROOT, 'audio')

os.makedirs(GFX, exist_ok=True)
os.makedirs(AUD, exist_ok=True)

# ---------------- Palette helpers (index 0 = magenta = transparent) ----------------
PALETTE_COLORS = [
    (255, 0, 255), (255, 255, 255), (0, 0, 0), (238, 238, 238),
    (136, 136, 136), (34, 34, 34), (67, 148, 0), (106, 190, 48),
    (55, 148, 110), (90, 60, 30), (222, 238, 214), (255, 204, 0),
    (255, 110, 89), (255, 36, 66), (0, 168, 255), (68, 36, 52),
]

def _write_bmp(path, pixels):
    w = len(pixels[0]); h = len(pixels)
    row_size = (w + 3) & ~3  # pad rows to 4 bytes
    img = bytearray()
    for y in range(h - 1, -1, -1):
        row = bytes(pixels[y])
        img.extend(row)
        img.extend(b"\x00" * (row_size - w))
    palette = bytearray()
    for i in range(256):
        if i < len(PALETTE_COLORS): r, g, b = PALETTE_COLORS[i]
        else: r = g = b = 0
        palette.extend([b, g, r, 0])
    header_size = 14 + 40 + len(palette)
    file_size = header_size + len(img)
    with open(path, 'wb') as f:
        f.write(struct.pack('<2sIHHI', b'BM', file_size, 0, 0, header_size))
        f.write(struct.pack('<IIIHHIIIIII', 40, w, h, 1, 8, 0, len(img), 0, 0, 256, 0))
        f.write(palette)
        f.write(img)

def _new_image():
    return [[0] * 32 for _ in range(32)]

def _circle(im, cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if 0 <= x < 32 and 0 <= y < 32 and (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                im[y][x] = color

def _rect(im, x0, y0, x1, y1, color):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < 32 and 0 <= y < 32:
                im[y][x] = color

def make_player(path_bmp, path_json):
    im = _new_image()
    _circle(im, 16, 16, 10, 7)
    _rect(im, 8, 24, 14, 28, 9)
    _rect(im, 18, 24, 24, 28, 9)
    _circle(im, 13, 14, 2, 1)
    _circle(im, 19, 14, 2, 1)
    _circle(im, 11, 11, 2, 3)
    _write_bmp(path_bmp, im)
    json.dump({"type": "sprite", "width": 32, "height": 32}, open(path_json, 'w'))

def make_enemies(path_bmp, path_json):
    im = _new_image()
    _rect(im, 4, 10, 28, 26, 12)
    _rect(im, 8, 14, 12, 18, 1)
    _rect(im, 20, 14, 24, 18, 1)
    for x in range(4, 28):
        im[26][x] = 5
    _write_bmp(path_bmp, im)
    json.dump({"type": "sprite", "width": 32, "height": 32}, open(path_json, 'w'))

def make_tiles(path_bmp, path_json):
    im = _new_image()
    _rect(im, 0, 20, 32, 32, 9)
    for x in range(0, 32, 2):
        im[28][x] = 5
    _rect(im, 0, 16, 32, 20, 6)
    for x in range(0, 32, 4):
        im[16][x] = 7
        if x + 1 < 32:
            im[17][x + 1] = 7
    _write_bmp(path_bmp, im)
    json.dump({"type": "sprite", "width": 32, "height": 32}, open(path_json, 'w'))

def make_beep(path_wav, freq_hz=880, ms=120, volume=0.6):
    rate = 22050; n = int(rate * ms / 1000)
    with wave.open(path_wav, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        for i in range(n):
            t = i / rate
            sample = int(volume * 32767 * math.sin(2 * math.pi * freq_hz * t))
            w.writeframes(struct.pack('<h', sample))

if __name__ == '__main__':
    make_player(os.path.join(GFX, 'player.bmp'), os.path.join(GFX, 'player.json'))
    make_enemies(os.path.join(GFX, 'enemies.bmp'), os.path.join(GFX, 'enemies.json'))
    make_tiles(os.path.join(GFX, 'tiles.bmp'), os.path.join(GFX, 'tiles.json'))
    make_beep(os.path.join(AUD, 'jump.wav'),   freq_hz=880)
    make_beep(os.path.join(AUD, 'collect.wav'),freq_hz=1320)
    make_beep(os.path.join(AUD, 'hit.wav'),    freq_hz=220, ms=180)
    make_beep(os.path.join(AUD, 'pause.wav'),  freq_hz=660)
    print('Assets generated into graphics/ and audio/')
