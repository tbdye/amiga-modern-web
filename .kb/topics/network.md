# Network

Scope: how the browser chip reaches the network, what the card's Ethernet does today (its filters, each step a received frame takes, and its link speed), the options compared and which are not under study, and how the control link stays off the network.
Status: draft

## Status

No decision records the browser chip's network attachment; everything here marked Proposed is a proposal.

| Question | Standing |
|---|---|
| Does browser traffic go through the Amiga's TCP/IP stack? | [G] Proposed: no; the browser chip has its own network connection and address, and the Amiga keeps using the card's Ethernet as it does today. [D] DEC-037: the Amiga keeps a TCP/IP address of its own |
| One socket or two? | [G] Proposed: with one card, one RJ45 shared through an on-card switch chip; with an SBC, the SBC's own Ethernet or Wi-Fi; open with packaging (K68, DC-D) |
| Does the control link carry browser traffic? | [G] Proposed, for the card design: never; it carries control, input, clipboard, window geometry, files, a heartbeat and, with the default DVI EDID, the browser's audio (K7), and is not reachable from the network. [G] This does not describe a session with a second computer across the home network (`topics/link-and-address.md`, "Safety on the home network") |

## The card's Ethernet today

- [F] The firmware terminates Ethernet on the A9 and bridges raw frames to the Amiga; it has no TCP/IP stack (`sections/architecture.md`, "Control link (K8)").
- [F] GEM0 is the only Ethernet controller the PS7 configuration enables, and it is the port bridged to the Amiga (`sections/architecture.md`, "Control link (K8)").
- [F] On the Replica, the Ethernet jack J3 is a 0826-1G1T-23-F MagJack, and the PHY's four MDI pairs run straight to it from U12 pins 7, 9, 10, 12, 13, 15, 16 and 18 (`replica@96bdef0`, netlist).
- [F] Each of J3's four centre taps goes to GND through its own 100 nF capacitor (C29-C32), and there is no bias rail (`replica@96bdef0`, netlist).
- [F] Both supported PHYs, Micrel KSZ9031 and MotorComm, go through the same `micrel_auto_negotiate` routine (`fw@bdfd8b0:os/ethernet.c:L1007-1020`), which sets `link_speed = 100` under a FIXME, advertises 10 and 100 Mb/s and clears the 1000BASE-T advertisement (`:L1085-1121`).
- [F] The firmware README describes the Ethernet as gigabit (`fw@bdfd8b0:README.md:L40, L658`), but the PHY set-up advertises only 10 and 100 Mb/s (`fw@bdfd8b0:os/ethernet.c:L1085-1121`).
- [G] So the link runs at 10 or 100 Mb/s whatever the README says.
- [F] A 1000 Mb/s branch exists in that routine, part of it commented out, and is never selected; the controller's clock and speed are then set from the speed the transceiver reports (`fw@cfbb910:os/ethernet.c:L1268-1286, L1354-1355`).
- [G] So a gigabit port at the other end of the cable links at 100 Mb/s.
- [G] The firmware sets the controller's speed from the negotiated one once: the routine that does so has one caller, in a start-up state that is not entered again (`fw@cfbb910:os/ethernet.c:L640-675, L1319-1356`).
- [F] The KSZ9031 transceiver negotiates again at each link-down to link-up transition, and its automatic MDI/MDI-X is on by default, so it needs no crossover cable (`ksz9031` p16-17).
- [F] The firmware's link-ready state is not cleared when the cable is pulled later (`fw@cfbb910:os/ethernet_mcast.c:L54-56`).

What the firmware and the Amiga's driver do with a frame, read at `fw@cfbb910` and `drivers@cb6a1c4`.
In the table a citation with no source ID is `fw@cfbb910`, `drivers` citations are at `cb6a1c4`, and `os/` and `bsp/` expand per `sources.md`.

