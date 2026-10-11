# Zynq and board

Scope: why the design stays on Zynq-7000, the parts and packages in play, the packaging options, and what carries over from the ZZ9000 and Replica.
Status: draft

## Why Zynq-7000

- [G] Only the Zynq-7000 carries the shipping firmware, RTL and drivers at no rewrite cost while keeping the monitor's clock independent of the browser chip [D] DEC-012, DEC-013.
- [G] Every alternative either pays a full firmware port (UltraScale+, Versal, a non-AMD FPGA) or hands the monitor clock to the SoC (`sections/options-rejected.md`).
- [F] The shipping Vivado project targets `xc7z020clg400-1` (`fw@8778ef3:zz9000_project.tcl:L115`).

## Parts

[F] `ds190` p3 (resources) and p4 (packages):

| Part | LUTs | Flip-flops | DSP slices | BRAM36 | PCIe hard block | Package: PL I/O |
|---|---|---|---|---|---|---|
| Z-7020 | 53,200 | 106,400 | 220 | 140 | None | CLG400: 125 HR; CLG484: 200 HR |
| Z-7015 | 46,200 | 92,400 | 160 | 95 | Gen2 ×4 | CLG485: 150 HR + 4 GTP |
| Z-7030 | 78,600 | 157,200 | 400 | 265 | Gen2 ×4 | SBG485: 50 HR + 100 HP; FBG484: 100 HR + 63 HP; FBG676: 100 HR + 150 HP |

- [F] The Z-7015 CLG485 is pin-compatible with the Z-7030 SBG485 (`ds190` p4, Table 2 note 2).
- [F] HR banks take 1.2-3.3 V; HP banks only up to 1.8 V (`ds190` p4 notes).
- [F] CLG400 is 17 × 17 mm; CLG484, CLG485 and SBG485 are 19 × 19 mm; all four have 0.8 mm ball pitch; FBG484 is 23 × 23 mm and FBG676 27 × 27 mm, at 1.0 mm pitch (`ds190` p4, Tables 2 and 3).
- [F] PS DDR3 runs at up to 1066 Mb/s at every speed grade (`ds187` Table 18, p15), and the shipping build runs DDR3 at 533 MHz, part MT41J256M16 RE-125, 32-bit (`fw@8778ef3:zz9000_project.tcl:L1185, L1193, L1206, L1209`).
- [G] So the card's PS DDR peaks at about 4.26 GB/s (32 bits at 1066 Mb/s); the f1 bridge's write and read (0.37-0.50 GB/s each at 1080p60) and RTG scanout (about 0.5 GB/s) are measured against it (K25).
- [F] PL-side DDR3 through the memory interface generator runs at 800 Mb/s at −1 and −2; 1066 only at −3, and then only with an external VREF (internal VREF caps it at 800) and never in bank 13 of a Z-7015 or Z-7020 (`ds187` Table 51 and notes 2-3, p33).

## Fit

- [G] BRAM is the likeliest resource to bind on a Z-7015: 95 BRAM36 against the Z-7020's 140, 32% fewer.
- [F] The firmware repository holds no utilisation report (`fw@bdfd8b0`, no `report_utilization` output or `.rpt` file in the tree), so the shipping design's use is unmeasured here (K20).
- [G] A fit build passes with ≤ 85% of BRAM36 (≤ 80 of 95 on a Z-7015, PCIe BAR windows included) and ≤ 85% of LUTs; WNS ≥ 0 and WHS ≥ 0 on every clock, BCLK included; no Place 30-574-class placement warnings beyond those the build's per-net `CLOCK_DEDICATED_ROUTE FALSE` overrides already accept (`sections/firmware-and-rtl.md`, "Capture clock"); and step 0 of the native-video regression (`sections/firmware-and-rtl.md`).
- [G] Its first step is `report_utilization` on the existing Z-7020 build.
- [G] V-tracked's line FIFO takes about 8 BRAM36 (`sections/display-coupling.md`); PCIe fetch takes about 8 for its FIFO and 2-3 for its BAR windows (`topics/pcie-path.md`).

## Modules

