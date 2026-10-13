# Replica interconnect

Scope: how the Replica carrier wires the Zynq module: where the PL and PS pins go, the level translators, what it and the stock ZZ9000 wire of what a Zorro bus master drives, headers and spare I/O, the video-slot and audio headers, and the VGA-USB add-on interposer for a stock ZZ9000.
Status: draft

Replica facts come from its netlist at `replica@96bdef0`, including the `ZZ9000-USB/` and `ZZ9000-VGA-Output/` sub-sheets; add-on facts from `addon@40bca90`; both are not public.
Connector pins use the 7020 numbering (J1/J2; `sections/gotchas.md`).
Pin budgets for a new board: `topics/zynq-pin-budget.md`; audio wiring: `topics/audio-path.md`; power tree: `topics/power-domains.md`.

## Module banks

- [F] The 7020 module's PL pins sit in bank 35 (50 pins, J1.29-90), bank 34 (50 pins, J2.7-64) and bank 13 (25 pins, J2.83-110) (`evidence/z20.json`).
- [F] PS bank 500 VDDIO is `+3V3` (J1.139) and bank 501 VDDIO is `+1V8` (J1.138) (`replica@96bdef0`, netlist), so MIO0-15 are 3.3 V and MIO48-51 are 1.8 V.

## Where the 125 PL pins go

[F] `replica@96bdef0`, netlist:

| Group | PL pins | Path |
|---|---|---|
| Zorro bus and video-slot capture | 85 | Eleven SN74LVC8T245 (U1-U11): 82 signal nets on their A sides, plus 3 direction nets driven by the PL (`DIRDATA`, `DIRADDR`, `DIRADDR2`) |
| Open-drain Zorro outputs | 5 | 74LVC06A U24: `/DTACK`, `/CINH`, `/MTACK`, `/BGACK`, and an interrupt that jumper J4 routes to `/INT6` or `/INT2` |
| HDMI out | 28 | Direct to the SiI9022A (U15): 24 data, IDCK, DE, HSYNC, VSYNC; the on-board ADV7125 VGA DAC (U23) taps the same lines |
| AX audio | 6 | Direct to the ADAU1701 (U103) and header J10 |
| `Free7` | 1 | Header J10.3 only |

- [F] All eleven translators have VCCA on `+3V3`, VCCB on `+5V` and `/OE` tied to ground; U7-U10 have DIR tied low (bus to FPGA), U11 tied high (FPGA to bus), and U1-U6 take DIR from the PL (`replica@96bdef0`, netlist).
- [F] U8-U10 and three channels of U7 carry the 27 video-slot capture nets: 24 RGB, `VHSYNC`, `VVSYNC` and `C28D` (`replica@96bdef0`, netlist).
- Which builds clock capture from `C28D` rather than `ZORRO_E7M`: `sections/firmware-and-rtl.md`, "Capture clock".
- [F] U24's sixth channel buffers PS MIO10 to the HDD LED (`replica@96bdef0`, netlist; `fw@bdfd8b0:os/sd_activity_led.h:L12`).
- [F] The 74LVC06A needs VIH ≥ 2.0 V at VCC 2.7-3.6 V and sinks only 4 mA at VCC 1.65 V (`lvc06a` p3); U24 runs from `+3V3` (`replica@96bdef0`, netlist).
- [G] So U24's five PL nets need a 3.3 V bank, or another translator, on any new board.

## Pins sensitive to bank voltage on a new board [G]

- Only timing-tolerant Zorro signals could move to a 1.8 V bank behind slower translators: `ZORRO_NIORST`, `ZORRO_NCFGIN` and `ZORRO_NCFGOUT`; translator delays are in `topics/zynq-pin-budget.md`, "Voltage".
- `ZORRO_NCCS` cannot move: the RTL uses it as Zorro II /AS (`fw@bdfd8b0:mntzorro.v:L909`), and /AS frames every Zorro II cycle.
- [F] At 1.8 V IOVCC the SiI9022A takes dual-edge IDCK only to 82.5 MHz, single-edge to 165 MHz (`sii9022a` Table 3.12, p18), so 1080p60 (148.5 MHz class) at 1.8 V needs the full 28-pin single-edge bus [G].

