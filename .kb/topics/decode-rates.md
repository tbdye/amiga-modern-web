# Decode rates

Scope: published decode speeds on 68k processors (lossless, JPEG, MPEG-1 video) and on Cortex-A9 class ARM cores, what the ZZ9000's ARM decodes today, and what reviews report of video playback on Raspberry Pi boards.
Status: current

- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; derived figures here are stated for it.
- Nothing here was measured by this project, and no program from a cited archive was run: every measurement is a third party's, on its machine, software and date.
- `[F]` opens what a source reports; `[G]` opens arithmetic or inference made here, shown beside it.
- Units: MB = 10^6 bytes; K in XPK tables = 1,024 bytes; Mpix = 10^6 pixels; a 16-bit pixel is 2 bytes, so 1 Mpix/s is 2 MB/s.
- Receive, copy and pixel rates are in `topics/target-config-rates.md`; bus ceilings in `topics/bus-and-card-rates.md`.

## 68k lossless decoders

XPK is a compression library system; `xBench` is its benchmark tool, and each sub-library is one coding.

| Decoder | Machine | Output rate | Conditions | Source |
|---|---|---|---|---|
| zlib inflate, as `xpkGZIP` 1.2 (deflate: LZ77 with Huffman coding, the coding inside PNG) | A4000, 68060 at 50 MHz | [F] 1,451 to 1,525 K/s at a size reduction of 46.8 to 49.7% | `xBench` on "an AmigaVision executable" | `aminet:util/pack/xpkGZIP`, `xpkGZIP.doc` L54-73 (2003) |
| The same library's modes 0 to 9: zlib's stored mode, with no compression | Same | [F] 4,575 K/s | Same | `xpkGZIP.doc` L42, L64 |
| `xpkGZIP` 1.0 inflate (zlib 0.93, 1995) | A500, 68030 with 68882 at 50 MHz | [F] 246, 263, 285 and 525 kB/s on files whose size reductions were 4.9%, 19.8%, 32.5% and 70.8% | `xBench`, files in the RAM disk; the 32.5% file is a 512×512 8-bit grey image | `aminet:util/pack/xpkSDHC`, `Docs/Deutsch/SDHC.guide` L196-199, L233-295 (1998) |
| `xpkRAKE` 1.7; `xpkSQSH` 1.10 (LZ77 without entropy coding) | Same 68030 | [F] 1.05, 1.58 and 1.92 MB/s; 0.87, 0.92 and 1.10 MB/s, on the three compressible files | Same | Same guide, L251-294 |
| `xpkNONE` (a copy through the XPK layer) | Same 68030 | [F] 4.73 MB/s | Same | Same guide, L213 |
| Speeds the XPK sub-libraries declare for themselves, K/s | A3000, 68030 at 25 MHz | [F] Copy (`NONE`) 2,477; run-length `FRLE` 1,480 at a declared reduction of 0.2% and `RLEN` 1,043 at 4.5%; LZ77 `FAST` 1,055 to 1,096, `NUKE` 630, `MASH` 400, `SMPL` 354, `IMPL` 270 to 340, `SQSH` "300K/s on A3000"; Huffman `HUFF` 138; arithmetic coding `SHRI` 21 to 25 | Each author's own approximate value, "with SCRAM and AmigaVision executable as standard test" | `aminet:util/pack/xpk_Develop`, `Include/C/xpk/xpk.h` L279-288 and `Autodocs/xpksub.doc` L327-328; `aminet:util/pack/xpk_Source`; `aminet:util/pack/xpk_User`, `XpkMaster.guide` L2119 (XPK 5.2a, 2000) |

