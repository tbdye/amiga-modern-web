# Bus ceilings and scrolls on the card

Scope: what bounds drawing on a Zorro graphics card: the Zorro II and Zorro III ceilings for pixels that cross the bus, published read and write cycles by machine, and published times for scrolls that a card does itself.
Status: current

- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it.
- Nothing here was measured by this project, and no program from a cited archive was run: every measurement is a third party's, on its machine, software and date.
- `[F]` opens what a source reports; `[G]` opens arithmetic or inference made here, shown beside it.
- Units: MB = 10^6 bytes; MiB = 2^20 bytes.
- Receive, copy and pixel rates are in `topics/target-config-rates.md`; decode rates in `topics/decode-rates.md`.
- `zz9000-bench` images are named `bench_gfx_<suffix>.png`, and their values were read by eye; `Compare.dat` is the comparison database inside `aminet:util/misc/P96Speed` (1999).

## Bus ceilings

Zorro II:

- [F] The bus is 16 bits wide, and its minimum cycle is four clocks of 7.16 MHz, 7.09 MHz on a PAL machine (`zorro3` §2.2 p23, §2.3.2 p25, §3.1.1 p32).
- [G] 4 ÷ 7.16 MHz = 559 ns a cycle, and 2 bytes ÷ 559 ns = 3.58 MB/s at most (3.55 on a PAL machine, 2 bytes ÷ (4 ÷ 7.09 MHz)), for any card, before the 68k's own copy loop.
- [F] A maker's specification for the EGS Spectrum 28/24 gives "Zorro II - 3.5 MB/Sec; Zorro III - 12.0 MB/Sec" (`aminet-rview:EGSSpectrum_2`, 1993-10-13).
- [G] The fastest published Zorro II copy, 337 × 9,090 = 3.06 MB/s on a 68060, is 86% of the ceiling (3.06 ÷ 3.58; `topics/target-config-rates.md`, "Copies into the card").

Zorro III:

- [F] The specification sets no rate: bus speed depends on the master and the slave of each cycle (`zorro3` §3.1 p31).
- [F] `bustest` times long runs of longword and `movem` moves on a memory region, with other tasks locked out, and reports 10^6 bytes a second (`aminet:util/moni/bustest`, readme, 1997).
- [G] Its write test moves a register to memory and its read test memory to a register, so a write figure is a write-only loop with no source read; this is read from the program file, which was not run.

| Region | Machine, CPU, bus controller | Longword write | Longword read | Source |
|---|---|---|---|---|
| Memory at `0x41000000`, taken to be the Picasso IV's frame buffer | A4000, Apollo 4060 (68060 at 50 MHz), revision 11 | [F] 418.0 ns = 9.6 MB/s; `movem` 9.6 | [F] 1,022 ns = 3.9 MB/s | `aminet:util/moni/p4_A4060`, `BUSTEST_P4` (1997) |
| CyberVision 64 at `0x40000000` | A3000 (motherboard revision 9.3), CyberStorm 68040 at 40 MHz, revision 11 | [F] 538.7 ns = 7.4 MB/s | [F] 690.1 ns = 5.8 MB/s | `aminet-rview:CyberVision64` (1995-06-23; `bustest` 0.07) |
| A3000 motherboard fast memory | A3000, CyberStorm Mk II, 68060 at 50 MHz by the readme's text | [F] 511.8 ns = 7.8 MB/s | [F] 299.0 ns = 13.4 MB/s | `aminet:util/moni/bustest`, readme |
| Chip memory | Same A3000 | [F] 569.0 ns = 7.0 MB/s | [F] 1,051.8 ns = 3.8 MB/s | Same readme |
| The accelerator's own memory | Same A3000 | [F] 174.7 ns = 22.9 MB/s | [F] 121.7 ns = 32.9 MB/s | Same readme |
| ZZ9000 Ethernet receive window, firmware later than release v2.8.1 | A3000, 68060, clock not stated for these cycles | Not given | [F] 569 to 574 ns a single-beat longword, about 280 ns of it the card's DDR round trip; 452 ns with a read-ahead that serves this window alone | `fw` commit `a30214c`, message |
| ZZ9000 framebuffer window, a third-party firmware line | A4000, 68060 at 50 MHz | [F] about 9.6 MiB/s | [F] about 6.3 MiB/s | `xacp@cca1f3c:applications/benchmarks/ZZBenchGUI_readme_v1.3.md:L94-120, L187-215` |

