#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import math, random
W=H=240
random.seed(0xA87111)
# Smooth deterministic low-frequency noise made from random harmonics.
harm=[(random.uniform(0.025,0.075),random.uniform(0.018,0.06),random.uniform(0,6.28),random.uniform(1.5,4.0)) for _ in range(7)]
a=[]
for y in range(H):
 for x in range(W):
  # Four long, independently bending diagonal veins.
  curves=[28+0.42*x+10*math.sin(x/25), 91-0.24*x+13*math.sin(x/31+1.1),
          146+0.18*x+11*math.sin(x/21+2.0), 213-0.38*x+9*math.sin(x/27+0.3)]
  d=min(abs(y-c) for c in curves)
  n=sum(math.sin(x*fx+y*fy+ph)*amp for fx,fy,ph,amp in harm)
  d += n
  # sparse secondary hairlines cross the broad ribbons
  hair=abs((x*0.31+y*0.72+8*math.sin(y/19))%71-35.5)
  lv=3 if d<1.8 else 2 if d<5.2 else 1 if d<10.5 or hair<0.75 else 0
  a.append(lv)
out=bytearray((len(a)+3)//4)
for i,v in enumerate(a): out[i>>2]|=v<<((i&3)*2)
p=Path('firmware/gen/blush_texture.h')
rows=[]
for i in range(0,len(out),24): rows.append('    '+', '.join(f'0x{x:02x}' for x in out[i:i+24])+',')
p.write_text('/* generated dark rose vein texture; 2 bits/pixel, absolute 240x240 coordinates */\nstatic const uint8_t BLUSH_TEX[14400] = {\n'+'\n'.join(rows)+'\n};\n')
