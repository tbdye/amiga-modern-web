# Glossary

Scope: every code, label and term the KB uses, including the event codes E1-E22.
Status: current

## Labels and status

| Term | Meaning |
|---|---|
| `[F]` | Fact; carries a citation (`sources.md`) |
| `[G]` | Guess, estimate or inference; carries its basis where one exists |
| `[R]` | Recalled or reported, not verified here; says what would verify it |
| `[D]` | Requirement that comes from a decision; carries the DEC ID |
| `Status: current` | Every input to the file was a reviewed finding, and its synthesis was reviewed |
| `Status: draft` | Every `[F]` was re-verified against its primary source at its pin, but the selection and synthesis have not had a separate design review |
| `Status: stale` | A source moved and the file has not been re-verified |

## Hardware and design terms

| Term | Meaning |
|---|---|
| ZZ9000 | The MNT ZZ9000 Zorro graphics and coprocessor card: a Zynq-7020 module on a carrier, with RTG, native video capture, scan doubler, HDMI out, audio (with the AX add-on) and Ethernet |
| Replica | A recreation of the ZZ9000 carrier with added features; its repository is not public (`sources.md`) |
| Zynq, PS, PL | AMD Zynq-7000 SoC; PS = the dual Cortex-A9 processing system ("A9"); PL = its FPGA fabric |
| RTG | Retargetable graphics: the card's own framebuffer modes, driven through Picasso96 (P96) |
| Native video | The Amiga chipset's own video, captured and scan-doubled by the card |
| Browser chip, SoC | The separate application processor that runs Chromium (RK3588, x86 or Raspberry Pi CM5 class) |
| Plane | A scanout layer in the Zynq that shows browser pixels inside the browser's Workbench window |
| Receiver | An HDMI/DVI receiver chip (ADV7611 class) that turns the SoC's HDMI into parallel RGB for the Zynq |
| V-tracked | The coupling under study: SoC HDMI into the receiver; the Zynq never adopts the SoC's clock, and it follows the SoC by lengthening or shortening each output frame by up to one line (`sections/display-coupling.md`) |
| V-locked | The Zynq's output running from the SoC's pixel clock; ruled out by DEC-013 |
| Frame-buffered V | The SoC's free-running HDMI written as whole frames into memory, then read out on the Zynq's clock |
| Fetch, copy | PCIe plane sources: the FPGA reads plane lines from SoC memory at scanout (fetch), or copies frames into Zynq DDR (copy) |
| Tracker | `video_source_sync.v`, the RTL that moves the output's last line inside vertical blanking to follow a source |
| Lock, acquisition | Lock: tracker phase inside its window. Acquisition: the time from an event that loses lock until lock |
| δ | SoC frame period minus Zynq frame period, in lines per frame |
| Φ | Phase between the SoC and Zynq frame starts, in lines |
| DTD | EDID detailed timing descriptor |
| HR, HP, MIO | 7-series high-range banks (1.2-3.3 V), high-performance banks (1.2-1.8 V), and Zynq PS multiplexed I/O |
| MYIR module | MYC-C7Z010/20 (V1, the ZZ9000's), MYC-C7Z010/20-V2, or MYC-C7Z015: Zynq modules on two 140-pin board-to-board connectors |
| J1/J2 | The 7020 module's connector numbering, used for every module in this KB (the 7015 map calls them J2/J3) |

## Packaging and option codes

| Code | Meaning |
|---|---|
| P1 | One card: chip-down Zynq-7000, receiver and a SoC module, V-tracked |
| P2 | Split: a Zynq card with a receiver, plus an unmodified SBC or mini PC joined by an HDMI cable and a control link |
| P3 | One card, PCIe fetch, Zynq-7015 plus an RK3588 or x86 module |
| P4 | A redesigned Replica with an on-board SoC module |
| P5 | Frame-buffered V in P1 or P2 form, with its own PL DDR3 |
| P6 | Zynq UltraScale+ (ZU2/ZU3) chip-down |
| P7 | Versal AI Edge Gen 2: one chip with CPU, GPU and fabric |
| P8 | Display owned by the SoC, with the FPGA reduced to a Zorro and capture bridge |
| P9 | A non-AMD FPGA plus a firmware CPU |
| R2 | A Replica plus a SoC card on a PCIe cable through a module interposer |
| NC-30, NC-20V | New-card variants: a Zynq-7030 with PCIe and PL DDR; a chip-down Zynq-7020 fed by V |

## Decision, unknown and rule IDs

| Prefix | Where defined |
|---|---|
| DEC-n | `decisions.md` |
| K1-K53 | `unknowns.md`, unknowns register; K6, K43 and K44 are retired |
| DC-A to DC-F | `unknowns.md`, design decisions still open |
| R-TRIM, R-SoC, R-PLANE, R-PCIe, R-DDR, R-RX | `unknowns.md`, test methods |
| SR1-SR16 | `topics/plane-safety.md` |
| f1, f3, f4, f5, a′, b, c | `sections/display-coupling.md`, mitigations (f2, f6 and f7 are not used) |

## Event codes (E1-E22)

Events that can leave the browser window black or not yet live; analysis in `sections/display-coupling.md`.

| Code | Event |
|---|---|
| E1 | Amiga cold boot with the SoC powered at the same time |
| E2 | Amiga cold boot with the SoC already running |
| E3 | Amiga warm reboot |
| E4 | RTG-to-RTG resolution change |
| E5 | Colour-depth change, or a screen reopened, at the same resolution |
| E6 | Switch between a native screen and RTG |
| E7 | SoC cold boot or reboot on its own |
| E8 | Chromium crash or restart without a display mode change |
| E9 | Chromium restart that triggers a kernel modeset on the SoC |
| E10 | SoC hang with its HDMI still live |
| E11 | SoC changes its own mode or re-reads EDID |
| E12 | SoC HDMI cable unplugged and replugged (P2 only) |
| E13 | SoC display blanking or DPMS |
| E14 | Receiver glitch; the tracker watchdog trips |
| E15 | Amiga screen blanker or DPMS |
| E16 | Window open, close or move; another same-mode screen in front |
| E17 | Window resize or full-screen |
| E18 | Browser on a native screen, on 2560×1440, or on a custom RTG mode |
| E19 | SoC emits timing the EDID does not list (e.g. 59.94 Hz) |
| E20 | ZZ9000 firmware watchdog reset |
| E21 | ZZ9000 firmware or bitstream update |
| E22 | Monitor power-cycle, input switch or replug on the Zynq output |
