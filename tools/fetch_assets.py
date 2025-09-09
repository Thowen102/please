#!/usr/bin/env python3
import os, io, sys, zipfile, json, requests
from PIL import Image


ROOT = os.path.dirname(os.path.dirname(__file__))
GFX = os.path.join(ROOT, 'graphics')
AUD = os.path.join(ROOT, 'audio')


os.makedirs(GFX, exist_ok=True)
os.makedirs(AUD, exist_ok=True)


session = requests.Session()


def dl(url):
r = session.get(url, timeout=60)
r.raise_for_status()
return r.content


# --- Helper: convert PNG->paletted BMP with first palette entry as transparent ---


def save_sprite_bmp(src_png_bytes, out_bmp_path, force_size=None):
im = Image.open(io.BytesIO(src_png_bytes)).convert('RGBA')
if force_size:
im = im.resize(force_size, Image.NEAREST)
# Make a transparency key: pick fully transparent pixels or top-left pixel if none
pixels = im.getdata()
transparent_color = None
for px in pixels:
if px[3] == 0:
transparent_color = (px[0], px[1], px[2], 0)
break
if transparent_color is None:
transparent_color = im.getpixel((0,0))
# Replace exact transparent RGBA with a unique magenta key (255,0,255)
new = Image.new('RGBA', im.size)
rep = []
for px in pixels:
if px[3] == 0:
rep.append((255,0,255,255))
else:
rep.append(px)
new.putdata(rep)
# Quantize to 16 colors and convert to P mode
pal = new.convert('P', palette=Image.ADAPTIVE, colors=16)
# Ensure index 0 is our transparent key
pal = pal.copy()
pal.info['transparency'] = 0
pal.putpalette([255,0,255] + list(pal.getpalette()[3:]))
pal.save(out_bmp_path, format='BMP')


# --- Player ---
print('Fetching ExplorerHero (player) ...')
player_png = dl('https://opengameart.org/sites/default/files/ExplorerHero.png')
open(os.path.join(GFX, 'player.json'), 'w').write(json.dumps({"type":"sprite", "width":32, "height":32}))
save_sprite_bmp(player_png, os.path.join(GFX, 'player.bmp'))


# --- Enemies ---
print('Fetching enemies ...')
creatures_png = dl('https://opengameart.org/sites/default/files/creatures_6.png'.replace('_6','')) if False else dl('https://opengameart.org/sites/default/files/creatures.png')
open(os.path.join(GFX, 'enemies.json'), 'w').write(json.dumps({"type":"sprite", "width":32, "height":32}))
save_sprite_bmp(creatures_png, os.path.join(GFX, 'enemies.bmp'))


# --- Tiles + coin ---
print('Fetching tiles ...')
tiles_png = dl('https://opengameart.org/sites/default/files/tiles_5.png'.replace('_5','')) if False else dl('https://opengameart.org/sites/default/files/tiles.png')
open(os.path.join(GFX, 'tiles.json'), 'w').write(json.dumps({"type":"sprite", "width":32, "height":32}))
save_sprite_bmp(tiles_png, os.path.join(GFX, 'tiles.bmp'))


# --- SFX: download zip and extract a few wavs ---
print('Fetching SFX ...')
zip_bytes = dl('https://opengameart.org/sites/default/files/The%20Essential%20Retro%20Video%20Game%20Sound%20Effects%20Collection%20%5B512%20sounds%5D.zip')
with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
picks = {
'Jump_00.wav': 'jump.wav',
'Pickup_Coin10.wav': 'collect.wav',
'Hit_Hurt31.wav': 'hit.wav',
'Menu_Navigate03.wav': 'pause.wav'
}
for name, out in picks.items():
for zname in z.namelist():
if zname.endswith(name):
with z.open(zname) as fsrc, open(os.path.join(AUD, out), 'wb') as fdst:
fdst.write(fsrc.read())
break
print('Done.')
