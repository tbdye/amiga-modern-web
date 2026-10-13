# The RTG software layer: P96 and PrismRTG

Scope: what the Amiga's RTG software layer gives a program that draws received pixel rectangles into its own Workbench window on a graphics card: P96 and the open-source PrismRTG, the calls that put pixels in a window, scroll-copy, overlay (picture-in-picture) windows, what in either layer could fill a rectangle without the pixels crossing the 68k, and what an open layer changes.
Status: current

- [D] DEC-028: the ZZ9000 is the likely benchmark, for performance only; P96 as what RTG cards have in common, and an open-source layer in its place, are raised, not adopted.
- Nothing here was built or run; third-party files were read as text on 2026-10-11, and a measurement is its source's own.
- `[F]` opens what a source states; `[G]` opens arithmetic or inference made here; a "none" names the search it rests on.
- `prism` citations are at `d62ee32`, which is tagged `v1.1-beta5`; `fw` at `cfbb910`; `drivers` at `cb6a1c4`.
- P96's and CyberGraphX's documentation is cited by entry: an autodoc entry, a wiki release note or a driver function ("Sources").
- "Card memory" means the bitmap that a window's RastPort draws into; every byte the 68k writes to it crosses the Zorro bus once.
- Published write rates into a card: `topics/target-config-rates.md`, "Copies into the card"; programs that already draw received pixels this way: `topics/prior-art.md`, "Remote and split-engine browsers".

## P96

- [F] P96 is "an RTG software package for the Amiga", sold as commercial software whose current package may not be redistributed; its old V2.0 stays redistributable as shareware (`p96-wiki`, "General").
- [F] What is published for developers is two archives, one for programs that call P96 and one for card drivers, and no source code of the package; the first holds headers, autodocs and examples under CC-BY terms, and the second was not read (`p96-wiki`, "Software Developer archive", "Hardware manufacturer archive"; `p96-develop`, `P96Develop.readme`).
- [F] Its release notes name its parts: `rtg.library`, `Picasso96API.library`, and `emulation.library`, "responsible for emulation of the villageTronic API and the cybergraphics API" (`p96-wiki`, "Update V3.3.3", "Update September 2021 (V3.1.2)").
- [F] Under P96 the Amiga's `graphics.library` is patched to render on RTG screens (`p96-develop`, `P96Develop.readme`).
- [G] So a program written to the CyberGraphX interface runs on P96 through `emulation.library`.

## PrismRTG

Under this heading a path with no ID is `prism@d62ee32`.