## PUDC_B

- [F] On the 7020 module PUDC_B is ball U13 on J2.57 (`myir-7020-pinout`), which the firmware constrains as `ZORRO_NCCS` (`fw@bdfd8b0:xdc/zz9000.xdc:L127`); on the Replica it is net `ZY/CCS` on translator U3 (`replica@96bdef0`, netlist).
- On the 7015 it moves to J2.14, a live HDMI pixel line (`sections/gotchas.md`, "Modules and pins").
- [R `ug470`] PUDC_B low enables pull-ups on every PL I/O during configuration, and the pin must not float.
- [G] So a 7015 on the Replica needs PUDC_B strapped high, which keeps today's configuration-window behaviour: pulled low, the pull-ups would change Zorro and capture pins before configuration completes.

## Zorro bus mastering

A bus master is a card that takes the bus from the backplane's bus controller and runs its own cycles.
The firmware never requests the bus: `sections/firmware-and-rtl.md`, "Anchors for a browser plane".
Stock-board facts are read from the schematic on page 2 of two MNT manuals, `zz9000-manual-r1` (drawing R-1) and `zz9000-manual-r3`; the R-4 manual carries the R-3 drawing (`sources.md`).

### What a master drives, by the specification

[F] `zorro3`, by section and PDF page; edge pins are from its Appendix A.1, pp76-78; "—" marks a role with no part in the signal:

| Signal (edge pin) | Zorro II master | Zorro III master | Slave | `zorro3` |
|---|---|---|---|---|
| `/BRn` (60) | Asserts on a rising 7M edge; negates once it has asserted `/BGACK` | Pulses it from one rising 7M edge to the next, once to register and once to unregister | — | §2.3.5 p28; §3.4 pp37-38 |
| `/BGn` (64) | Reads | Reads; a grant is for one full cycle | — | §2.3.5 p28; §3.4 p37, §4.5 p47 |
| `7M` (92) | Reads, to time `/BRn` | Reads, to time `/BRn` | — | §2.3.5 p28; §4.2 p44 |
| `/OWN` (7) | Asserts, open collector | Must not drive; the bus controller does | — | §2.3.5 p27; §4.5 p47 |
| `/BGACK` (62) | Asserts, open collector, only once it sees `/AS`, `/DTACK` and `/BGACK` negated | Must not drive; the bus controller does | — | §2.3.5 p28; §4.5 p47 |
| Address | Drives `A1-A23` | Drives `A8-A31` until just after `/FCS` falls, and `A2-A7` for the whole cycle | Reads | §2.3.6 pp28-29; §4.6 pp47-48 |
| `FC0-FC2` (31, 33, 35) | Need not drive them valid | Drives, with the address | Reads | §2.3.6 p30; §3.1.2 p33, §4.6 p48 |
| `/AS`, named `/CCS` in Zorro III (74) | Drives | The bus controller drives it, for Zorro II address space | Reads | §2.3.6 pp28-29; §3.6 p40, §4.6 p48 |
| `/FCS` (97) | No connect in Zorro II | Drives | Reads | Appendix A.1 p78; §3.1.2 p33, §4.6 p49 |
| `READ` (68) | Drives | Drives | Reads | §2.3.6 pp28-29; §4.6 p47 |
| Data strobes | Drives `/UDS` (72) and `/LDS` (70) | Drives `/DS3-/DS0` (72, 70, 98, 51) | Reads | §2.3.6 pp28-29; §3.1.2 p33, §4.7 p49 |
| `DOE` (93) | Not stated | Drives | Reads | §2.3.4 p27; §3.1.2 p33, §4.7 p49 |
| Data | `D0-D15`: drives on a write, reads on a read | `D0-D31`: the same | The reverse | §2.3.6 p29; §3.1.2 pp33-34, §4.7 p49 |
| `/DTACK` (66) | Reads: samples it before ending the cycle | Reads: ends the cycle on it | Drives, open collector | §2.3.6 p29; §3.1.2 pp33-34, §4.7 p49, §6.1.3 p63 |
| `/BERR` (46) | Reads: every card must monitor it | Reads: ends the cycle and retries it | Reads | §2.3.3 p26; §3.4 p38, §4.3 p45 |
| `/LOCK` (29; `A1` in Zorro II) | Not a Zorro II signal | Asserts it to lock the bus | Reads | §3.2.1 p34; Appendix A.1 p76 |
| `/MTCR` (18), `/MTACK` (48) | Not Zorro II signals | In a burst, which a card need not support: drives `/MTCR`, reads `/MTACK` | Reads `/MTCR`, drives `/MTACK` | §3.3 pp35-36, §4.7 pp49-50 |
| `/BCLR` (95) | Reads: another card wants the bus | May read | — | §2.3.5 p28; §4.5 p47 |