| Step | What happens | Citation |
|---|---|---|
| Filter | [F] One station address, in the first of four filters, set by the Amiga's driver or the card's configuration file; the other three are zeroed at reset. Broadcast is accepted. The Amiga's driver sets a 64-bucket multicast hash through the firmware, and every Amiga reset clears it. Unicast-hash matching is switched on by the vendored reset and nothing switches it off. Promiscuous reception, 1536-byte reception and the receive-only-VLAN filter are off. Receive checksum checking is on, and the controller discards a frame with a bad IPv4, TCP or UDP checksum before the firmware sees it | `os/ethernet.c:L376, L1044`; `os/main.c:L631-633, L1447-1470`; `os/ethernet_mcast.c:L15-47, L81-86`; `os/ethernet.h:L30`; `drivers:docs/cli-tools.md:L59-60`; `bsp/xemacps.h:L222-235, L374-384, L435-444`; `bsp/xemacps.c:L119, L310, L334-336, L385-390, L411-413`; `bsp/xemacps_control.c:L200-209, L483-486, L519-520`; under `os/` nothing calls `XEmacPs_SetOptions` or `XEmacPs_ClearOptions`, the only direct writes of the configuration register are `os/ethernet.c:L331-334` and `os/ethernet_mcast.c:L26-46`, and the unicast-hash enable is used only at `bsp/xemacps.c:L336` |
| Arming | [F] Before any frame arrives, each of the 32 receive descriptors is pointed at the next slot round the receive backlog, and that slot's header is zeroed (the backlog's size and its pause rule: `sections/firmware-and-rtl.md`, "What the card offers today") | `os/ethernet.c:L124-131, L198-202, L718-737, L757-797`; `os/ethernet.h:L70` |
| Arrival | [F] The controller writes the frame into that slot. The receive handler runs inside the controller's interrupt, on slots mapped uncached; it reads the descriptor's length and no byte of the frame, gives the frame a serial, and accepts slots strictly in order: a frame in any slot but the one the write pointer names is dropped as a mismatch | `os/ethernet.c:L174-178, L406-407, L799-924` |
| To the Amiga | [F] The main loop raises an Amiga interrupt while the backlog is not empty. The 68k driver reads the presented slot's header through the card's Zorro window, copies the frame and acknowledges its serial, and the backlog then advances one slot. The driver takes an all-zero header for an empty slot and waits without acknowledging, and it counts a gap in serials as overruns | `os/main.c:L1438-1445, L2277-2279`; `os/ethernet.c:L151-171, L926-928, L962-1019`; `drivers:net/device.c:L94, L519-531, L1270-1304, L1365-1370`; `drivers:net/rx.c:L11-75` |
| Rebuild | [F] The backlog is rebuilt, and everything waiting in it dropped, on an Amiga reset, a write of the hardware address, a receive-offset request that changes the offset, and a transmit time-out. The firmware advertises the receive-offset capability, and the driver then asks for the offset when it starts receiving and hands it back when it stops | `os/ethernet_mcast.c:L51-52, L81-92`; `os/ethernet.c:L576-631, L1029-1052, L1470-1481`; `drivers:net/device.c:L1263-1267, L1375-1376` |
| From the Amiga | [F] The 68k writes one frame into a single transmit buffer and its length to a register; the firmware sends it and waits up to about 1 ms for completion; there are two transmit descriptors | `os/main.c:L1434-1435`; `os/ethernet.c:L96, L1421-1488`; `os/ethernet.h:L71` |
| On the ARM | [F] Nothing on the card consumes a frame: beside the missing TCP/IP stack, there is no ARP or UDP code | No match for `ethertype`, `lwip`, `udp`, `arp` or `tcp/ip` in the Ethernet sources under `os/` |

