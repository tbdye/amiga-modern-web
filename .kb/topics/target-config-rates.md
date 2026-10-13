# Rates on the target configuration

Scope: published measurements of how fast a 68k Amiga receives from the network and copies pixels into a graphics card, and the pixel rate derived from them for a 68060 at 50 MHz on Zorro III with a ZZ9000.
Status: current

- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it.
- Nothing here was measured by this project, and no program from a cited archive was run: every measurement is a third party's, on its machine, software and date.
- `[F]` opens what a source reports; `[G]` opens arithmetic or inference made here, shown beside it.
- Units: MB = 10^6 bytes; MiB = 2^20 bytes; Mpix = 10^6 pixels; a 16-bit pixel is 2 bytes, so 1 Mpix/s is 2 MB/s.
- Derived figures are stated for 50 MHz; a bracket that runs to another clock says so.
- Bus ceilings and scrolls done on the card are in `topics/bus-and-card-rates.md`; decode rates, on the 68k and on the card's ARM, in `topics/decode-rates.md`.

## At a glance

Each figure is `[G]`, derived under the heading named, where its conditions are.

| On a 68060 at 50 MHz, Zorro III, ZZ9000 | Figure | Heading |
|---|---|---|
| TCP receive through the ZZ9000, benchmark into memory, firmware later than release v2.8.1 | 2.6 to 2.9 MB/s | "Network receive" |
| Copy from memory into the card | 4.3 to 7.3 MB/s by the P96 call (firmware 1.5 to 1.9a); 5.3 and 5.8 MB/s on firmware 2.8 | "Copies into the card" |
| Uncompressed pixels from the network to the screen | 1.62 to 2.08 MB/s | "Pixel rate" |

## Network receive

The ZZ9000 and `anx` rows, the browser's download rate and the 997 KBytes/s are stated as rates into the Amiga; the sources of the other rows state no direction; method and stack are as each source states them.
`amigaorg-66041` is a forum thread, cited by reply number.

| Card (bus, link) | Machine, CPU | Stack | Rate | Method | Source |
|---|---|---|---|---|---|
| ZZ9000 (Zorro III, 100 Mb/s) | A3000, 68060 at 50 MHz | Not stated | [F] 20.6, then 21.4, then 21.7 Mbit/s over two driver changes; 21.6, then 23.1 with a read-ahead in the FPGA that is Zorro III only; 27.9 at 82 MHz | iperf TCP receive, the last three figures over 8 cold boots; firmware and drivers later than release v2.8.1, the first three figures on top of a driver priority change that `drivers` does not hold at `cb6a1c4` | `drivers` commits `6f45554`, `936b96d`, messages; `fw` commit `a30214c`, message |
| ZZ9000 | A4000, 68060, clock not stated | Roadshow | [F] 3-4 Mbit/s sustained with about 43% of frames dropped, before a receive-backlog change that is in release v2.8.1; the message puts Zorro-side reads at about 4 MB/s and gives no rate after the change | Not stated | `fw` commit `4b12ca4`, message; stack from `fw@4b12ca4:notes/zz9000net-rx-throughput.md:L13` |
| ZZ9000, driver `ZZ9000Net.device` 2.2 | A3000, 68030 at 25 MHz | AmiNetXDuo, whose README reports it | [F] 3.6 Mbit/s in | Not stated | `anx@9a6f6fc:README.md:L111` |
| X-Surf 100 (Zorro III, 100 Mb/s), driver `anxnet.device` | A3000, 68030 at 25 MHz | AmiNetXDuo | [F] 3.8 Mbit/s in | Not stated | `anx@9a6f6fc:README.md:L109` |
| X-Surf 100, driver `anxnet.device` | A3000, 68060 at 50 MHz | AmiNetXDuo | [F] 22.5 Mbit/s in with flow control on the switch port, 18.9 without | Not stated | `anx@9a6f6fc:README.md:L110` |
| X-Surf 100 | A3000T, WarpEngine 68040 at 40 MHz | Roadshow and AmiTCP Genesis, "about exactly as fast" | [F] "about 1.700 MByte/s" | "TCP transmission tests" on a local network, with NetIO ported and `tcpspeed` reworked (reply 10) | `amigaorg-66041` reply 2 (2013-10-03) |
| X-Surf 100 | CyberStorm Mk II, 68060 at 50 MHz | Not stated | [F] "about 2 MByte/s", reported second hand | Not stated | Same reply |
| X-Surf 100 | A3000, CyberStorm Mk III 68060 at 50 MHz | Miami; EasyNet; Roadshow | [F] 1.280; 2.185; 2.066 MB/s | `tcpspeed`, whose client receives 20 MB; which side the Amiga ran is not stated | Reply 56 (2013-11-14); machine in reply 3 |
| X-Surf 100 | Same machine, same day | EasyNet; Roadshow | [F] The IBrowse web browser downloading at 80,000; 350,000 characters a second, and over 800,000 with Roadshow after tuning | The browser's own download rate; what was downloaded is not stated | Replies 56, 60 |
| X-Surf 100 | Same machine, three weeks earlier | Miami; Roadshow demo; EasyNet | [F] 0.9; 1.2; 1.5 MB/s | FTP with a storage box on the local network | Reply 39 (2013-10-23) |
| X-Surf 100 | A4000, A3660 at 50 MHz, running from Zorro III memory (Fastlane Z3) | Genesis; Roadshow; Miami | [F] 849; 685; 422 "kb/s" | `tcpspeed` | Reply 75 (2016-11-15) |
| X-Surf 100 | Not stated | Not stated | [F] "Transfer rates of over 1600kBytes/s have been measured" | Not stated | `icomp-shop-xsurf100` |
| Ariadne (Zorro II, 10 Mb/s) | A3000T, WarpEngine 68040 at 40 MHz | Roadshow | [F] "able to receive 997 KBytes/s" | "sustained data transmission tests" | `roadshow` |
| Ariadne | A3000UX, 68060 at 50 MHz | Roadshow | [F] "more than 900 KByte/s" | Not stated | `amigaorg-66041` reply 77 (2016-11-16) |
| Ariadne II (Zorro II, 10 Mb/s) | A4000, CyberStorm PPC with a 68060 at 50 MHz | Miami 3.2b | [F] "around 470 kb/s" | FTP between the Amiga and a PC over a crossover cable | `aminet-rview:Ariadne` (1998-12-30) |
| Ariadne | "A4000/40" | AmiTCP/IP 4 | [F] "up to 430KB/s (peak)" | FTP with a Linux machine, 150 MB file | `aminet-rview:AmiTCP4.2` (1995-02-28) |
| A2065 in one machine, Ariadne in the other (both Zorro II, 10 Mb/s) | Two A3000s, 68030 at 25 MHz | AmiTCP/IP 4 | [F] "up to 300KB/s" by FTP; 360 KB/s by NFS | 150 MB file, so disk included | Same review |