- [F] A Zorro III card must use Zorro III arbitration (`zorro3` §3.4 p38).
- [F] Address, data, `/FCS`, the data strobes, `READ`, `DOE`, `FC0-FC2`, `/LOCK` and `/MTCR` are Standard signals, whose driver gives +2.5 V at −3.0 mA and +0.4 V at +64 mA; `/OWN`, `/BGACK`, `/DTACK` and `/BERR` are open collector, +0.4 V at +20 mA; `/BRn` and `/BGn` are slot-specific, +0.4 V at +4.0 mA (`zorro3` Table 6-1 and §6.1.1 p62, §6.1.3-§6.1.4 p63).

### What the two boards wire

[F] The Replica from its netlist (`replica@96bdef0`, not public); the stock board from `zz9000-manual-r1` p2 and `zz9000-manual-r3` p2, where each module pin named below carries the same net unless the last column says otherwise.
Module pin to FPGA ball is from `myir-7020-pinout`, ball to firmware port from `fw@cfbb910:xdc/zz9000.xdc:L96-159`, and port direction from `fw@cfbb910:mntzorro.v:L132-153, L188`.
"No port" means no `PACKAGE_PIN` constraint in any `.xdc` or `.tcl` file at `fw@cfbb910`.

| Signals | Replica part and path | Direction control | Module pin; firmware port | Stock R-1 and R-3 |
|---|---|---|---|---|
| `D0-D15` | U1, U2; bidirectional | `DIRDATA` | J2.90, `ZORRO_DATADIR`, output; `ZORRO_DATA[15:0]`, inout | Same |
| `A8-A23` | U4, U5; bidirectional | `DIRADDR` | J2.91, `ZORRO_ADDRDIR`, output; `ZORRO_ADDR[22:7]`, inout | Same |
| `A1-A7`, `/CCS` | U3; bidirectional, the eight together | `DIRADDR2` | J2.33, `ZORRO_ADDRDIR2`, output; `ZORRO_ADDR[6:0]`, inout; `/CCS` on J2.57, `ZORRO_NCCS`, input | Same |
| `DOE`, `/FCS`, `/DS0`, `/DS1`, `READ`, `/LDS`, `/UDS` | U6, seven channels; bidirectional, the seven together | `DIRADDR2`, the net on U3 | J2.86, 84, 60, 58, 56, 54, 50; `ZORRO_DOE`, `ZORRO_NFCS`, `ZORRO_NDS0`, `ZORRO_NDS1`, `ZORRO_READ`, `ZORRO_NLDS`, `ZORRO_NUDS`, inputs | Same |
| `/BRn` | U11; FPGA to bus, push-pull | DIR on `+3V3` | J2.29, `ZORRO_NBRN`, output | Same |
| `/BGn`, `7M` (net `E7M`) | U7; bus to FPGA | DIR grounded | J2.31, `ZORRO_NBGN`; J2.45, `ZORRO_E7M`; inputs | Same |
| `/DTACK` | U24, open drain; FPGA to bus only: the net's two nodes are edge pin 66 and U24's output | None | J2.88, `ZORRO_NDTACK`, output | Same path, through transistor Q1 (an NPN on R-1, a 2N7002E on R-3) |
| `/BGACK` | U24, open drain; FPGA to bus only | None | J2.64, ball U12; no port | No-connect mark at edge pin 62; J2.64 is `Free8` |
| `/MTCR` | U7; bus to FPGA | DIR grounded | J2.27, ball T16; no port | No-connect mark at pin 18; J2.27 is `Free10` |
| `/MTACK` | U24, open drain; FPGA to bus only | None | J2.19, ball P18; no port | No-connect mark at pin 48; J2.19 is `Free9` |
| `/OWN`, `FC0-FC2`, `/BERR`, `/BCLR` | Unconnected | — | — | Same: no-connect marks |

