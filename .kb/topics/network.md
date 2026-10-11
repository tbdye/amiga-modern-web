# Network

Scope: how the browser chip reaches the network, what the card's Ethernet does today, the options compared and which are not under study, and how the control link stays off the network.
Status: draft

## Status

No decision records the browser chip's network attachment; everything here marked Proposed is a proposal.

| Question | Standing |
|---|---|
| Does browser traffic go through the Amiga's TCP/IP stack? | [G] Proposed: no; the browser chip has its own network connection and address, and the Amiga keeps using the card's Ethernet as it does today |
| One socket or two? | [G] Proposed: with one card, one RJ45 shared through an on-card switch chip; with an SBC, the SBC's own Ethernet or Wi-Fi; open with packaging (K68, DC-D) |
| Does the control link carry browser traffic? | [G] Proposed: never; it carries control, input, clipboard, window geometry, files, a heartbeat and, with the default DVI EDID, the browser's audio (K7), and is not reachable from the network |

## The card's Ethernet today

- [F] The firmware terminates Ethernet on the A9 and bridges raw frames to the Amiga; it has no TCP/IP stack (`sections/architecture.md`, "Control link (K8)").
- [F] GEM0 is the only Ethernet controller the PS7 configuration enables, and it is the port bridged to the Amiga (`sections/architecture.md`, "Control link (K8)").
- [F] On the Replica, the Ethernet jack J3 is a 0826-1G1T-23-F MagJack, and the PHY's four MDI pairs run straight to it from U12 pins 7, 9, 10, 12, 13, 15, 16 and 18 (`replica@96bdef0`, netlist).
- [F] Each of J3's four centre taps goes to GND through its own 100 nF capacitor (C29-C32), and there is no bias rail (`replica@96bdef0`, netlist).
- [F] Both supported PHYs, Micrel KSZ9031 and MotorComm, go through the same `micrel_auto_negotiate` routine (`fw@bdfd8b0:os/ethernet.c:L1007-1020`), which sets `link_speed = 100` under a FIXME, advertises 10 and 100 Mb/s and clears the 1000BASE-T advertisement (`:L1085-1121`).
- [F] The firmware README describes the Ethernet as gigabit (`fw@bdfd8b0:README.md:L40, L658`), but the PHY set-up advertises only 10 and 100 Mb/s (`fw@bdfd8b0:os/ethernet.c:L1085-1121`).
- [G] So the link runs at 10 or 100 Mb/s whatever the README says.

## Options

Every assessment in this table is [G].

| Option | Control-link load | Amiga CPU | Security | Setup | Standing [G] |
|---|---|---|---|---|---|
| A. The browser chip's own Ethernet or Wi-Fi | None | None | An internet-facing chip, like any PC; see `topics/security.md` | Two network ports; the chip uses DHCP | Proposed |
| A′. As A, with one card and one RJ45 shared through an on-card switch chip | None | None | The Amiga and the chip share an upstream port, so a guest network needs VLAN tagging in the switch chip and a VLAN-capable router | One cable, two addresses | Proposed for one card |
| B. Share the card's PHY with the A9 forwarding every frame | None if switched in hardware; otherwise every frame | None | Browser traffic passes through the Zynq | One cable | Not under study in software; switching in hardware is A′ |
| C. Tunnel through the Amiga's TCP/IP stack (bsdsocket) | All web traffic | Very high on a 68k | The Amiga becomes the chip's gateway | One network configuration | Not under study |

## Not under study

- [G] **Tunnelling through the Amiga's TCP/IP stack:** every byte of web traffic would cross the control link and the 68k, an Amiga stack moves a few MB/s at best [R: a throughput measurement of an Amiga stack would verify it], the Amiga becomes the chip's gateway, and browsing stops whenever the Amiga's stack is down.
- [G] **The A9 forwarding the chip's traffic through the card's PHY:** the A9 would handle every frame, browser traffic would pass through the Zynq, and it works against SR16's rate limit on the control link (`topics/plane-safety.md`); a switch chip doing the same in hardware is option A′.

## Configuration

- [G] Proposed: the chip takes its address by DHCP, its network settings come from an Amiga preferences tool over the control link, and proxies use Chromium's own proxy settings.
- [G] So browsing works with no Amiga TCP/IP stack running.

## The control link and the network

- [G] Proposed: the control link carries control, input, clipboard, window geometry, files, a heartbeat and, with the default DVI EDID, the browser's audio (K7), never the browser's network traffic, and is not reachable from the network.
- [G] Over the card's Ethernet port that needs an isolated switch port plus a VLAN, or a second MAC, because GEM0 is the Amiga's own port; otherwise the link shares the Amiga's LAN segment (`sections/architecture.md`, "Control link (K8)").
- [R] On Ethernet, SR16's real bound is the GEM receive ring times the line rate, not A9 rate limiting (`topics/plane-safety.md`, "Evidence behind the rules").
- [G] A point-to-point Ethernet control link on an existing board's RJ45 needs no hardware change, but it takes the port the Amiga otherwise uses for its LAN, and it needs a receive classifier (by EtherType or UDP port) in the firmware, because the firmware bridges raw frames and has no TCP/IP stack (K54).
- The physical layer of the control link is open (K8).

## Placement

- [G] Proposed: the chip on a guest network or VLAN, with LAN destinations blocked in the chip's image as a second layer.
- [G] With one shared socket (A′), a guest network needs VLAN tagging in the switch chip and a VLAN-capable router.
- LAN exposure per placement is in `topics/security.md`, "Network placement".
