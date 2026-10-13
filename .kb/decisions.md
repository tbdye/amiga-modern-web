# Decisions

Scope: the project's design decisions, restated as rules with reasons and consequences.
Status: current

Numbers are stable and never reused; gaps are entries that were never published.
A rule cited as `[D] DEC-n` elsewhere comes from the entry here.

## DEC-001: Keep the ZZ9000 module

Status: superseded by DEC-008.
Decided: 2026-10-04.

## DEC-002: The design under study runs the browser engine on a separate chip

Status: active.
Decided: 2026-10-04; amended 2026-10-11.
Rule: in the design under study, Chromium executes on its own application processor, and the Zynq is what shows its output to the Amiga user.
Rule: that is the design's rule, not a settled choice of the project: no engine and no design is fixed (DEC-020).
Rule: whether a ZZ9000 is still what shows the engine's output is not decided; DEC-028 gives the ZZ9000's standing.
Why: the card's dual Cortex-A9 is far too slow for current Chromium, the engine this rule names (`sections/firmware-and-rtl.md`, "Why the Zynq cannot host the browser").
Consequences: how the pixels get from that processor to the Zynq is the coupling question (`sections/display-coupling.md`).

## DEC-003: Browser chip placement, packaging and power

Status: active.
Decided: 2026-10-04; revised 2026-10-05; amended 2026-10-11.
Rule: the browser chip may live inside the Amiga or next to it; whether it shares a card with the Zynq is undecided.
Rule: its power can come from a spare drive lead off the machine's PSU, a floppy-type connector being the default, or from a dedicated supply; the Zorro slot's limits do not bind it.
Rule: a networked browser computer is not ruled out, nor is any role chosen for it.
Why: power and packaging are design variables, not constraints.

## DEC-004: A direct link outside Zorro is in scope

Status: active.
Decided: 2026-10-04.
Rule: a connection between browser chip and Zynq that bypasses Zorro may be explored, within DEC-005.
Why: Zorro throughput, and on Zorro II the small PIP memory pool, cap what Zorro alone could carry (`sections/firmware-and-rtl.md`).

## DEC-005: Native video keeps working on the board we build

Status: active.
Decided: 2026-10-04; scope clarified 2026-10-05; amended 2026-10-11.
Rule: on any board this project produces, native capture, scan doubling and NTSC/PAL pass-through work in all modes, RTG included.
Rule: the project is not required to stay compatible with existing MNT ZZ9000 or Replica boards; DEC-022 holds the preference for something that existing cards can use.
Why: native video is the card's primary job; a browser feature may not cost it.
Consequences: the video-slot DPI input is rejected (`sections/options-rejected.md`); every browser-plane design carries the safety rules in `topics/plane-safety.md`; any board or module change re-runs a native-video regression.

## DEC-008: Compression may be explored; the FPGA and module choice is open

Status: active; supersedes DEC-001.
Decided: 2026-10-05; amended 2026-10-11.
Rule: compression of the browser's pixels may be explored and is not ruled out; none is chosen.
Rule: it is not decided whether text and user-interface areas have to be pixel-exact.
Rule: module, FPGA and board are all still open.
Rule: Amiga-side 3D and video decode are not goals; decoding web video on the browser chip is unaffected.

## DEC-009: 1080p output is required

Status: active.
Decided: 2026-10-05.
Rule: 1080p on a 16:9 monitor is supported for RTG and for native pass-through alike.
Why: most current monitors are 16:9 at 1080p or above.
Consequences: any option that loses 1080p RTG or the centred-1080p native profiles is out (`topics/zynq-pin-budget.md`).

## DEC-010: A full-screen 1080p60 browser is not required

Status: active.
Decided: 2026-10-05; amended 2026-10-11.
Rule: neither 60 frames per second (DEC-021) nor a browser filling a 1080p screen is required; no other rate or size replaces them.
Rule: in the design under study, RK3588, x86 and Raspberry Pi CM5 class chips remain in the running, to be settled on integration and price.
Consequences: in the design under study, per-chip criteria at full-screen 1080p60, with power as a further tie-breaker, are proposed, not decided [G] (DC-B; `sections/browser-chip.md`, "Pass criteria (DC-B)"); a chip that misses them may still serve users below 1080p [D] DEC-012.
Consequences: under PCIe the CM5's single Gen2 lane is too narrow for 1080p60 frames [G]; under V-tracked its limit is GPU headroom (K15).

## DEC-011: Design first

Status: active.
Decided: 2026-10-05; amended 2026-10-11.
Rule: answer questions by analysis and research; prototype or measure only where those cannot reach.
Rule: bench testing comes among the last things done, and only in support of analysis; no bench test is a given.
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
Rule: browsing looks and feels native on Workbench: the window chrome is Workbench's, dialogs are Workbench dialogs, and downloads go natively to the Amiga's file system.
Rule: the mechanisms that deliver it are not decided; any mechanism this KB describes is a proposal.
Consequences: CEF's dialog, file, JS-dialog, context-menu and download handlers are candidate hooks (K50; `sections/browser-chip.md`, "The Chromium host").
Consequences: the proposed mechanisms and the open items are listed in `topics/look-and-feel.md`.

