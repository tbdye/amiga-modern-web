# Firmware and RTL

Scope: what the ZZ9000 firmware and RTL already provide, the anchors a browser plane builds on, the native-video regression, and the toolchain.
Status: draft

`fw` citations are at `8778ef3` unless they name another commit.
`os/`, `xdc/`, `rtl/` prefixes expand per `sources.md`.

## Why the Zynq cannot host the browser

- [F] Dual Cortex-A9 at 666 MHz with 1 GB of DDR3 (`fw@8778ef3:sdk/README.md:L17-18`); the PS7 configuration sets the CPU clock to 666.666 MHz (`fw@bdfd8b0:zz9000_project.tcl:L834`).
- [F] The A9 has no AES or crypto extensions (`fw@8778ef3:sdk/docs/zz9k-crypto-acceleration.md:L58`).
- [G] No GPU or video-decode block; decode is ARM software or FPGA RTL.

## What the card offers today

| Capability | Citation |
|---|---|
| [F] Card-assisted JPEG/PNG decoding and scaling | `fw@8778ef3:sdk/README.md:L36` |
| [F] Native FPGA P96 PIP plane, packed YUV422 by design | `fw@8778ef3:docs/native-p96-pip.md:L39-57` |
| [F] At release `v2.8.1` (`6aa71d1`), ZZPlay plays MPEG-1 Program Streams and MP3 | `fw@6aa71d1:sdk/docs/zzplay.md:L3, L12-14` |
| [F] At `b470c23`, ZZPlay also decodes MPEG-2 Program Streams (AC-3, MP2 or LPCM), WebM (VP8/VP9 with Opus or Vorbis), native FLAC, Ogg Vorbis and animated WebP; the firmware advertises these only when built with `ZZ9000_QUALIFY_UNADVERTISED` | `fw@b470c23:sdk/docs/zzplay.md:L17-28`; `os/sdk_service_catalog.h:L32-57` |
| [F] On a 4 MiB Zorro II profile the PIP source pool fits 352×288 but not 640×360; the 2 MiB profile has none | `fw@8778ef3:sdk/docs/zzplay.md:L34-37` |
| [F] A synchronous mailbox round trip's floor measures 225-339 µs (average 279 µs) on a 68060; its conditions, and the 6.1 ms figure it supersedes | `topics/arm-offload.md`, "Per-call cost" |
| [F] A drop-in `amissl.library` with an OpenSSL 3 provider offloads TLS crypto to BearSSL on the A9: handshake (X25519, P-256, ECDSA and RSA verify) and record (ChaCha20-Poly1305, AES-GCM); the handshake operations run two to three orders of magnitude faster than the SDK's portable 68k code; how it is built and when it falls back: `topics/arm-offload.md`, "How the TLS offload is built" | `fw@bdfd8b0:sdk/docs/zz9k-crypto-acceleration.md:L10-18, L128-140, L183-185`; `sdk/docs/zz9k-amissl-provider.md:L19-31` |
| [F] Service IDs at `0x8000` and above are set aside for vendor and loadable services, allocated on `0x0100` boundaries, with `0x8100` assigned to the JEDI renderer; the range is an ID space only, with no loader and no vendor opcode handler in the firmware (`topics/arm-offload.md`, "Mechanisms in the firmware") | `fw@cfbb910:sdk/docs/zz9k-vendor-services.md:L3-8, L20-23, L36-38`; `sdk/docs/zz9k-modules.md:L56-61` |
| [F] Ethernet terminates on the A9 and is bridged to the Amiga as raw frames | `fw@8778ef3:os/ethernet.c` |
| [F] The GEM DMAs each received frame into a 128-slot × 2048 B backlog at `0x3FE00000` that the Amiga reads in order; at 96 pending frames (128 less 32 RX descriptors) the firmware stops re-arming descriptors and sends an 802.3x pause frame (quantum `0x800`), and it advertises symmetric and asymmetric pause | `fw@bdfd8b0:os/memorymap.h:L30, L500`; `os/ethernet.h:L58-60`; `os/ethernet.c:L352-359, L596-612, L640-644, L853-856, L1103-1105` |
| [F] ARM-side surface jobs: fill, copy and clipped scale (bilinear on supporting builds) on SDK surfaces and the RTG framebuffer; ARM-local surfaces not mapped into 68k memory; a helper that walks a window's visible ClipRects | `fw@bdfd8b0:sdk/docs/zz9k-library.md:L326-347, L362-368, L404-415, L694-700` |
| [F] Card-side drawing operations (`gfx_acc_op`): buffer flip and clear, rectangle blit, surface allocate and free, setting the bits-per-pixel conversion table, line, rectangle fill, circle draw and fill, flat and textured triangles; also template and pattern fills and planar-to-chunky conversion | `fw@bdfd8b0:os/gfx.h:L59-84, L648-663` |
| [F] On Zorro II, general P96 offscreen bitmaps are disabled, and the 4 MiB profile's PIP source pool is 224 KiB | `fw@bdfd8b0:sdk/docs/zz9k-zorro2-services.md:L28, L52-53` |
| [F] `REG_ZZ_VIDEOCAP_STATS` (`0x4e`) returns the live ten-bit frame line count | `fw@bdfd8b0:README.md:L381-382` |
| [F] An Amiga reset drops a partly uploaded firmware update file | `fw@bdfd8b0:os/fw_update.c:L503-509` |

