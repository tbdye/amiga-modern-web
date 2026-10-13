# Connecting a second computer, and the Amiga's own address

Scope: the ways to connect a second computer that runs the browser engine to an Amiga, each link's own rate, and whether the Amiga's own address and its other network use are kept in each.
Status: current

- [D] DEC-037: a second computer and a co-processor board are both acceptable, and the Amiga keeps a TCP/IP address of its own.
- The second computer is a Linux computer that runs the browser engine; the home network is the network the Amiga is on today, with its router.
- The session is the connection that carries the engine's pixels to the Amiga and the Amiga's input back.
- [G] "The service" is a firmware service on the ZZ9000 that would keep the second computer's Ethernet frames on the card and draw their pixels there, in place of passing them to the 68k; it does not exist, and what it would meet in the firmware is in `topics/card-ethernet-sharing.md`.
- No row is judged against DEC-037 ("Not established").
- Nothing here was run, built or measured; a third party's figure is its source's own.
- A citation with no source ID is `fw@cfbb910`; `drivers` citations are at `cb6a1c4` and `linux` citations at `adc218676eef`, the commit of tag v6.12; `os/` expands per `sources.md`.
- MB = 10^6 bytes.

## The ways

Every cell without a label is `[G]`, an inference whose basis is under the heading the row names.

| # | Way | Own address kept | Connections the Amiga opens; connections opened to it; lookups by broadcast; dependence on the second computer being up | The user owns or sets up | Must be built | The link's rate |
|---|---|---|---|---|---|---|
| 1 | Both on the home network; the session runs through the Amiga's TCP/IP stack | Yes | All three work; no dependence. The session shares the one 68k and the one network card ("Through the Amiga's stack") | A second computer; a TCP/IP stack on the Amiga; a switch or router port, or Wi-Fi on the second computer | A program on each side and a protocol between them; no hardware | The card's link speed is in `topics/network.md`, "The card's Ethernet today"; what the 68k receives through it is in `topics/target-config-rates.md`, "Network receive" |
| 2a | The service; the card and the second computer both on the home switch | Yes | All three work as today, through the same socket; no dependence. Both kinds of frame share the link, one receive backlog and one flow-control mechanism (`topics/card-ethernet-sharing.md`) | As 1 | As 1, plus the service, which needs a firmware change: the firmware has no loader (`topics/arm-offload.md`, "Mechanisms in the firmware") | 12.5 MB/s on the wire at the card's link speed, shared with the Amiga's own traffic, and not a floor (`topics/card-ethernet-sharing.md`, "Sharing the link") |
| 2b | The service; the second computer cabled straight to the card and bridging to the home network | Yes, while the second computer forwards: the same address, hardware address and lookups as today. It needs two bridgeable ports ("Cabled straight to the card") | All three work. Every frame passes through the second computer: the Amiga has no network when that computer is off, restarting or not yet forwarding | A second computer with two wired ports, or with Wi-Fi that can be bridged; a cable | As 2a, plus a bridge set up on the second computer | As 2a |
| 2c | As 2b, but the second computer routes with address translation | An address of its own on a private link behind the second computer; none on the home network | Connections the Amiga opens work, with the qualifier under "Cabled straight to the card". Nothing on the home network can open one to it without a static address map. Lookups by broadcast and `.local` names do not cross ("Lookups"). No network when the second computer is off, as 2b. IPv4 only | A second computer with one wired port and Wi-Fi; a cable | As 2a, plus routing, translation and an address service on the second computer | As 2a |
| 2d | As 2b, routed without translation: a static route in the home router, or proxy ARP | Static route: an address of its own on a second subnet behind the second computer, outside the home network's range. Proxy ARP: an address in the home network's range, for which the second computer answers with its own hardware address | Connections work in both directions by address. Lookups by broadcast and `.local` names do not cross. No network when the second computer is off, as 2b. IPv4 only | As 2c; for the static route, access to the home router's settings | As 2c without translation | As 2a |
| 2e | The card's socket carries the second computer's frames alone; the Amiga's own network runs on a second network card | Yes | All three work through the second card, independent of the session's link and of the second computer | A second Zorro network card and slot; a cable; the second computer needs its own way to the Internet | As 2a, without telling two kinds of traffic apart on one link | The whole 12.5 MB/s for the session; the Amiga's own traffic at the second card's rate (`topics/target-config-rates.md`, "Network receive") |
| 3 | An off-the-shelf board inside the case, with its own cable or Wi-Fi | Yes, as 1. If its only wired port is cabled to the card instead: rows 2b to 2d | As 1 | As 1, plus power and a mounting (`topics/engine-options.md`, "Mounting and power in a big-box case") | As 1 | As 1 |
| 4 | A Zorro card that carries the second computer; the session does not use the Amiga's network | Yes ("A Zorro card that carries the second computer") | Untouched by the session | The card; the second computer's own network port or Wi-Fi | The card and its driver | Not a network link; for pixels that cross the bus, `topics/bus-and-card-rates.md`, "Bus ceilings" |
| 5 | USB, parallel port, serial port, clock port or SCSI | Yes: none uses the Amiga's network card | Untouched | `topics/other-attachments.md`, "Links" | Same | Same |

