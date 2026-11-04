#!/usr/bin/env python3
"""Host regression for contextual ARP mutation and one-level undo."""
import subprocess
from pathlib import Path
from PIL import Image, ImageChops
ROOT=Path(__file__).resolve().parent.parent
subprocess.run(['sh','tests/run_host.sh','tests/scripts/mutate-context.txt'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
def strip(ms): return Image.open(ROOT/f'build/host/artihive-{ms}.png').crop((0,114,480,340))
a,b,c,d=map(strip,(500,1000,1800,3300))
assert ImageChops.difference(a,b).getbbox(), 'short ARP changed no visible control'
assert ImageChops.difference(a,c).getbbox() is None, 'SAVE+SEQ did not restore the page exactly'
assert ImageChops.difference(a,d).getbbox(), 'long ARP changed no visible control'
print('MUTATE OK: short changed one control; SAVE+SEQ restored exactly; long changed the page')
