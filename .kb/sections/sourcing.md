# Sourcing

Scope: dated list prices, channels and stock for the costliest parts; component list prices only, no per-card totals.
Status: current

[F] Every figure was read on 2026-10-08, as shown to an anonymous visitor, from the source named in its row (`sources.md`, "Web pages").
Prices are USD unless marked **CAD**; Newark's figures are shown in CAD and are left unconverted.
Prices and stock change daily; re-read before relying on one.

## Channels

| Channel | Meaning |
|---|---|
| Auth | An authorized distributor, as flagged by findchips |
| Broker | An unauthorized reseller |
| LCSC | LCSC/JLCPCB stock; not an AMD-authorized channel [R] |

[G] Broker and LCSC parts have no documented chain of custody to the manufacturer; prices far below the authorized list raise relabel or remark risk.
[F] Authorized stock was zero for every Zynq part below at Avnet and Newark (`findchips`).

## Zynq chips

| Part | Auth (qty 1, stock) | LCSC (C-number: qty-break prices, stock) | Brokers (qty 1, stock) |
|---|---|---|---|
| XC7Z020-1CLG400C | Avnet 141.75, 0; Newark CAD 169.05, 0 | C2988113: 82.32 (1), 78.66 (30); 114 | MacroQuest 110.29, 0; Win Source 85.21, 3,330 |
| XC7Z020-1CLG484C | Avnet 156.60, 0; Newark CAD 147.94, 0 | C1519066: 97.25 (1), 93.94 (30); 57 | MacroQuest 35.65, 1,260; Win Source 71.82, 3,002 |
| XC7Z020-2CLG400I (the -V2 module's chip) | — | C569043: 88.52 (1), 78.37 (5), 76.32 (30); 970 | — |
| XC7Z015-1CLG485C | Avnet 162.00, 0; Newark CAD 150.78, 0 | C1519065: 63.32 (1); 12 | MacroQuest 146.82, 0; Win Source 80.73, 1,350 |
| XC7Z015-2CLG485I | Avnet 214.65, 0 | C1522056: 75.40 (1), 65.42 (3), 62.27 (30); 261 | MacroQuest 187.05, 0; Win Source 76.61, 6,250 |

Sources: `findchips` for Auth and Broker columns; `lcsc` for the LCSC column.
MacroQuest stock of 0 is findchips' in-stock figure; its listings also offer 1,000-5,300 pieces on request (RFQ), which are not counted here.

## Modules

| Item | Notes | Price (qty basis) | Source |
|---|---|---|---|
| MYIR MYC-C7Z020-V2-4E1D-766-C / -I | XC7Z020-2CLG400I; the ZZ9000 module's replacement | 147 / 150 (first 2 pieces; above that by quote) | `myir-order` |
| MYIR MYC-C7Z015-4E1D-766-I | XC7Z015-2CLG485, industrial only | 124 (first 2 pieces) | `myir-order` |
| Raspberry Pi CM5 Lite 4 / 8 / 16 GB (CM5004000 / CM5008000 / CM5016000) | Two HDMI 2.0 (`cm5-ds` p6) | 100 / 165 / 335 | `pishop` |
| LattePanda Mu N100, 8 / 16 GB (x86) | 260-pin module | 359 / 499; in stock | `dfrobot` |
| Radxa CM5, 4 / 8 / 16 / 32 GB (RM120-D4E32R26 / -D8E64R26 / -D16E128R26 / -D32E256R26) | RK3588 class (RK3588S2 [R], per Radxa's CM5 datasheet); page titled a time-limited discount | 89 / 119 / 179 / 299; out of stock | `arace` |
| Radxa X4, 4 / 8 / 16 GB, no eMMC (x86) | Intel N100 board, not a module; P2 form | 60 / 80 / 120; out of stock | `arace` |

## Receiver and connectors

| Item | Price (qty) | Stock | Source |
|---|---|---|---|
| ADV7611BSWZ (HDMI receiver), C146553 | 9.30 (1), 6.75 (100) | 93 | `lcsc` |
| ADV7611BSWZ-RL, C706706 | 5.64 (1), 4.84 (100) | 549 | `lcsc` |
| Amphenol 61083-141402LF (MYIR module socket, two per module), C5338666 | 4.05 (1), 3.44 (10) | 900 | `lcsc` |

## Assembly

- [F] JLCPCB Economic PCBA places one side only; Standard PCBA places both sides on 1-32 layers (`jlc-capabilities`).
- [F] Minimum BGA pitch is 0.5 mm on Economic and 0.3 mm on Standard, and BGA parts get X-ray inspection (`jlc-capabilities`).
- [F] Zynq CLG400, CLG484 and CLG485 are 0.8 mm pitch (`ds190` p4).
- [G] A Zynq carrier with back-side decoupling needs double-sided placement, so it is a Standard PCBA job.
- [G] JLCPCB places module connectors, not the modules; the builder plugs the module in.
