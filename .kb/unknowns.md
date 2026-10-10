# Unknowns, open decisions and risks

Scope: the K register of open questions with what settles each, the design decisions still open, freeze criteria, test methods and unresolved risks.
Status: draft

**Classes:** **a** desk (datasheets, manuals, source, published data); **b** tool, no hardware (Vivado, SI/SPICE, SigmaStudio, emulation); **c** vendor or third-party inquiry; **d** needs a physical measurement; **v** acceptance of the built board, not a design input.
"Gates" names the decision the item feeds (DC-A to DC-D below), or "design" or "freeze".
IDs are stable; K6, K43 and K44 were retired as moot or answered, and K24 by DEC-015.
[D] DEC-011: only the d rows need hardware before the design freezes.

## Coupling and display

| # | Unknown | Class | Settles it | Gates |
|---|---|---|---|---|
| K1 | Can the SoC lock its display to an external VSYNC? | a | DRM drivers (Rockchip VOP2, vc4, i915) and TRMs; expected unsupported [R] | DC-A |
| K2 | Tracker V variant: receiver anchor, ±1-line cap, engages at SoC boot, never hides RTG, nominal frames on unlock, keeps engagement on unchanged output timing (f5) | a + b | RTL reading of `video_source_sync.v`; its source-sync bench adapted to a receiver anchor; static timing; R-PLANE | DC-A |
| K3 | Line FIFO depth and phase bound | a | 0.54 lines per frame drift at 1080p, plus one line each of horizontal phase and quantisation: 4 lines [G]; outside the lock window the plane stays off (SR13, SR14) | DC-A |
| K4 | Receiver interop | a, else d | ADV7611 desk facts in `sections/browser-chip.md`; TFP401-class is DVI only, no EDID, no audio [R]; residual: R-RX | DC-A |
| K5 | The SoC emits each RTG mode at the Zynq's exact timing, within the ±1 cap (~0.09% at 1080p) | a | EDID DTDs carry the Zynq timings and stock KMS selects them; fixed EDID holds 7 DTDs + 3 DMT modes (`sections/display-coupling.md`); 720p preset moved near CEA (M/D/O 52/5/14 → 74.286 MHz [G]); readback on R-SoC | DC-A |
| K7 | Audio route under V | a | With a DVI EDID there is no HDMI audio, so PCM goes over the control link; 48 kHz 16-bit stereo is 1.536 Mb/s of payload, about 1.92 Mbaud with 8N1 framing, plus control traffic, so a UART route needs about 2 Mbaud or more on both ends, and 1.5 Mbaud is too slow [G]; each end's maximum UART rate (TRM or bridge datasheet) settles it; an HDMI EDID allows receiver I2S through an ASRC | DC-A |
| K8 | Control link | a | PS USB0 and the UART1 console occupy the obvious MIO (`sections/architecture.md`); candidates are UART0 plus USB-serial for a split SBC, or Ethernet through an on-card switch on GEM0, which is the Amiga's Ethernet port and runs at 10/100 (`sections/architecture.md`, "Control link (K8)"), so it shares the Amiga's LAN unless ports are isolated or VLANs used [G]; SR16's real bound under GEM RX DMA | design |
| K45 | Window coherence during drags and popups | a | Policy: plane off during a drag, or rely on outline drag [R]; windowed CEF has no popup callback (`topics/cef-frame-path.md`), so popup rectangles come from the X11 side [G] and feed the occlusion list (SR2) | design |
| K46 | EDID is a design input (format, range, bpc) | a | Driver behaviour in `sections/browser-chip.md`; default a DVI-only EDID with exact DTDs [G]; readback on R-SoC | DC-A |
| K47 | SoC-side dither, gamma and colour matrix are neutral | a | Kernel source per SoC; readback on R-SoC | DC-B |
| K48 | Tracker constants for every RTG mode (delay, nominal, maximum, engagement floor, lock window); Vtotal above 1152 needs a new ceiling | a | `video_source_sync.v:L122-128` against `os/zz_video_modes.c`; proposed lock window ±2 lines and shorter-direction acquisition [G] | design |
| K49 | Monitors accept the trim without resync, in steady state and through repeated acquisitions | a, then **d** | No reports found in the firmware repo or its issues (searched 2026-10-05); standards define fixed timings only [R]; then **R-TRIM**, then R-PLANE | DC-A |

