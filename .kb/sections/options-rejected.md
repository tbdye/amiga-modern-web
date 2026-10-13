# Options and rejections

Scope: the alternatives to the design under study, why each lost, stays a fallback or is not under study, and dead ends; no ranking or case for the design.
Status: draft

## Options compared

Qualitative columns only [G]; firmware-rewrite cost per [D] DEC-012.
[D] DEC-008 keeps the FPGA, module and board open, so "Rejected" marks only options a decision rules out; the rest are "Not under study".
[G] V-tracked's properties: the monitor only ever sees the Zynq's clock; any SoC with an HDMI output works; no PCIe link is needed; the line FIFO adds microseconds (4 lines, about 59 µs at 1080p); and the firmware, RTL and drivers carry over without a rewrite.

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
- **Remote rendering with lossless tiles or display lists** [G]: every DOM change pays a network round trip, and the A9 has no GPU; retired with the networked-box design, the browser chip sitting inside the Amiga or next to it [D] DEC-003.
- **Zorro III DMA as the main link** [G]: below a 720p60 surface, and it leaves Zorro II out.
  [F] As wired, neither the ZZ9000 nor the Replica can run a master's cycle by the specification (`topics/replica-interconnect.md`, "Zorro bus mastering").
- **A SoC module beside an unchanged Z-7020 over Ethernet** [G]: the same round trip on one PCB, with no gain in feel.
- **The SoC doing capture itself, with a CPLD for Zorro** [R]: no app SoC exposes a low-latency slave bus for Zorro RTG, so the CPLD grows into an FPGA and native video runs through SoC Linux.
- **Jetson Orin** [R]: Chromium GPU acceleration on L4T is unproven and the stack is proprietary; revisit if that changes.
- **A direct parallel video output from the SoC instead of a receiver**: it does not generalise.
  [R] RK3588's parallel output is BT.1120, YCbCr 4:2:2, which breaks lossless text.
  [F] The CM5's 24-bit DPI takes GPIO0-27, every I2S pin among them (`cm5-ds` p12-13).
  [R] x86 parts have none.
  [G] An HDMI receiver works with any SoC.
- **Zynq UltraScale+ (P6)**: [R] a ZU+ module such as the Enclustra Mercury XU5 offers 92 HP (≤ 1.8 V) and 54 HD (≤ 3.3 V) I/O, with PCIe Gen2 ×4 on ZU2/ZU3 or Gen3 ×4 on ZU4EV/ZU5EV, which add a video codec unit; the vendor's datasheet would verify it.
  [G] Its 52-54 usable 3.3 V pins fall far short of the 88-91 that Zorro, capture and I2S need (`topics/zynq-pin-budget.md`), so it adds translators and their timing work.
  [R] A chip-down ZU2/ZU3 in SFVC784 may have about 96 HD pins, and whether HD banks offer the IOB input registers the capture and I2S inputs use (`sections/firmware-and-rtl.md`) is unverified; DS925 and UG571 would settle both.
  [R] Alone, its 4 × A53 at about 1.2-1.5 GHz is Raspberry Pi 3 class and its Mali-400 MP2 is GLES 2 class, often blocklisted for Chromium GPU raster, so it cannot host the browser.
- **Versal AI Edge Gen 2 (P7)** [R]: the only single chip with Zorro-capable fabric, an application CPU and a Chromium-capable GPU (Mali-G78AE), but silicon and module availability and the Chromium GPU driver are unproven; its XPIO banks reach only about 1.5 V and its 3.3 V HDIO count is unverified (K28).
- **The card's A9 rasterising Chromium display lists** [G]: it makes scrolling local, but needs a Chromium cc/Skia fork with a standing rebase cost and unproven A9 raster coverage, and every DOM change still round-trips; it went with the remote tier.
- **A downstream HDMI compositor card** [G]: a P8 variant, in which a SoC card takes the ZZ9000's HDMI in and composites Chromium into it; all Amiga video then passes through the card (at least a frame added, the display depending on the card) and there is no VGA path; it was the only option giving stock ZZ9000 owners full feel; out with P8 [D] DEC-013.
- **A second monitor** [G]: the browser would not be in Workbench.
- **A second Ethernet MAC (GEM1 over EMIO RGMII)** [G]: about 12-14 PL pins; the Replica has none free, and on a chip-down 7020 CLG484 with PL DDR it reaches or overflows the 150 HR left.
- **MIPI DSI or CSI into the Zynq** [R]: D-PHY needs a 1.2 V low-power receiver plus a high-speed receiver, which a 3.3 V bank shared with Zorro and HDMI cannot provide, and no pins are free; XAPP894 would verify the D-PHY levels.
- **The SoC as a USB device on the card's USB** [F]: the card's USB is a single-owner proxy aperture shared by the firmware and `zzusbhw.device` (`fw@bdfd8b0:docs/usb-proxy-protocol.md:L3`), the Poseidon stack's device, and the CM5's USB device mode is not officially documented (`cm5-ds` p10).
- **A PCIe-coupled SoC as a "coprocessor"** [G]: in topology there are two chips, but the link is a memory bus, not a network: no damage protocol, layer export, compression or A9 compositing budget.
- **Keeping the engine remote and forking Chromium** [G]: the large gain in feel comes from putting the engine next to the scanout; a fork on a remote path gains much less, and with the engine local, layer export is unnecessary.
- **A clock-switching genlock bench** [G]: under V-tracked no clock switch exists, so tracking is tested on existing hardware (R-TRIM, R-PLANE) and receiver interop at the desk, with R-RX optional.
- **Browser traffic through the Amiga's TCP/IP stack, or forwarded by the card's A9** [G]: not under study for the browser chip's network; reasons in `topics/network.md`, "Not under study".
- **The existing Replica with V input** [F]: the Replica connects all 125 PL pins of its module; 124 have on-board loads, and `Free7` (J2.62) reaches only expansion header J10.3 (`replica@96bdef0`, netlist, not public); a 7015 module adds 12 unconnected pins, so the free count is 12 plus `Free7` (header only) (`topics/zynq-pin-budget.md`); a 28-pin receiver input does not fit, and an 8-pin TMDS input on HR pins caps the pixel clock near 125 MHz on the −2 module, from the DDR LVDS receiver's 1250 Mb/s (950 at −1, about 95 MHz; `ds187` Table 50, p33), so 1080p60 does not fit on either grade, 720p60 would on either, and 1280×1024 at 60 Hz (108 MHz) would only on the −2, and it also needs EDID, HPD and DDC pins [G] (`topics/zynq-pin-budget.md`).

