# Options and rejections

Scope: the alternatives to the design under study, why each lost, stays a fallback or is not under study, and dead ends; no ranking or case for the design.
Status: current

## Options compared

Qualitative columns only [G]; firmware-rewrite cost per [D] DEC-012.
[D] DEC-008 keeps the FPGA, module and board open, so "Rejected" marks only options a decision rules out; the rest are "Not under study".

| Option | Felt quality | Integration effort | Firmware-rewrite cost | DEC-005 / DEC-013 | Standing |
|---|---|---|---|---|---|
| P1: one card, V-tracked | The SoC's own display path, no added frames | High | None (stays Zynq-7000; PS7, plane, tracker and control-link additions) | Yes / yes, if monitors accept the trim (K49) | Under study |
| P2: Zynq card plus unmodified SBC, V-tracked | As P1 | Medium | None | Yes / yes (K49) | Under study |
| P3: one card, PCIe fetch, Zynq-7015 | As P1, with a late latch | High: Gen2 signal integrity; the OSR frame hand-off to the FPGA (cefclient has a Linux `OnAcceleratedPaint` reference at CEF `a875f407e36b`, `topics/cef-frame-path.md`) | None, plus PCIe endpoint, fetch and MSI | Yes / yes | Alternative if the SoC display path misses its targets |
| P4: redesigned Replica with on-board SoC | As P3 | High; needs a Replica PCB revision, outside this project | As P3 | Yes / yes | Open, PCIe only |
| P5: frame-buffered V | Adds up to 1 frame | High: ×16 PL DDR3 layout | None, plus a memory controller | Yes / yes | Fallback if K49 fails with no trim fix |
| P6: Zynq UltraScale+ chip-down | As P1 or P3 | Very high | **Full port** off the A9 | Yes / yes | Not under study: a full port for headroom that adds nothing felt [G] |
| P7: Versal AI Edge Gen 2, one chip | Unproven [R] | Extreme | Full port plus an unproven GPU stack [R] | Re-qualify / — | Not under study: silicon and Chromium GPU driver unproven [R] |
| P8: the SoC owns the display | Native video gains ≥ 1 frame [G] | Very high | **Full rewrite** of every ZZ9000 service on Linux | **No / no** | Rejected [D] DEC-013: a SoC reboot or hang would blank the monitor and drop native video |
| P9: non-AMD FPGA plus firmware CPU (e.g. Cyclone V SoC, Agilex 5 [R]) | As P1 if the FPGA owns scanout | Very high | **Full rewrite**: PL off Xilinx primitives and IP, the A9 firmware re-hosted | Yes / yes if it ports the tracker | Not under study: a full rewrite of the PL and firmware [G] |
| V-locked | — | — | — | Fails DEC-013 | Rejected [D] DEC-013 |
| External LAN browser box | Network round trip per interaction | Low | None | Yes / yes | Retired [D] DEC-003 |

## Why each pruned approach lost

- **A browser engine on the 68k, a fast 68k, or the card's A9** [G]: none is fast enough for a current browser engine.
- **Remote rendering with lossless tiles or display lists** [G]: every DOM change pays a network round trip, and the A9 has no GPU; superseded by an on-card browser chip [D] DEC-003.
- **Zorro III DMA as the main link** [G]: below a 720p60 surface, and it leaves Zorro II out.
- **A SoC module beside an unchanged Z-7020 over Ethernet** [G]: the same round trip on one PCB, with no gain in feel.
- **The SoC doing capture itself, with a CPLD for Zorro** [R]: no app SoC exposes a low-latency slave bus for Zorro RTG, so the CPLD grows into an FPGA and native video runs through SoC Linux.
- **Jetson Orin** [R]: Chromium GPU acceleration on L4T is unproven and the stack is proprietary; revisit if that changes.
- **The existing Replica with V input** [F]: the Replica connects all 125 PL pins of its module; 124 have on-board loads, and `Free7` (J2.62) reaches only expansion header J10.3 (`replica@96bdef0`, netlist, not public); a 7015 module adds 12 unconnected pins, so the free count is 12 plus `Free7` (header only) (`topics/zynq-pin-budget.md`); a 28-pin receiver input does not fit, and the 8-pin TMDS alternative caps near 720p on HR banks [G].

## DPI into the video-capture path

Rejected [D] DEC-005: feeding the SoC's parallel video into the capture input takes the place of native Amiga video capture.
Firmware-side facts that show it is not a drop-in input [F]:

- The capture front end samples 8-bit R, G and B into IOB registers (`fw@8778ef3:videocap_sampler.v:L558-560`), with per-build RGB modes that replicate nibbles on non-Z3 builds (`:L563-566`).
- The capture line is fixed at 1280 samples (`fw@8778ef3:videocap_writeback_layout.v:L16`).
- Capture writes into DDR through Zorro `m01` (`fw@8778ef3:mntzorro.v:L2042`).
- The PIP plane that could show it is YUV422 only (`fw@8778ef3:docs/native-p96-pip.md:L55-57`).

The Replica-side electrical points (video-slot net ties, translator input thresholds) wait for a re-derivation at the current Replica revision.

## Dead ends

- [G] Showing the plane before the tracker locks: the picture rolls (`sections/display-coupling.md`).
- [G] MMCM phase-shift trim to speed acquisition: slower than the ±1-line cap.
- [G] A partial BRAM line buffer to absorb phase: about 64 lines against a phase of up to 562.
- [G] An occlusion mask in BRAM: about 56 BRAM36 at 1080p of a 7015's 95.

## Prior approaches

[R] Named for orientation only; each is a landscape note, not verified here.

| Approach | What it does |
|---|---|
| Native Amiga browsers (NetSurf, AWeb, Voyager, IBrowse) | Render on the 68k; cannot run current JavaScript-heavy sites at speed |
| Browservice, WRP | A modern browser elsewhere renders pages for a legacy browser to display |
| FrogFind | A server simplifies pages for vintage browsers |
| Opera Mini | A server lays pages out and sends a compact interactive snapshot |
| Carbonyl | A patched Chromium that renders to a terminal |
| A314 | A Raspberry Pi on the Amiga through shared memory, offering services |
| A2088/A2286 Bridgeboard | A PC on a Zorro card shown in an Amiga window |