## Through the Amiga's stack

Rows 1 and 3.

- [F] The card's network driver is a SANA-II device that its documentation says works with any SANA-II stack (`drivers:docs/cli-tools.md:L58-62`; `drivers:README.md:L80-81`).
- [G] So the session can be an ordinary TCP connection through the stack's `bsdsocket.library`, with no new hardware.

| Stack | Terms | What bears on a second flow or a second interface | Source |
|---|---|---|---|
| Roadshow | [F] Sold; a free demonstration version shuts down after 15 minutes of network access | [F] Its feature list names compatibility with the AmiTCP 4.0 API, a packet filter with address translation, and an IPv4 address it assigns itself when no DHCP server answers; it names no `.local` lookup | `roadshow` |
| AmiTCP 3.0b2 | [F] Its Aminet entry is headed "GNU TCP/IP stack" and comes with a source archive; its uploader calls it the last free version | [F] A socket table of 64 slots for each opener of the library by default, stated for the AmiTCP 4.3 interface | `aminet:comm/net/AmiTCP-bin-30b2`, readme; `aminet:comm/tcp/AmiTCP-SDK-4.3`, `help/bsdsocket.guide` L482-485, L2503-2504 |
| AmiTCP 4.0 | [F] Proprietary by its readme; a demonstration version exists | [F] The version optimised for a 68020 and up is in the commercial version only | `aminet:comm/tcp/AmiTCP-demo-40`, readme |
| Genesis | [F] Its demonstration readme says it is based on the AmiTCP Professional kernel, version 4.6 | [F] More than one interface connected at a time | `aminet:comm/tcp/gendemo104`, readme |
| Miami 3.2b | [F] Its demonstration version interrupts SANA-II connections after 30 minutes and has no multicasting | [F] One interface only | `aminet:comm/tcp/Miami32b2-main`, `Miami.guide` L5426-5443, L5532-5537 |
| AmiNetXDuo | [F] MIT, with exceptions its README lists; public source | [F] Up to four interfaces; answers and resolves `.local` names, off by default and absent from its two smallest builds; IPv6; reads Roadshow's configuration files | `anx@9a6f6fc:README.md:L26-28, L236-247, L286-288, L329-331` |

- Published receive rates by stack and card are in `topics/target-config-rates.md`, "Network receive".
- The figures below take that heading's 2.6 to 2.9 MB/s through the ZZ9000 for a 68060 at 50 MHz; the conditions of each end of that bracket are stated there and hold for everything derived from it here.
- [G] The choice of stack moves the rate: on one machine and card that table has 1.280, 2.185 and 2.066 MB/s for three stacks, a spread of 2.185 ÷ 1.280 = 1.7 times; its source does not say which way the data ran.
- [G] The link is not the limit in row 1: the 2.9 MB/s the 68k receives at 50 MHz (same heading) is 23% of 12.5 MB/s.
- [G] Each 1 MB/s of other received traffic takes 1 ÷ 2.9 to 1 ÷ 2.6 = 34 to 38% of what the 68k can receive, before the receiving program's own work.
- [G] While another flow receives s MB/s the session's pixel rate is at most (1 − s ÷ receive) × the pixel rate of `topics/target-config-rates.md`, "Pixel rate": at s = 0.5, 0.81 × 1.62 = 1.31 to 0.83 × 2.08 = 1.72 MB/s; at s = 1.0, 1.00 to 1.36 MB/s.
- [G] These are upper bounds: they divide the 68k's time by bytes and count the other program's own work as free.
- [F] Exec gives the processor to a higher-priority task before a lower-priority one (`amigaos-wiki-exec-tasks`).
- Both flows also pass one receive backlog on the card: `topics/card-ethernet-sharing.md`, "One receive backlog".
- [F] One third-party observation of two uses at once: during and after a 150-second TCP receive run through a ZZ9000 at 8.4 Mbit/s, the Amiga's HTTP services answered; the machine is an A3000 with a 68030 at 25 MHz under AmiNetXDuo, with an X-Surf 100 also fitted (`anx@9a6f6fc:docs/plans/zz9000-ethernet.md:L3-6, L31-38`).

## Cabled straight to the card

Rows 2b to 2d.