| Item | What its files state |
|---|---|
| Its own description | [F] "Graphics card (RTG) software for AmigaOS 3.x, written from scratch", which "takes the place of Picasso96 on the Amiga it runs on" (`README.md:L3, L12-13`) |
| Licence | [F] GPL-3.0-only (`README.md:L435`; `LICENSE`) |
| Releases | [F] Version 1.0 is dated 5 October 2026 (`README.md:L188`); the commit read is the tag `v1.1-beta5` |
| How it hooks in | [F] A background program, `PrismD`, replaces about 50 entry points of `graphics.library`, `intuition.library` and `exec.library` with `SetFunction`: blits, fills, text, lines, `ScrollRaster`, pixel arrays, bitmap allocation, the display database, screen open and close (`src/prismd.c:L1858-1911, L2047-2058`); [F] it has no `rtg.library` (`src/prismd.c:L1999-2000`) |
| Libraries it supplies | [F] Its own `Picasso96API.library` 2.500 and `cybergraphics.library` 41.99, added in memory by `PrismD` (`src/p96.c:L45-46, L1082-1103`; `src/cgx.c:L41`); [F] no `emulation.library` and no `cgxvideo.library`: neither name occurs in the repository |
| P96 interface | [F] Every slot of the published function table is filled: bitmap allocation, locking and attributes, mode queries and requester, screens, `p96WritePixelArray`, `p96ReadPixelArray`, pixel and rectangle calls, true-colour data, the six `p96PIP_*` calls, board data (`src/p96.c:L1049-1080`) |
| CyberGraphX interface | [F] Mode queries and requester, `ScalePixelArray`, `ReadPixelArray`, `WritePixelArray`, `WriteLUTPixelArray`, `MovePixelArray`, `FillPixelArray`, `InvertPixelArray`, `LockBitMapTagList`, `UnLockBitMap`, `ExtractColor`, `DoCDrawMethodTagList`; `CVideoCtrlTagList` only logs, and seven private slots return 0 (`src/cgx.c:L711-714, L806-835`) |
| Relation to P96's interfaces | [F] It reproduces the published function order, tag values, pixel-format codes and structure layouts, with implementations of its own (`docs/provenance.md:L25-32`) |
| Card drivers | [F] An interface of its own, not P96's (`docs/design.md:L41-42`); four loadable modules: `PICASSO2`, `ZZ9000`, `P96` and `UAEGFX` (`README.md:L66-70`) |
| P96 drivers | [F] The `P96` module is an "experimental" adapter that loads a P96 `.card` driver "without loading P96's `rtg.library` or monitor program"; it "supports linear framebuffers, not every P96 memory model", and private `rtg.library` services stay outside it (`README.md:L90-91, L105-106`; `docs/p96-drivers.md:L103-104`) |
| ZZ9000 | [F] "MNT ZZ9000, Zorro III", firmware 2.8, on an A4000 with a 68060: "Real hardware. Blitter fills, copies, text, lines; hardware pointer. 8/16/32-bit up to 1280x1024"; in Zorro II mode: "Untested. No blitter or pointer support in this mode" (`README.md:L22, L29`) |
| | [F] The driver is native: it writes the firmware's command mailbox itself, does not load `ZZ9000.card`, and was checked against the v2.8.1 driver and firmware sources (`src/drv_zz9000.c:L1-17, L162-227`); [F] it offers 8-bit, 16-bit big-endian (5-6-5 and 5-5-5) and 32-bit BGRA, and keeps its bitmaps in the first 13.9 MB of card memory (`src/drv_zz9000.c:L623-631`) |
| Other cards | [F] One real Cirrus GD5434 board on an A2000 with a 68030; five Cirrus boards in emulation only; one card through its P96 driver, as a user's report; UAE's emulated card (`README.md:L20-30, L129-136`) |
| Machines | [F] "Needs Kickstart 3.1 or newer", "and a 68020 or better. No FPU needed" (`README.md:L32-33`) |
| Build and tests | [F] Built with amiga-gcc under WSL or Linux; its host tests run under an emulator, and programs that need a booted Amiga are built and not run by the suite (`README.md:L351-359`; `tests/README.md:L10-15, L39`) |
| Its own statement of maturity | [F] "Tested on two machines by one person. Treat it as early software." (`README.md:L320`); [F] the ZZ9000 driver is tested on one real A4000 only, the emulator used having no ZZ9000 (`docs/design.md:L20`) |
| Tested software | [F] About 40 programs started on an emulated Picasso II+ and four on the real A4000; its `p96test` "checks every call at 8, 16 and 24 bits" (`README.md:L155-157, L267-278`) |

- [F] The two cannot coexist: "PrismRTG and Picasso96 cannot both be active on one Amiga", and its installer moves P96's monitor files and API library aside (`README.md:L286-290, L299-301`).
- [F] Its README reports drawing speed against P96 on one A4000 with a 68060 and a ZZ9000 at 800×600, 8-bit, in operations a second by its own benchmark program: `ScrollRaster` 400×100 5,520 under P96 and 10,737 under version 1.1 beta 4; `ClipBlit` 200×100 5,493 and 8,882; bitmap-to-screen blit 64×32 11,178 and 24,883 (`README.md:L213-224`).
- [F] Its conditions: P96 was `rtg.library` 43.760 with the card's own driver, measured two days earlier than the version 1.0 column of 5 October 2026, and the beta 4 column was measured on 9 October; run-to-run noise is "about 5%", and speeds vary "by up to 5-10% from one boot to the next" (`README.md:L175-178, L188-193`).
- [F] The README does not state P96's asynchronous-blit setting ("async" occurs nowhere in it), and says "16-bit and 32-bit show the same pattern" (`README.md:L226`).
- [F] Its benchmarks, it says, "say nothing about everything else Picasso96 does and PrismRTG does not: a long list of cards, picture-in-picture, years of tested compatibility" (`README.md:L180-182`).

## Putting pixels into a window