- [F] DIR low passes a translator's B side, the bus, to its A side, the FPGA, and DIR high the reverse (`lvc8t245` Table 7-1, p15).
- [F] On the Replica 10 kΩ resistors pull the three direction nets to ground (R45-R47) and `/BRn`'s FPGA side to `+3V3` (R50), and 100 kΩ resistors pull U24's `/DTACK`, `/CINH`, `/MTACK` and `/BGACK` inputs to ground (R14, R36-R38) (`replica@96bdef0`, netlist).
- [G] So U24 releases `/MTACK` and `/BGACK` only while their FPGA pins are high-impedance or low.
- [F] The firmware keeps a commented-out `ZORRO_NMTCR` port and a commented-out constraint that put it on ball C20, which `VCAP_R7` now takes (`fw@cfbb910:mntzorro.v:L143`; `xdc/zz9000.xdc:L28, L121`).

### The wiring against the specification

- [F] Bus request, bus grant and the 7M clock reach the FPGA on both boards, and each direction net reaches an FPGA output, so address, data and the seven strobes can be turned toward the bus (table above).
- [F] No translator's output enable is under FPGA control, so each always drives one of its sides ("Where the 125 PL pins go"; `zz9000-manual-r1` p2; `zz9000-manual-r3` p2).
- [F] `DIRADDR2` turns U3 and U6 together, so driving the strobes also drives `A1-A7` and `/CCS` (table above).
  [F] The specification has a Zorro III master drive all of that group but `/CCS` (`zorro3` §3.2.1 p34, §4.6-§4.7 pp47-49); a Zorro II master drives `/AS`, `/UDS`, `/LDS`, `READ` and `A1-A7`, and the group also holds `DOE` and pins 51, 97 and 98, in Zorro II `(/VMA)` and two no-connects (`zorro3` Appendix A.1 pp77-78).
- [F] Neither board can run a master's cycle that follows the specification: a Zorro III master ends its cycle on `/DTACK` and a Zorro II master samples it (`zorro3` §3.1.2 pp33-34, §2.3.6 p29), and on both boards `/DTACK` has a driver and no path back to the FPGA (table above).
- [F] `/OWN`, which a Zorro II master must assert, is unconnected on both boards; `/BGACK` can be asserted on the Replica alone and read on neither, and a Zorro II master must see it negated first (`zorro3` §2.3.5 pp27-28).
- [F] `FC0-FC2`, which a Zorro III master drives, and `/BERR`, which every card must monitor, are unconnected on both boards (`zorro3` §4.6 p48, §4.3 p45).
- [F] Neither board can run a burst as master: the Replica wires `/MTCR` as an input and `/MTACK` as an output, the slave's direction, and the stock board connects neither (`zorro3` §4.7 pp49-50).
- [F] `SenseZ3` (edge pin 91) is unconnected on both boards; a Zorro II backplane grounds it and a Zorro III backplane leaves it floating, for a card to tell which it is in (`zorro3` §4.4 p46).
- [F] At a 4.5-5.5 V supply the translator's recommended output current is 32 mA, with VOL at most 0.55 V at 32 mA and 4.5 V (`lvc8t245` §5.3 p7, §5.6 p9), against the Standard driver's 64 mA at +0.4 V; as a slave the card already returns read data through translators of this type (`fw@cfbb910:mntzorro.v:L797-798`).
  [F] U24's recommended output current is 24 mA at a 3 V supply (`lvc06a` p3).
