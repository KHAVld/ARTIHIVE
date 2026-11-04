# Building ARTIHIVE

## Requirements

- Linux or a compatible POSIX environment
- JieLi AC791N toolchain
- AC79 SDK artifacts: `uboot.boot`, `cfg_tool.bin`, and `eq_cfg_hw.bin`
- Python 3, a C compiler, `make`, `zip`, and standard shell tools

The proprietary SDK artifacts are not distributed with ARTIHIVE. Point `AC79_SDK` to a compatible SDK tree and `JIELI_TOOLCHAIN` to the extracted compiler toolchain.

## Release build

```sh
export JIELI_TOOLCHAIN=/path/to/jieli/toolchain
export AC79_SDK=/path/to/fw-AC79_AIoT_SDK
./build.sh --release 2.0.0
```

Expected output:

```text
build/artihive.bin
build/loader/ota.bin
build/artihive-2.0.0.fwsc
```

The package identity is `FM-1_9620`.

## Tests

```sh
tests/run_tests.sh
```

The suite checks DSP behavior, UI rendering, storage boundaries, application and loader packaging, updater protocol behavior, flash-device acceptance, and release-package structure.

## Host build

```sh
tests/run_host.sh tests/scripts/legacy-demo.txt
```

Host output is written under `build/host/` and can include audio and rendered screen captures.