- [G] A written firmware or bitstream update takes effect at the next card power-on; no runtime PL reload was found, and the A9 keeps running across an Amiga reset.
- [G] A Zorro-only path is capped by bus throughput and, on Zorro II, by the small PIP source pool, which is why DEC-004 allows a non-Zorro link.

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

- [F] Three constrained Zorro ports are unused: `ZORRO_NBRN` is tied to 1 ("TODO busmastering"), `ZORRO_NBGN` is declared but never read, and `ZORRO_ADDRDIR2` is constant 0 (`fw@8778ef3:mntzorro.v:L138-140, L799-800`).
- [F] The PL uses two ODDRs (`fw@8778ef3:mntzorro.v:L836, L850`) and no IDDR, IDELAYE2 or ISERDESE2 in its RTL (`fw@bdfd8b0`, `git grep` over the `.v` sources).
- [F] It packs the capture RGB inputs (`fw@bdfd8b0:videocap_sampler.v:L558-560`) and the I2S LRCLK and data inputs (`rtl/audio_clock.v:L49-50`) into IOB registers, and `verify_vcap_iob_placement.tcl` fails the build unless the capture registers sit in ILOGIC sites (`fw@bdfd8b0:verify_vcap_iob_placement.tcl:L7-29`).
- [F] The pixel clock powers up at 75 MHz, and implementation is timed against the fastest runtime mode, the 150 MHz 1920×1080 native-video container (`fw@bdfd8b0:xdc/runtime_pixel_timing.xdc:L4-14`).
- [F] The preset table also holds 1600×1200 at 161.538 MHz (`fw@bdfd8b0:os/zz_video_modes.c:L23`), above that 150 MHz; whether that mode meets timing is unverified [G].
- [F] Six presets, 1600×1200 among them, put the pixel PLL outside the datasheet range of the −1 part the build targets, and the custom-mode check exempts presets (`sections/gotchas.md`, "Firmware and RTL").
- [G] So 1600×1200 is outside both the timed 150 MHz container and the datasheet PLL range.
- [F] At `bdfd8b0` the main RTL files run to a few thousand lines each (`mntzorro.v` about 3,500; `video_formatter.v` and `videocap_sampler.v` about 1,600-1,700), and the C source and header files under `os/` run to about 126,000 lines, about 82,000 of them in `.c` files, third-party code included (line counts of each file at that commit).

## Lessons from the PIP bring-up

- [F] The PIP reserves formatter operations 22-27 (`OVERLAY_CTRL`, `_POS`, `_SIZE`, `_KEY`, `_SOURCE_SIZE`, `_FRAME`); the VDMA address, pitch, HSIZE and VSIZE stay AXI-Lite registers, and geometry and control changes latch at vblank (`fw@bdfd8b0:docs/native-p96-pip.md:L66-80`).
- [F] A running AXI VDMA commits a new `START_ADDR` only after `VSIZE` is written, so a flip writes `START_ADDR`, then `VSIZE`, then advances the generation (`docs/native-p96-pip.md:L111-116`).
- [F] Row and generation metadata crossing between the 100 MHz AXI clock and the pixel clock through raw multi-bit synchronizers caused missing rows; the fix carries it through bundled-data `xpm_cdc_handshake` instances (`docs/native-p96-pip.md:L281-293`).
- [G] A browser plane on the same structure inherits all three rules.

