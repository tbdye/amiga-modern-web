# Replica interconnect

Scope: how the Replica carrier wires the Zynq module: where the PL and PS pins go, the level translators, headers and spare I/O, the video-slot and audio headers, and the VGA-USB add-on interposer for a stock ZZ9000.
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