- The card's socket is its only Ethernet: `topics/network.md`, "The card's Ethernet today".
- [G] So a cable from that socket straight to the second computer takes the Amiga off the home network, unless the second computer forwards for it in one of the ways below.
- Which candidate boards have a wired port, Wi-Fi or both: `topics/engine-options.md`, "Candidate computers".

| Arrangement | What it does | The Amiga's address and reach | Needs | Source |
|---|---|---|---|---|
| The second computer bridges (2b) | [F] A bridge forwards frames between interfaces by their layer-2 headers alone, whatever the layer-3 protocol | [G] Unchanged: the home router sees the Amiga's own hardware address and gives it its address; broadcasts cross; connections work in both directions. [F] Pause frames do not cross: the bridge drops them | Two bridgeable ports: two wired ports, or Wi-Fi in 4-address mode at both ends (below) | `linux:Documentation/networking/bridge.rst:L14-15, L310-319`; `linux:net/bridge/br_input.c:L376-377` |
| It routes with address translation (2c) | [F] Sessions run one way, outbound from the private network; inbound ones only through static address maps | [F] Outbound access works "in most cases", in the RFC's words. [G] A connection the Amiga opens is such a session; nothing on the home network reaches the Amiga without a map. [F] NetBIOS broadcast nodes work only within one bridged network | Forwarding and translation on the second computer; [G] an address service for the Amiga, since a router does not forward the home router's DHCP broadcasts | `rfc:3022:L130-136`; `rfc:1001:L964-968`; `rfc:1812:L5185`; `linux:Documentation/networking/ip-sysctl.rst:L10-14`; `linux:net/netfilter/xt_MASQUERADE.c:L2-3` |
| It routes without translation, by a static route (2d) | [F] Plain forwarding between two subnets | [G] The Amiga's own address on a second subnet, reachable both ways once the home router has a route to it; lookups by broadcast fail | [R] A static route in the home router; a router's manual would verify that it takes one | `linux:Documentation/networking/ip-sysctl.rst:L10-14` |
| Proxy ARP (2d) | [F] The gateway answers an ARP request for a host behind it with its own hardware address, and forwards | [G] An address in the home subnet, reachable both ways; the home network sees the second computer's hardware address for it; lookups by broadcast fail | `proxy_arp` and forwarding on the second computer | `rfc:1027:L66-87`; `linux:Documentation/networking/ip-sysctl.rst:L1643-1648` |

Conditions on every row of this table:

- [G] Start order: the Amiga has no network until the second computer is forwarding, and none while it is off or restarting; an address request made at the Amiga's start-up before then gets no answer, which bears most on a board powered with the Amiga.
- The card's link as built, at its transceiver and in the firmware: `topics/network.md`, "The card's Ethernet today".
- [G] From the facts there: no crossover cable is needed; after the second computer restarts, frames flow again only if negotiation lands on the speed first set; and the Amiga is not told that the link went away.
- [F] Wi-Fi as the bridge's uplink takes three parties: the access point and the client must both send 4-address frames, and each Linux Wi-Fi driver declares that capability itself (`linux-wireless-iw`).
- [F] Without 4-address mode Linux marks a Wi-Fi client interface as not bridgeable, and the bridge refuses it (`linux:net/wireless/util.c:L1225-1234`; `linux:net/bridge/br_if.c:L592-597`).
- [F] The driver bound to a Raspberry Pi 4's on-board Wi-Fi sets no such capability at this commit: its flags are at `linux:drivers/net/wireless/broadcom/brcm80211/brcmfmac/cfg80211.c:L7621-7629`, the file holds no `4ADDR`, and the binding is `linux:arch/arm/boot/dts/broadcom/bcm283x-rpi-wifi-bt.dtsi:L20-23`, `bcm2711-rpi-4-b.dts:L7` and `brcmfmac/of.c:L117`.
- [G] Where the Wi-Fi uplink lacks 4-address mode at either end the second computer therefore cannot bridge it, and rows 2c and 2d are what is left.
- [F] The routed rows are IPv4 only: RFC 3022 and RFC 1027 are IPv4; IPv6 crosses a bridge (`linux:Documentation/networking/bridge.rst:L317-319`); for proxying IPv6 neighbour discovery the kernel page records only that the setting exists (`linux:Documentation/networking/ip-sysctl.rst:L2259-2260`).
- [F] A second wired port can be a USB Ethernet adapter: Linux has drivers for Realtek RTL8152/RTL8153 and ASIX AX88xxx adapters (`linux:drivers/net/usb/Kconfig:L99-110, L168-198`).
- [F] Boards with more than one wired port exist: the Radxa E52C, an RK3582 board with two 2.5 Gb ports (`radxa-docs@bfb1f40:i18n/en/docusaurus-plugin-content-docs/current/e/e52c/getting-started/introduction.md:L9-11`), and the NanoPi R6S, an RK3588S board with two 2.5 Gb ports and one gigabit port (`nanopi-r6s`).
- These two are identities only: their fitness as the second computer was not researched.