## PCIe path (live only while DC-A keeps PCIe)

| # | Unknown | Class | Settles it | Gates |
|---|---|---|---|---|
| K9 | Usable Gen2 rates and ~15% read overhead | a | TLP/DLLP arithmetic at the chosen MPS/MRRS | DC-A |
| K10 | Tag depth (AXI-PCIe bridge PG055 vs DMA/bridge PG195); completion timeout; no SRIS on 7-series [R] | a | PG054/PG055/PG195, UG477; a common refclk on one board | DC-A |
| K11 | Read-latency tail under GPU load | a, else d | A documented SoC QoS bound, else R-PCIe | DC-A |
| K12 | Bus Master Enable, IOMMU mapping, 64-bit outbound addressing, buffer contiguity, cache maintenance before a flip | a | Kernel PCIe/IOMMU drivers, TRMs | DC-A, DC-B |
| K13 | 5 Gb/s signal integrity | b | IBIS-AMI to UG482 rules | freeze |
| K14 | CEF shared-texture OSR on the SoC's GPU driver (panthor on RK3588): buffer layout and the copy before the callback returns (`topics/cef-frame-path.md`) | b, else d | Mesa and Chromium source; R-SoC second pass | DC-A |

## SoC and Chromium

| # | Unknown | Class | Settles it | Gates |
|---|---|---|---|---|
| K15 | Full-screen 1080p60 frame time and input-to-presentation latency per SoC | **d** | Irreducible: benchmarks report throughput, not p95 frame time [R]; **R-SoC** against the pass bar in `sections/browser-chip.md` | DC-A, DC-B |
| K16 | SoC power | a | [F] Vendor maximum input, CM5: 5 V, 5 A (`cm5-ds` p6); peak logged on R-SoC | DC-B |
| K17 | Module or SBC form, HDMI exposure, lifecycle | a + c | Datasheets and vendors | DC-B, DC-D |
| K18 | Thermals inside an Amiga case | a | Heatsink sized for no airflow at a stated ambient; moot for an external box | freeze |
| K19 | Other SoCs (Jetson, i.MX95, Genio) | a | Desk, if DC-B widens | DC-B |
| K50 | Mechanism for DEC-014: whether CEF windowed mode keeps the dialog, file, JS-dialog and context-menu handlers that ASL and EasyRequest would use | a | `cefclient` beside stock Chromium on R-SoC | design |

## FPGA side

