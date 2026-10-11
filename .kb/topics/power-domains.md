# Power domains

Scope: where each part of the design draws power: Zorro slot limits, the Replica's power tree, PSU-lead inlets, machine PSU rails, per-browser-chip arithmetic, and the checks a second power domain needs; thermals are open (K18, `unknowns.md`).
Status: draft

Replica facts come from its netlist at `replica@96bdef0` (not public).
The budgets and checks below are planning values for a design under study, not measurements.

## Two domains

- [D] DEC-003: the browser chip may take power from a spare drive lead off the machine's PSU, a floppy-type connector by default, or from its own supply; the slot's limits do not bind it.
- [G] The Zynq side (Zorro buffers, the Zynq, capture, HDMI out, audio) stays on slot power: only the Zorro buffers must draw from the backplane, but keeping the rest there too ties it to the Amiga's power and reset, so native video never depends on an auxiliary lead (DEC-005).
- [G] The browser chip cannot count on the slot: a CM5's power input is rated to 5 A at 5 V (`cm5-ds` p6) and its peak draw is open (K16), against 2.0 A per slot at +5 V.

## Zorro slot limits

| Rail (edge pin) | Zorro III, per card | Zorro II |
|---|---|---|
| +5 V (5, 6) | 2.0 A [F `zorro3` §2.3.1 p24, §6.2 p63] | 2.0 A per slot; the older 4.0 A allowance for one card is no longer supported [F `zorro3` §2.3.1 p24] |
| +12 V (10) | 500 mA [F `zorro3` §4.1 p44, §6.2 p63] | No per-slot limit; the A2000 specifies 8.0 A for the whole system, mostly for drive motors [F `zorro3` §2.3.1 p24] |
| −5 V (8) | 60 mA [F `zorro3` §6.2 p63] | No per-slot limit [F `zorro3` §2.3.1 p24] |
| −12 V (20) | 60 mA [F `zorro3` §6.2 p63] | No per-slot limit; the A2000 specifies 0.3 A for the system [F `zorro3` §2.3.1 p24] |

- [F] The Zorro III figures are minimums: a backplane is free to supply more (`zorro3` §6.2 p63).

## The Replica's power tree

[F] `replica@96bdef0`, netlist:

| Source | Path | Loads |
|---|---|---|
| Slot +5 V (`5V_IN`) | F1, JK-nSMD350L-12 PPTC, to `+5V` | Module, translator B sides, the rest of the 5 V logic |
| Slot +5 V | F4 (1 A) | J17, 5 V fan |
| Slot +5 V | F6 (1 A) | Case LED |
| Slot +12 V (`12V_IN`) | F2 (0.5 A), FB101, U104 78M09 regulator, to `+9VA` | Two OPA1692 audio op-amps (U101, U102) and passives |
| Slot +12 V | F5 (1 A) | J18, 12 V fan |
| Floppy lead J125 (TE 171826-4), pin 4 (`AUX_12V`) | F3, 1206L250/16AR PPTC, then FB102 and FB103 | Two LMR33630 bucks: U105 to `+5V0_USB_A` (external port and hub), U111 to `+5V0_USB_B` (internal header ports) |
| Floppy lead J125, pin 1 (+5 V) | Unconnected | — |

- [F] F1 holds 2.60 A at 50 °C (3.50 A at 25 °C) (`jk-nsmd350l` thermal derating chart, pp3-4), so the 2.0 A slot limit binds `5V_IN`, not F1.
- [F] F3 holds 2.50 A in still air at 25 °C (`lutefuse-1206l` p4).
- [G] `+9VA` draws tens of mA, and F5 passes only the fan's current, so a fan of 400 mA or less keeps +12 V inside the 500 mA Zorro III figure.
- [F] The MYC-C7Z015 module is rated 5 V, 0.5 A (`myir-7015`); with capture it fits the 2.0 A slot limit [G].

### Stock ZZ9000 with the VGA-USB add-on