## PS DDR map and card pool

[F] The card's 1 GB of PS DDR at `bdfd8b0` (`fw@bdfd8b0:docs/memory-map.md:L7-18`; `os/memorymap.h:L307-335, L409-434`):

| Range | Size | Owner |
|---|---|---|
| 0x00000000-0x08000000 | 128 MB | What the Amiga reaches through the Zorro board window: low firmware sections, framebuffer and RTG surfaces, SDK heaps |
| 0x08000000-0x08200000 | 2 MB | Z3 SDK mailbox, audio direct rings, AHI/MHI audio scratch |
| 0x08200000-0x18000000 | 254 MB | Linker region `ps7_ddr_hi`: high firmware code, the 224 MB newlib heap, stacks |
| 0x18000000-0x18100000 | 1 MB | Dual-core task queue and session tables |
| 0x18100000-0x1BF00000 | 62 MB | Card pool range A1 |
| 0x1BF00000-0x1C000000 | 1 MB | Core-1 stack |
| 0x1C000000-0x20000000 | 64 MB | Card pool range A2 |
| 0x20000000-0x30000000 | 256 MB | Zorro III fast RAM while it is advertised; card pool range B otherwise |
| 0x30000000-0x3FC00000 | 252 MB | Card pool range C |
| 0x3FC00000-0x40000000 | 4 MB | Fixed buffers: audio TX/RX rings, boot ROM, Ethernet descriptors and frames, SD/USB block buffer |

