# Overview

Scope: the problem, the goal, the project's status, the brief, the design under study, non-goals and what is open.
Status: current

## Problem and goal

- [F] The ZZ9000's Zynq-7020 has a dual Cortex-A9 at 666 MHz and 1 GB of DDR3 (`fw@8778ef3:sdk/README.md:L17-18`).
- [G] No Amiga-side processor, the card's A9 included, runs current Chromium at usable speed; a Pi 4 class SoC is about the floor for current Chromium (Speedometer by board: `topics/prior-art.md`, "App SoC plus FPGA"); that is a limit of speed, for Chromium, and the features of the native Amiga browsers are stated apart (`topics/prior-art.md`, "Native Amiga browsers").
- Goal [D] DEC-020: "modern web" browsing, meaning that nearly any website works; how that is reached is open.
- [G] The design under study aims at a browser in a Workbench window or full screen, up to full-screen 1080p60; that is this design's target, not a requirement (DEC-010).

## Status

- Design stage only: nothing has been built, and there is no code in this repository.
- Decisions so far: `decisions.md`.
- Every open question, with what settles it: `unknowns.md`.

## The brief

- [D] DEC-020: by "modern web" the project means that nearly any website works; no design and no engine is fixed.
- [D] DEC-022: approaches are preferred in this order: an acceptable software solution, then a co-processor board if the software needs one, then a full card such as the design under study; none is chosen, and something that existing cards can use is preferred, not required.
- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it; no minimum is named.
- [D] DEC-036: that configuration should support video with synchronised audio.
- [D] DEC-037: needing a second computer is acceptable, and so is a co-processor board; the Amiga must keep a TCP/IP address of its own.

## The design under study

One proposal, not the project's settled design [D] DEC-020; this section describes it.
[G] A Zynq-7000 does all a ZZ9000 with its audio add-on does today (RTG, native capture, scan doubler, audio, Ethernet) and drives the monitor's HDMI.
[D] DEC-002: in this design a separate browser chip runs Chromium.
[D] DEC-010: in this design RK3588, x86 and Raspberry Pi CM5 class chips remain candidates.
[G] Its rendered frames reach the Zynq uncompressed; that is a property of this design, which no decision requires (DEC-008).
[G] The Zynq composites them into the browser's Workbench window or across the full screen.

| Element | Under study [G] | Detail |
|---|---|---|
| Coupling | V-tracked: the SoC's HDMI into a receiver chip; the Zynq trims its own frame length by ±1 line per frame to follow it | `sections/display-coupling.md` |
| Zynq | Zynq-7000 family, so firmware, RTL and drivers carry over | `sections/zynq-and-board.md` |
| Browser chip | RK3588, x86 or CM5, settled on integration and price [D] DEC-010; full-screen 1080p60 is the design's target, not a bar a chip must clear (DC-B), and a lower tier below 1080p is acceptable [D] DEC-012 | `sections/browser-chip.md` |
| Packaging | Open: one card; a Zynq card plus an unmodified SBC or mini PC; or a redesigned Replica [D] DEC-003 | `sections/zynq-and-board.md` |
| Safety | Nothing the SoC does can touch native capture, the doubler or scanout [D] DEC-005 | `topics/plane-safety.md` |

[G] The browser plane is planned for RTG modes up to 1920 wide, so the 2560×1440 RTG mode (`fw@8778ef3:os/zz_video_modes.c:L24`) gets none.
[F] The Linux ADV7611 driver caps input width at 1920 (`linux@6c377d19d4a5:adv7604.c:L798-803`).
[F] The ADV7611's TMDS clock is 165 MHz maximum (`adv7611` p1), and its LLC range is 13.5-165 MHz, with the maximum limited to the 8-bit UXGA 60 Hz clock (`adv7611` Table 2 and note 1, p5).
[R] VESA UXGA 60 Hz is 162 MHz; the VESA DMT standard would verify it.
[F] The Zynq's 1080p60 runs at 148.57 MHz and its 1600×1200 at 161.54 MHz (`fw@8778ef3:os/zz_video_modes.c:L18, L23`), both under that clock; so the 1920 cap is the Linux driver's, not the chip's clock [G].
[G] The 1600×1200 preset is still outside the Zynq's timed 150 MHz pixel clock and the datasheet's PLL range (`sections/firmware-and-rtl.md`, "Anchors for a browser plane").
[F] The Zynq's 2560×1440 runs at 30 Hz, 146.43 MHz (`fw@8778ef3:os/zz_video_modes.c:L24`), also under the clock, but a 2560-pixel line is outside the datasheet's documented formats [R]; the ADV7611 hardware manual would verify it.

## Non-goals

- 3D acceleration and video decode as Amiga-side features [D] DEC-008.
- Board spins as a way to learn [D] DEC-011.
- Throwaway scaffolding: a test rig exists only where it settles a measurement (class d) unknown more cheaply than anything else, and is never a board designed here [G] (follows from DEC-011).

## What is open

| Question | Where |
|---|---|
| Which approach is taken, whether any new hardware is built, and which computer runs the engine | `decisions.md` (DEC-020, DEC-022) |
| Do monitors accept the frame-length trim? Only hardware can show it | K49; `sections/display-coupling.md`, "R-TRIM" |
| Which browser chip, and how near each comes to the design's full-screen 1080p60 target | K15, DC-B |
| Which Zynq part and package? | DC-C; `topics/zynq-pin-budget.md` |
| One card or a split? | DC-D |
| Does the DDR headroom allow the acquisition bridge (f1)? | K25 |
| Zorro and capture timing on a new board | K29; the leading board-level risk |
| Is there a path for owners of stock ZZ9000 boards? | K54 |
| How would the feature ship in the firmware? | K56 |

[G] The design's top risk is monitor acceptance of the trim (K49, `topics/monitor-trim.md`); K29 is the top risk among board-level items, which is a different class.

## Faults found at acceptance

[G] A firmware, PL or SoC-software fault is fixed in place; a board-level fault (pin plan, signal integrity, power, translator timing, back-feed) means a respin, so the board-level unknowns are settled before the design freezes (`unknowns.md`, "Freeze criteria").

## Who decides

| Change | Decided by [G] |
|---|---|
| This project's design (`decisions.md`) | The project maintainer, through issues and pull requests here (`CONTRIBUTING.md`) |
| ZZ9000 firmware or drivers | Their upstream maintainers, through those repositories' reviews |
| The Replica board | The Replica project, outside this repository |

## Licences

- [F] The ZZ9000 firmware and drivers are GPL-3.0-or-later (`fw@bdfd8b0:README.md:L677-681`; `drivers@ad9606b:README.md:L580-584`); a few firmware files carry GPL-2.0+, GPL-2.0 or MIT notices instead (`fw@bdfd8b0`, `SPDX-License-Identifier` lines).
- [F] CEF is under a BSD-style licence (`cef@a875f407e36b:LICENSE.txt:L1-29`); Chromium is too [R], which its `LICENSE` file would verify.
- Open: this repository's licence (`CONTRIBUTING.md`, "Licence"), with the project not planned as closed-source [D] DEC-019; Amiga fonts in Chromium (K40); whether the ADV7611 hardware manual, which receiver set-up needs, is freely available [R].
