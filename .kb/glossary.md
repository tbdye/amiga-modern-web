# Glossary

Scope: every code, label and term the KB uses, including the event codes E1-E22.
Status: current

## Labels and status

| Term | Meaning |
|---|---|
| `[F]` | Fact; carries a citation (`sources.md`) |
| `[G]` | Guess, estimate or inference; carries its basis where one exists |
| `[R]` | Recalled or reported, not verified here; says what would verify it |
| `[D]` | A decision's rule, at its entry's strength; carries the DEC ID |
| `Status: current` | Every statement in the file rests on a primary source, a decision or reviewed analysis |
| `Status: draft` | Every `[F]` was re-verified against its primary source at its pin, but the selection and synthesis have not had a separate design review |
| `Status: stale` | A cited fact is known or suspected to differ at HEAD and has not been re-verified; a source moving is not by itself a reason |

## Hardware and design terms

| Term | Meaning |
|---|---|
| Design under study | The Zorro-card proposal this KB describes; not fixed [D] DEC-020 |
| Approach | One of DEC-022's three: software, a co-processor board, a full card |
| Target configuration | 50 MHz 68060 with a ZZ9000 on Zorro III [D] DEC-035 |
| Second computer | A computer, not the Amiga, that runs the engine [G] (DEC-037) |
| ZZ9000 | The MNT ZZ9000 Zorro graphics and coprocessor card: a Zynq-7020 module on a carrier, with RTG, native video capture, scan doubler, HDMI out, audio (with the AX add-on) and Ethernet |
| Replica | A recreation of the ZZ9000 carrier with added features; its repository is not public (`sources.md`) |
| Zynq, PS, PL | AMD Zynq-7000 SoC; PS = the dual Cortex-A9 processing system ("A9"); PL = its FPGA fabric |
| RTG | Retargetable graphics: the card's own framebuffer modes, driven through Picasso96 (P96) |
| Native video | The Amiga chipset's own video, captured and scan-doubled by the card |
| Scan doubler | The card's output of captured native video at HDMI-monitor timings |
| Zorro | The big-box Amiga expansion bus: Zorro II (16-bit) or Zorro III (32-bit) |
| Workbench | The AmigaOS desktop and its screen, where application windows open |
| Requester | The AmigaOS term for a dialog box |
| ASL requester | A standard AmigaOS file, font or screen-mode requester, from `asl.library` |
| Browser chip, SoC | The separate application processor that runs Chromium (RK3588, x86 or Raspberry Pi CM5 class) |
| Plane | A scanout layer in the Zynq that shows browser pixels inside the browser's Workbench window |
| PIP overlay | The firmware's P96 picture-in-picture plane over RTG scanout (`sections/architecture.md`, "The plane") |
| Receiver | An HDMI/DVI receiver chip (ADV7611 class) that turns the SoC's HDMI into parallel RGB for the Zynq |
| V-tracked | The coupling under study: SoC HDMI into the receiver; the Zynq never adopts the SoC's clock, and it follows the SoC by lengthening or shortening each output frame by up to one line (`sections/display-coupling.md`) |
| V-locked | The Zynq's output running from the SoC's pixel clock; ruled out by DEC-013 |
| Frame-buffered V | The SoC's free-running HDMI written as whole frames into memory, then read out on the Zynq's clock |
| Fetch, copy | PCIe plane sources: the FPGA reads plane lines from SoC memory at scanout (fetch), or copies frames into Zynq DDR (copy) |
| Tracker | `video_source_sync.v`, the RTL that moves the output's last line inside vertical blanking to follow a source |
| Lock, acquisition | Lock: tracker phase inside its window. Acquisition: the time from an event that loses lock until lock |
| δ | SoC frame period minus Zynq frame period, in lines per frame |
| Φ | Phase between the SoC and Zynq frame starts, in lines |
| EDID | Extended Display Identification Data: a display's list of accepted timings |
| DTD | EDID detailed timing descriptor |
| HR, HP, MIO | 7-series high-range banks (1.2-3.3 V), high-performance banks (1.2-1.8 V), and Zynq PS multiplexed I/O |
| MYIR module | MYC-C7Z010/20 (V1, the ZZ9000's), MYC-C7Z020-V2, or MYC-C7Z015: Zynq modules on two 140-pin board-to-board connectors |
| J1/J2 | The 7020 module's connector numbering, used for every module in this KB (the 7015 map calls them J2/J3) |
| Chip-down | A chip soldered onto the board itself, not carried on a module |
| Bus master | A card that takes the bus and runs its own cycles |
| VGA-USB add-on | An interposer card for a stock ZZ9000 that adds VGA output and a USB hub between the module and the carrier; the Replica has both on board (`topics/replica-interconnect.md`) |
| Audio fabric; pump, lease | The A9 firmware's audio mixer; slot 0, the pump, carries MHI and ZZPlay, and slots 1-2 are leases taken by AHI and other producers (`topics/audio-path.md`) |
| Inlet | A card header that takes a PSU drive lead, floppy-type by default, for the browser chip's power (`topics/power-domains.md`) |
| Scroll-copy | Client moves pixels it holds; only the newly exposed strip is sent |
| Byte-weighted ratio | Raw bytes of all units ÷ their coded bytes (`topics/page-pixels.md`) |
| PSNR | Peak signal-to-noise ratio in dB; higher is closer to the original |
| Soft text | Text after a lossy coding such as JPEG (`topics/page-pixels-lossy.md`) |
| Hextile, TRLE, ZRLE | VNC tile encodings, ZRLE with zlib (`topics/page-pixels.md`, "Method") |
| Whole-window slide, region-aware slide | Two models of what a scroll resends (`topics/scroll-redraw.md`) |
| Browservice | A remote browser: CEF renders off-screen and sends the view as images to a legacy browser (`topics/prior-art.md`) |
| Pixel rate | MB/s of pixels reaching the screen by receive then copy (`topics/target-config-rates.md`) |
| Mpix | 10^6 pixels; 1 Mpix/s of 16-bit pixels is 2 MB/s |
| MB/s, MiB/s | On the rate pages, 10^6 and 2^20 bytes a second (`topics/target-config-rates.md`) |
| Owner group | Amiga owners who have the same kind of hardware (`topics/audience.md`) |
| PiStorm | An adapter with a Raspberry Pi in place of the 68k (`topics/audience-pistorm.md`) |
| SDK mailbox | Request and completion rings in card DDR, called through `zz9k.library` (`topics/arm-offload.md`) |
| AmiSSL | The Amiga's shared TLS library, `amissl.library` |
| XACP | A third-party ZZ9000 firmware line that loads ARM programs (`topics/arm-hosted-engine.md`) |
| JIT | Just-in-time compiler in a script engine; an interpreter has none |
| DOM | Document Object Model: the page's tree, which script reads and changes |
| Dhrystone, VAX MIPS | An integer benchmark; its score divided by a VAX-11/780's |

## Packaging and option codes

| Code | Meaning |
|---|---|
| P1 | One card: chip-down Zynq-7000, receiver and a SoC module, V-tracked |
| P2 | Split: a Zynq card with a receiver, plus an unmodified SBC or mini PC joined by an HDMI cable and a control link |
| P3 | One card, PCIe fetch, Zynq-7015 plus an RK3588 (not RK3588S) or x86 module |
| P4 | A redesigned Replica with an on-board SoC module |
| P5 | Frame-buffered V in P1 or P2 form, with its own PL DDR3 |
| P6 | Zynq UltraScale+ (ZU2/ZU3) chip-down |
| P7 | Versal AI Edge Gen 2: one chip with CPU, GPU and fabric |
| P8 | Display owned by the SoC, with the FPGA reduced to a Zorro and capture bridge |
| P9 | A non-AMD FPGA plus a firmware CPU |
| R2 | A Replica plus a SoC card on a PCIe cable through a module interposer |

## Option families and the quality ceiling

| Term | Meaning |
|---|---|
| Family A | The browser engine runs on a separate machine, and the ZZ9000 shows its output (the remote tier: not ruled out, no role chosen [D] DEC-003) |
| Family B | The engine runs on an application-class chip on the card, coupled to the FPGA that owns the display (P1-P5, R2) |
| Family C | The application chip owns the display, and native video passes through it (P8) |
| Family D | One chip does everything (P7; a ZU+ alone) |
| Quality ceiling | A SoC with a GPU, coupled to the Zynq's FPGA by memory (PCIe) or by its video output (V), with the FPGA keeping Zorro, native capture, the scan doubler and final scanout under the safety rules; the GPU draws the page and Chromium's compositor scrolls it, and the 68k runs only native chrome [G] |

## Other names for the same thing

| Name | Means |
|---|---|
| Genlocked V | K1's route (the SoC locks to the Zynq's VSYNC) or V-locked (the Zynq runs on the SoC's clock) |
| Line-locked V | V with the SoC's pixels at a fixed phase to the Zynq's scanout, keyed in through a few-line FIFO; V-tracked does this |
| Families A-D; family C | The option families above; family C is P8 |
| J9, video-slot input | `sections/options-rejected.md`, "DPI into the video-capture path" |
| Downstream HDMI compositor card | A P8 variant (`sections/options-rejected.md`) |
| Fetch FIFO | The plane line FIFO under PCIe fetch (`topics/pcie-path.md`) |
| Frame-length trim, monitor trim | The ±1-line change of the Zynq's frame length under V-tracked (`topics/monitor-trim.md`) |

## Engine terms

| Term | Meaning |
|---|---|
| Control program | Takes an engine's frames and events; talks to the Amiga (`topics/engine-control.md`) |
| Remote-control protocol | Chrome DevTools Protocol (CDP): how another program drives Chrome or Chromium |
| Stock browser | A browser as its maker or a distribution packages it, unmodified |
| Hidden display | A Wayland compositor or virtual X display with no monitor (`topics/hidden-display.md`) |
| Wayland compositor | A Wayland session's display server; clients hand it surfaces and damage |
| Damage | Rectangles of a window or frame that changed since the last frame |
| CEF | Chromium Embedded Framework, a library that embeds Chromium in another program |
| Blink, Gecko, WebKit | The engine families of Chrome, Firefox and Safari (`topics/engine-options.md`) |
| Widevine | Google's content-decryption module, required by some streaming services |

## Decision, unknown and rule IDs

| Prefix | Where defined |
|---|---|
| DEC-n | `decisions.md` |
| K1-K75 | `unknowns.md`, unknowns register; K6, K24, K43 and K44 are retired |
| DC-A to DC-F | `unknowns.md`, design decisions; DC-E is closed |
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
| E18 | Browser on a native screen (a buffered native path is proposed: `topics/native-screens.md`), on 2560×1440, or on a custom RTG mode |
| E19 | SoC emits timing the EDID does not list (e.g. 59.94 Hz) |
| E20 | ZZ9000 firmware watchdog reset |
| E21 | ZZ9000 firmware or bitstream update |
| E22 | Monitor power-cycle, input switch or replug on the Zynq output |