| Call | Needs | What its documentation says | Source pixel formats | Copies on the 68k side |
|---|---|---|---|---|
| `p96WritePixelArray` | `Picasso96API.library`; a `RenderInfo` with the buffer's address, bytes a row and format | [F] It writes "to a rectangular area of the RastPort"; nothing on clipping, conversion or speed (`p96-develop`, autodoc `p96WritePixelArray`) | [F] 8-bit palette, six 15- and 16-bit orders, two 24-bit and four 32-bit, "B8G8R8A8" among them (autodoc, colour formats) | [G] One: the caller's buffer to card memory; [F] PrismRTG copies a buffer already in the bitmap's format row by row straight into the bitmap, and converts any other into a row buffer in RAM first (`prism:src/p96.c:L531-548`); P96's own behaviour is not documented |
| `WritePixelArray`, `WriteLUTPixelArray` | `cybergraphics.library`: CyberGraphX's, P96's `emulation.library` or PrismRTG's | [F] They "write the color value from a linear array of color values into the bitmap used to describe a particular rastport" (`cgx-devkit`, autodoc `WritePixelArray`) | [F] 24-bit RGB, 32-bit RGBA and ARGB, 8-bit with a palette, 8-bit grey; no 16-bit source format (same entry); [F] PrismRTG also takes a "raw" format, bytes already in the bitmap's layout, copied without conversion (`prism:src/cgx.c:L202-203`) | [G] One, with a conversion whenever the screen is not in the source format |
| `WriteChunkyPixels` | `graphics.library` V40, Kickstart 3.1 | [F] It writes pen numbers; "The source array can be in fast RAM" (`gfx-autodocs`, `WriteChunkyPixels`) | 8-bit pens only | [G] One; on a deep screen each pen goes through the palette |
| `p96LockBitMap`; `LockBitMapTagList` | A P96 or CyberGraphX bitmap | [F] Each returns the bitmap's address, bytes a row and pixel format for direct writes; P96: "Never hold the lock for longer than about one second as all screen switching is disabled", and the address may differ after every unlock; CyberGraphX: "DON'T lock the bitmap longer than for one frame. DON'T use any library calls while the bitmap is locked!" (`p96-develop`, autodoc "bitmaps" and `p96LockBitMap`; `cgx-devkit`, autodoc `LockBitMapTagList`) | The bitmap's own format only | [G] None beyond the write itself: a program may decode or copy straight into card memory; [F] in PrismRTG the address is the card's on boards with a linear framebuffer and a RAM shadow on others (`prism:docs/driver-architecture.md:L55-60`) |
| `BltBitMapRastPort` from an off-screen bitmap that is a friend of the screen's | An off-screen bitmap that the layer has placed in card memory | [F] `p96AllocBitMap` allocates "with the same color format" as a friend bitmap, and a `BMF_USERPRIVATE` bitmap is in fast RAM and "will never move or be accessed by graphics board hardware" (`p96-develop`, autodoc `p96AllocBitMap`); [F] on a card with a blitter P96 "will also store non-visible bitmaps on the board" (`p96-drv`, "BIB_BLITTER"), and PrismRTG puts a friend bitmap "to free VRAM if there is some" (`prism:src/bitmap.c:L328-329`) | The screen's format | [G] The fill of the off-screen bitmap crosses the bus once; the blit to the window can then stay on the card ("Scroll-copy") |

- [R] Neither locking entry mentions windows or clipping, so the caller must clip to its own visible area; the layers documentation would verify it.
- [F] The "raw" format of PrismRTG's `WritePixelArray` is absent from the CyberGraphX Release VI header: PrismRTG defines it only where the header has not, and its test tool calls the definition "missing from the NDK header" (`prism:src/cgx.c:L121-122`; `prism:tools/tmpltest.c:L17-18`); which other layers accept it was not checked.
- [F] The ZZ9000's 16-bit screen is `R5G6B5`, bits `rrrrrggggggbbbbb`, so bytes `rrrrrggg gggbbbbb` with the high byte first, and its 32-bit screen is BGRA, under both layers (`drivers@cb6a1c4:rtg/mntgfx-gcc.c:L149-161, L232-240`; `p96-develop`, `Include/libraries/Picasso96.h`; `prism:src/drv_zz9000.c:L630-631`; `fw@cfbb910:sdk/docs/zz9k-library.md:L349-352`).
- [G] No documented CyberGraphX source format is BGRA or 16-bit, so every `WritePixelArray` in a documented format to a ZZ9000 screen deeper than 8 bits converts.
- One raw write figure into a ZZ9000 under PrismRTG, and frames a second through its pixel-array call: `topics/target-config-rates.md`, "Copies into the card".