- [G] The ZZ9000 figures divided by 8: 2.6 to 2.7 MB/s without the read-ahead and 2.9 with it at 50 MHz; 3.5 at 82 MHz; 0.45 on the 68030 at 25 MHz.
- [F] The release's own rate is not given: 20.6 was measured on top of a change to the driver process's priority that the message names, while the driver at `cb6a1c4` starts that process at priority 0 (`drivers` commit `6f45554`, message; `drivers@cb6a1c4:net/device.c:L502-503`).
- [F] The note that `4b12ca4` added gives its unit as kilobits a second: receive topping out at 3,000-4,000, falling to 2,500-3,500 on transfers of 800 kB or more, and transmit about 10,300 (`fw@4b12ca4:notes/zz9000net-rx-throughput.md:L13-17`).
- [G] Driver commits of the day before print "KB/s" beside the same magnitudes, about 7,600 falling to about 2,800 for receive and 10,170 and 9,749 for transmit, so they are read as kilobits a second, 0.35 MB/s of sustained receive; the first of those messages also writes a transfer size as "KB", so the reading rests on the magnitudes alone; the messages name no machine (`drivers` commits `f8ee04e`, `c45c415`, `224dde8`, messages).
- [G] The X-Surf 100 figures from `anx` are 0.48 MB/s on the 68030 and 2.8 and 2.4 MB/s on the 68060.
- [F] Of the 1.7 and 2 MB/s figures the same reply says that at these rates "your CPU load will be at 96%, if not higher"; a later reply calls 2.2 MB/s "the top end of the scale" for a 68060 (`amigaorg-66041` replies 2 and 58).
- [G] The 1.7 MB/s is a receive rate if it came from `tcpspeed`: those tests ran the Amiga as the client, and the tool's client receives; NetIO was also in use, and no reply says which tool gave the figure (`amigaorg-66041` reply 10; `aminet:comm/tcp/TcpSpeed`, readme).
- [G] `tcpspeed` moves a fixed amount of data and times it, with no file or display, so it is a memory sink; on the machine it put at 2.07 to 2.19 MB/s a real program got 3.7% (80,000 ÷ 2,185,000), 17% (350,000 ÷ 2,066,000) and 39% (800,000 ÷ 2,066,000), reading characters as bytes.
- [G] "kb/s" in reply 75 and in the Ariadne II review is read as kilobytes a second.
- [G] The 10 Mb/s Ariadne's 0.9 to 1.0 MB/s is 72 to 80% of its 1.25 MB/s wire rate, on a 68040 at 40 MHz and on a 68060 at 50 MHz alike; the X-Surf 100's 1.7 to 2.8 MB/s is 14 to 22% of 12.5 MB/s, and the processor is the stated limit for the 1.7 and 2 MB/s figures.
- [F] The X-Surf 100's maker says a Zorro III machine runs it "up to five times faster than Z2" (`icomp-shop-xsurf100`).
- [G] Every figure for a Zorro II card above is from an A3000 or an A4000, which are Zorro III machines.