- [G] The first region is inferred: the address lies inside the one 32 MiB Zorro III board in that package's board list, at `0x40000000`, and its readme lists a Picasso IV among the cards; the result file names no region.
- [G] The ZZ9000 reads are 4 ÷ 569 ns = 7.0 MB/s and 6.3 × 1.048576 = 6.6 MB/s; the write is 9.6 × 1.048576 = 10.1 MB/s, 397 ns a longword.
- [G] With the card's 280 ns removed, the A3000 of the 569 ns read would reach about 13.8 MB/s (4 ÷ 289 ns), near the 13.4 of the other A3000's motherboard memory in the table.
- [G] Write-only longword loops into a Zorro III graphics card therefore span 7.4 to 10.1 MB/s on three cards and three machines, and 6.5 on the ZZ9000 with firmware 2.8 (`topics/target-config-rates.md`, "Copies into the card"); they are ceilings for a copy.
- [G] On the one card with both figures the copy from memory is 11% below the register write (5.5 against 6.2), if the pair keeps the program's column order (same heading).
- [G] Reads from these cards are slower than writes: Picasso IV 3.9 against 9.6 MB/s, CyberVision 64 5.8 against 7.4, ZZ9000 6.6 against 10.1.
- [G] These are cycles the 68k drives; they do not measure a card that drives the bus itself.
- [F] The CyberVision 64's review says a revision 11 bus controller "is 'recommended' for optimum performance" (`aminet-rview:CyberVision64`).

Whole windows at the ceilings, 16 bits a pixel (halve for 32-bit, double for 8-bit); every cell is `[G]`, bytes ÷ rate:

| Window | Bytes a frame | Frames a second at the Zorro II ceiling, 3.58 MB/s | At 4 bytes ÷ 569 ns on Zorro III |
|---|---|---|---|
| 640×480 | 614,400 | 5.8 | 11.4 |
| 800×600 | 960,000 | 3.7 | 7.3 |
| 1024×768 | 1,572,864 | 2.3 | 4.5 |
| 1280×720 | 1,843,200 | 1.9 | 3.8 |
| 1920×1080 | 4,147,200 | 0.9 | 1.7 |

- [G] The Zorro III column applies the 569 ns read cycle of the ZZ9000's Ethernet receive window on one A3000, 7.03 MB/s, to framebuffer writes on any card; that rate is inside the published copies from memory (4.3 to 7.3 MB/s; `topics/target-config-rates.md`, "Copies into the card") and below the write-only loops above.
- [G] A 16-row strip 800 pixels wide is 25,600 bytes: about 140 a second at the Zorro II ceiling and 275 at 4 bytes ÷ 569 ns, so a scroll done on the card plus a strip costs far less than a repaint.

## Scrolls on the card

- [G] Each P96Speed `ScrollRaster()` call moves the full screen width below the title bar by one pixel, X sideways and Y vertically, so no pixel crosses the bus; this is read from the program's instructions, as its test sizes are (`topics/target-config-rates.md`, "Copies into the card").
- [G] Bytes a call = width × (height − 11) × bytes a pixel, the title bar taking rows 0 to 10 by the `[R]` rule stated there.
- [G] The last column scales the Y time by bytes to the 883,200 bytes of an 800×552, 16-bit move (an 800×600 window less a 48-row strip), taking time as proportional to bytes.