## Scroll-copy

- [F] The documented calls: `ScrollRaster` moves "the bits in the raster by (dx,dy)" and fills the vacated strip; `ClipBlit` "Calls BltBitMap() after accounting for windows"; `BltBitMap` works on bare bitmaps (`gfx-autodocs`, `ScrollRaster`, `ClipBlit`, `BltBitMap`).
- [F] CyberGraphX adds `MovePixelArray`: "The blitter can be used to move the data if the bitmap is in display memory" (`cgx-devkit`, autodoc `MovePixelArray`).
- [F] P96 card drivers accelerate copies through two hooks: `BlitRect` "shall copy a rectangular image region in the video RAM", where "Source and destination rectangle may be overlapping", and P96 calls it "to implement some of the parameter combinations of the BltBitMap() function"; `BlitRectNoMaskComplete` copies between two regions and is also used "to move bitmaps in video RAM" (`p96-drv`, "BlitRect", "BlitRectNoMaskComplete").
- [G] A driver may fall back to the processor for any combination, and that page does not say that P96 routes `ScrollRaster` and `ClipBlit` through these hooks.
- [F] On the ZZ9000 under P96 the driver's `BlitRect` writes source and destination coordinates, size, pitch and colour mode into the card's command mailbox and then the opcode `OP_COPYRECT`, and the firmware does the copy; `BlitRectNoMaskComplete` does the same with `OP_COPYRECT_NOMASK`; both hooks are installed whenever the driver loads (`drivers@cb6a1c4:rtg/mntgfx-gcc.c:L1063, L1067, L1709-1767, L1770-1811`).
- [G] So no pixel crosses the bus; how long the card takes: `topics/bus-and-card-rates.md`, "Scrolls on the card".
- [F] In Zorro II mode `BlitRect` starts the same copy through the card's register file instead of the mailbox (`drivers@cb6a1c4:rtg/mntgfx-gcc.c:L1749-1766`); PrismRTG has no blitter in that mode ("PrismRTG").
- [F] On the ZZ9000 under PrismRTG `ScrollRaster` and `ClipBlit` reach the same firmware opcode through its own driver, for copies larger than 64 pixels (`prism:src/render.c:L487-488, L2689-2724, L2751-2764, L2826-2864`; `prism:src/prismint.h:L222-242`; `prism:src/drv_zz9000.c:L186-204`).
- [F] PrismRTG takes the on-card path for `ClipBlit` only when source and destination are the same layer and bitmap and each rectangle lies wholly inside one visible clip rectangle; otherwise it reads the rectangle into RAM and writes it back (`prism:src/render.c:L2657-2681, L2704-2744`).
- [G] That covers a rectangle spanning several clip rectangles, as in a partly covered window, and any `ClipBlit` between two layers or bitmaps: two bus crossings for each pixel.
- [F] `ScrollRaster` does the same when its rectangle is not in one piece (`prism:src/render.c:L2779-2824, L2854-2858`); `BltBitMapRastPort` from an off-screen bitmap uses the card's copy between areas when both bitmaps are in card memory (`prism:src/render.c:L2511-2529, L2628-2633`; `prism:src/prismint.h:L233-239`).
- [F] P96 3.6.0 added asynchronous blitting, with which "the 68K CPU is allowed to run in parallel to the blitter" (`p96-wiki`, "Update V3.6.0").

## Overlay windows