## Copies into the card

What the two benchmark programs measure:

- [G] P96Speed 1.2: a `WritePixelArray8()` or `WriteChunkyPixels()` result is calls a second, each writing an 8-bit rectangle of 101 × 90 = 9,090 pixels at a random place on the test screen with multitasking off; this is read from the program's instructions and data, since its guide states no test size (`aminet:util/misc/P96Speed`, program file and `P96Speed.guide` L447-448).
- [R] Both this size and the scroll size in `topics/bus-and-card-rates.md` rest on Intuition's title-bar height being 10 for the 8-point font the program fixes, which makes the rectangle 100 − 10 rows high and puts the bar on rows 0 to 10; Intuition's documentation would verify it.
- [G] So a rate below is calls × 9,090; on an 8-bit screen a pixel is a byte, and each call's overhead outside the copy puts the true copy rate at or above the figure.
- [F] CgxBenchmark 1.3, whose banner prints "v1.1": "Raw transfer speed" gives two write rates per screen depth on a 640×480 screen, as longword writes over a 320×240 area with multitasking off, first of a counter held in a register and then of data copied from memory; its "MB/s" divides by 1,048,576 (`aminet:driver/video/CgxBenchmark`, `CgxBenchmark.c` L31, L169, L206-276).

`zz9000-bench` images are named `bench_gfx_<suffix>.png`; the suffix is given, and values were read by eye.
`Compare.dat` is the comparison database inside `aminet:util/misc/P96Speed` (1999), its entries from version 1.1 or later.

