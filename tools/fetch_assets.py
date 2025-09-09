#!/usr/bin/env python3
# Generates minimal-but-stylish placeholder assets locally so CI never breaks.
# (No internet required.) Creates BMP+JSON for Butano and simple WAV SFX.

import os, json, math, wave, struct
from PIL import Image, ImageDraw

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

palette = []
for i in range(256):
    if i < len(PALETTE_COLORS): r, g, b = PALETTE_COLORS[i]
    else: r = g = b = 0
    palette.extend([r, g, b])

def new_pal_image(w, h):
    im = Image.new('P', (w, h), color=0)
    im.putpalette(palette)
    return im

def make_player(path_bmp, path_json):
    im = new_pal_image(32, 32); d = ImageDraw.Draw(im)
    d.ellipse((6, 6, 26, 26), fill=7)
    d.ellipse((12, 12, 15, 16), fill=1); d.ellipse((18, 12, 21, 16), fill=1)
    d.ellipse((9, 9, 13, 13), fill=3)
    d.rectangle((8, 24, 14, 28), fill=9); d.rectangle((18, 24, 24, 28), fill=9)
    im.save(path_bmp, format='BMP')
    json.dump({"type": "sprite", "width": 32, "height": 32}, open(path_json, 'w'))

def make_enemies(path_bmp, path_json):
    im = new_pal_image(32, 32); d = ImageDraw.Draw(im)
    d.rectangle((4, 10, 28, 26), fill=12)
    d.rectangle((8, 14, 12, 18), fill=1); d.rectangle((20, 14, 24, 18), fill=1)
    d.line((4, 26, 28, 26), fill=5, width=1)
    im.save(path_bmp, format='BMP')
    json.dump({"type": "sprite", "width": 32, "height": 32}, open(path_json, 'w'))

def make_tiles(path_bmp, path_json):
    im = new_pal_image(32, 32); d = ImageDraw.Draw(im)
    d.rectangle((0, 20, 31, 31), fill=9)
    for x in range(0, 32, 2): d.point((x, 28), fill=5)
    d.rectangle((0, 16, 31, 20), fill=6)
    for x in range(0, 32, 4): d.line((x, 16, x+2, 18), fill=7)
    im.save(path_bmp, format='BMP')
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
