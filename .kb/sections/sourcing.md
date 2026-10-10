# Sourcing

Scope: channels, ordering routes and part identifiers for the costliest parts, the LCSC chip decision (DEC-015), and PCB assembly; no prices or stock.
Status: current

This file records no prices, stock or availability (`AGENTS.md`, "Rules for agents that write here"); read them from the channel when you need them.
[F] Part numbers, LCSC C-numbers and channels are as the source in each row lists them (`sources.md`, "Web pages").

## Channels

| Channel | Meaning |
|---|---|
| Broker | An unauthorized reseller |
| LCSC | LCSC/JLCPCB parts; not an AMD-authorized channel [R]; AMD's authorized-distributor list would verify it |

[G] Broker and LCSC parts have no documented chain of custody to the manufacturer; prices far below the authorized list raise relabel or remark risk.
[D] DEC-015: Zynq-7000 chips bought through LCSC are acceptable for production.

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
| Raspberry Pi CM5 Lite 4 / 8 / 16 GB (CM5004000 / CM5008000 / CM5016000) | Two HDMI 2.0 (`cm5-ds` p6) | Retail (PiShop.us) | `pishop` |
| LattePanda Mu N100, 8 / 16 GB (x86) | 260-pin module | DFRobot | `dfrobot` |
| Radxa CM5, 4 / 8 / 16 / 32 GB (RM120-D4E32R26 / -D8E64R26 / -D16E128R26 / -D32E256R26) | RK3588S2 [R], per Radxa's CM5 datasheet; the CM5 Lite is RK3582 [R]. [F] An RK3588S has only two Gen2 ×1 PCIe controllers: `rk3588s.dtsi` includes `rk3588-base.dtsi` but not `rk3588-extra.dtsi` (`linux@6c377d19d4a5:rk3588s.dtsi:L7-8`; `rk3588-base.dtsi:L2188-2266`); so the module cannot serve P3 [G] | Radxa store (arace.tech) | `arace` |
| Radxa X4, 4 / 8 / 16 GB, no eMMC (x86) | Intel N100 board, not a module; P2 form | Radxa store (arace.tech) | `arace` |

## Receiver and connectors

| Item | LCSC C-number | Source |
|---|---|---|
| ADV7611BSWZ (HDMI receiver) | C146553 | `lcsc` |
| ADV7611BSWZ-RL | C706706 | `lcsc` |
| Amphenol 61083-141402LF (MYIR module socket, two per module) | C5338666 | `lcsc` |

## Assembly

- [F] JLCPCB Economic PCBA places one side only; Standard PCBA places both sides on 1-32 layers (`jlc-capabilities`).
- [F] Minimum BGA pitch is 0.5 mm on Economic and 0.3 mm on Standard, and BGA parts get X-ray inspection (`jlc-capabilities`).
- [F] Zynq CLG400, CLG484 and CLG485 are 0.8 mm pitch (`ds190` p4).
- [G] A Zynq carrier with back-side decoupling needs double-sided placement, so it is a Standard PCBA job.
- [G] JLCPCB places module connectors, not the modules; the builder plugs the module in.
