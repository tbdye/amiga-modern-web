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
| Browser chip | RK3588, x86 or CM5; chosen by a full-screen 1080p60 pass bar, then integration, price, power | `sections/browser-chip.md` |
| Packaging | Open: one card; a Zynq card plus an unmodified SBC or mini PC; or a redesigned Replica [D] DEC-003 | `sections/zynq-and-board.md` |
| Safety | Nothing the SoC does can touch native capture, the doubler or scanout [D] DEC-005 | `topics/plane-safety.md` |

[G] The browser plane is planned for RTG modes up to 1920 wide, so the 2560×1440 RTG mode (`fw@8778ef3:os/zz_video_modes.c:L24`) gets none.
[F] The Linux ADV7611 driver caps input width at 1920 (`linux@6c377d19d4a5:adv7604.c:L798-803`).
[G] Here the A9 programs the receiver without Linux, so that cap points to the chip's limit rather than proving it; the ADV7611 hardware manual would settle it.

## Non-goals

- 3D acceleration and video decode as Amiga-side features [D] DEC-008.
- Compatibility with stock MNT ZZ9000 or Replica boards as a requirement [D] DEC-005.
- A compressed or remote-desktop video path [D] DEC-008.
- Board spins as a way to learn: a PCB designed here is the product [D] DEC-011.

## What is open

| Question | Where |
|---|---|
| Do monitors accept the frame-length trim? (the cheapest test of the design, runnable today) | K49; `sections/display-coupling.md`, "R-TRIM" |
| Which browser chip passes full-screen 1080p60? | K15, DC-B |
| Which Zynq part and package? | DC-C; `topics/zynq-pin-budget.md` |
| One card or a split? | DC-D |
| Does the DDR headroom allow the acquisition bridge (f1)? | K25 |
| Zorro and capture timing on a new board | K29; the leading board-level risk |
