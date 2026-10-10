# Sourcing

Scope: channels, ordering routes and part identifiers for the costliest parts, the LCSC chip decision (DEC-015), lifecycle commitments, module connectors, and PCB assembly; no prices or stock.
Status: draft

This file records no prices, stock or availability (`AGENTS.md`, "Rules for agents that write here"); read them from the channel when you need them.
[F] Part numbers, LCSC C-numbers and channels are as the source in each row lists them (`sources.md`, "Web pages").

## Channels

| Channel | Meaning |
|---|---|
| Broker | An unauthorized reseller |
| LCSC | LCSC/JLCPCB parts; not an AMD-authorized channel [R]; AMD's authorized-distributor list would verify it |

[G] Broker and LCSC parts have no documented chain of custody to the manufacturer; prices far below the authorized list raise relabel or remark risk.
[D] DEC-015: Zynq-7000 chips bought through LCSC are acceptable for production.

## Lifecycle

- [F] AMD extends its 7 Series FPGAs and adaptive SoCs, Zynq-7000 included, through 2040 (`amd-zynq7000`).
- [F] MYIR states a minimum product life cycle of 10 years, based on its chip vendors' commitments; its lifecycle page lists no per-product dates (`myir-lifecycle`).
- [F] MYIR's V1 7020 module is discontinued, with the -V2 as its stated replacement (`sections/zynq-and-board.md`, "Modules").

## Zynq chips

| Part | LCSC C-number |
|---|---|
| XC7Z020-1CLG400C | C2988113 |
| XC7Z020-1CLG484C | C1519066 |
| XC7Z020-2CLG400I (the -V2 module's chip) | C569043 |
| XC7Z015-1CLG485C | C1519065 |
| XC7Z015-2CLG485I | C1522056 |

Source: `lcsc`.

## Modules

| Item | Notes | Channel | Source |
|---|---|---|---|
| MYIR MYC-C7Z020-V2-4E1D-766-C / -I | XC7Z020-2CLG400I; the ZZ9000 module's replacement | MYIR direct, first 2 pieces; above that by quote | `myir-order` |
| MYIR MYC-C7Z015-4E1D-766-I | XC7Z015-2CLG485, industrial only | MYIR direct, first 2 pieces | `myir-order` |
| Raspberry Pi CM5 Lite 4 / 8 / 16 GB (CM5004000 / CM5008000 / CM5016000; PiShop SC1562 / SC1568 / SC1574) | Two HDMI 2.0 (`cm5-ds` p6) | Retail (PiShop.us) | `pishop` |
| LattePanda Mu N100, 8 or 16 GB RAM, 64 GB eMMC (DFR1146 / DFR1147) (x86) | 260-pin module | DFRobot | `dfrobot` |
| Radxa CM5, 4 / 8 / 16 / 32 GB (RM120-D4E32R26 / -D8E64R26 / -D16E128R26 / -D32E256R26) | [F] RK3588S2; the CM5 Lite is RK3582, with no GPU (`radxa-cm5`). [F] An RK3588S has only two Gen2 ×1 PCIe controllers: `rk3588s.dtsi` includes `rk3588-base.dtsi` but not `rk3588-extra.dtsi` (`linux@6c377d19d4a5:rk3588s.dtsi:L7-8`; `rk3588-base.dtsi:L2188-2266`); so the module cannot serve P3 [G] | Radxa store (arace.tech) | `arace` |
| Radxa X4, 4 / 8 / 16 GB, no eMMC (x86) | Intel N100 board, not a module; P2 form | Radxa store (arace.tech) | `arace` |

## Receiver and connectors

| Item | LCSC C-number | Source |
|---|---|---|
| ADV7611BSWZ (HDMI receiver) | C146553 | `lcsc` |
| ADV7611BSWZ-RL | C706706 | `lcsc` |
| Amphenol 61083-141402LF (MYIR module socket, two per module) | C5338666 | `lcsc` |
| Hirose DF40C-100DS-0.4V(51), 100-pin 0.4 mm board-to-board (Raspberry Pi compute-module carriers [R]) | C597931 | `lcsc` |
| TE 2309409-1, 260-position DDR4 SO-DIMM socket (SO-DIMM-edge modules) | C5164025 | `lcsc` |
| TE 3-1827253-6, 220-position 0.5 mm board-to-board plug (COM Express-class modules [R]) | C194182 | `lcsc` |

- [F] The CM5 datasheet names Amphenol 10164227-1001A1RLF (1.5 mm stack) and 10164227-1004A1RLF (4.0 mm stack) as carrier connectors (`cm5-ds` p17); that the Hirose DF40C also mates is [R], which Raspberry Pi's carrier design guide would verify.
- [G] Each of these has an LCSC number, so JLCPCB assembly can source it.

## Assembly

[F] JLCPCB's two assembly services, as defined on 2026-10-10 (`jlc-capabilities`):

| Feature | Economic PCBA | Standard PCBA |
|---|---|---|
| Placement | One side only | One or both sides |
| Layers | 2, 4 or 6 | 1-32 |
| Board thickness | 0.8-1.6 mm | Any |
| Stack-up | Standard only | Any |
| Reflow | 255 ± 5 °C, fixed | 240 ± 5 °C |
| Solder-paste inspection (SPI) | No | Yes |
| Minimum BGA pitch | 0.5 mm | 0.3 mm |
| X-ray inspection | For parts such as BGA | For parts such as BGA |

- [G] Zynq packages are 0.8 mm pitch or coarser (`sections/zynq-and-board.md`, "Parts"), within both limits.
- [G] A Zynq carrier with back-side decoupling needs double-sided placement, so it is a Standard PCBA job.
- [G] JLCPCB places module connectors, not the modules; the builder plugs the module in.
- [G] Proposed assembly policy: standard assembly for everything except plug-in modules; a part JLCPCB cannot source or place is consigned, swapped for one it can, or moved onto a module.
