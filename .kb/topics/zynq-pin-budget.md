# Zynq pin budget

Scope: PL pin and bank budgets for the 7020, 7015 and 7020-V2 modules and for chip-down packages, under V-tracked and PCIe.
Status: draft

Connector pins use the 7020 numbering (J1/J2; `sections/gotchas.md`).
Pin-map data: `evidence/z15.json` (MYC-C7Z015), `evidence/z20.json` (MYC-C7Z010/20), reproducible per `evidence/README.md`.
Replica facts come from its netlist at `replica@96bdef0` (not public; not reproducible outside the project).

## The modules on the Replica footprint

- [F] The 7020 module exposes 125 PL pins (bank 35: 50, bank 34: 50, bank 13: 25); the 7015 module exposes 137 (bank 13: 37) (`evidence/z20.json`, `evidence/z15.json`).
- [F] The Replica connects all 125 of the 7020's PL pins (`replica@96bdef0`, netlist).
- [F] The 7015 adds 12 bank-13 pins on J2.67-78 and GTP bank 112 (4 lanes, 2 reference clocks) on J2.111-140 (`evidence/z15.json`); the Replica leaves J2.67-78 and the GTP signal pins unconnected, and the interleaved GND pins are on GND (`replica@96bdef0`, netlist).
- [F] Every power, GND, PS MIO, Ethernet, USB and VCCO pin matches between the two maps, and every PL pin stays a PL pin in the same bank (`evidence/z15.json`, `evidence/z20.json`).
- [F] All module VCCO pins are on `+3V3` on the Replica, so every PL bank runs at 3.3 V (`replica@96bdef0`, netlist, U12.59/60, U13.35/36, U13.81/82).
- [F] J2.68/70 and J2.76/78 are clock-capable pairs L13 and L14 in bank 13 (`evidence/z15.json`).
- [F] MGTREFCLK0 is on J2.135/137 and MGTREFCLK1 on J2.138/140 (`evidence/z15.json`; `myir-7015-pinmap` p1).
- [F] Of the 125 Replica PL pins, 36 change clock-capable status on a 7015 (16 gain, 20 lose); only J2.28 carries a declared clock, `I2SO_BCLK` (`evidence/` pair comparison; `fw@8778ef3:xdc/zz9000.xdc:L270`).
- [F] `xdc/zz9000.xdc` constrains Zorro 61, HDMI-out parallel 28, capture 26 and I2S 6 ports (`fw@8778ef3:xdc/zz9000.xdc`).
- 7020-V2: same connectors and size as V1, so the same budget [F `myir-7020v2`].

## Fresh budget for a new board

| Group | Pins | Note |
|---|---|---|
| Zorro | 59 | 61 constrained, less /BR and /BG, which the RTL never uses: `ZORRO_NBRN` is tied off and `ZORRO_NBGN` is declared but never read (`fw@8778ef3:mntzorro.v:L140, L799-800`) [F]; strapping `ZORRO_ADDRDIR2` would save one more |
| Capture | 26 | Behind 74LVC8T245 translators |
| I2S | 6 | ADAU1701, 3.3 V |
| HDMI out, today's 24-bit bus | 28 | |
| HDMI out, 12-bit dual-edge | 16 | 12 data + IDCK + HSYNC + VSYNC + DE |
| Receiver input (V-tracked) | 28 | 24-bit RGB + clock + HSYNC + VSYNC + DE |
| Receiver HPD/INT/RESET | 3 | Could move to MIO |
| SoC power-good and isolation enables | 2-4 [G] | Aux-domain check |
| Receiver I2S | +4 | Only with an HDMI (not DVI) EDID |
| PCIe PERST# | 1 | PCIe options only |

[F] The SiI9022A runs 12-bit dual-edge input to 165 MHz at 3.3 V IOVCC (`sii9022a` Table 3.13, p19).
[F] Above 82.5 MHz it requires IDCK high ≥ 3.6 ns, low ≥ 2.4 ns and duty 40-60% (`sii9022a` Table 3.13, p19).
[F] At 148.57 MHz (6.73 ns) that leaves a 53.5-60% duty window, so a 50% clock fails (arithmetic on the above); the 16-pin bus at 1080p depends on K51.

