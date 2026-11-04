# ARTIHIVE 2.0 copyright and licence audit

Date: 2026-11-03

This is a technical provenance and licence-compliance review, not legal advice.

## Conclusion

No direct licence conflict was identified that prevents publishing ARTIHIVE 2.0.0 under `GPL-3.0-only`, provided the source archive, licence texts, existing copyright headers and third-party notices remain available with the firmware.

The principal redistributable components are compatible:

- ARTIHIVE application and project code: `GPL-3.0-only`.
- Dinghy and the Felucca-derived copies used by this tree: `GPL-3.0-only`.
- JieLi AC79 SDK package files: Apache-2.0.
- Terminus font: SIL OFL 1.1.

The GitHub release must include or clearly accompany the complete corresponding ARTIHIVE source. The release currently provides `artihive-2.0.0-src.tar.gz` next to the firmware.

## Verified repository facts

- Root `LICENSE` contains GNU GPL version 3.
- Core firmware and platform files carry `SPDX-License-Identifier: GPL-3.0-only` headers.
- Imported contributor copyright lines are retained in the relevant source files.
- `LICENSING.md` records Dinghy, Felucca, SLOOP, OberVave, SMK-37 and installer provenance.
- Dinghy's separately controlled designburg signet is absent.
- The ARTIHIVE logo is project artwork.
- No SOMA code, firmware, samples, logos, photographs or manual text were identified.
- The source archive does not contain the JieLi SDK binaries.
- The `.fwsc` package does contain the three expected SDK package components inserted at build time.
- Build-time SHA-256 pins verify the exact expected SDK files.
- The Terminus OFL notice is retained in the source tree.

## Remediation completed by this audit

- Added `THIRD_PARTY_NOTICES.md`.
- Added the full Apache License 2.0 text at `LICENSES/Apache-2.0.txt`.
- Added a release-facing copy of the Terminus OFL notice at `LICENSES/Terminus-OFL-1.1.txt`.
- Added a clear non-affiliation and trademark-use statement.
- Linked `LICENSING.md` to the bundled licence texts.

## Distribution requirements

When distributing `artihive-2.0.0.fwsc`, keep these items available together:

1. `artihive-2.0.0-src.tar.gz` — complete corresponding ARTIHIVE source.
2. `LICENSE` — GPL-3.0-only text.
3. `THIRD_PARTY_NOTICES.md` — provenance and acknowledgements.
4. `LICENSES/Apache-2.0.txt` — licence for the JieLi package files included in `.fwsc`.
5. `LICENSES/Terminus-OFL-1.1.txt` — font copyright and licence notice.

Do not remove copyright or SPDX headers from derived source files.

## Residual risks that cannot be eliminated by static inspection

- Only the copyright holders or a qualified lawyer can give a binding legal opinion.
- Repository licence labels do not independently prove ownership of every historical contribution.
- Trademark and unfair-competition rules vary by jurisdiction.
- A future upstream relicensing or correction does not automatically change the licence of the exact revision already received, but should trigger a new review.
- The statements that ARTIHIVE artwork and DSP are original depend on the project authors' factual representations; source inspection cannot prove independent creation.

## Branding guidance

Use the names M-VAVE FM-1, JieLi AC791N, Felucca, Dinghy, SOMA and LYRA-8 only for compatibility, provenance or acknowledgement. Do not use third-party logos or imply endorsement. Keep this statement visible:

> ARTIHIVE is independent community firmware and is not affiliated with, endorsed by, or sponsored by M-VAVE, JieLi Technology, Hügelton Instruments, or SOMA Laboratory.

## Upstream references reviewed

- JieLi AC79 SDK: <https://github.com/Jieli-Tech/fw-AC79_AIoT_SDK>
- Felucca: <https://github.com/hugelton/Felucca>
- Felucca BSP: <https://github.com/hugelton/felucca-bsp>
- Dinghy: <https://github.com/zvenson/dinghy>
- SIL Open Font License information: <https://software.sil.org/oflt/>
