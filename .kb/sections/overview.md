# Overview

Scope: the problem, the goal, the project's status, the design under study, non-goals and what is open.
Status: current

## Problem and goal

- [F] The ZZ9000's Zynq-7020 has a dual Cortex-A9 at 666 MHz and 1 GB of DDR3 (`fw@8778ef3:sdk/README.md:L17-18`).
- [G] No Amiga-side processor, the card's A9 included, runs a current browser engine at usable speed; a Pi 4 class SoC is about the floor for current Chromium.
- Goal [D] DEC-008, DEC-010: modern web pages in a Workbench window or full screen, up to a full-screen 1080p60 browser, with text and UI pixel-exact (no compressed video stream).

## Status

- Design stage only: nothing has been built, and there is no code in this repository.
- Decisions so far: `decisions.md`.
- Every open question, with what settles it: `unknowns.md`.

## The design under study

[G] A Zynq-7000 does all a ZZ9000 does today (RTG, native capture, scan doubler, audio, Ethernet) and drives the monitor's HDMI.
A separate browser chip (RK3588, x86 or Raspberry Pi CM5 class) runs Chromium [D] DEC-002.
Chromium's rendered frames arrive at the Zynq without compression, and the Zynq composites them into the browser's Workbench window, or across the full screen [D] DEC-008.

| Element | Under study [G] | Detail |
|---|---|---|
| Coupling | V-tracked: the SoC's HDMI into a receiver chip; the Zynq trims its own frame length by ±1 line per frame to follow it | `sections/display-coupling.md` |
| Zynq | Zynq-7000 family, so firmware, RTL and drivers carry over | `sections/zynq-and-board.md` |
| Browser chip | RK3588, x86 or CM5, settled on integration and price [D] DEC-010; a full-screen 1080p60 pass bar is proposed (DC-B), and a lower tier below 1080p is acceptable [D] DEC-012 | `sections/browser-chip.md` |
| Packaging | Open: one card; a Zynq card plus an unmodified SBC or mini PC; or a redesigned Replica [D] DEC-003 | `sections/zynq-and-board.md` |
| Safety | Nothing the SoC does can touch native capture, the doubler or scanout [D] DEC-005 | `topics/plane-safety.md` |

[G] The browser plane is planned for RTG modes up to 1920 wide, so the 2560×1440 RTG mode (`fw@8778ef3:os/zz_video_modes.c:L24`) gets none.
[F] The Linux ADV7611 driver caps input width at 1920 (`linux@6c377d19d4a5:adv7604.c:L798-803`).
[F] The ADV7611's TMDS clock is 165 MHz maximum (`adv7611` p1), and its LLC range is 13.5-165 MHz, with the maximum limited to the 8-bit UXGA 60 Hz clock (`adv7611` Table 2 and note 1, p5).
[R] VESA UXGA 60 Hz is 162 MHz; the VESA DMT standard would verify it.
[F] The Zynq's 1080p60 runs at 148.57 MHz and its 1600×1200 at 161.54 MHz (`fw@8778ef3:os/zz_video_modes.c:L18, L23`), both under that clock; so the 1920 cap is the Linux driver's, not the chip's clock [G].
[F] The Zynq's 2560×1440 runs at 30 Hz, 146.43 MHz (`fw@8778ef3:os/zz_video_modes.c:L24`), also under the clock, but a 2560-pixel line is outside the datasheet's documented formats [R]; the ADV7611 hardware manual would verify it.

## Non-goals

- 3D acceleration and video decode as Amiga-side features [D] DEC-008.
- Compatibility with stock MNT ZZ9000 or Replica boards as a requirement [D] DEC-005.
- A compressed or remote-desktop video path [D] DEC-008.
- Board spins as a way to learn [D] DEC-011.

## What is open

| Question | Where |
|---|---|
| Do monitors accept the frame-length trim? (the cheapest test of the design, runnable today) | K49; `sections/display-coupling.md`, "R-TRIM" |
| Which browser chip passes full-screen 1080p60? | K15, DC-B |
| Which Zynq part and package? | DC-C; `topics/zynq-pin-budget.md` |
| One card or a split? | DC-D |
| Does the DDR headroom allow the acquisition bridge (f1)? | K25 |
| Zorro and capture timing on a new board | K29; the leading board-level risk |