- [F] A note in the firmware repository's history states, from the RTL and the constraints and without the schematic, that the stock board routes the strobes through unidirectional level shifters (`fw@4b12ca4:notes/zz9000net-rx-pushmodel-plan.md:L10-15, L54-57`); on the R-1 and R-3 drawings that holds for `/DTACK` alone (table above).

### Not established

- Whether the R-2 drawing, or a stock board later than the R-3 drawing, differs: the firmware's history names an R5 board (`fw@4b12ca4`, commit message), and no schematic of one was read.
- Whether a board earlier than R-1 routed `/MTCR`.
- What a backplane does while a card is master: whether the bus controller drives or releases `/CCS` outside Zorro II address space, who drives `DOE` for a Zorro II master, what holds `/MTCR` negated, and what level undriven `FC0-FC2` take, which the specification gives only for a Zorro II master on a Zorro III backplane (FC1 = 0, `zorro3` §2.3.6 p30); a backplane's schematic would show them.
- [R] Which bus-controller revisions grant a Zorro III card's request varies by Buster revision; no file read covers it, and the controller's documentation would verify it.
- Whether turning the translators round meets the master timings of `zorro3` chapter 5: no analysis was made; a static timing analysis of the translator and FPGA delays would settle it.
- Whether ball U13, whose configuration function is PUDC_B ("PUDC_B"), carries any restriction as an output; `ug470` would settle it.
- The state of the FPGA pins on U24's `/MTACK` and `/BGACK` inputs while the FPGA configures, which the netlist does not show ("PUDC_B").

## PS MIO and the J5 header

[F] Header J5 "MIO" (2×7, 3.3 V) and what else each pin reaches (`replica@96bdef0`, netlist):

| J5 pin | Signal | Other loads on the Replica |
|---|---|---|
| 1, 2 | MIO14, MIO15 | None |
| 3, 4 | MIO12, MIO13 | ADAU1701 I2C (PS I2C1) |
| 5 | MIO10 | HDD LED through U24 |
| 6 | MIO11 | None; the firmware pulses it at boot (`topics/zynq-pin-budget.md`, "Spare MIO on the module") |
| 7 | MIO8 | None; [R] a boot-voltage strap |
| 8 | MIO9 | None |
| 10 | MIO0 | None |
| 11 | `+3V3` | — |
| 13, 14 | Ground | — |
| 9, 12 | Unconnected | — |

- [F] UART1 (MIO48/49) reaches header J12 (TX, RX, ground) through U19, a TXS0108E with VCCA on `+1V8` and VCCB on `+3V3`; I2C0 (MIO50/51) reaches the SiI9022A's configuration pins through the same part (`replica@96bdef0`, netlist).
- [F] UART1 is the console, standard output at base 0xE0001000, and the only UART the PS7 configuration enables (`fw@bdfd8b0:zz9000_project.tcl:L1180-1181`; `ZZ9000_proto.sdk/zz9000_bsp_new/ps7_cortexa9_0/include/xparameters.h:L22, L641, L645`).
- [R `ug585`] UART0 can map onto MIO14/15, so J5.1/J5.2 could become a 3.3 V UART0 by a PS-configuration change alone (`ps7_init`, FSBL), with no board change.
- [F] Module pins with no connection on the Replica: MDIO (J1.22/24), the XADC pins (J1.93, 95, 97, 99, 101), `SDIO0_WP` (J1.118; write-protect is disabled in the PS7 configuration, `fw@bdfd8b0:zz9000_project.tcl:L1159`), J1.136 and eMMC reset (J1.137) (`replica@96bdef0`, netlist).
- [F] PS USB0 runs to an on-board FE1.1s hub (U106), which feeds the external port P1 and internal header J112 (`replica@96bdef0`, netlist, `ZZ9000-USB/` sheet).