- [G] The 68060 figures are 1.49 to 1.56 MB/s for deflate and 4.68 MB/s for the stored mode (× 1,024).
- [G] `xBench` turns task switching off while it unpacks, so the timed step is memory to memory (`aminet:util/pack/xpk_User`, `XpkMaster.guide` L2224-2226).
- [F] The 68060 figures also stand in the mode table of the library's source file, dated 2002-04-09, so they were not measured on the build of 2003-08-14; which earlier zlib, 1.1.3 or 1.1.4, produced them is not stated (`aminet:util/pack/xpkGZIP`, `source/GZIP/xpkGZIP.c` L34-43; `xpkGZIP.doc` L100-108).
- [F] The source maps modes 0 to 9 to zlib level 0 and unpacks every mode with `inflate()` (`xpkGZIP.c` L145-149, L184-185).
- [R] That path carries an Adler-32 checksum of the output; the zlib format specification would verify it.
- [F] `xpkNONE` is a plain memory copy (`aminet:util/pack/xpkGZIP`, `source/NONE/xpkNONE.c` L79-84).
- [G] So the two no-compression figures, 4.68 MB/s on the 68060 and 4.73 on the 68030, are unlike operations, and neither bounds a decoder's output rate.
- [G] Deflate's output rate depends on the data: on the 68030 it rises from 246 kB/s at a 4.9% reduction to 525 at 70.8%; the 68060's figure is for data that halves, and the rate on page-like data (text, flat colour) is unmeasured and likely higher.
- [G] The 68060 rows are 2.8 to 6.35 times the 68030 rows (1,485,824 ÷ 525,114 to 1,561,600 ÷ 245,997), but the sides differ in zlib version and in data, so this is not a ratio between the processors.
- [F] The package's readme says its later zlib "is faster on compression as well as on decompression" (`aminet:util/pack/xpkGZIP`, readme L14-16).
- [G] On the 68030 at 50 MHz the plain LZ77 decoders run at 18 to 41% of that machine's copy rate (0.87 ÷ 4.73, 1.92 ÷ 4.73) and deflate at 5 to 11%.
- [G] The two declared run-length figures are for data with almost no runs, so they are close to copies.
- [F] For a 68000 the same tables say: "Divide by 5 to get timings for 68000." (`XpkMaster.guide` L2476-2477).
- [G] Declared values not in a shipped source file were read out of the library files' mode tables.
- [F] `xpkLZ40`, an LZ4 sub-library, is for PowerPC only (`aminet:util/pack/xpkLZ40`, readme).

## 68k JPEG

| Decoder | Machine | Result | Method | Source |
|---|---|---|---|---|
| Four picture datatypes: `jfif` 44.18, `akjfif` 45.95, `warpjpeg` 45.16 and the OS 3.2 datatype 47.8 | A3000, 68060 at 100 MHz (BFG9060), CyberVision 64 in a 16-bit mode, picture.datatype 47.15 | [F] Seconds a picture, fastest to slowest of the four: 640×480 0.319 to 0.501; 800×600 0.630 to 0.945; 1024×768 1.479 to 2.027; 1536×1024 1.227 to 1.871; 2592×1728 3.069 to 4.713 and 5.553 to 8.376 | Median of 5 runs of a viewer's timed load through the datatype system, pictures in the RAM disk | `aminet:util/dtype/JFIFdt44`, readme L17-36 (2022-06-26); `jpegbench` |
| The same four, OS datatype 47.6 | A4000, BFG9060 board with a 68040 at 25 MHz, Picasso IV | [F] 640×480 2.549 to 3.566; 800×600 5.550 to 7.424; 1024×768 13.733 to 17.822; 1536×1024 10.239 to 14.160 | Same | Same readme, L38-55; `jpegbench` |
| FastJPEG 1.10 and three other viewers | A1200, 68030 at 50 MHz (Microbotics 1230XA), AGA | [F] A 597×796 colour JPEG: FastJPEG 14.3 s real, 12.6 s processor time; PPShow 18.9 s; Viewtek 40.4 s; ViewJpeg 57.9 s; the same picture in grey, FastJPEG 6.9 s real, 5.8 s processor time | One run each; includes start-up and conversion for an AGA screen | `aminet-rview:PictureViewerS` (1994-03-15) |
| FastJPEG 1.0 | "a 7MHz 68000" | [F] 276×212 in 28 s; 415×473 in 64 s | "timed with my watch" | `aminet-rview:FastJPEG` (1994-03-02) |