## Lookups

| Means of finding | Works when | Source |
|---|---|---|
| A typed address or a DNS name | [G] Always | None |
| A `.local` name | [F] Both are on one link: such names are meaningful only on the link where they originate, so not across a router (2c, 2d). [G] The Amiga's stack must also resolve them ("Through the Amiga's stack") | `rfc:6762:L305-311` |
| A broadcast | [F] Both are in one broadcast domain (rows 1, 2a, 2b, 3): a router must not forward a limited broadcast, and Linux forwards a subnet's own broadcast only where `bc_forwarding` is set, which is off by default | `rfc:1812:L5185`; `linux:Documentation/networking/ip-sysctl.rst:L293-298` |

- [F] Across a router, a DHCP relay passes DHCP messages between clients and servers (`rfc:2131:L311-314`).
- [F] A NetBIOS name server serves point-to-point nodes, which neither send nor listen for broadcasts (`rfc:1001:L974-982`).
- [G] So in rows 2c and 2d a program that finds its peer by broadcast needs an address, a name the Amiga's resolver knows, or one of these two services.

## Safety on the home network

- [G] In rows 1 and 3 the session is a connection across the home network, so the control link of the design under study, proposed as unreachable from the network (`topics/network.md`, "The control link and the network"), does not describe it.
- [G] A guest network that keeps its clients off the home network also keeps the second computer off the Amiga in rows 1 and 3.
- [R] What a given router's guest network does is in its manual, which would verify it.
- [G] The assumption that a web page eventually takes over the computer that runs the engine carries over, with the proposed parser rules and crossing defaults (`topics/security.md`, "Threat model", "Proposed parser rules", "Proposed crossing defaults").
- [F] TLS on a 68k exists: with the card's acceleration (`topics/arm-offload.md`, "How the TLS offload is built"), and in AmiNetXDuo's `tls.library`, which its README says also runs on Roadshow, AmiTCP and Miami, with a first handshake of about 4 to 9 seconds on a 68020 (`anx@9a6f6fc:README.md:L256-265`).
- In rows 2a to 2e the second computer's frames reach the card's firmware: `topics/card-ethernet-sharing.md`, "Exposure".

## A Zorro card that carries the second computer

Row 4.

- [G] By construction the session uses neither the Amiga's network card nor its TCP/IP stack, so the Amiga's address and other network use are as they are without the browser.
- The design under study is of this kind: its browser chip is proposed to have its own network connection, and tunnelling its traffic through the Amiga's stack is not under study (`topics/network.md`, "Status", "Not under study").

## Not established

- Whether rows 2c and 2d meet DEC-037 is not judged here, and no row is: the entry speaks of the Amiga's own address, and not of the range that address lies in or of which computer answers for it; a decision would settle it.
- How the two programs identify each other, and whether the session is encrypted: no design exists; a design choice settles it.
- How the 68k's time divides between two flows, and the rate of two flows at once: the priorities the stacks and programs run at were not read, no published figure was found, and only a measurement on a machine shows it.
- What each stack does at start-up when no address server answers; whether Roadshow runs several interfaces at once [R]: each stack's documentation would settle it.
- Crossover behaviour of the second transceiver the firmware supports (`os/ethernet.c:L1160-1165`): its data sheet.
- 4-address support in the Wi-Fi driver of a Raspberry Pi 5, whose device tree at this commit has no Wi-Fi node (`linux:arch/arm64/boot/dts/broadcom/bcm2712-rpi-5-b.dts`), and in the vendor's own kernel: their sources.
- What a given home router's guest network and static routes do: its manual.
- Whether the link returns after the second computer restarts, and what the Amiga's stack then does: only hardware shows it.
- Mounting and cooling of a board inside the case, and Wi-Fi reception inside a metal case: not researched.

## Sources

`fw`, `drivers`, `linux`, `aminet`, `anx`, `roadshow` and `rfc` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `linux-wireless-iw` | Linux wireless documentation for `iw`, "Using 4-address for AP and client mode" | `https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw.html` | 2026-10-11 |
| `radxa-docs` | Radxa documentation sources | `github.com/radxa-docs/docs` | `bfb1f40` |
| `nanopi-r6s` | FriendlyElec wiki, NanoPi R6S, introduction and hardware specification | `https://wiki.friendlyelec.com/wiki/index.php/NanoPi_R6S` | 2026-10-11 |
| `amigaos-wiki-exec-tasks` | AmigaOS documentation wiki, "Exec Tasks", on task priority | `https://wiki.amigaos.net/wiki/Exec_Tasks` | 2026-10-11 |