- [F] The VGA-USB add-on for a stock ZZ9000 takes a floppy lead on J123 and passes it through to J124 (both 171826-4); its +12 V feeds its own USB buck through a 1206L250/16AR, and +5 V is passed through unused (`addon@40bca90`, `README.md:L3` and netlist, not public).

## Browser-chip domain: PSU-lead inlets

- [F] The ATX12V guide's floppy drive connector is AMP 171822-4 or equivalent on 20 AWG wire: pin 1 +5 V, pins 2 and 3 ground, pin 4 +12 V (`atx12v` §4.5.5, p39).
- [F] The TE 171826-4 header's contact is rated 5 A maximum (`te-171826` p2).
- [R] The PSU-side receptacle contact is rated about 2 A and binds; its datasheet would settle it (K36).
- [G] Planning value per inlet: 2 A at +5 V plus 2 A at +12 V, about 34 W, reached only when the load splits across both rails.
- [R] How many spare floppy leads a machine has is unknown (K37); on a Replica, J125 already takes one.

## Machine PSU per rail

These bind only when the browser chip feeds from the machine's PSU.

| Machine | +5 V | +12 V | −12 V |
|---|---|---|---|
| A4000 | 20.0 A [F `a4000-sm` p52] | 4.0 A, 8 A surge [F `a4000-sm` p52] | 600 mA [F `a4000-sm` p52] |
| A2000 | [R] | 8.0 A system [F `zorro3` §2.3.1 p24] | 0.3 A system [F `zorro3` §2.3.1 p24] |
| A3000 | [R] | [R] | [R] |

- [F] The A4000 figures are the functional specification's stated power-supply requirements, not a supply's label rating (`a4000-sm` p52, section 6-14).
- [R] Upgraded ATX-style supplies are common in these machines.

## Per browser-chip class [G]

| Chip | Draw | One inlet gives | Fit |
|---|---|---|---|
| CM5 | Power input rated to 5 A at 5 V, a 25 W ceiling [F `cm5-ds` p6; G arithmetic]; typically about 900 mA operating and 400 mA idle [F `cm5-ds` p16, §3.3] | 10 W direct from +5 V at 2 A, or about 22 W through a 12 V to 5 V buck from +12 V at 2 A (92% efficient) | One inlet; whether 22 W covers the CM5's peak is open (K16) |
| RK3588 module | About 15-20 W [R] | About 34 W split across both rails | One inlet split across rails, two for margin |
| x86 board | 15-45 W [G]; SoC TDP 6-25 W [R] | About 34 W split | One inlet at the 15 W end; at a 40 W planning point after a 92% converter, about 3.6 A on +12 V (two inlets on that rail alone, most of an A4000's 4.0 A) or about 8.7 A on +5 V (five or more inlets), so its own supply or an upgraded PSU |

- [F] The CM5's consumption figures exclude what its 3.3 V and 1.8 V regulators supply to peripherals, up to 600 mA each (`cm5-ds` p16, §3.4).

## Own supply [G]

- A second internal PSU, or an external brick through a DC jack on the slot bracket.
- The machine PSU then stops binding; thermals (K18) and the checks below bind instead, more so because the two supplies rise and fail independently.

## Aux-domain checks (K35) [G]

1. **Inrush:** bulk capacitance behind each PPTC against the PSU's surge rating; soft-start where it exceeds it.
2. **Per-rail fusing** on the browser-chip domain.
3. **Sequencing:** slot and aux rails may rise in either order, even from one PSU, and do from separate supplies; the plane's fail-safe rules cover it (SR9, SR10, SR14 in `topics/plane-safety.md`).
4. **No back-feed:** a powered browser chip with the Zynq side off must not drive HDMI into an unpowered receiver whose outputs face PL banks, I2S into the ADAU1701, PCIe into unpowered transceivers, or anything into the Zorro buffers, and must not back-power slot +5 V through ESD diodes; use power-good gating or isolation with Ioff-rated level shifters.
5. **Ground return** through the aux connector's ground pins, not the Zorro edge; with its own supply, a single ground reference at the card.