- [F] `p96PIP_OpenTagList` "Opens a Picasso96API picture-in-picture window", which "behaves like a standard intuition window"; the caller gets a source bitmap and RastPort and draws into them; the types are a memory window, the default, and a video window (`p96-develop`, autodoc `p96PIP_OpenTagList`, `p96PIP_GetTagList`).
- [F] A driver supplies it as a "special feature" through `CreateFeature` and `SetFeatureAttrs`, and in the overlay "the chip may offer color spaces such as YUV" (`p96-drv`, "BIB_VIDEOWINDOW", "CreateFeature").
- Which cards have an overlay under P96, and the limits of each: `topics/audience.md`, "P96 overlay windows by card".
- [F] The ZZ9000's driver advertises an overlay on firmware 2.6 or later and accepts three packed YUV 4:2:2 orderings only (`drivers@cb6a1c4:rtg/mntgfx-gcc.c:L1111-1139`; `rtg/overlay_feature.h:L52-57`).
- [G] On the ZZ9000, RGB browser pixels would therefore need converting to YUV 4:2:2 and would still cross the bus; the plane behind that overlay: `sections/firmware-and-rtl.md`, "What the card offers today".
- [F] The firmware's note says applications reach the overlay through `p96PIP_*` "directly or through cgxvideo" (`fw@cfbb910:docs/native-p96-pip.md:L20-21`).
- [F] A program can also open a `cgxvideo.library` video layer on its window and write pixels into it through a lock; one VNC client does so with a 16-bit RGB source (`twinvnc@86a5721:twinvnc/gfxoverlay.c:L48-64, L208-232`); [G] the ZZ9000 driver would refuse that source unless P96's `cgxvideo` side converts, which was not checked.
- [F] In PrismRTG memory-window overlays are software composition into a RAM frame that is then uploaded; video windows and YUV source formats are refused (`prism:src/p96.c:L799-813`; `prism:docs/p96-drivers.md:L95-101`).
- [F] Its documents say "This is not a hardware overlay or page-flip implementation" and "It does not invoke card overlay engines", and its P96 adapter never calls `CreateFeature` (`prism:docs/driver-architecture.md:L153`; `prism:docs/p96-drivers.md:L101`; a search of `src/drv_p96.c`).
- [F] Its README says both "No picture-in-picture windows" and that such windows "go through a compositor"; the source matches the second (`prism:README.md:L157-158, L326-330`).
- [G] So under PrismRTG the ZZ9000's hardware overlay is unused, and a program that needs `cgxvideo.library` finds none.

## Filling a rectangle without the 68k

| What | Exists? | Source |
|---|---|---|
| A P96 driver hook that takes pixel data from anywhere but 68k memory or card memory | [F] None on the driver-development page, whose function index was read in full: every drawing hook takes 68k memory (templates, patterns, planar bitmaps) or card memory (`BlitRect`); the special-feature types are flicker fixer, memory window, video window and video capture | `p96-drv`, "Functions", "Blitter Support", "GetFeatureAttrs" |
| Hooks in the driver header that the page does not describe | [F] `ScrollPlanar`, `UpdatePlanar`, `WriteYUVRect`, `GetVBeamPos` and the driver's own bitmap allocation; `WriteYUVRect` takes an untyped source pointer and a `RenderInfo`, and its meaning is undocumented | `prism:src/p96sdk/boardinfo.h:L511-514, L543-554` |
| The same in PrismRTG's driver interface | [F] None: fill, copy within a bitmap, copy between two card areas, 1-bit template expansion, line and cursor; a newer table adds planar-to-chunky conversion and byte-range reads and writes between RAM and device memory | `prism:src/prismboard.h:L101-131`; `prism:src/boardops.h:L28-47` |
| Drawing into the RTG framebuffer from the ZZ9000's own processor, beside the RTG layer | Yes, through `zz9k.library` and not through P96 | `sections/firmware-and-rtl.md`, "What the card offers today"; `topics/arm-offload.md`, "Mechanisms in the firmware" |
| Decoding on the card, shown in a P96 overlay window | Yes | `topics/decode-rates.md`, "What the card's ARM decodes today" |
| A network path into the ZZ9000's processor that bypasses the 68k | No | `sections/architecture.md`, "Control link (K8)" |
| Whether `zz9k.library` services work while PrismRTG drives the card | [F] Not stated: PrismRTG's files mention neither `zz9k` nor the card's SDK, but for two comments on memory layout | `prism:src/drv_zz9000.c:L623-626`; `prism:tools/prismtest.c:L237-239` |

