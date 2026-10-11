# PCIe path

Scope: the PCIe plane sources (fetch and copy), kept as the alternative if the SoC's own display path misses its targets: link load, copy time, outstanding reads, the fetch FIFO, flips and input, reference clock, pin budgets, remedies and pass thresholds.
Status: draft

[G] This path is live only while DC-A keeps PCIe (`unknowns.md`, "PCIe path"); the CEF side is in `topics/cef-frame-path.md` and the safety rules in `topics/plane-safety.md`.

## Fetch and copy

[G] One plane engine serves both, with two source addresses: a PIP-style line fetcher reads SoC memory through the PCIe bridge's AXI window (fetch), or Zynq DDR over an HP port (copy).

| Source | What happens [G] | Gains [G] | Costs [G] |
|---|---|---|---|
| Fetch (preferred [G]) | The FPGA reads each plane line from the SoC's front buffer into a few-line FIFO at scanout | No copy time; a late latch for free, since the front-buffer address is latched at vblank; no plane traffic in Zynq DDR; an underrun hits only plane pixels | The link carries the active-line rate all the time; read latency must stay bounded under GPU load (K11); an underrun policy |
| Copy (fallback) | The FPGA pulls each frame's damage into a dedicated Zynq DDR plane region (SR3), and the plane scans it out | Tolerates any link jitter: a stalled SoC leaves the last complete frame on screen | Plane write and read in Zynq DDR, about 1 GB/s at 1080p60 and 32 bpp (K25); copy time per frame |

[R] A 7-series endpoint reads root-complex memory by mastering through the AXI-PCIe bridge's AXI slave port, or through the DMA subsystem's host-to-card channel, as an NVMe drive does; the PG055 and PG195 product guides would verify it.

## Link load

[G] Fetch, full-width plane at 32 bpp, CEA-861 timing, about 15% read overhead (K9), against about 400 MB/s usable per Gen2 lane [R] (basis in `sections/browser-chip.md`, "Candidates"):

| Mode | Line average | With overhead | Gen2 ×1 | ×2 | ×4 |
|---|---|---|---|---|---|
| 720p60 (74.25 MHz, 1650-pixel line) | 230 MB/s | ~265 MB/s | 66% | 33% | 17% |
| 1080p60 (148.5 MHz, 2200-pixel line) | 518 MB/s | ~600 MB/s | Exceeds | 75% | 37% |

- [G] If the ~400 MB/s already includes the read overhead, the overhead is counted twice and 1080p60 on ×2 is about 65%.
- [G] Fetching 24 bpp packed cuts the load by 25%: 1080p60 becomes about 450 MB/s, still over ×1, and ×2 drops to 56%.
- [G] The fetch load is constant whatever the damage, and scales with plane width.

## Copy time per frame

[G] Full frames at 32 bpp, link rates as above:

| Link | Usable | 720p (3.69 MB) | 1080p (8.29 MB) |
|---|---|---|---|
| Gen2 ×1 (the CM5's link) | ~400 MB/s [R] | 9.2 ms, 0.55 frame | 20.7 ms, 1.24 frames |
| Gen2 ×2 | ~800 MB/s | 4.6 ms, 0.28 frame | 10.4 ms, 0.62 frame |
| Gen2 ×4 | ~1.6 GB/s | 2.3 ms, 0.14 frame | 5.2 ms, 0.31 frame |

[G] Where the copy takes more than half a frame (×1 at 720p, ×2 at 1080p), copies must be damage-only or overlapped with rendering; on ×1 at 1080p a full copy takes 1.24 frames, so it cannot complete within a frame.

## Outstanding reads

- [G] Sustained fetch throughput is at most the bytes in flight divided by the read latency (Little's law): 32 tags × 512 B = 16 KB in flight sustains 600 MB/s only while latency stays under about 27 µs.
- [R] So the PCIe IP's tag limit could bind before link width does; the AXI-PCIe bridge (PG055) and the DMA/bridge subsystem (PG195) differ in tag depth, which their product guides would settle (K10).

## The fetch FIFO and underruns

- [G] 4 lines at 1080p and 32 bpp is 4 × 7,680 B, about 59 µs of scanout and about 8 BRAM36; its depth is sized against the read-latency tail (K11).
- [G] A 4-line FIFO banks almost nothing across vblank, so the link must sustain the line average, not the frame average (`sections/browser-chip.md`, "Candidates").
- [G] Proposed underrun policy: the rest of that plane line shows the RTG pixels beneath, where the 68k client paints a neutral fill; underruns are counted, and repeated underruns trip the frame watchdog, which disables the plane (SR4, SR5, SR9).
- [G] The two BAR windows (SR1) end in PL BRAM, about 2-3 BRAM36 more; there is no fallback window into Zynq DDR (`topics/plane-safety.md`), so a 7015 build that cannot fit them fails its fit target (`sections/zynq-and-board.md`, "Fit").

## Flips and input

- [G] Flip: the SoC posts a BAR write of the new front-buffer address; the FPGA latches it at vblank and sends a vblank MSI, which frees the old buffer and paces `SendExternalBeginFrame` (`topics/cef-frame-path.md`).
- Open (K12): Bus Master Enable; IOMMU mapping; 64-bit outbound addressing for buffers above 4 GB; contiguous against scatter-gather buffers; cache maintenance before a flip, since PCIe is not coherent here; the CM5's inbound DMA window.
- [G] Input: the 68k writes input and commands into a ring in Zorro space, where latency starts; under PCIe the ring sits in the control BAR window in PL BRAM, the Zynq signals the SoC by MSI, and the SoC reads the ring within 1 ms.

## GTPs and reference clock

- [F] MYIR labels the 7015 module's MGTREFCLK0 (J2.135/137) "Pcie" and MGTREFCLK1 (J2.138/140) "Sfp" (`myir-7015-pinmap` p1), so a PCIe link uses MGTREFCLK0 [G].
- [R] A PCIe reference clock is 100 MHz; the PCI Express CEM specification would verify it.
- [R] 7-series has no SRIS, so a link over a cable needs a common reference clock, or spread spectrum off at the root complex (K10).
- [G] DisplayPort input and PCIe compete for the 7015's four GTPs; DP ×2 at HBR plus PCIe ×1 is plausible.
- [R] The 7-series DisplayPort RX core is licensed (`sections/firmware-and-rtl.md`, "Toolchain"); V-tracked needs neither it nor PCIe.

## Pin budget under PCIe

[G] A new board with the PCIe design: Zorro 59 + capture 26 + I2S 6 + 12-bit dual-edge HDMI 16 + PERST# 1 + 2-4 enables = 110-112 pins; 102-104 with an 8-pin TMDS output (groups in `topics/zynq-pin-budget.md`, "Fresh budget for a new board").

| Part and package, with PL DDR3 for copy | Result [G] |
|---|---|
| MYIR 7015 module (137 HR) | A 50-pin DDR3 bank at 1.5 V leaves 87: does not fit |
| 7015 chip-down CLG485 (150 HR) | 100 HR left: fits only with TMDS output and the slow controls on MIO, which loses 1080p (`topics/zynq-pin-budget.md`, "PL DDR on a 7015 loses 1080p") |
| 7030 SBG485 (50 HR + 100 HP) | DDR3 on HP leaves 50 HR + 50 HP: does not fit |
| 7030 FBG484 (100 HR + 63 HP) | DDR3 on HP leaves 13 HP, too few for a 28-pin 1.8 V HDMI bus, so 3.3 V needs 88 + 16 = 104 of 100 HR: 4 short; a translator moving I2S onto HP closes it |
| 7030 FBG676 (100 HR + 150 HP) | Fits: 94-96 of 100 HR at 3.3 V, HDMI as the 28-pin bus at 1.8 V on HP |

- [F] Package I/O is per `ds190` p4 (`sections/zynq-and-board.md`, "Parts").
- [G] The 88 assumes three timing-tolerant Zorro signals move to 1.8 V behind translators (`topics/zynq-pin-budget.md`, "Voltage: why Zorro and capture stay at 3.3 V").
- [G] Without PL DDR, the 7015 module fits the Replica's PL set plus PERST# and the enables, on the 12 pins the Replica leaves free.

## Remedies

- [G] Under fetch the Zynq DDR load is capture writeback plus RTG scanout, roughly today's 1080p workload, so PL DDR used only for the plane cannot fix a fetch-load failure; it matters only if fetch fails its latency tests and copy fails the DDR test.
- [G] If Zynq DDR fails under the fetch load, in order: on a board or module whose PS DDR runs below 1066 Mb/s, raise it to 1066, legal at every speed grade (`ds187` Table 18) and the shipping build's rate (`sections/zynq-and-board.md`, "Parts"), which restores parity rather than adding headroom; then move buffers into PL DDR on a new card, capture buffers first, since only PL masters touch them, and RTG buffers last, since the A9 draws on the framebuffer in software (`fill_rect`, `fw@bdfd8b0:os/gfx.h:L59-60`); or leave Zynq-7000 for a part with faster PS DDR, a full port (`sections/options-rejected.md`).
- [G] If copy fails the DDR test: fetch, if its latency tests pass; otherwise the V route.

## Pass thresholds [G]

| Measurement | Pass |
|---|---|
| SoC frame time with a PCIe frame path (R-SoC second pass, K14) | At 1280×720, and 1920×1080 on RK3588 and x86: p95 from BeginFrame to frame available ≤ 1 frame − T_hand for a compositor scroll and ≤ 2 frames − T_hand for a DOM change; ≤ 1% of frames missed over a 60 s scroll. T_hand is the hand-off to the plane: the copy time under copy, posting the flip (≤ 1 ms) under fetch |
| Zynq DDR headroom (R-DDR) | At 720p60 and at 1080p60, under the fetch load and the copy load, for 10 minutes: zero dropped capture lines, zero scanout underruns, DDR utilisation ≤ 75% of theoretical |
| Read latency (R-PCIe) | The p99.99 and worst observed latency fit the planned FIFO with 2× margin at the target mode and link width |
| Link on the built path | Gen2 trains at the target width with zero uncorrectable errors over 24 h under full load, replay and correctable counts flat; for fetch, 24 h at the target mode with zero plane underruns |
| Receiver input and line lock (R-RX, R-PLANE) | Zero dropped or duplicated frames over 10 minutes; phase within 2 lines; the receiver path bit-exact at 1080p60 |