| Card, bus | Machine, CPU | Screen | Calls a second, X / Y [F] | Y call: time; bytes; rate [G] | Scaled [G] | Source |
|---|---|---|---|---|---|---|
| ZZ9000, firmware 1.13 | A4000, 68060 at 50 MHz | 1024×768, 16-bit | 129 / 320 | 3.1 ms; 1,550,336; 496 MB/s | 1.8 ms | `zz9000-bench` `1.13_1024_768` |
| ZZ9000, firmware 1.13 | A4000, 68060 at 50 MHz | 1920×1080, 16-bit | 50 / 114 | 8.8 ms; 4,104,960; 468 MB/s | 1.9 ms | `zz9000-bench` `1.13_1920_1080` |
| ZZ9000, firmware 1.13 | A4000, 68060 at 50 MHz | 640×480, 32-bit | 168 / 379 | 2.6 ms; 1,200,640; 455 MB/s | 1.9 ms | `zz9000-bench` `1.13_640_480` |
| ZZ9000, firmware 1.7 | A4000, 68060 at 50 MHz | 640×480, 8-bit | 707 / 2,110 | 0.47 ms; 300,160; 633 MB/s | 1.4 ms | `zz9000-bench` `1.7DMA` |
| ZZ9000, firmware 1.9a with driver 1.8 | A4000, 68060 at 50 MHz | 640×480, 8-bit | 636 / 1,717 | 0.58 ms; 300,160; 515 MB/s | 1.7 ms | `zz9000-bench` `1.9a_640_480` |
| ZZ9000, firmware 1.8 | A3000, 68040 at 25 MHz | 640×480, 8-bit | 558 / 1,289 | 0.78 ms; 300,160; 387 MB/s | 2.3 ms | `zz9000-bench` `1.8DMA_640_480` |
| ZZ9000, firmware 1.8 | A3000, 68040 at 25 MHz | 1920×1080, 16-bit | 49 / 112 | 8.9 ms; 4,104,960; 460 MB/s | 1.9 ms | `zz9000-bench` `1.8DMA_1920_1080` |
| Picasso IV, Zorro III | A4000, 68060 at 50 MHz | 640×480, 8-bit | 394 to 420 / 384 to 411 | 2.4 to 2.6 ms; 300,160; 115 to 123 MB/s | 7.2 to 7.7 ms | `Compare.dat`; `zz9000-bench` `1.6.2` |
| Picasso IV, Zorro II | A500 tower, 68060 at 50 MHz | 640×480, 8-bit | 163 / 154 | 6.5 ms; 300,160; 46 MB/s | 19 ms | `Compare.dat` |
| CyberVision 64/3D on a Zorro II board | A1200 tower, Blizzard 1260, described as 75 MHz | 640×480, 8-bit | 372 / 371 | 2.7 ms; 300,160; 111 MB/s | 7.9 ms | `aminet:util/moni/060_75MHz_Voodoo3` |
| Picasso II or II+, Zorro II | A2000, 68030 at 25 MHz | 640×480, 8-bit | 48 / 49 | 20.4 ms; 300,160; 14.7 MB/s | 60 ms | `Compare.dat` |
| AGA, no card | A4000, 68060 at 50 MHz | PAL high resolution | 6 / 7 | 143 ms a call | Not scaled | `Compare.dat` |

- [G] So a ZZ9000 moves an 800×600, 16-bit window's pixels vertically in 1.4 to 1.9 ms with a 68060 at 50 MHz; the 2.3 ms figure is the 68040 at 25 MHz.
- [G] Those times are scaled from whole-screen one-pixel scrolls on firmware 1.7 to 1.13, not measured at that size or on the 2.8 line.
- [G] The ZZ9000's sideways scroll runs at 0.33 to 0.44 of its vertical rate in every run of the table (707 ÷ 2,110 to 168 ÷ 379), so a sideways move takes 2.3 to 3 times as long.
- [G] At 1920×1080 the ZZ9000's time is the same on the 68040 at 25 MHz as on the 68060 at 50 MHz (112 against 114 calls), so the card sets it; at 640×480, 8-bit the 68040 run is slower (1,289 against 1,717 and 2,110), so the 68k side shows on small moves, and the firmware also differs between those runs.
- [G] For the older cards the scaling from an 8-bit scroll to a 16-bit move is untested.
- [F] The runs at 1280×1024, 32-bit show 41,430 and 54,362 scroll calls a second on firmware 1.13, 38,999 and 49,609 on 1.9a, and 22,601 and 40,814 on 1.8 (`zz9000-bench` `1.13_1280_1024`, `1.9a_1280_1024`, `1.8DMA_1280_1024`).
- [G] At 5.2 MB a call the first would be 280 GB/s, so the calls did no scroll at that size, and the three runs are left out.

## Not established

"Not found" means absent from Aminet (the first results page of each search) and a few maker, vendor and review pages; Amiga forums and magazine archives were not searched.

- A bus test on a machine with an earlier bus-controller revision, on an A3000 or A4000 with its stock processor card, or on any Zorro II card: not found; the Zorro II copy figures are the only published rates found for that bus.
- The rate of a card that drives the bus itself: not found; the cycles the 68k drives bound it and do not measure it.
- A write cycle into a ZZ9000 on the firmware the read cycle was measured on: not given; the write figures are from a third-party firmware line and from firmware 2.8.
- The ZZ9000's time for a window-sized move, and any whole-screen scroll figure on the 2.8 firmware line: only whole-screen one-pixel scrolls on firmware 1.7 to 1.13 are published.
- Whether an 8-bit scroll's time scales by bytes to a 16-bit move on the Picasso IV, CyberVision 64/3D or Picasso II: untested.

## Sources

`aminet`, `aminet-rview`, `zz9000-bench`, `fw`, `zorro3` and `xacp` are defined in `sources.md`.