- [F] The RTG framebuffer starts at 0x00200000, and the Zorro III main board window is 128 MB from there, so it ends at 0x08200000 (`fw@bdfd8b0:os/memorymap.h:L16, L125-137`).
- [F] The linker region is 0x08200000 plus 0x0FE00000, the heap is 0x0E000000 (224 MB), and the linker fails the build if the image reaches 0x18000000 (`fw@bdfd8b0:os/lscript.ld:L17, L33, L540`).
- [F] The fixed buffers start at 0x3FC00000: audio TX 0x3FC00000, audio RX 0x3FC20000, boot ROM 0x3FCF0000, Ethernet descriptors from 0x3FD00000, SD/USB block buffer 0x3FE40000 (`fw@bdfd8b0:os/memorymap.h:L24-32`).
- [F] The pool hands out 64 KB pages to owners in classes: FIRMWARE (permanent, survives Amiga resets, never placed in a revocable range), MEDIA and IMAGE, limited to 64, 128 and 72 MB (`fw@bdfd8b0:os/card_pool.h:L21, L29-43`).
- [F] Ranges A1, A2 and C open at boot; B opens only through `card_pool_open_range` (`fw@bdfd8b0:os/card_pool.h:L76-84`).
- [F] On an Amiga reset with range B lent, the firmware quiesces core 1 (or cold-restarts it), takes B back and flushes the caches, then releases every non-FIRMWARE owner and lends B again if the Amiga cannot use it (`fw@bdfd8b0:os/main.c:L447-463, L572-575`; `os/card_pool.h:L114-124`).
- [F] The firmware's memory-map document sends large working memory to the pool, not to new fixed ranges or the general heap; a fixed range is for hardware or the Amiga needing a stable address (`fw@bdfd8b0:docs/memory-map.md:L22, L34`).
- [F] The 0x30000000 codec scratch of earlier firmware is gone: `0a17831` removed the codecs that used it and freed it for the pool (`fw` `git show 0a17831`).
- [F] The pool entered `master` with the allocator `04b157f` and the map document `c019f60`, both dated 2026-10-10 and merged by `bdfd8b0` (pull request #158); neither is in `8778ef3` (`fw` `git log -1`, `git merge-base --is-ancestor`).
- [F] Before the pool, 0x18000000-0x30000000 held only the 1 MB task queue at 0x18000000, the 1 MB core-1 stack below 0x1C000000 and the 256 MB Z3 fast-RAM window from 0x20000000, with codec scratch at 0x30000000; 0x18100000-0x1BF00000 and 0x1C000000-0x20000000 were unassigned (`fw@8778ef3:os/memorymap.h:L310-311, L319, L330-331, L407-409`; `os/codec37.c:L19`; no other fixed address there in `os/`, `git grep`).
- [G] An f1 acquisition ring (about 18.7 MB at 1080p, `sections/display-coupling.md`), if built, must survive an Amiga reset (E3), so it would be a pool allocation; a FIRMWARE-class owner fits the 64 MB limit and stays out of range B.
- [G] Whether a PL master may write pool memory coherently is unverified.

## Capture clock

- [F] Default builds clock capture from `ZORRO_E7M` (ball R14) through the capture MMCM, which has dynamic phase shift; R14 is regular I/O, so the route is allowed per net with `CLOCK_DEDICATED_ROUTE FALSE`, and `ZORRO_C28D` is false-pathed (`fw@bdfd8b0:xdc/zz9000.xdc:L134`; `xdc/capture_e7m.xdc:L4-12, L34-38`; `mntzorro.v:L1465-1489, L1581-1587`).
- [F] The `zorro3-aga` release variant is built with `--capture-c28` and clocks capture from video-slot `ZORRO_C28D` (ball B20, regular I/O, the same per-net override), constrained at 34.9 ns (`fw@bdfd8b0:xdc/zz9000.xdc:L117`; `xdc/capture_c28.xdc:L4-13`; `build_variant_bitstreams.sh:L256-260`; `README.md:L440-447`).
- [F] A bitstream fixes its capture clock source, which `ZZ9000.CFG` alone cannot change; the E7M bitstreams serve the A3000, other machines and an A4000 as a fallback (`fw@cfbb910:README.md:L444-446`).

## Native-video regression [D] DEC-005

- [F] The firmware has simulation benches for capture and the formatter under `test/video/` (sampler, phase, recovery, row timing, csync, variant, doubled, writeback, source sync, formatter, overlay), plus `video_mode_switch_test.c` (`fw@bdfd8b0:test/video/`), and the bitstream build runs four checks: `verify_formatter_ooc_timing.tcl` after the formatter's out-of-context synthesis, then `verify_vcap_iob_placement.tcl`, `verify_vcap_cdc_timing.tcl` and `verify_runtime_pixel_timing.tcl` after implementation, the last being the release timing gate (no negative slack in any clock group, the 150 MHz runtime pixel clock included) (`fw@bdfd8b0:build_run_synthesis.tcl:L38, L59-61`; `verify_runtime_pixel_timing.tcl:L71-111`).
- [F] The PIP was physically accepted on the default `zorro3` variant only; other variants passed build and timing gates but need their own hardware acceptance (`fw@8778ef3:docs/native-p96-pip.md:L12-16`).
- [F] Release variants are `zorro3`, `zorro3-aga`, `zorro2`, `zorro2-2mb` and the A500-family builds (`fw@8778ef3:build_variant_bitstreams.sh:L44-54`).
- [G] Regression for any board or module change: the benches and the four build checks above as step 0; then NTSC and PAL, each scan-doubler mode, native↔RTG switching, PIP takeover and return, plane on and off, one fault row per applicable SR, on each Zorro variant; pass is no lost or corrupted native frame, by per-frame CRC identity with the Z-7020 baseline from a lossless RGB 4:4:4 HDMI capture (K30, K31).
- [G] The same run checks audio BCLK timing and listens for defects, and checks the VGA output where a VGA add-on is fitted.

## Toolchain

- [F] The bitstream builds with Vivado 2018.3 (`fw@8778ef3:BUILD.md:L16-18`; `zz9000_project.tcl:L2`); the ARM firmware builds without it (`topics/arm-offload.md`, "Mechanisms in the firmware").
- [F] From Vivado 2026.1 a free BASIC tier covers every Zynq 7000 device; only PRO and above include pre-2026.1 versions, and BASIC users keep an existing licence file to use them (`amd-vivado-editions`).
- [F] BASIC limits XSIM to 50K design instances with no UVM, and debug to one ILA core with up to 5 probes (`amd-vivado-editions`).
- [G] So either the project ports to 2026.x, or a 2018.3 installation is used; whether 2018.3 WebPACK still downloads and needs no licence file is [R].
- [R] Tool-only analysis for this project (PL fit, static timing, the regression benches under XSIM) has not been run yet; verify by checking `unknowns.md` K20, K29, K30 for results.
- [R] The 7-series PCIe IP is free; a DisplayPort RX core is licensed but not needed under V-tracked.
- [R] IBIS-AMI simulation needs a tool (commercial, or PyBERT); needed only if PCIe stays in play.