| Module | Chip | Status [F] |
|---|---|---|
| MYC-C7Z010/20 (V1; the ZZ9000's) | XC7Z020 | Discontinued; MYIR states its -V2 is a fully compatible replacement (`myir-7020v1`) |
| MYC-C7Z020-V2 | XC7Z020-2CLG400I; 1 GB DDR3 as 2 × 512 MB, 32-bit; 75 × 55 mm; 5 V / 0.5 A, 2.5 W | Active; Ethernet PHY YT8531SH (`myir-7020v2`) |
| MYC-C7Z015 | XC7Z015-2CLG485; 766 MHz CPU (up to 866 MHz); 1 GB DDR3 as 2 × 512 MB; 75 × 55 mm; 5 V / 0.5 A | Active, industrial grade; MYIR states it can share a base board with the MYC-C7Z010/20 (`myir-7015`) |

- [F] Each module sits on two 0.8 mm pitch 140-pin board-to-board connectors (`myir-7015`, `myir-7020v2`); the Replica's mating parts are two Amphenol 61083-141402LF, U12 and U13 (`replica@96bdef0`, netlist; LCSC number in `sections/sourcing.md`).
- [G] Moving a design to the Z-7015 also needs the new part in the Vivado project, a PS7 configuration with the module's DDR3 parameters, regenerated `ps7_init` and FSBL, a new BSP and device ID, and the module's Ethernet PHY identified (K22).

- [F] V1 and V2 differ in the Ethernet PHY; MYIR states they are otherwise compatible (`myir-7020v2`, `list.asp?id=694`).
- [F] The firmware reads PHY register 2 and accepts only `0x22` (Micrel) or `0x4f51` (MotorComm); any other value fails with "Unsupported PHY" (`fw@8778ef3:os/ethernet.c:L100-103, L1007-1024`).
- [F] Linux lists YT8522, YT8531, YT8531S and YT8821 IDs that all start `0x4f51` (`linux@6c377d19d4a5:motorcomm.c:L18-21`); so a YT8531SH is accepted whichever of those it reports [G: the SH reports one of them].
- [F] MotorComm PHY support entered the firmware in `d80e21f` (2022-10-18), a change to `os/ethernet.c` only (`fw` `git show --stat d80e21f`).
- [F] On the Replica carrier, the module's eight Ethernet MDI pins run straight to the MagJack, and its MDIO pins are unconnected, so MDIO stays on the module (`replica@96bdef0`, netlist, U12.7-18 and U12.22/24; not public).
- [G] So a Replica takes the -V2 module on its existing footprints with no PCB change; the open questions (V2 DDR3 part, LED strap polarity) are firmware-only and go to MYIR (`unknowns.md`, vendor rows).

## Packaging options

[D] DEC-003: packaging is open.

| Option | Shape | Integration effort [G] |
|---|---|---|
| P1 | One card: chip-down Zynq, receiver and SoC module | High: SoC site, power and thermals on one PCB |
| P2 | Zynq card plus receiver; unmodified SBC or mini PC in an adjacent slot or external box; HDMI cable plus a USB-serial or Ethernet control link | Medium: no SoC on our PCB; the user picks the SoC; needs an HDMI back-feed check (K35) |
| P4 | Redesigned Replica with an on-board SoC module | High; needs a Replica PCB revision, outside this project |
| R2 | Replica plus a SoC card over PCIe | PCIe only; the Replica cannot take V: it connects all 125 PL pins of its 7020 module, 124 have on-board loads and `Free7` reaches only header J10.3, and a 7015 module adds only 12 unconnected pins against the receiver's 28 (`topics/zynq-pin-budget.md`) |

## Reuse

| Area | Unchanged [G] | Changed [G] | New [G] |
|---|---|---|---|
| Firmware (A9) | RTG, capture control, scan doubler, audio fabric, Ethernet, vendor-service framework | PS7 configuration for a new package; the PHY table if the PHY changes; the 720p preset (K5) | Plane and control services; receiver set-up and EDID; heartbeat watchdog |
| PL | `mntzorro.v`, capture (`videocap_sampler.v`), `audio_clock.v`; the 28-pin HDMI bus on a 7020 CLG484 | `video_formatter.v`: an RGB plane and rectangle occlusion; dual-edge HDMI on a 7015 | Receiver input, async line FIFO, tracker V variant, safety island |
| AmigaOS drivers | RTG, net, AHI, ZZTop, SD, USB, if the Zorro ID and register map are kept (K41) | Every ID site, only if the ID forks | 68k browser client; `zz9k.library` plane calls |
| Replica blocks | Zorro buffers and translators; the capture front end, reused with its layout unchanged (K29); SiI9022A HDMI TX; ADAU1701 audio; slot power | Ethernet PHY on a chip-down design | Chip-down Zynq; receiver and EDID; SoC site or connectors; aux-domain protection |

- [F] The RTG driver binds by manufacturer `0x6d6e` and the ZZ9000 Z3/Z2 products (`drivers@ad9606b:rtg/mntgfx-gcc.c:L143, L814-815`); likewise the network and AHI drivers (`net/device.c:L337`, `ahi/driver/zz9000ax-ahi.c:L235`).
- [G] `0x6d6e` is MNT Research's manufacturer ID; the Replica runs this firmware, whose autoconfig ROM presents it (`fw@bdfd8b0:mntzorro.v:L2289-2292, L2460-2463`, inverted nibbles), so it already reuses the ID; whether a new board may is MNT's call (K41).
- [F] Forking the ID also touches ZZTop (`drivers@ad9606b:ZZTop/Sources/ZZTop.c:L7043, L7047`), SD boot (`sd-boot/zzsd_device.c:L94, L96`), the Poseidon USB device (`usb-poseidon/zzusbhw_device.c:L3136, L3138`), `ZZNetReady/ZZNetReady.c:L48`, and `include/zz9000_hw.h:L19`, whose macro the AHI and MHI drivers use (`ahi/driver/zz9000ax-ahi.c:L235`, `mhi/mhizz9000.c:L239`).
- [F] In the firmware it touches the autoconfig ROM (above), `sdk/include/zz9k/abi.h:L33` and `sdk/host/src/zz9k_host.c:L945, L952` (`fw@bdfd8b0`).

## What a new card removes, and where reuse stops

- [G] A new card removes the Replica-specific problems of a Z-7015 module: the PUDC_B strap on a live pixel line, the BCLK pin losing clock capability (`sections/gotchas.md`), add-on stacking and a GTP interposer; the Z-7015's BRAM squeeze goes only with a Z-7030 or a chip-down Z-7020.
- [G] The new-card designs are a chip-down Z-7020 CLG484 fed by V, with or without a PL DDR3 bank (`topics/zynq-pin-budget.md`, "Package results under V-tracked"), and a Z-7030 FBG676 with PL DDR3 for PCIe copy (`topics/pcie-path.md`, "Pin budget under PCIe"); which leads is open (DC-C, `unknowns.md`).
- [G] Reuse stops paying at the MYIR 7015 module's 137 PL pins under V (`topics/zynq-pin-budget.md`), at the Replica as a host for a 1080p V input (P4, R2 above), and, for firmware and PL, at the Zynq-7000 boundary (P6, P7, P9) and at a SoC-owned display (P8).