| Card, bus | Machine, CPU | Screen | Calls a second [F] | Rate [G] | Source |
|---|---|---|---|---|---|
| ZZ9000, Zorro III, firmware 1.5; 1.6.2; 1.7 | A4000, 68060 at 50 MHz | 640×480, 8-bit | 733; 795; 801 | 6.7; 7.2; 7.3 MB/s | `zz9000-bench` `1.6.2`, `1.7DMA` |
| ZZ9000, firmware 1.9a with driver 1.8 | A4000, 68060 at 50 MHz | 640×480, 8-bit | 471 | 4.3 MB/s | `zz9000-bench` `1.9a_640_480` |
| ZZ9000, "early" firmware 1.4 | A4000, 68060, clock shown as 0 MHz | 640×480, 8-bit | 319 | 2.9 MB/s | `zz9000-bench` `early1.4_1` |
| ZZ9000, firmware and driver 1.8 | A3000, 68040 at 25 MHz | 640×480, 8-bit | 344 | 3.1 MB/s | `zz9000-bench` `1.8DMA_640_480` |
| ZZ9000, firmware 1.13 | A4000, 68060 at 50 MHz | 1024×768 and 1920×1080, 16-bit | 134 | 1.2 Mpix/s = 2.4 MB/s, P96 converting 8-bit pens | `zz9000-bench` `1.13_1024_768`, `1.13_1920_1080` |
| ZZ9000, firmware 1.13 | A4000, 68060 at 50 MHz | 640×480 and 1280×1024, 32-bit | 128 | 1.2 Mpix/s = 4.7 MB/s, converting | `zz9000-bench` `1.13_640_480`, `1.13_1280_1024` |
| ZZ9000, firmware 1.9a with driver 1.8 | A4000, 68060 at 50 MHz | 1024×768, 16-bit; 1920×1080, 16-bit; 1280×1024, 32-bit | 124; 123; 129 | 1.13; 1.12; 1.17 Mpix/s, converting | `zz9000-bench` `1.9a_1024_768`, `1.9a_1920_1080`, `1.9a_1280_1024` |
| ZZ9000, firmware 1.8 | A3000, 68040 at 25 MHz | 1920×1080, 16-bit; 1280×1024, 32-bit | 104; 104 | 0.95 Mpix/s, converting | `zz9000-bench` `1.8DMA_1920_1080`, `1.8DMA_1280_1024` |
| Picasso IV, Zorro III | A4000, 68060 at 50 MHz, two machines | 640×480, 8-bit | 630; 635 | 5.7; 5.8 MB/s | `Compare.dat` |
| Picasso IV, Zorro III | A4000T, 68060 at 66 MHz | 640×480, 8-bit | 686 | 6.2 MB/s | `Compare.dat` |
| Picasso IV, Zorro III | A4000, 68060 at 50 MHz | 640×480, 8-bit | 888 | 8.1 MB/s | `zz9000-bench` `1.6.2` (result dated 2019-09-04) |
| Picasso IV, Zorro II | A500 tower, 68060 at 50 MHz | 640×480, 8-bit | 337 | 3.1 MB/s | `Compare.dat` |
| Picasso II or II+, Zorro II | A2000, 68030 at 25 MHz | 640×480, 8-bit | 222 | 2.0 MB/s | `Compare.dat` |
| CyberVision 64/3D on a Zorro II board | A1200 tower, Blizzard 1260, described as 75 MHz | 640×480, 8-bit | 192 | 1.7 MB/s | `aminet:util/moni/060_75MHz_Voodoo3` (2009) |
| AGA, no card | A4000, 68060 at 50 MHz | PAL high resolution | 120 | 1.1 Mpix/s | `Compare.dat` |
| Picasso IV, Zorro III | A4000, Apollo 4060 at 50 MHz, bus controller revision 11 | 720×480, 24-bit | "796 pix/ms", printed by P96Speed 0.14 | 0.80 Mpix/s, converting from 8-bit | `aminet:util/moni/p4_A4060`, `P96Speed.results` (1997) |

[F] The figures below were taken under PrismRTG, an RTG layer that takes the place of P96, on an A4000 with a 68060 whose clock is not stated and a ZZ9000 that its README lists with firmware 2.8 (`prism@d62ee32:README.md:L12-13, L22`; `docs/design.md:L1350`).

- [F] "CgxBenchmark 1.1 runs to the end here. Raw VRAM 6.2 / 5.5 MB/s." (`prism@d62ee32:docs/design.md:L1358`).
- [G] Both are 68k-to-card write rates, 6.5 and 5.8 MB/s (× 1.048576); that 6.5 is the register column and 5.8 the copy from memory follows the program's column order, and neither that order nor the screen depth is stated.
- [F] Frames of 320×240 a second through its pixel-array call: 8-bit to an 8-bit screen 68.7, 8-bit to 16-bit 28.0, ARGB to 16-bit 13.5, ARGB to 32-bit 13.1 (`prism@d62ee32:docs/design.md:L1363-1368`).
- [G] 68.7 × 76,800 = 5.3 MB/s into the card for the same-format copy; 13.5 × 76,800 × 2 = 2.1 MB/s of screen pixels for the 32-bit to 16-bit conversion.

What the table shows:

- [G] The P96Speed runs on the ZZ9000 are on firmware 1.4 to 1.13, not the 2.8 line, and the 8-bit same-format call stands in for a 16-bit same-format write, which no run measured.
- [F] The page dates the firmware 1.4a release to 2019-09-30 and gives no date for the 1.13 runs (`zz9000-bench`).
- [G] On a 68060 at 50 MHz the Picasso IV's 5.7 to 8.1 MB/s and the ZZ9000's 4.3 to 7.3 MB/s overlap; the ZZ9000's figure varies 1.7 times across firmware 1.5 to 1.9a (801 ÷ 471).
- [G] Like for like, the converting call is 3.65 to 3.83 times slower in pixels than the same-format call on firmware 1.9a at 50 MHz (471 ÷ 129, 471 ÷ 123), and 3.31 times on the 68040 at 25 MHz (344 ÷ 104).
- [G] The converting rate is the same on 16-bit and 32-bit screens and across firmware 1.8 to 1.13, though a 32-bit screen takes twice the bytes, so it is a per-pixel processor cost, 41 to 45 clock cycles a pixel at 50 MHz (50,000,000 ÷ 1,218,060 and ÷ 1,118,070), not a bus limit.
- [G] That cost is the 8-bit palette path, since the call writes pen numbers; it is not the conversion a 16-bit or 24-bit source would need.

