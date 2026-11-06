<img width="1456" height="720" alt="artihive-logo-640x320-byKHAV" src="https://github.com/user-attachments/assets/35a2a57f-775d-4690-bc15-717b30609ded" />
<img width="240" height="240" alt="drone" src="https://github.com/user-attachments/assets/26d97bfd-9c01-470f-84ce-f4ef8ce3e419" />
<img width="240" height="240" alt="artihive-arpeggio-user-16-steps-240x240" src="https://github.com/user-attachments/assets/8e88d442-c40d-4900-ae34-67ad706f07d0" />
<img width="240" height="240" alt="hyper-lfo" src="https://github.com/user-attachments/assets/4ab6cf19-9aab-4890-84de-9bf41d1c47c3" />
<img width="240" height="240" alt="output" src="https://github.com/user-attachments/assets/1280812a-6d5b-4a09-8372-82eee119425c" />
<img width="240" height="240" alt="out-comp" src="https://github.com/user-attachments/assets/8172a7e6-4234-476d-a7f9-12f1b5ed7ba2" />
<img width="240" height="240" alt="fm-route" src="https://github.com/user-attachments/assets/1bb9cd30-3c31-4fab-ac5f-c3bf5b41c6f2" />

> ⚠️ **Photosensitivity notice:** ARTIHIVE 2.0.1 contains repeated high-contrast flashing in DISORDER mode and may be unsuitable for people who are sensitive to flashing images. This behaviour has been removed in ARTIHIVE 2.0.2. Users of version 2.0.1 are strongly advised to update to the latest release.

## Hardware testing notice

> **Please note:** This firmware has received only limited testing on physical FM-1 hardware. Automated tests, package verification and host-based stress tests have passed, but not every function, hardware revision, preset combination or long-duration operating condition has been tested on the device. Use it carefully, keep a copy of the previous working firmware, and make sure you have access to the recovery procedure before installing.


# ARTIHIVE

ARTIHIVE is an experimental eight-voice drone and polyphonic synthesizer firmware for the **M-VAVE FM-1**. It combines evolving FM textures, long envelopes, stereo motion, modulated delay, distortion, compression, mutation and exact-tempo arpeggiation in a compact performance instrument.

## Main features

- Separate **DRONE** and **POLY** modes.
- Eight oscillator voices arranged as four interacting FM pairs.
- Full 27-key chromatic POLY keyboard, including black-key semitones.
- Eight-voice allocation with oldest-note stealing.
- ROOT, global SHARP, DETUNE and global MOD controls in POLY.
- Global envelope editing when no key is held.
- Hold a note while editing to change that voice's FAST, RELEASE or ATTACK independently.
- Hyper LFO with linked operators and stereo SPACE movement.
- Dual modulated delay with LFO and self-modulation sources.
- Output distortion and lightweight stereo-linked compression.
- ARPEGGIO with exact 10–400 BPM, multiple traversal orders and programmable USER steps.
- Context-sensitive mutation with one-level undo.
- Sixteen factory presets and eight user slots.
- Twelve visual themes with high-contrast text and logo outlines on textured backgrounds.

## DRONE mode

DRONE preserves the original ARTIHIVE performance model. The eight lower sensors trigger independently tuned voices, while latches, PLAY and HOLD can create sustained layers. OCT− and OCT+ transpose by semitones.

## POLY mode

Press **HOME** a second time from DRONE to enter POLY. Press HOME again to return to DRONE.

All 27 physical keys play chromatically. Eight notes can sound simultaneously; a ninth note steals the oldest active voice. OCT− and OCT+ move the keyboard by octaves.

POLY intentionally has no drones, latches, PLAY drones or HOLD floor. Note level and outgoing velocity are fixed at 127.

### POLY envelope editing

- With no held key, FAST, RELEASE and ATTACK change all eight voices together.
- While notes are held, the controls edit only the newest still-held voice.
- HOLD remains inactive and displays `OFF`.

### Current POLY boundaries

- POLY settings are not stored in presets.
- Incoming MIDI retains the compatible DRONE voice-address mapping.
- Chromatic POLY allocation applies to the physical keyboard.
- Outgoing POLY key events use their true note numbers with velocity 127.



## Physical-device status

The final ARTIHIVE 2.0.0 firmware has successfully started on a physical FM-1. This confirms real-device startup, but is not presented as a complete long-duration test of every function or every FM-1 hardware revision.

## Package identity

- Firmware version: `2.0.0`
- Package identity: `FM-1_9620`
- Target: M-VAVE FM-1 / JieLi AC791N
- License: GPL-3.0-only

## Release files

- `artihive-2.0.0.fwsc` — ready-to-install firmware.
- `artihive-2.0.0-src.tar.gz` — corresponding source archive.
- `artihive-manual-en.pdf` — English manual.
- `artihive-manual-ru.pdf` — Russian manual.
- `install.html` — self-contained offline WebMIDI installer.
- `RELEASE_NOTES.md` — concise release summary.
- `SHA256SUMS` — integrity hashes for all release files.
- `LICENSE` — GNU General Public License version 3.

## Verification

The release passed host integration tests, DSP tests, POLY allocation and envelope tests, MIDI and arpeggiator tests, update-loader and package checks, ASan/UBSan runs, target resource checks and a clean reproducible firmware rebuild.

Verify downloaded files with:

```sh
sha256sum -c SHA256SUMS
```
## Acknowledgements

ARTIHIVE was created by KHAV with development, documentation, testing, and release-preparation assistance from Arena.ai Agent Mode.

Artistically inspired by the experimental sound philosophy and hands-on approach of the SOMA Laboratory LYRA-8. ARTIHIVE is an independent project and is not affiliated with or endorsed by SOMA Laboratory. No SOMA software, firmware, schematics, branding, or other proprietary materials are used.
## License

ARTIHIVE is distributed under the **GNU General Public License v3.0 only**. See `LICENSE` for the full terms.