## Voltage: why Zorro and capture stay at 3.3 V

[F] SN74LVC8T245 maximum delays with VCCB = 5 V (`lvc8t245` §5.7 p10, §5.9 p11):

| ns, max | VCCA 1.8 V | VCCA 3.3 V |
|---|---|---|
| B→A (bus to FPGA) | 23.4 | 6.0 |
| A→B (FPGA to bus) | 7.1 | 4.4 |
| OE→B disable | 10.3 | 6.3 |

- [R] Zorro III limits /FCS to /SLAVEn at 25 ns (`zorro3`); the translator alone takes 23.4 + 7.1 = 30.5 ns at VCCA 1.8 V against 10.4 ns at 3.3 V.
- [G] So Zorro timing signals, capture and the three open-drain bus drivers keep 3.3 V banks: 88-91 pins at 3.3 V.

## Package results under V-tracked [G]

HR pins at 3.3 V; sums use 91 Zorro, capture and I2S pins.

| Part and package | Budget | Result |
|---|---|---|
| Chip-down 7020 CLG484 (200 HR, `ds190` p4) | 91 + 28 HDMI + 28 receiver + 2-4 + 3 = 152-154; 156-158 with I2S | Fits, 140 BRAM36; HDMI and formatter unchanged; XDC re-pinned |
| Same, with frame-buffered V (P5) | A ×16 DDR3 bank takes 50 HR at 1.5 V, leaving 150 | 147 of 150 if the slow controls move to MIO; otherwise forces the 16-pin HDMI (K51) |
| Chip-down 7015 CLG485 (150 HR) | 140-146 with the 16-pin HDMI | Tight; 95 BRAM36; 1080p depends on K51; no room for PL DDR (P5) |
| 7030 FBG676 (100 HR + 150 HP) | HDMI 28 at 1.8 V IOVCC on HP; receiver translated onto HP | Fits |
| MYIR 7015 module (137 PL) | 136-139 with slow controls on 3-4 spare MIO | Zero margin; with I2S, 4 short |
| Replica as host (125 PL + 12 on a 7015) | 28-pin receiver against 12 free | Does not fit |

## PL DDR on a 7015 loses 1080p

- [F] The 7015 CLG485 has 150 HR in three 50-pin banks (`ds190` p4); a DDR3 bank leaves 100.
- [G] HDMI from HR pins as TMDS then caps the pixel clock near 125 MHz at −2/−3, from the OSERDES DDR LVDS limit of 1250 Mb/s (`ds187` Table 50, p33; −1: 950 Mb/s), so 1080p60 RTG and the centred-1080p profiles are lost [D] DEC-009.
- [F] PL DDR3 runs at 800 Mb/s on −1 and −2 (`ds187` Table 51, p33), so a ×16 gives 1.6 GB/s against about 1 GB/s of un-genlocked 1080p60 V at 32 bpp [G].

## Spare MIO on the module

- [F] The module brings out MIO0 and MIO8-15 (`evidence/z15.json`, section 1 pins 107-127); on the Replica, MIO10 drives the HDD LED and MIO12/13 are the ADAU1701 I2C (`replica@96bdef0`, netlist; I2C1 on MIO 12-13 at `fw@8778ef3:zz9000_project.tcl:L926`), leaving MIO0, 8, 9, 11, 14 and 15.
- [F] The reset pin J1.133 is `PS_500_RESET_OUTn` in the 7020 map and `PS_500_RESET_OUT` in the 7015 map (`evidence/z20.json`, `evidence/z15.json`); polarity is unconfirmed (K21).
- [F] The console is UART1 on MIO 48-49 (`fw@8778ef3:zz9000_project.tcl:L1181`), so MIO14/15 are free for UART0 [G].
- [R] MIO8 is a boot-voltage strap; 3-4 MIO are realistically usable for slow controls.