- [G] A "put these pixels from a card-side buffer into this window" operation could exist as a new driver hook in an open layer or, as the ZZ9000's SDK does, beside the layer; nothing read shows either done for received pixel rectangles.

## What an open layer changes

- [F] PrismRTG's source is public under GPL-3.0-only, while P96 is distributed without source and is extended through its documented driver hooks and calls ("P96", "PrismRTG").
- [F] PrismRTG's driver interface is versioned, `PRISM_BOARD_ABI 2` and `PRISM_OPS_ABI 1`, and a module from another build "is rejected with an ABI/version or layout diagnostic" (`prism:src/prismboard.h:L20-21`; `prism:src/boardops.h:L48`; `prism:README.md:L68-70`).
- [G] So a new hook means a new `PrismD` and rebuilt driver modules together.
- [F] A driver for another board is one C file, selected by name, and needs no change to `PrismD` (`prism:README.md:L72-80`).
- [G] A new call that keeps pixels off the bus would need three things: a hook in the layer, with a new interface revision; an implementation in each card's driver, where a card reached only through the P96 adapter gets what P96's driver hooks offer; and PrismRTG in place of P96 on the machine, since the two cannot both be active.
- [G] A program that relies on a call only PrismRTG has finds no such call on a machine that runs P96.
- [G] On the ZZ9000 an open RTG layer is not a precondition for a card-side path: the SDK draws into the RTG framebuffer with P96 driving the card ("Filling a rectangle without the 68k").
- [F] The application-side calls of "Putting pixels into a window" and "Scroll-copy" exist under both layers: PrismRTG fills both libraries' published function tables and patches `WriteChunkyPixels`, `BltBitMapRastPort`, `ClipBlit` and `ScrollRaster` (`prism:src/prismd.c:L1858-1911`); [G] a client written to those calls names neither layer.
- [G] Differences visible in PrismRTG's source: the "raw" pixel-array format, overlays as software composition without video windows or YUV, `CVideoCtrlTagList` that only logs, and no `cgxvideo.library`; whether the calls behave alike beyond that rests on its own tests.

## Not established

- What P96 does with a pixel-array write whose source is not in the screen's format, and whether it routes `ScrollRaster` and `ClipBlit` through its drivers' copy hooks, a partly covered window included: P96 is closed, and its documentation does not say.
- Whether P96's `emulation.library` accepts the "raw" `WritePixelArray` format, and whether its `cgxvideo` side converts an RGB source for the ZZ9000's overlay: not checked; `cgxvideo.library`'s autodoc was not read.
- Whether `zz9k.library` services work with PrismRTG driving the card, and PrismRTG with `ZZ9000.card` through its P96 adapter: its files record neither; the adapter's recorded tests are UAE's driver and one user's report (`prism:README.md:L107-110`).
- PrismRTG on a ZZ9000 in a machine other than its one A4000, or in Zorro II mode: its README records none.
- Any statement about PrismRTG by P96's publisher or in the ZZ9000 firmware and driver histories: none in the commit messages of `fw@cfbb910` or `drivers@cb6a1c4`; statements elsewhere were not looked for.
- Not read: PrismRTG's Cirrus driver, P96's driver-development archive beyond the header above, and the NDK's own copy of the graphics autodocs.

## Sources

`prism`, `fw`, `drivers`, `twinvnc`, `p96-wiki` and `p96-drv` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `p96-develop` | `P96Develop.lha`: `Include/autodocs/Picasso96API.doc`, `Include/libraries/Picasso96.h`, `P96Develop.readme` | `https://wiki.icomp.de/w/images/6/62/P96Develop.lha` | 2026-10-11; readme "Version: 3.6.0"; SHA-256 `983d2d9d3354913d19701cd90ed39ca69a6dd6991b248b243b80bc230de0130c` |
| `cgx-devkit` | CyberGraphX Developer Kit, Release VI: `Autodocs/cybergraphics.doc` | `https://aminet.net/package/dev/misc/CGraphX-DevKit` | 2026-10-11; SHA-256 `dd2610649a692863dc27bbce595520b0ee269a03e03f73a8858396127df0fb0c` |
| `gfx-autodocs` | `graphics.library` autodocs, a third-party mirror and not the NDK itself | `https://d0.se/autodocs/graphics.library/` | 2026-10-11 |
