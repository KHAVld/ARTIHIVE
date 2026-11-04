# ARTIHIVE 2.0.0

ARTIHIVE is an independent eight-voice drone and polyphonic synthesizer firmware for the M-VAVE FM-1. It uses integer DSP on the JieLi AC791N and provides eight evolving FM voices, a 27-key chromatic POLY mode, Hyper LFO, stereo motion, modulated delay, distortion, output compression, mutation, presets and 10–400 BPM arpeggiation.

## Instrument modes

- **DRONE:** eight lower keys trigger eight independently tuned voices; the keys are envelope sensors rather than pitch keys. The upper row controls voice latches.
- **POLY:** all 27 keys form a chromatic keyboard. Eight voices use oldest-note stealing. Note level is fixed at 127; HOLD and drone latches are inactive.

ARTIHIVE remains silent until PLAY is pressed. OCT minus and OCT plus move by semitones in DRONE and whole octaves in POLY.

## Build

The firmware requires the JieLi toolchain and three non-redistributable AC79 SDK artifacts. See [docs/BUILD.md](docs/BUILD.md).

```sh
export JIELI_TOOLCHAIN=/path/to/jieli/toolchain
export AC79_SDK=/path/to/fw-AC79_AIoT_SDK
./build.sh --release 2.0.0
```

The release package is written to `build/artihive-2.0.0.fwsc` with identity `FM-1_9620`.

## Tests

```sh
tests/run_tests.sh
```

The application and update loader accept both known 1 MiB FM-1 flash devices:

- Puya P25Q80, JEDEC `0x856014`
- UC25HQ80, JEDEC `0xB36014`

Unknown flash devices are refused.

## Firmware Hub metadata

The repository root contains `fmhub.json`. Its square card image is `docs/card.png`.

## License and provenance

ARTIHIVE is GPL-3.0-only. See [LICENSE](LICENSE), [LICENSING.md](LICENSING.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and [COPYRIGHT-AUDIT.md](COPYRIGHT-AUDIT.md). Bundled JieLi-derived components retain Apache-2.0 notices, and the Terminus font retains its OFL-1.1 notice.

ARTIHIVE was created by KHAV with assistance from Arena.ai Agent Mode as an exploration of the FM-1 platform. Thanks to SOMA Laboratory for its approach to sound and aesthetics; LYRA-8 is acknowledged only as artistic inspiration. ARTIHIVE is independent and is not affiliated with SOMA Laboratory or M-VAVE.