## Pixel rate

- [G] The pixel rate is the MB/s of 16-bit pixels that reach the screen when the 68k receives them from the network and then copies them into the card, one step after the other: 1 ÷ (1/receive + 1/copy).
- [G] On the target configuration, uncompressed: 1 ÷ (1/2.6 + 1/4.3) = 1.62 MB/s to 1 ÷ (1/2.9 + 1/7.3) = 2.08 MB/s, slow inputs paired with slow and fast with fast.
- [G] Its inputs are the ZZ9000's receive at 50 MHz ("Network receive") and the P96 copies on firmware 1.5 to 1.9a ("Copies into the card").
- [G] With the copies measured on firmware 2.8 instead: 1 ÷ (1/2.6 + 1/5.3) = 1.74 MB/s to 1 ÷ (1/2.9 + 1/5.8) = 1.93 MB/s.
- [G] The bracket that runs to 82 MHz is 1.62 to 2.37 MB/s: its top, 1 ÷ (1/3.5 + 1/7.3), takes the receive figure at 82 MHz.
- [G] The inputs carry their conditions: receive is a benchmark into memory on an A3000 with firmware later than the release, the copies are A4000s with an 8-bit screen standing in for a 16-bit one, and no source measures one program doing both.
- [G] The sum takes the 68k as the limit while receiving, which a source states for the X-Surf 100 and is assumed for the ZZ9000; a 10 Mb/s card gives the same 0.9 to 1.0 MB/s on a 68040 at 40 MHz and a 68060 at 50 MHz, so there the link may be the limit.
- [G] Where the 68k also decodes: 1 ÷ (1/(ratio × receive) + 1/decode + 1/copy), ratio being the compression against 16-bit pixels; this beats the uncompressed rate only if decode > receive × ratio ÷ (ratio − 1).
- [G] For JPEG decoded on the 68k, the slow end takes the 2.1 MB/s converting copy ("Copies into the card") in place of the copy rate, and the fast end takes the decoder to write the screen's format at no added cost, so it is a best case.
- [G] Where the card decodes, time is summed for each case: compressed bytes ÷ the uncompressed pixel rate, since they take the same path, plus pixels ÷ the card's decode rate, plus the calls.

## Not established

"Not found" means absent from Aminet (the first results page of each search), one forum thread and a few maker, vendor and review pages; other Amiga forums and magazine archives were not searched.

- The receive rate of the released firmware and drivers through a ZZ9000, and any rate on an A4000 after the change of April 2026: no source gives either; a published iperf figure would settle each.
- A same-format 16-bit write into a ZZ9000, through P96 or on the firmware 2.8 line: every P96 figure is an 8-bit screen; a published run at 16-bit depth would settle it.
- Which of 6.5 and 5.8 MB/s is the register write, and at which screen depth: the benchmark's own output for that run would settle it.
- The rate at which the system converts a 16-bit or 24-bit source for a screen of another format under P96: only the 8-bit palette path and one PrismRTG figure are published.
- What a real program that receives and draws achieves: the figures are benchmark sinks and one browser's download rate; only a measurement on a machine would show it.
- TCP on a Zorro II machine, through a 100 Mb/s card in Zorro II mode, with a 68040 at 25 MHz on a current stack, with TLS, or through a USB Ethernet adapter: not found.
- P96Speed or CgxBenchmark results for the CyberVision 64, Retina, Merlin or Piccolo cards, or for any card but the ZZ9000 at 16-bit depth: not found.

## Sources

`aminet`, `aminet-rview`, `zz9000-bench`, `fw` and `drivers` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `amigaorg-66041` | Forum thread on TCP/IP stacks for the X-Surf 100 | `https://forum.amiga.org/index.php?topic=66041.0` | 2026-10-11 |
| `icomp-shop-xsurf100` | The maker's product page for the X-Surf 100 | `https://shop.icomp.de/index.php/en/shop/product/x-surf-100.html` | 2026-10-11 |
| `roadshow` | Roadshow's home page | `http://roadshow.apc-tcp.de/index-en.php` | 2026-10-11 |
| `anx` | AmiNetXDuo | `github.com/tinic/AmiNetXDuo` | `9a6f6fc` |
| `prism` | PrismRTG | `github.com/lainejones/PrismRTG` | `d62ee32` |