## DEC-015: LCSC-sourced Zynq chips are acceptable for production

Status: active.
Decided: 2026-10-10.
Rule: production may use Zynq-7000 chips sourced from LCSC, a channel that AMD has not authorized [R].
Consequences: chip supply no longer waits on an authorized-channel quote, so K24 is retired; part numbers and LCSC C-numbers are in `sections/sourcing.md`.

## DEC-019: Not planned as closed-source; no licence is chosen

Status: active.
Decided: 2026-10-11.
Rule: the project is not planned as closed-source.
Rule: no licence is chosen.

## DEC-020: "Modern web" means nearly any website works; no design or engine is fixed

Status: active.
Decided: 2026-10-11.
Rule: by "modern web" the project means that nearly any website works.
Rule: how that is reached is open: the project is restricted neither to the design under study nor to Chromium, so no design and no engine is fixed.

## DEC-021: 60 frames per second is not a hard goal

Status: active.
Decided: 2026-10-11.
Rule: 60 frames per second is not a hard goal.
Rule: no rate is set in its place.

## DEC-022: Order of preference: software, a co-processor board, a full card

Status: active.
Decided: 2026-10-11.
Rule: approaches are preferred in this order: an acceptable software solution; then a co-processor board, if the software needs one; then a full card responsible for every part of the browser (the design under study is of this kind).
Rule: no approach is chosen.
Rule: something that existing cards can use, ZZ9000 and other RTG cards alike, is preferred; it is not required.
Consequences: [G] so whether any new hardware is built, and which computer runs the engine, are open (DEC-037).

## DEC-024: A PiStorm alone is not seen as a solution

Status: active.
Decided: 2026-10-11.
Rule: a PiStorm by itself is not seen as a solution.
Rule: a Raspberry Pi as a co-processor is a different case, the second approach of DEC-022, and is not chosen.

## DEC-027: Support is preferred over performance; no floor is set

Status: active.
Decided: 2026-10-11.
Rule: support that performs poorly is preferred over good performance without support.
Rule: no performance floor is set; DEC-033 gives a likely one for video.

## DEC-028: The ZZ9000 is the likely performance benchmark; P96 is raised, not adopted

Status: active.
Decided: 2026-10-11.
Rule: the ZZ9000 is likely the benchmark, and for performance only; DEC-035 names a whole configuration.
Rule: two things are raised, not adopted: P96 as what RTG cards have in common, and PrismRTG, an open-source alternative to P96.

## DEC-031: No single machine is named; the meaning of "supported" is open

Status: active.
Decided: 2026-10-11.
Rule: no single machine is named as the one the result is for.
Rule: what "supported" means is open; DEC-035 names a target configuration.

## DEC-032: Most use is expected at 1024×768 or below; no window size is set

Status: active.
Decided: 2026-10-11.
Rule: most use is expected at a browser window size of 1024×768 or below.
Rule: no size is set: neither a maximum, nor a required size, nor a size that a design is measured at.

## DEC-033: A likely floor for video: about 15 frames per second

Status: active.
Decided: 2026-10-11.
Rule: the likely floor for video is about 15 frames per second, at no stated picture size.
Rule: no floor is set for repainting, for scrolling or for key to screen.
Rule: it is not decided whether video below that figure rules an approach out or only leaves it without video.

## DEC-035: Target configuration: 68060 at 50 MHz, Zorro III, ZZ9000

Status: active.
Decided: 2026-10-11.
Rule: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it.
Rule: it is the configuration the project is thought to target, not a requirement; no minimum is named.
Consequences: the published rates for this configuration are in `topics/target-config-rates.md`, with bus ceilings in `topics/bus-and-card-rates.md` and decode rates in `topics/decode-rates.md`.

## DEC-036: Video with synchronised audio on the target configuration

Status: active.
Decided: 2026-10-11.
Rule: the target configuration of DEC-035 should support video with synchronised audio.
Rule: no tolerance for the synchronisation is set, nor a picture size or frame rate; where the sound plays, and what other Amigas must support, are not decided.

## DEC-037: Needing a second computer is acceptable; the Amiga keeps a TCP/IP address of its own

Status: active.
Decided: 2026-10-11.
Rule: needing a second computer is acceptable, and so is a co-processor board; no approach is chosen (DEC-022).
Rule: the Amiga keeps a TCP/IP address of its own; this is a requirement.

## DEC-042: New or existing Amiga program: an engineering choice

Status: active.
Decided: 2026-10-11.
Rule: whether the program on the Amiga is new or built on an existing one is an engineering choice.

## DEC-045: Less browser-engine work is better

Status: active.
Decided: 2026-10-11.
Rule: the less work on a browser engine the project carries, the better; this is a preference.
Rule: no engine is fixed (DEC-020).
