# Firmware and RTL

Scope: what the ZZ9000 firmware and RTL already provide, the anchors a browser plane builds on, the native-video regression, and the toolchain.
Status: draft

All `fw` citations are at `8778ef3`; `os/`, `xdc/`, `rtl/` prefixes expand per `sources.md`.

## Why the Zynq cannot host the browser

- [F] Dual Cortex-A9 at 666 MHz with 1 GB of DDR3 (`fw@8778ef3:sdk/README.md:L17-18`).
- [F] The A9 has no AES or crypto extensions (`fw@8778ef3:sdk/docs/zz9k-crypto-acceleration.md:L58`).
- [G] No GPU or video-decode block; decode is ARM software or FPGA RTL.

## What the card offers today

| Capability | Citation |
|---|---|
| [F] Card-assisted JPEG/PNG decoding and scaling | `fw@8778ef3:sdk/README.md:L36` |
| [F] Native FPGA P96 PIP plane, packed YUV422 by design | `fw@8778ef3:docs/native-p96-pip.md:L39-57` |
| [F] ZZPlay plays MPEG-1 program streams and MP3 | `fw@8778ef3:sdk/docs/zzplay.md:L3, L19-21` |
| [F] On a 4 MiB Zorro II profile the PIP source pool fits 352×288 but not 640×360; the 2 MiB profile has none | `fw@8778ef3:sdk/docs/zzplay.md:L34-37` |
| [F] A synchronous mailbox round trip measures about 6.1 ms | `fw@8778ef3:sdk/docs/zz9k-crypto-acceleration.md:L58-59` |
| [F] Vendor and loadable services live at `0x8000` and above; `0x8100` is taken | `fw@8778ef3:sdk/docs/zz9k-vendor-services.md:L3-8` |
| [F] Ethernet terminates on the A9 and is bridged to the Amiga as raw frames | `fw@8778ef3:os/ethernet.c` |

- [G] The 6.1 ms round trip makes per-frame synchronous calls costly; a Zorro-only path is capped by bus throughput and, on Zorro II, by the small PIP source pool, which is why DEC-004 allows a non-Zorro link.

## Anchors for a browser plane

| Anchor | What it gives | Citation |
|---|---|---|
| `video_source_sync.v` | The frame-wrap tracker the V variant extends (`sections/display-coupling.md`) | `fw@8778ef3:video_source_sync.v:L14-63, L122-128` |
| `video.c` mode init | Keeps HDMI running when output timing is unchanged; drops source sync on every mode init | `fw@8778ef3:os/video.c:L1174-1192, L1207, L1232-1236` |
| `video.c` profile select | `centered_1080p_match` picks 1080p60 for NTSC and 1080p50 for PAL | `fw@8778ef3:os/video.c:L528-534` |
| Source-sync capability bit | `ZZ_FW_CAP_VIDEOCAP_SOURCE_SYNC` | `fw@8778ef3:os/video.c:L484-485` |
| `zz_video_modes.c` | Preset table: pixel clocks and PLL M/D/O per mode | `fw@8778ef3:os/zz_video_modes.c:L13-34` |
| `xdc/runtime_pixel_timing.xdc` | The pixel clock is `clk_wiz_0`, a PLLE2_ADV set per mode through DRP | See `sections/gotchas.md` |
| `docs/native-p96-pip.md` | VDMA, line-buffer and takeover structure to reuse with an RGB mode | `fw@8778ef3:docs/native-p96-pip.md:L39-51` |
| `mntzorro.v` | Zorro, capture writeback over `m01` | `fw@8778ef3:mntzorro.v:L2023, L2042, L2081` |

- [F] Two constrained Zorro ports are unused: `ZORRO_NBRN` is tied to 1 ("TODO busmastering") and `ZORRO_ADDRDIR2` is constant 0 (`fw@8778ef3:mntzorro.v:L799-800`).
- [F] The PL uses two ODDRs (`fw@8778ef3:mntzorro.v:L836, L850`).

## Native-video regression [D] DEC-005

- [F] The firmware has simulation benches for capture and the formatter under `test/video/` (sampler, phase, recovery, row timing, writeback, source sync, formatter, overlay), plus `video_mode_switch_test.c` (`fw@8778ef3:test/video/`).
- [F] The PIP was physically accepted on the default `zorro3` variant only; other variants passed build and timing gates but need their own hardware acceptance (`fw@8778ef3:docs/native-p96-pip.md:L12-16`).
- [F] Release variants are `zorro3`, `zorro3-aga`, `zorro2`, `zorro2-2mb` and the A500-family builds (`fw@8778ef3:build_variant_bitstreams.sh:L44-54`).
- [G] Regression for any board or module change: the benches above as step 0; then NTSC and PAL, each scan-doubler mode, native↔RTG switching, PIP takeover, plane on and off, one fault row per applicable SR, on each Zorro variant; pass is per-frame CRC identity with the Z-7020 baseline from a lossless RGB 4:4:4 HDMI capture (K30, K31).

## Toolchain

- [F] The firmware builds with Vivado 2018.3 (`fw@8778ef3:BUILD.md:L16-18`; `zz9000_project.tcl:L2`).
- [F] From Vivado 2026.1 a free BASIC tier covers every Zynq 7000 device; only PRO and above include pre-2026.1 versions, and BASIC users keep an existing licence file to use them (`amd-vivado-editions`).
- [F] BASIC limits XSIM to 50K design instances with no UVM, and debug to one ILA core with up to 5 probes (`amd-vivado-editions`).
- [G] So either the project ports to 2026.x, or a 2018.3 installation is used; whether 2018.3 WebPACK still downloads and needs no licence file is [R].
- [R] Tool-only analysis for this project (PL fit, static timing, the regression benches under XSIM) has not been run yet; verify by checking `unknowns.md` K20, K29, K30 for results.
- [R] The 7-series PCIe IP is free; a DisplayPort RX core is licensed but not needed under V-tracked.
- [R] IBIS-AMI simulation needs a tool (commercial, or PyBERT); needed only if PCIe stays in play.
