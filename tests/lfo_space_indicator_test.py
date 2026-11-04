#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import subprocess
subprocess.run(['sh','tests/run_host.sh','tests/scripts/lfo-space-indicator.txt'],check=True,stdout=subprocess.DEVNULL)
src=Path('firmware/src/artihive.c').read_text()
body=src.index('static void draw_body')
start=src.index('case PG_LFO:',body)
block=src[start:src.index('case PG_DLY:',start)]
assert 'static const char *const pair' not in block
assert 'cv_text(8,y-3' not in block
assert 'cv_line(8,y,231,y' in block
for t in (1400,2200,3000):
 im=Image.open(f'build/host/artihive-{t}.png').convert('RGB').resize((240,240),Image.Resampling.NEAREST)
 counts=[]
 for y in (60,75,90,105):
  counts.append(sum(1 for x in range(8,232) if sum(im.getpixel((x,y)))<180))
 if min(counts)<165: raise SystemExit(f'LFO SPACE full-width lane missing at {t}: {counts}')
print('LFO SPACE indicator: four label-free full-width lanes in ALL, PAIR and ALT  ok')