## Expansion and audio headers

[F] `replica@96bdef0`, netlist:

| Header | Pins |
|---|---|
| J10 "EXPANSION" (2×7) | 1 ADAU1701 reset; 2 `SDATA_OUT0`; 3 `Free7`; 4 serial-input BCLK; 6 `SDATA_IN0`; 8 output LRCLK; 10 output BCLK; 11 `+5V`; 12 `+3V3`; 13, 14 ground; 5, 7, 9 unconnected |
| J111 (1×5) | ADAU1701 `OUT2L`/`OUT2R` (2, 3), `SDATA_IN1` (5), ground (1, 4) |
| J110 | ADAU1701 `SDATA_OUT2`/`SDATA_OUT3`, `+3V3`, ground |
| J7 | SiI9022A audio: S/PDIF, MCLK, WS, SD0, SD1, SCK, interrupt, ground |
| J12 | Console UART: TX, RX, ground |
| J4 | Jumper: U24's interrupt output to `/INT6` or `/INT2` |
| J30 | VGA output from the ADV7125 |

## Video slot (J8, J9)

- [F] J8 "SlotIDC_IN" carries the A4000 video-slot edge signals (VS1, VS2), and net ties NT1-NT32 join it to J9 "SlotIDC_OUT" pin for pin; J9 feeds translators U7-U10 into the PL (`replica@96bdef0`, netlist).
- [F] With VCCB at 5 V, those translators need VIH = 0.7 × VCCI on their B-side data inputs, 3.5 V (`lvc8t245` §5.3, p7), so a 3.3 V parallel-video source does not meet it [G].
- [G] Feeding J9 replaces native capture, because J9 and the video slot share nets; that is why DPI into the capture path is rejected [D] DEC-005 (`sections/options-rejected.md`).

## VGA-USB add-on (for a stock ZZ9000)

- [F] The add-on is a card for the MNT ZZ9000 with VGA output and internal USB ports (`addon@40bca90:README.md:L3`).
- [F] The Replica carries both functions on board (ADV7125 U23, FE1.1s hub U106), so the add-on applies only to a stock ZZ9000 (`replica@96bdef0`, netlist).
- [F] It is an interposer: the module plugs into its sockets U12/U13 (Amphenol 61083-141402LF), and its plugs UZ12/UZ13 (61082-141402LF) go into the carrier's module sockets (`addon@40bca90`, netlist).
- [F] Every pin the add-on connects passes straight through except the USB0 data pair (J1.19, J1.21), which it routes into an FE1.1s hub (U106) and passes on from a downstream port (`addon@40bca90`, netlist).
- [F] It taps the 24 HDMI data lines (HG0 included) and DE into an ADV7125 VGA DAC (U23), IDCK through buffer U22, and HSYNC and VSYNC through R31/R32 (`addon@40bca90`, netlist).
- [F] It also taps `USB_VBUS_EN` (J1.30) through R159 into the hub's VBUSM pin (`addon@40bca90`, netlist).
- [F] It leaves J2.67-78, the GTP signal pins on J2.111-140, MDIO, the XADC pins (J1.93, 95, 97, 99, 101), `SDIO0_WP` and J1.136 unconnected (`addon@40bca90`, netlist).
- [G] So a 7015's extra bank-13 or GTP pins can be reached only by a board between the module and the add-on.
- Its floppy-lead inlet is in `topics/power-domains.md`, "Stock ZZ9000 with the VGA-USB add-on".
