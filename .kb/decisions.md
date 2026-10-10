# Decisions

Scope: the project's design decisions, restated as rules with reasons and consequences.
Status: current

Numbers are stable and never reused; gaps are entries that were never published.
A rule cited as `[D] DEC-n` elsewhere comes from the entry here.

## DEC-001: Keep the ZZ9000 module

Status: superseded by DEC-008.
Decided: 2026-10-04.

## DEC-002: The browser engine runs on a separate chip

Status: active.
Decided: 2026-10-04.
Rule: Chromium executes on its own application processor, and the Zynq is what shows its output to the Amiga user.
Why: the card's dual Cortex-A9 is far too slow for a current browser engine (`sections/firmware-and-rtl.md`, "Why the Zynq cannot host the browser").
Consequences: how the pixels get from that processor to the Zynq is the coupling question (`sections/display-coupling.md`).

## DEC-003: Browser chip placement, packaging and power

Status: active.
Decided: 2026-10-04; revised 2026-10-05.
Rule: the browser chip may live inside the Amiga or next to it; whether it shares a card with the Zynq is undecided.
Rule: its power can come from a spare drive lead off the machine's PSU, a floppy-type connector being the default, or from a dedicated supply; the Zorro slot's limits do not bind it.
Why: power and packaging are design variables, not constraints.
Consequences: an early design with the browser in a networked box on the LAN is retired.

## DEC-004: A direct link outside Zorro is in scope

Status: active.
Decided: 2026-10-04.
Rule: a connection between browser chip and Zynq that bypasses Zorro may be explored, within DEC-005.
Why: Zorro throughput, and on Zorro II the small PIP memory pool, cap what Zorro alone could carry (`sections/firmware-and-rtl.md`).

## DEC-005: Native video keeps working on the board we build

Status: active.
Decided: 2026-10-04; scope clarified 2026-10-05.
Rule: on any board this project produces, native capture, scan doubling and NTSC/PAL pass-through work in all modes, RTG included.
Rule: staying compatible with existing MNT ZZ9000 or Replica boards is a bonus, not a requirement.
Why: native video is the card's primary job; a browser feature may not cost it.
Consequences: the video-slot DPI input is rejected (`sections/options-rejected.md`); every browser-plane design carries the safety rules in `topics/plane-safety.md`; any board or module change re-runs a native-video regression.

## DEC-008: Uncompressed pixels; the FPGA and module choice is open

Status: active; supersedes DEC-001.
Decided: 2026-10-05.
Rule: no part of the design depends on a lossy video stream of the remote-desktop kind; showing the browser's pixels as an uncompressed framebuffer is fine.
Rule: module, FPGA and board are all still open.
Rule: Amiga-side 3D and video decode are not goals; decoding web video on the browser chip is unaffected.
Why: compressed streams bring latency and artifacts on text and UI.

## DEC-009: 1080p output is required

Status: active.
Decided: 2026-10-05.
Rule: 1080p on a 16:9 monitor is supported for RTG and for native pass-through alike.
Why: most current monitors are 16:9 at 1080p or above.
Consequences: any option that loses 1080p RTG or the centred-1080p native profiles is out (`topics/zynq-pin-budget.md`).

## DEC-010: Target experience is a full-screen 1080p60 browser

Status: active.
Decided: 2026-10-05.
Rule: the goal is a browser filling a 1080p screen at 60 frames per second.
Rule: RK3588, x86 and Raspberry Pi CM5 class chips remain in the running, to be settled on integration and price.
Why: maximising the browser on a 1080p Workbench is an expected use.
Consequences: a per-chip pass bar at full-screen 1080p60, with power as a further tie-breaker, is proposed, not decided [G] (DC-B; `sections/browser-chip.md`, "Pass criteria (DC-B)"); a chip below that bar may still serve users below 1080p [D] DEC-012.
Consequences: under PCIe the CM5's single Gen2 lane is too narrow for 1080p60 frames [G]; under V-tracked its limit is GPU headroom (K15).

## DEC-011: Design first

Status: active.
Decided: 2026-10-05.
Rule: answer questions by analysis and research; prototype or measure only where those cannot reach.
Why: design time costs less than iterative hardware spins.
Consequences: every unknown carries a class saying whether desk work, a tool, a vendor or a measurement settles it (`unknowns.md`).

## DEC-012: Aim high, within reason

Status: active.
Decided: 2026-10-05.
Rule: go for the strongest result that stays reasonable; a lower tier that still meets the goal is acceptable.
Rule: comparisons include, as a factor of its own, what porting the firmware to another architecture would cost.
Why: plenty of RTG users run below 1080p, so a CM5 limited there may still serve them.

## DEC-013: Everyday use never resyncs the monitor

Status: active.
Decided: 2026-10-05; exemptions confirmed 2026-10-10.
Rule: no ordinary browser action (open, close, resize, full screen) may cause the monitor to lose sync or go blank, and neither may the browser chip restarting or freezing.
Rule: events that already resync the monitor are exempt, and a resync then is acceptable: a screen-mode change the user asks for (for example a new Workbench resolution), an Amiga reboot, and a switch between a native screen and RTG.
Consequences: V-locked coupling is out, because the monitor's clock would depend on the browser chip.
Consequences: under V-tracked the open items are the tracker variant (K2) and whether monitors accept the frame-length trim (K49).

## DEC-014: Native Workbench look and feel

Status: active.
Decided: 2026-10-10.
Rule: browsing has a native look and feel on Workbench: the window chrome is Workbench's, dialogs are Workbench dialogs, and downloads go natively to the Amiga's file system.
Rule: the mechanisms that deliver it are not decided; any mechanism this KB describes is a proposal.
Consequences: CEF's dialog, file, JS-dialog, context-menu and download handlers are candidate hooks (K50; `sections/browser-chip.md`, "The Chromium host").
Consequences: the proposed mechanisms and the open items are listed in `topics/look-and-feel.md`.

## DEC-015: LCSC-sourced Zynq chips are acceptable for production

Status: active.
Decided: 2026-10-10.
Rule: Zynq-7000 chips bought through LCSC, which is not an AMD-authorized channel [R], are acceptable for production.
Consequences: chip supply no longer waits on an authorized-channel quote, so K24 is retired; part numbers and LCSC C-numbers are in `sections/sourcing.md`.