## DPI into the video-capture path

Rejected [D] DEC-005: feeding the SoC's parallel video into the capture input takes the place of native Amiga video capture.
Firmware-side facts that show it is not a drop-in input [F]:

- The capture front end samples 8-bit R, G and B into IOB registers (`fw@8778ef3:videocap_sampler.v:L558-560`), with per-build RGB modes that replicate nibbles on non-Z3 builds (`:L563-566`).
- The capture line is fixed at 1280 samples (`fw@8778ef3:videocap_writeback_layout.v:L16`).
- Capture writes into DDR through Zorro `m01` (`fw@8778ef3:mntzorro.v:L2042`).
- The PIP plane that could show it is YUV422 only (`fw@8778ef3:docs/native-p96-pip.md:L55-57`).

Replica-side facts:

- [F] Net ties NT1-NT32 join 32 nets of the video-slot output header J9 to the video-slot input header J8: 24 RGB nets reach the capture translators U8-U10, 3 (VVSYNC, VHSYNC, C28D) reach U7, another 74LVC8T245, 4 are audio nets (AUDFLTL/R, AUDRAWL/R), and NT30 joins GND to the slot's audio ground (`replica@96bdef0`, netlist, not public); so a source on J9 drives the Amiga's video nets [G].
- [F] U7-U10 (74LVC8T245) run their bus side at +5 V and their FPGA side at +3V3, with DIR tied low so the bus side is the input (`replica@96bdef0`, netlist), and the part's high-level input threshold for data inputs at 4.5-5.5 V is 0.7 × VCCI, 3.5 V at 5 V (`lvc8t245` §5.3 p7); so a 3.3 V DPI source would need 5 V drivers [G].
- Rejected likewise [D] DEC-005: a 2:1 bus switch selecting the video slot or a SoC header ahead of those translators, since native capture is lost while the SoC is selected.
- Where J8, J9 and the translators sit in the Replica's wiring: `topics/replica-interconnect.md`, "Video slot (J8, J9)".

## Dead ends

- [G] Showing the plane before the tracker locks: the picture rolls (`sections/display-coupling.md`).
- [G] MMCM phase-shift trim to speed acquisition: slower than the ±1-line cap.
- [G] The SoC placing its content at the current phase offset Φ, fed a new Φ every frame: it works for windows smaller than the screen but fails full-screen, where content crosses the SoC's 45-line vertical blanking (1125 − 1080 at 1080p60), and full-screen 1080p60 is the target [D] DEC-010.
- [G] The SoC timing its own modeset to land near the Zynq's phase: a 1080p60 line is 14.8 µs, so each 1 ms of software jitter leaves about 67 lines, over 1 s of acquisition at the ±1 cap, and when a stock driver completes a modeset is not controlled; f1 (about 1 frame after receiver lock) does better.
- [G] A partial BRAM line buffer to absorb phase: about 64 lines against a phase of up to 562.
- [G] An occlusion mask in BRAM: about 56 BRAM36 at 1080p of a 7015's 95.

## Prior approaches

Depth, with sources and lessons: `topics/prior-art.md`.

[R] Named for orientation only; verified rows are in `topics/prior-art.md`.

| Approach | What it does |
|---|---|
| Native Amiga browsers (NetSurf, AWeb, Voyager, IBrowse) | Render on the 68k; cannot run current JavaScript-heavy sites |
| Browservice, WRP | A modern browser elsewhere renders pages for a legacy browser to display |
| FrogFind | A server simplifies pages for vintage browsers |
| Opera Mini | A server lays pages out and sends a compact interactive snapshot |
| Carbonyl | A patched Chromium that renders to a terminal |
| A314 | A Raspberry Pi on the Amiga through shared memory, offering services |
| A2088/A2286 Bridgeboard | A PC on a Zorro card shown in an Amiga window |