- [F] The benchmark's logs report 24-bit pictures; whether the timed span holds any conversion to the 16-bit screen or any display is not stated (`jpegbench`, result logs).
- [G] So the datatype figures are decodes to 24-bit in memory; conversion for a 16-bit screen and the write to the card are separate costs.

Rates `[G]`, pixels ÷ seconds, in Mpix/s; bits a pixel from the file sizes in `jpegbench`:

| Picture | Bits a pixel in the file | 68060 at 100 MHz: fastest datatype / OS 3.2's own | 68040 at 25 MHz: fastest / OS 3.2's own |
|---|---|---|---|
| 640×480 | 1.59 | 0.96 / 0.80 | 0.121 / 0.086 |
| 768×576 | 2.01 | 1.00 / 0.83 | 0.126 / 0.091 |
| 800×600 | 3.65 | 0.76 / 0.63 | 0.086 / 0.065 |
| 1024×768 | 8.09 | 0.53 / 0.43 | 0.057 / 0.044 |
| 1536×1024 | 1.86 | 1.28 / 1.07 | 0.154 / 0.111 |
| 2592×1728, two files | 1.99 and 3.92 | 1.46 and 0.81 / 1.20 and 0.67 | 0.166 and 0.090 / 0.123 and 0.068 |
| All ten sized pictures, all four datatypes | 0.99 to 8.09 | 0.39 to 1.46 | 0.044 to 0.166 |

- [G] A 68060 at 50 MHz, by halving the 100 MHz figures: 0.19 to 0.73 Mpix/s, which is 0.39 to 1.46 MB/s of 16-bit pixels; with the fastest datatype alone, 0.27 to 0.73 Mpix/s.
- [G] Halving by clock assumes that speed follows the clock, which memory and bus do not; it is an upper estimate for accelerator boards of the period, since the test board's memory writes at 78.5 MB/s by longwords (`jpegbench`, machine report) against 22.9 MB/s for a CyberStorm Mk II's own memory (`topics/bus-and-card-rates.md`, "Bus ceilings").
- [G] The 68040 at 25 MHz, as measured: 0.044 to 0.166 Mpix/s, which is 0.09 to 0.33 MB/s of 16-bit pixels; the 68060 at 100 MHz is 8.0 times as fast on the 640×480 picture (2.549 ÷ 0.319).
- [G] The 68030 at 50 MHz with the 1994 viewer: 475,212 pixels ÷ 12.61 s = 0.038 Mpix/s, which is 0.075 MB/s of 16-bit pixels by processor time, and 0.033 Mpix/s by real time; it includes conversion for a planar screen, so it is not like for like with the datatype rows.
- [G] The 68000 at 7 MHz: 2.1 to 3.1 thousand pixels a second.
- [G] All of these are whole-picture loads; no source gives a rate for small JPEG tiles, where the cost of each call would weigh more.

## 68k MPEG-1 video

Decode and display together:

| Player | Machine | Result | Source |
|---|---|---|---|
| `mp` 1.03 | "An Amiga A3000" (68030 at 25 MHz) | [F] "about 3.7 frames per second for average MPEG streams of 160x120 pixels per frame" | `aminet:gfx/show/mp103`, readme (1993) |
| aMiPEG 0.3 | "the A4000/040" | [F] "renders to HAM8 with 6.5 fps (was 6.3)"; stream size not stated | `aminet:gfx/show/aMiPEG_1.1_bin`, readme (1998) |

- [G] The first is 3.7 × 19,200 = 0.071 Mpix/s.

## Cortex-A9 JPEG

- [F] The ZZ9000 firmware builds libjpeg-turbo with NEON, the processor's vector instructions (`fw@cfbb910:build_libjpeg_turbo.sh:L64-79`).
- [F] It selects the library's fast integer inverse transform (`fw@cfbb910:os/sdk_jpeg.c:L189`; `os/sdk_image_stream.c:L2414`).
- [F] The library's own study on a phone with an "800 MHz dual-core ARM Cortex-A9", quality 95, output to RGB, five test images of 1240×960 to 3136×2352, in Mpix/s (`libjpeg-turbo-perf`, sheet "iOS-A9"; command `tjbench {file} 95 -rgb -qq -nowrite -warmup 10`):

