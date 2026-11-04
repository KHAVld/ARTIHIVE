# Third-party notices

ARTIHIVE is independent community firmware. It is not affiliated with, endorsed by, or sponsored by M-VAVE, JieLi Technology, Hügelton Instruments, SOMA Laboratory, or any other hardware or software vendor mentioned below. Product and company names are used only to identify compatibility, provenance, and attribution.

## Dinghy

ARTIHIVE is built on the Dinghy firmware template by zvenson. Dinghy is licensed under `GPL-3.0-only` and carries the FM-1 platform work described below.

Source: <https://github.com/zvenson/dinghy>

## Felucca and SLOOP

The FM-1 platform, update transport, hardware access, loader and related infrastructure originate from Felucca by Leo Kuroshita / Hügelton Instruments, with changes carried through SLOOP by isod89 and later Dinghy-derived work. The copies used by ARTIHIVE retain `GPL-3.0-only` headers and copyright notices.

Sources:

- <https://github.com/hugelton/Felucca>
- <https://github.com/isod89/sloop-fm1>

Additional contributor attribution is recorded in `LICENSING.md` and in individual source-file headers.

## JieLi AC79 SDK package files

A built `.fwsc` package contains these files taken at build time from the public JieLi AC79 AIoT SDK:

- `cpu/wl82/tools/uboot.boot`
- `cpu/wl82/tools/cfg_tool.bin`
- `cpu/wl82/tools/cfg/eq_cfg_hw.bin`

Copyright: ZhuHai JieLi Technology Co., Ltd. and contributors.

License: Apache License 2.0. A copy is included at `LICENSES/Apache-2.0.txt`.

Source: <https://github.com/Jieli-Tech/fw-AC79_AIoT_SDK>

The JieLi SDK and toolchain are not included in the ARTIHIVE source tree. The build reads the three package files from a separately obtained SDK checkout.

## Terminus font

The display font data in `firmware/gen/felucca_font.h` is rendered from Terminus Font 8x16 (`ter-u16n`).

Copyright (C) 2020 Dimitar Toshkov Zhekov and Terminus contributors.

License: SIL Open Font License 1.1. A copy is included at `LICENSES/Terminus-OFL-1.1.txt`; the original notice is also retained at `assets/fonts/Terminus-LICENSE.txt`.

## Skiff loader-screen influence

The update loader screen and tests retain attribution to Skiff by illuminus5 and later work by zvenson. The included implementation is distributed under `GPL-3.0-only`; details are in `LICENSING.md` and the relevant source headers.

## ARTIHIVE artwork and SOMA acknowledgement

The ARTIHIVE name, DSP application code, generated textures and `assets/artihive.svg` mark are project material distributed under `GPL-3.0-only` unless a file states otherwise. Dinghy's designburg signet is not included.

SOMA Laboratory and LYRA-8 are acknowledged only as artistic and philosophical inspiration. No SOMA code, firmware, samples, logos, photographs, or manual text are included. ARTIHIVE is unaffiliated with and not endorsed by SOMA Laboratory.