| # | Unknown | Class | Settles it | Gates |
|---|---|---|---|---|
| K20 | PL fit and BRAM margin | b | `report_utilization` on the 7020 build; fit builds per DC-C candidate | DC-C |
| K21 | Pin plan: PUDC_B strap, BCLK on a clock-capable pin, J1.133 reset polarity; optional `ZORRO_ADDRDIR2` strap | a + b | UG470; static timing | DC-C |
| K22 | PS port, PHY ID, DDR3 at 1066 | a + c | A chip-down board picks its PHY; [F] DDR3 1066 is legal at every grade (`ds187` Table 18); MYIR only on the module path (7015 PHY, DDR3 rate, PUDC_B tie) | DC-C |
| K23 | Module lifecycle and lanes | a + c | AMD and MYIR lifecycle statements; ×2/×4 lane validation via MYIR | DC-C |
| K25 | Zynq DDR headroom | a, else d | V-tracked adds no plane traffic: parity with the shipping 7020 [G], UG585 arithmetic. **Gate for f1:** at 1080p60 on an existing ZZ9000, RTG scanout (≈ 0.5 GB/s) plus bridge write and read (0.37-0.50 GB/s each) against the 4.26 GB/s peak of 32-bit DDR3-1066, with audio playing and recording; effective load could approach half of peak [G]. If it fails, the wait stays ≤ 9.4 s at 1080p60 (R-DDR) | DC-A |
| K26 | S_AXI_GP width and speed; no bus timeout | a | UG585 | design |
| K27 | 7030 memory controller rate on HP banks | a | DS191 | DC-C |
| K28 | UltraScale+ HD pins and IOB input registers; Versal Gen 2 availability | a + c | DS925/UG571; AMD | remedy |
| K29 | **Zorro and capture timing on the new board** | b | Static timing with translator delays; capture margin against [R] the super-hires pixel period of about 35 ns (28.375 MHz PAL, 28.636 MHz NTSC; verify in the Amiga Hardware Reference Manual); copy the Replica capture front end; IBIS for the capture lines | freeze |
| K30 | Native-video regression step 0 (the `test/video/` benches, IOB and CDC scripts) | b | Run against the frozen PL; XSIM limits under Vivado BASIC (`sections/firmware-and-rtl.md`) | freeze |
| K31 | Native-video hardware matrix with per-frame CRCs | v | Acceptance on the built board | build |
| K51 | 16-pin dual-edge HDMI clock duty at 1080p (53.5-60% window, `topics/zynq-pin-budget.md`) | b | PLL duty setting (odd divider 7 → ~57% [G]) plus static timing and IBIS; binds the 7015 and P5 | DC-C |
| K52 | MYC-C7Z020-V2 DDR3 part number (the firmware's PS7 setup assumes MT41J256M16) | c | MYIR; a mismatch is a firmware change, not a PCB change [G] | design |
| K53 | MYC-C7Z020-V2 Ethernet LED strap and polarity | c | MYIR; worst case is inverted link/activity LEDs, fixable in firmware [G] | design |

## Audio, power, software

| # | Unknown | Class | Settles it | Gates |
|---|---|---|---|---|
| K32 | Audio-fabric slot for the SoC producer (pump, lease or a fourth slot) | a | `docs/audio-fabric.md` and the fabric headers in `fw` | design |
| K33 | ADAU1701 second serial input | b | SigmaStudio compile; needed only for receiver I2S | design |
| K34 | A/V sync: active sink and delay sign | a + v | Chromium audio renderer source; flash-and-beep test at acceptance | design |
| K35 | Aux-domain checks: inrush, per-rail fusing, sequencing, no back-feed (incl. a powered SoC's HDMI into an unpowered receiver), ground return | a + b | Design rules; SPICE | freeze |
| K36 | PSU-side floppy receptacle current rating (~2 A) | a | Receptacle datasheet; moot for P2 | freeze |
| K37 | Spare floppy leads per machine | c | Owner survey; an own supply removes it | freeze |
| K38 | Zorro slot draw | a + v | Sum of datasheet maxima; measured at acceptance | freeze |
| K39 | 68k client: native conventions and ClipRect occlusion | b | An emulator with a P96 RTG card [R] against a stub plane interface | design |
| K40 | Amiga font licensing for Chromium | a | Desk | design |
| K41 | Reusing MNT's `0x6d6e` Zorro ID | c | Ask MNT; fallback is a new ID in every driver | fw freeze |
| K42 | SR table edits for V (`topics/plane-safety.md`) | a | Desk edit | design |

## Design decisions still open

| DC | Decision | Settled by | Status |
|---|---|---|---|
| DC-A | Coupling | K1-K5, K7, K46, K49 (R-TRIM; R-PLANE if R-TRIM fails or is unclear), K15; PCIe rows only if needed | V-tracked with the ±1 cap is under study [G]; accepted if R-SoC's display path meets the latency targets and K49 passes. If K49 fails with no trim fix: frame-buffered V (needs a 7020). If the display path misses its targets: PCIe fetch |
| DC-B | Browser chip | K15 pass bar, then integration, price, power | Open (`sections/browser-chip.md`) |
| DC-C | Zynq part and form | K20-K23, K51, pin plan | Open; budgets in `topics/zynq-pin-budget.md` |
| DC-D | Packaging | DC-A; K17, K18, K35; for P4, a Replica PCB revision outside this project | Open [D] DEC-003 |
| DC-E | May native video pass through the SoC? | DEC-013 | Ruled out by DEC-013's rule [D] DEC-013: a SoC reboot or hang would blank the monitor |
| DC-F | Remote tier | — | Closed: the LAN box is retired [D] DEC-003 |

## Freeze criteria

- Every a, b and c row is answered with a citation, or parked with a reason.
- Every d row is settled by its test method, or recorded as a risk below.
- DC-A to DC-D are decided.
- SR1-SR16 are mapped to the chosen coupling, each with its regression row (K42).
- The pin plan and power tree close: static timing, SI and SPICE clean (K13 if PCIe; K29, K35, K51 if 16-pin HDMI).

## Test methods

All use off-the-shelf hardware or an existing ZZ9000; none is a PCB of this project.

| Method | Settles | What it is |
|---|---|---|
| R-TRIM | K49 (timing itself) | The shipping `centered_1080p_match` profile on existing monitors; steps in `sections/display-coupling.md`. Results welcome by issue |
| R-SoC | K15, K50, K16 peak; readback of K5, K46, K47 | An RK3588 SBC, a CM5 with IO board and an N100-class mini PC driving a 1080p60 monitor; heavy-page scroll, video and DOM-heavy pages in stock Chromium and `cefclient`; Chromium trace from input to presentation; boot with the target EDID via `drm.edid_firmware`, then read back mode, clock, bpc and range |
| R-PLANE | K2, K3, K45, the 68k client | An existing ZZ9000 with a test bitstream: a second PL clock generating a synthetic SoC raster, the FIFO, the tracker variant and the plane. Sweep offsets: 0.048% tracks and locks; 0.148% (59.94 Hz) and 1% are rejected cleanly with RTG unaffected; repeated drops and re-locks on each monitor |
| R-DDR | K25 | An existing ZZ9000 with a traffic-generator bitstream and an AXI performance monitor |
| R-PCIe | K11 | An Artix-7 GTP Gen2 M.2 card in the SoC boards' M.2 slots; only if DC-A leans PCIe |
| R-RX | K4 residual | A receiver evaluation board and one SBC; only if desk work leaves doubt |

## Risks

| Risk | Why analysis cannot close it | Bound or mitigation |
|---|---|---|
| **Zorro and capture timing on the new board** (the leading board-level risk) | Layout parasitics and translator placement; models are only as good as IBIS | Copy the Replica capture front end and translator placement; static timing with translator delays; the `test/video/` benches (K29, K30) |
| Monitor acceptance of the trim | Monitor firmware is undocumented; one tested setup (`fw@8778ef3:README.md:L403-407`) | R-TRIM; ±1 cap by default; exact-timing DTDs. A problem found after board freeze needs a PL-only remedy (MMCM phase-shift trim [R]); frame-buffered V would need a new board |
| Chromium and GPU-driver performance across releases | K15 measures one version | Pin the measured versions; re-run R-SoC before upgrades |
| Receiver × SoC interop: InfoFrames, hot-plug timing, limited range, deep colour, exact clock | Vendor behaviour beyond datasheets | DVI-only EDID with exact DTDs; pass-through colour conversion; neutral SoC colour pipeline (K47); R-SoC readback; optional R-RX |
| Thermals in real cases (P1) | Airflow varies | Design for no airflow (K18); P2 moves the SoC out |
| SI on the new board (DDR3, HDMI in and out; PCIe if chosen) | Simulation is only as good as its models | Vendor layout rules plus IBIS; verified at acceptance |
| Part supply | LCSC is not an AMD-authorized channel [R], so chips carry no documented chain of custody | Accepted [D] DEC-015; the 7020 CLG484, which has the most HR pins and which fits PL-DDR P5 if the slow controls move to MIO (`topics/zynq-pin-budget.md`), is listed with its LCSC C-number in `sections/sourcing.md` |
| MNT's answer on `0x6d6e` | An external judgement | New-ID fallback (K41) |
| PCIe read-latency tail (only if DC-A goes PCIe) | SoC DDR arbitration under GPU load | FIFO with 2× margin over R-PCIe's worst case; an underrun policy |