| Chroma subsampling | libjpeg-turbo 1.5 with NEON [F] | Without vector instructions [F] | libjpeg v6b [F] | NEON figure × 667 ÷ 800 [G] |
|---|---|---|---|---|
| 4:2:0 | 15.5 to 21.7 | 7.4 to 9.2 | 6.8 to 8.8 | 13.0 to 18.1 |
| 4:2:2 | 16.0 to 24.8 | 6.4 to 8.2 | 5.9 to 7.8 | 13.4 to 20.7 |
| 4:4:4 | 12.3 to 20.0 | 5.4 to 7.7 | 4.9 to 7.2 | 10.3 to 16.6 |
| Grey | 23.7 to 37.5 | 15.3 to 23.2 | 13.2 to 21.2 | 19.8 to 31.3 |

- [G] The last column scales to the card's 667 MHz by clock alone and takes the study to have used one core, which its sheet does not state; the phone's chip is another maker's, and cache and memory are not accounted for.
- [G] The three colour rows together span 10.3 to 20.7 Mpix/s; a rate is paired only with a size ratio of the same chroma format, so for 4:2:0 the bracket is 13.0 to 18.1 Mpix/s.
- [F] The same page puts the fast inverse transform 4 to 14% ahead in decompression, "with very little overall loss in quality", and merged upsampling "as much as 15-20%" ahead for subsampled files (`libjpeg-turbo-perf`, "Fast Upsampling and Fast IDCT").
- [G] The study's command names neither option, so the firmware's transform may run faster than the table; its speed on this processor is unmeasured.
- [G] Quality 95 is a heavy setting; no figure at a lower quality is given for this core.
- [G] These rates are decodes to RGB; on a 16-bit screen the card adds a second pass ("What the card's ARM decodes today").
- [F] One figure from the card itself, for another codec: MPEG-1 video measured 209 decode calls a second on a 318×240 clip and 93.113 on 640×480, in a test build on Zorro III with the Amiga not named (`fw@cfbb910:docs/native-p96-pip.md:L313-314, L329-337, L394`).
- [G] That is 16 to 29 Mpix/s (76,320 × 209; 307,200 × 93.113).

## Inflate, LZ4 and PNG on neighbouring ARM cores

- [F] The firmware uses zlib 1.3.2 and libpng 1.6.58, the latter from a NEON build directory (`fw@cfbb910:ZZ9000_proto.sdk/ZZ9000OS/Makefile:L45-54`).
- [F] No figure for a Cortex-A9 was found: the Squash compression benchmark lists a Cortex-A9 board (PandaBoard ES, 1.2 GHz) only as a disabled entry, and its data file is absent (`squash-benchmark`, `squash-benchmark.js`).
- [G] Its three 32-bit ARM boards are other cores; rates are uncompressed size ÷ decompression processor time over its 28 files, in MB/s of output, each median the mean of the two middle values; the page gives gcc 4.9.2 for all three:

| Board, core, clock | zlib level 6 inflate: lowest, median, highest | LZ4 level 1, median | LZO1X level 1, median | Plain copy, median |
|---|---|---|---|---|
| BeagleBoard-xM, Cortex-A8, 1 GHz | 14.5, 28.2, 50.2 | 46.8 | 37.3 | 65.7 |
| Raspberry Pi 2, Cortex-A7, 900 MHz | 16.9, 34.6, 63.3 | 61.2 | 55.1 | 99.3 |
| ODROID-C1, Cortex-A5, 1.5 GHz | 24.4, 53.3, 102.2 | 98.7 | 80.8 | 147.0 |