- [G] Because unicast-hash matching uses the multicast hash, a single-station frame whose address falls in a bucket the driver has set is accepted too; the driver's exact-membership filter covers group frames only (`drivers@cb6a1c4:net/device.c:L266-283`).
- [F] With no driver draining the backlog the descriptors run out, and a firmware comment calls the drops that follow expected and self-healing (`fw@cfbb910:os/ethernet.c:L1068-1079`).
- What a service that kept a second computer's frames on the card would meet in these steps: `topics/card-ethernet-sharing.md`.

## Options

Every assessment in this table is [G].

| Option | Control-link load | Amiga CPU | Security | Setup | Standing [G] |
|---|---|---|---|---|---|
| A. The browser chip's own Ethernet or Wi-Fi | None | None | An internet-facing chip, like any PC; see `topics/security.md` | Two network ports; the chip uses DHCP | Proposed |
| A′. As A, with one card and one RJ45 shared through an on-card switch chip | None | None | The Amiga and the chip share an upstream port, so a guest network needs VLAN tagging in the switch chip and a VLAN-capable router | One cable, two addresses | Proposed for one card |
| B. Share the card's PHY with the A9 forwarding every frame | None if switched in hardware; otherwise every frame | None | Browser traffic passes through the Zynq | One cable | Not under study in software; switching in hardware is A′ |
| C. Tunnel through the Amiga's TCP/IP stack (bsdsocket) | All web traffic | Very high on a 68k | The Amiga becomes the chip's gateway | One network configuration | Not under study |

## Not under study

- [G] **Tunnelling through the Amiga's TCP/IP stack:** every byte of web traffic would cross the control link and the 68k, at the receive rates published for Amiga stacks (`topics/target-config-rates.md`, "Network receive"; the card's receive path is under "The card's Ethernet today"), the Amiga becomes the chip's gateway, and browsing stops whenever the Amiga's stack is down.
- [G] **The A9 forwarding the chip's traffic through the card's PHY:** the A9 would handle every frame, browser traffic would pass through the Zynq, and it works against SR16's rate limit on the control link (`topics/plane-safety.md`); a switch chip doing the same in hardware is option A′.

## Configuration

- [G] Proposed: the chip takes its address by DHCP, its network settings come from an Amiga preferences tool over the control link, and proxies use Chromium's own proxy settings.
- [G] So browsing works with no Amiga TCP/IP stack running.

## The control link and the network

- [G] Proposed, for the card design: the control link carries control, input, clipboard, window geometry, files, a heartbeat and, with the default DVI EDID, the browser's audio (K7), never the browser's network traffic, and is not reachable from the network.
- [G] Where the engine runs on a second computer reached across the home network, the session is itself a network connection, and this does not describe it (`topics/link-and-address.md`, "Safety on the home network").
- [G] Over the card's Ethernet port that needs an isolated switch port plus a VLAN, or a second MAC, because GEM0 is the Amiga's own port; otherwise the link shares the Amiga's LAN segment (`sections/architecture.md`, "Control link (K8)").
- [R] On Ethernet, SR16's real bound is the GEM receive ring times the line rate, not A9 rate limiting (`topics/plane-safety.md`, "Evidence behind the rules").
- [G] A point-to-point Ethernet control link on an existing board's RJ45 needs no hardware change, but it takes the port the Amiga otherwise uses for its LAN, and it needs a receive classifier (by EtherType or UDP port) in the firmware, because the firmware bridges raw frames and has no TCP/IP stack (K54).
- The physical layer of the control link is open (K8).

## Placement

- [G] Proposed, for a browser chip that reaches the Amiga by a control link and not across the home network: the chip on a guest network or VLAN, with LAN destinations blocked in the chip's image as a second layer.
- [G] Where the session with the Amiga crosses the home network, a guest network that keeps its clients off that network cuts the second computer off from the Amiga (`topics/link-and-address.md`, "Safety on the home network").
- [G] With one shared socket (A′), a guest network needs VLAN tagging in the switch chip and a VLAN-capable router.
- LAN exposure per placement is in `topics/security.md`, "Network placement".
