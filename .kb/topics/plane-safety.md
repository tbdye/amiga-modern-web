# Plane safety rules

Scope: SR1-SR16, the safety rules for the browser plane that DEC-005 requires, which plane paths each binds, and its regression row.
Status: current

[D] DEC-005: nothing the browser chip does, or fails to do, can touch native capture, the scan doubler or scanout.
The rules are [G] design requirements that bind the implementation; each maps to one row of the native-video regression matrix (`sections/firmware-and-rtl.md`), and the citations show the existing structure each one protects.
"Applies" names the plane path: PCIe (fetch and copy), copy, fetch, V (receiver input), or all.

| # | Applies | Requirement | Regression row |
|---|---|---|---|
| SR1 | PCIe | Two BAR windows only (plane/descriptor; control with input, command and audio rings), ending in PL BRAM and registers. No path to Zynq DDR, PS registers, OCM, firmware memory or the PCIe IP's registers; the A9 alone configures translation | SoC floods both windows at link rate and probes every offset outside them |
| SR2 | All (V: through the A9 over the control link) | SoC-writable state is the front-buffer address plus a stride within an A9-set maximum. Enable, geometry, occlusion and the RTG-only gate are A9/68k-only; the PL hard-gates the plane off in native modes | SoC writes every register at 0, max, max+1 and all-ones, plus a random sweep, in native and RTG modes |
| SR3 | Copy; V un-genlocked; the f1 bridge | The FPGA masters every plane transfer; writes go only to a dedicated plane region, never firmware memory, below scanout priority | Copy at full rate with capture running and audio playing and recording |
| SR4 | Fetch; V line FIFO (fail-closed); the f1 reader | The plane path shares no interconnect or AXI ID ordering with scanout or capture; an empty FIFO never stalls the formatter; plane-disable abandons outstanding reads | Link pulled mid-burst; forced underruns |
| SR5 | Fetch (and copy reads) | An Unsupported Request, Completer Abort or poisoned completion counts as an underrun | SoC clears Bus Master Enable mid-fetch |
| SR6 | PCIe; V | No Zorro, capture or scanout logic takes reset from the link or receiver; link- and receiver-clock-derived resets stay inside a plane island | Hot reset and function-level reset mid-frame; receiver clock loss |
| SR7 | PCIe; V (receiver I2C) | A9 access to the link IP, receiver and plane island passes a timeout firewall that errors rather than hangs | Refclk or receiver removed while the A9 accesses it |
| SR8 | PCIe | PCIe interrupts to the A9 are rate-limited; MSI is fire-and-forget | MSI disabled; interrupt storm |
| SR9 | All | The plane disables itself on link-down (V: SR14), PERST# or a frame watchdog (missed flips, repeated underruns, lost heartbeat); the same signals gate aux-domain isolation | Hung SoC; link down; SoC power removed |
| SR10 | All | The bitstream loads before the SoC enumerates; V: the receiver stays in reset, its input ignored, until the A9 enables it | Each power-up order |
| SR11 | Fetch (and copy reads) | The fetch engine tracks MRRS/MPS live; D3hot or a disallowed link power state disables the plane | SoC writes D3hot, enables ASPM, shrinks MRRS mid-frame |
| SR12 | Copy; V un-genlocked; the f1 bridge | The DDR writer issues only fully buffered bursts from a Zynq-clocked domain, so losing the link or input clock leaves no partial AXI transaction | Hot reset, refclk removal and link pull mid-copy, with audio recording |
| SR13 | V | The input writer's address (line FIFO, or frame region) stays bounded by A9-set geometry, whatever the input timing | Garbage sync: random HSYNC, VSYNC and DE lengths |
| SR14 | V | Loss of input clock or lock counts as link-down and disables the plane | Input clock pulled mid-frame |
| SR15 | V | SoC-anchored tracking applies only in RTG; native modes are unchanged (capture-anchored tracking in `centered_1080p_match`, free-running in every other profile); on loss of lock the output returns to its own nominal frames | SoC mode change mid-frame, and during a native↔RTG switch |
| SR16 | All with a non-PCIe control link | The control link (Ethernet, USB, UART, or SPI over EMIO) is rate-limited, bounding its traffic into Zynq DDR | Control flood |

## Binding set by coupling

| Coupling | Rules |
|---|---|
| V-tracked | SR2, SR4 (fail-closed line FIFO), SR6, SR7, SR9, SR10, SR13, SR14, SR15, SR16 |
| V-tracked with the f1 bridge | Adds SR3, SR12 and SR13's frame clause; the bridge reader follows SR4 |
| Frame-buffered V | V-tracked set plus SR3 and SR12 |
| PCIe fetch | SR1, SR2, SR4-SR11 |
| PCIe copy | SR1-SR3, SR5-SR12 |

## Evidence behind the rules

- [F] Today's AXI masters: HP0 scanout and PIP, HP1 Zorro `m01` (capture writes), HP2/HP3 audio, ACP Zorro `m00`; S_AXI_GP0 is disabled and GP1 never enabled (`fw@8778ef3:zz9000_project.tcl:L1233-1238, L1304-1319`).
- [F] So an f1 bridge writer cannot use HP1: capture writes share it (`fw@8778ef3:zz9000_project.tcl:L1309, L1316`).
- [G] Whether it uses HP3 (shared with audio S2MM) or S_AXI_GP (32-bit, slower [R `ug585`]) stays open.
- [F] The PIP precedent shares HP0 with scanout at AXI priority 15 over the overlay's 0 (`fw@8778ef3:docs/native-p96-pip.md:L41-42, L164`).
- [R] AXI has no abort, and a PCIe read stalled by a completion timeout (50 µs-50 ms) back-pressures whatever it shares; hence SR4.
- [R] Zynq general-purpose ports have no bus timeout; hence SR7.
- [G] With SR1 the SoC's outbound DMA is not needed, and a window into Zynq DDR would let a misbehaving SoC post traffic at link rate (0.4-1.6 GB/s) and starve capture: there is no DDR-window fallback.
- [F] In native modes the source-sync tracker is enabled only under the `centered_1080p_match` profile; every other native profile free-runs (`fw@bdfd8b0:os/video.c:L527-534, L943-945`).
- [R `ug585`] SPI1 can sit on MIO10-15.
- [F] Those pins are taken: MIO10 drives the HDD LED (net `PS_MIO10_HDD_LED`, through inverter U24, with R40 a 100 kΩ pull-down; `replica@96bdef0`, netlist) and MIO12/13 are I2C1 (`fw@bdfd8b0:zz9000_project.tcl:L926, L1151`).
- [R] Every other MIO pin set for SPI falls on MIO the PS7 configuration gives to Ethernet (16-27), USB (28-39), SD (40-45), UART1 (48-49) or I2C0 (50-51) (`fw@bdfd8b0:zz9000_project.tcl:L1151`); the `ug585` MIO table would verify which sets SPI can use.
- [R] GEM receive DMA writes frames into DDR before the A9 sees them, so SR16's real bound is line rate times the RX ring, not A9 rate limiting (`ug585` desk check pending, K8).