- [G] If a Cortex-A9 at 667 MHz inflated at the Cortex-A8's or Cortex-A7's rate, a 24-bit PNG, 3 bytes a pixel, would inflate at 9 to 12 Mpix/s at the median (28 ÷ 3, 35 ÷ 3).
- [G] On the slowest file, of 4 KB, where set-up cost shows, 5 to 6 Mpix/s (14.5 and 16.9 MB/s); on the slowest file of 1 MB or more, 6 to 8 (19.1 and 23.7); on the least compressible file of 1 MB or more, 7 to 9 (21.1 and 26.2).
- [G] All of that is before PNG's row filters and any colour conversion, and no source ties those cores' rates to the Cortex-A9.
- [G] The card's PNG decode rate is a guess of 3 to 10 Mpix/s with no measurement behind it; the neighbours' figures do not contradict it.
- [G] On the Cortex-A8 and Cortex-A7 boards LZ4 runs at 1.7 to 1.8 times their zlib rate (46.8 ÷ 28.2, 61.2 ÷ 34.6).

## What the card's ARM decodes today

Every line is `[F]` at `fw@cfbb910` unless it opens with another label; `lib.md` stands for `sdk/docs/zz9k-library.md`.
The video service, its codecs and its Zorro II limit are in `sections/firmware-and-rtl.md`, "What the card offers today".

- Formats: JPEG, and PNG through streaming image sessions; the one-shot PNG and GIF calls return `UNSUPPORTED`; a WebP decoder is in the firmware and not advertised (`lib.md:L448-452, L561-566`).
- Output is 32-bit, or 24-bit RGB, and must match the format of the surface it lands in (`os/sdk_image_stream.c:L292-298`; `os/sdk_mailbox.c:L3133-3140, L5289-5294`).
- [G] So a decode straight into a 16-bit framebuffer is refused.
- On a 16-bit screen the route is two passes: a decode into a 32-bit surface, then the scaler's conversion from 32-bit to 16-bit into the framebuffer (`lib.md:L399-404, L541-543, L663-665`).
- A scale or conversion that touches the live framebuffer is computed inline on the first core and is not handed to the second core's worker (`topics/arm-offload.md`, "Which core runs what").
- The SDK splits such draws into bands of 96 rows, "so large bilinear draws do not monopolize a single mailbox call" (`lib.md:L432, L633-635`).
- Limits: 4 image sessions, 16 surfaces and 32 shared buffers (`os/sdk_mailbox.h:L984-985, L1013`); a shared heap of 4,128,768 bytes (`os/memorymap.h:L114-115`).
- [G] A 1280×720, 32-bit surface is 3,686,400 bytes, which leaves 442,368 bytes of that heap for the compressed input and every other client: a full-window decode at that size needs tiles or a surface in the card's own memory.
- A program can aim this at its own Workbench window with no change to the firmware: the firmware's image tools walk the window's list of visible rectangles and submit one clipped job for each (`sdk/tools/zz9k-image-window.c:L213-230`; `lib.md:L690-704`).
- [G] The writes go to absolute framebuffer positions, so the program owns the clipping and must keep the window layout still while a job runs.
- Video frames go to the P96 overlay as a decoder-owned planar frame, not into the window's bitmap, and compressed input arrives in shared-buffer chunks (`lib.md:L722-733, L751-753`).
- [G] So a program could feed the video service from a network stream; the firmware's own player takes files (`sdk/docs/zzplay.md:L17-23`).
- The document's own real-time envelope for WebM on this processor, which release firmware does not advertise, is about 1280×720 for VP8 and 854×480 for VP9 (`lib.md:L801-807, L815-816`).

## Video playback on Raspberry Pi boards

| Board | Statement | Method | Source |
|---|---|---|---|
| Raspberry Pi 5 | [F] With the screen at 1080p, a 1080p YouTube video at about 24 frames a second "was smooth with few dropped frames", and a 1080p video at 60 frames a second "still looked pretty smooth", with "a fair number of dropped frames" reported; with the screen at 4K and the videos at 1080p, each dropped "about two thirds of their frames", full screen or in part of the browser window | The reviewers' own playback in a browser; decode path not stated | `toms-pi5` (2023-10-23) |
| Raspberry Pi 5 | [F] "only 4kp60 H265 (HEVC) decode is available. But it only uses 50% of the processors to do 1080p60 on YouTube" | Not stated | `rpi5-launch`, a comment from the maker of 2023-09-28 |
| Raspberry Pi 5 and 4 | [F] "Opening Firefox took 5.1 seconds on the Pi 5, versus to 8.6 seconds on the Raspberry Pi 4": a program start from a microSD card, not a page load | Not stated | `toms-pi5` |
| Raspberry Pi 4 | [F] YouTube "videos can appear jerky if you view them at full screen (they play fine in a window)" | Not stated | `toms-pi4` (updated 2022-09-17) |
| Raspberry Pi Zero 2 W | [F] "it failed to play a clip at even 720p resolution"; with wired Ethernet "we still saw frequent pauses and stutters"; one browser tab loading the reviewer's site "crawled along" | Not stated | `toms-pizero2w` (2021-10-28) |

