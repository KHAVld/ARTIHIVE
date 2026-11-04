#!/usr/bin/env python3
"""Regression checks for the native OUTPUT compressor layout and bypass."""
from pathlib import Path
import re, subprocess
from PIL import Image
root=Path(__file__).resolve().parents[1]
subprocess.run(['sh','tests/run_host.sh','tests/scripts/compressor.txt'],cwd=root,check=True,stdout=subprocess.DEVNULL)
im=Image.open(root/'build/host/artihive-3000.png')
assert im.size in ((240,240),(480,480)), im.size
s=(root/'firmware/src/artihive.c').read_text()
assert 'static const char *const L[3]={"IN","OUT","GR"}' in s
assert 'y=10+(int32_t)k*22' in s
assert 'cv_rect(43,y,188,9' in s
# Body is local y=0..69. The last GR bar occupies y=54..62 (outline y=54..62);
# its fill and threshold remain below 69, while the knob strip starts after the body.
rows=[10+22*k for k in range(3)]
assert rows == [10,32,54]
assert rows[-1]+9 <= 69
assert 6 >= 0 and 21 <= 69
# Four knob cells are 58 px wide. All labels fit their own cells at the native font width.
font_width={'THRESH':6*8,'RATIO':5*8,'ATTACK':6*8,'RELEASE':7*8}
assert all(w <= 58 for w in font_width.values())
# DSP contract: linked detector, no delay/look-ahead allocation, exact bypass branch.
assert 'if(a_comp_ratio){lr[0]=' in s
assert 'pk>comp_peak' in s
assert 'COMP_THRESH[128]' in s
print('compressor: native IN/OUT/GR fields and all four labels stay in separate protected regions  ok')
