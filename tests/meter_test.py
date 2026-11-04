#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""English regression descriptionARTIHIVE 1.1, English regression description

    python3 tests/meter_test.py

1. English regression descriptionQ31, English regression description
   English regression descriptionQ15: `(e * 46) >> 15` English regression descriptionint32, English regression description
   English regression description
   English regression description

2. English regression descriptionQ24,
   English regression description
   English regression description
"""
import pathlib
import subprocess
import sys
import wave

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build" / "host"
FS = 44100
fails = 0


def check(ok, msg):
    global fails
    print(("  ok    " if ok else "  FAIL  ") + msg)
    if not ok:
        fails += 1


def render(script):
    subprocess.run(["sh", "tests/run_host.sh", f"tests/scripts/{script}.txt"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def indicator_area(px, voice):
    """Black envelope pixels inside the octagonal contact (Blush Vein graph ink)."""
    cx = 3 + voice * 30 + 12
    return sum(1 for y in range(172 + 27, 172 + 44)
               for x in range(cx - 8, cx + 9) if px[x, y] == (0, 0, 0))

def shots(script, times):
    out = []
    for ms in times:
        im = Image.open(BUILD / f"artihive-{ms}.png").convert("RGB")
        if im.size != (240, 240):
            im = im.resize((240, 240), Image.NEAREST)
        out.append((ms, im.load()))
    return out


print("== English regression description")
render("meter")
TIMES = [1500, 1700, 1950, 2000, 2050, 2100, 2150, 2200, 2250,
         2300, 2400, 2500, 2600, 2700, 2800, 3000, 3200]
frames = shots("meter", TIMES)
areas = [(ms, indicator_area(px, 0)) for ms, px in frames]
print("     English regression description", ", ".join(f"{ms}:{a}" for ms, a in areas))
check(all(0 <= a <= 289 for _, a in areas), "English regression description")
held = [a for ms, a in areas if ms <= 1700]
check(min(held) >= 20, f"English regression description{min(held)} English regression description")
tail = [a for ms, a in areas if ms >= 1950]
rises = [(a, b) for a, b in zip(tail, tail[1:]) if b > a]
check(not rises, f"English regression description{len(rises)})")
check(tail[-1] <= 5, f"English regression description{tail[-1]} English regression description")

print("== English regression description")
render("envelope")
with wave.open(str(BUILD / "artihive.wav")) as w:
    d = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2).astype(float)
mono = d.mean(axis=1)
win = FS // 20                                  # 50 English regression description


def rms(a, b):
    seg = mono[int(a * FS):int(b * FS)]
    return float(np.sqrt((seg * seg).mean())) if len(seg) else 0.0


held_rms = rms(1.8, 2.15)
check(held_rms > 100, f"English regression descriptionRMS {held_rms:.0f})")
target = held_rms / 1000.0                      # −60 English regression description
release_at = 2.2
t = release_at
fallen = None
while t < len(mono) / FS - 0.05:
    if rms(t, t + 0.05) < target:
        fallen = t - release_at
        break
    t += 0.05
print(f"     English regression description{fallen if fallen is not None else 'English regression description'} English regression description")
check(fallen is not None and 7.0 <= fallen <= 9.0,
      "SLOW English regression descriptionREL=0 English regression descriptionQ24 English regression description")

print("== English regression descriptionREL English regression description")


def decay(script):
    render(script)
    with wave.open(str(BUILD / "artihive.wav")) as w:
        m = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, 2).astype(float).mean(axis=1)

    def r(a, b):
        seg = m[int(a * FS):int(b * FS)]
        return float(np.sqrt((seg * seg).mean())) if len(seg) else 0.0

    held = r(1.8, 2.15)
    t, fall = 2.2, None
    while t < len(m) / FS - 0.05:
        if r(t, t + 0.05) < held / 1000.0:
            fall = t - 2.2
            break
        t += 0.05
    return fall, r(5.0, 6.0)


long_fall, _ = decay("rel-long")
short_fall, short_rest = decay("rel-short")
print(f"     REL=0: {long_fall} English regression descriptionREL=127: {short_fall} English regression description{short_rest:.4f}")
check(long_fall is not None and 7.0 <= long_fall <= 9.0, "REL=0 English regression description")
check(short_fall is not None and short_fall <= 0.25, "REL=127 English regression description")
check(short_rest == 0.0, "English regression description")

print()
print("METER/ENVELOPE FAILURES:" if fails else "METER/ENVELOPE OK:", fails if fails else "English regression description")
sys.exit(1 if fails else 0)