- [G] The maker's comment implies software decoding of YouTube's video on the Pi 5, since it names H.265 as the only hardware decode.
- [G] A 1080p frame has 9.0 times the pixels of a 640×360 frame and 5.1 times those of an 854×480 frame (2,073,600 ÷ 230,400 and ÷ 409,920), so playback that holds at 1080p and 24 frames a second has that margin at those sizes; no report at 360p or 480p was found.

## Not established

"Not found" means absent from Aminet (the first results page of each search), a few maker, vendor and review pages and web searches; Amiga forums other than one thread, magazine archives, video reviews and the Raspberry Pi forums were not searched.

- Run-length, plain LZ77, LZ4, LZO, LhA or LZX decode rates on a 68060, and PNG decode times or a VNC client's rate on any 68k: not found, and for run-length and LZ77 the 68030 rows are a lower bound with no upper bound.
- Deflate's rate on page-like data on a 68060: unmeasured; an instruction count of the decoder on such data would bound it.
- The current JPEG datatypes on a 68030, and any JPEG rate at a 68060's 50 MHz that is measured, not halved: not found.
- MPEG-1 frame rates on a 68060: not found in the Aminet descriptions of four players.
- Inflate, PNG or LZ4 rates on a Cortex-A9, or any figure from a Zynq-7000 board: not found.
- The card's own JPEG and PNG decode rates, the rate of its second pass on a 16-bit screen, and the fast transform's effect on text: unmeasured; only the card would show them.
- On Raspberry Pi boards: page-load times, YouTube frame counts at 360p, 480p or 720p, any figure for a Compute Module, and the cost of off-screen rendering, screen capture or a VNC server: not found.

## Sources

`aminet`, `aminet-rview`, `fw` and `rpi5-launch` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `jpegbench` | Test images, scripts, machine reports and raw results of the JPEG datatype benchmark | `http://bax.comlab.uni-rostock.de/fileadmin/downloads/jpegbench.zip` | 2026-10-11; SHA-256 `ea7ff069be392a7fa9e53ef7a0000e6219ede6b09fb0da95782da086726bbc7c` |
| `libjpeg-turbo-perf` | libjpeg-turbo performance page and its spreadsheet for version 1.5 | `https://libjpeg-turbo.org/About/Performance`; `https://libjpeg-turbo.org/pmwiki/uploads/About/libjpegturbo-1.5.ods` | 2026-10-11; the page gives 2021-02-02 as its last change; spreadsheet SHA-256 `1537cf59d9bf9512de1c3f9fce37c552a27c637f2874df8fb8f8fa7df6915fc6` |
| `squash-benchmark` | Squash compression benchmark: page script and one data file a board | `https://quixdb.github.io/squash-benchmark/` (`squash-benchmark.js`, `data/<board>.csv`) | 2026-10-11 |
| `toms-pi5` | Review of the Raspberry Pi 5 | `https://www.tomshardware.com/reviews/raspberry-pi-5` | 2026-10-11 |
| `toms-pi4` | Review of the Raspberry Pi 4 | `https://www.tomshardware.com/reviews/raspberry-pi-4` | 2026-10-11 |
| `toms-pizero2w` | Review of the Raspberry Pi Zero 2 W | `https://www.tomshardware.com/reviews/raspberry-pi-zero-2-w-review` | 2026-10-11 |
