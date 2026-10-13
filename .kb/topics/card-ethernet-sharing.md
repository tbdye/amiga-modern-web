# Sharing the card's Ethernet with a second computer

Scope: what a firmware service that kept a second computer's frames on the ZZ9000 would meet in the firmware as built: where a frame could be claimed, how its frames could be told from the Amiga's, and what the two share on one link and one receive backlog.
Status: current

- [G] "The service" does not exist: it is the firmware service of `topics/link-and-address.md`, rows 2a to 2e, which would keep the second computer's Ethernet frames on the card and draw their pixels there, in place of passing them to the 68k.
- The card's Ethernet as built is in `topics/network.md`, "The card's Ethernet today": its filters, each step a received frame takes, when the receive backlog is rebuilt, and its link speed.
- The backlog's size and its pause rule are in `sections/firmware-and-rtl.md`, "What the card offers today".
- This page holds what follows from them for the service; "the Arming step" and the like name rows of that table.
- Every `[G]` here is read from the source lines those places and this page cite; no firmware was built or run.
- A citation with no source ID is `fw@cfbb910`; `drivers` citations are at `cb6a1c4` and `linux` citations at `adc218676eef`, the commit of tag v6.12; `os/` and `bsp/` expand per `sources.md`.
- MB = 10^6 bytes.

## Where a frame could be claimed

- [G] The receive handler is where a service would see each frame; by then the frame is already in a slot of the backlog the Amiga reads (the Arrival step).
- [F] A service is compiled into the firmware image: the firmware has no loader (`topics/arm-offload.md`, "Mechanisms in the firmware").
- [G] A claimed frame that is not published leaves the write pointer on its slot S while arming moves on round the backlog's 128 slots (the Arming and Arrival steps): the next 127 frames land in S+1 to S+127 and are dropped as mismatches, and the 128th lands in S and passes, so order resumes with no rebuild.
- [G] During that lap each slot's header is zeroed as it is armed again, and that includes a frame queued for the Amiga, if it is still unread when arming comes round to its slot.
- [G] The Amiga's driver then sees an empty slot and waits without acknowledging (the To the Amiga step), the state a firmware comment describes as receive wedging (`os/ethernet.c:L447-450`).
- [G] The lines read hold no way out of that state short of a rebuild of the backlog (the Rebuild step).
- [G] If the pointer is moved on instead, the Amiga is shown an empty slot, with the same result (`os/ethernet.c:L826-829`).
- [G] A service that leaves the backlog's order, serials and acknowledgement as they are needs no change to the Amiga's driver (the To the Amiga step).
- [G] The handler gives a frame its serial before it tests the frame's slot (`os/ethernet.c:L823-840, L860-866`), so claimed frames would show in the driver's count of overruns unless they take no serial.
- [F] The descriptor's status word has, for each frame, bits the vendored header names for a broadcast frame, a multicast-hashed frame, a unicast-hashed frame, a two-bit specific-address match, a type-ID match and a VLAN tag (`bsp/xemacps_hw.h:L570-578`).
- [G] How the two-bit field tells the four address filters apart is in neither header read: the vendored one labels the bit above it as buffer exhaustion (`bsp/xemacps_hw.h:L573`).
- [F] Another open-source driver for this controller reads that bit as a specific-address match and the two bits as the number of the register that matched, citing Table 16-2 of the controller's manual (`zephyr@8469084dfae8:drivers/ethernet/eth_xlnx_gem_priv.h:L26, L43-44, L62-64`).
- [G] If that reading is right, a match bit and a two-bit register number give each of the four filters its own code, so a second filter would be told from the first and from no match.

## Telling the two kinds of frame apart

What the card does today with each filter is the Filter step; the cells below add only what a service would change or rely on.

| Told apart by | Crosses | What the firmware would have to do | Source |
|---|---|---|---|
| EtherType | [F] Linux bridges, which forward by layer-2 headers alone. [R] Other switches; the bridging standard, IEEE 802.1Q, would verify it. [G] No router | [G] Read two bytes of each frame from its slot. [F] The controller's four type-match registers report through descriptor bits that give way to checksum bits while receive checksum offload is on. [G] So they do not help as built, since the offload is on (the Filter step) | `bsp/xemacps_hw.h:L166-169`; `bsp/xemacps.h:L229-232`; `linux:drivers/net/ethernet/cadence/macb.h:L889-895`; `linux:Documentation/networking/bridge.rst:L317-319` |
| A second hardware address on the card | [G] A direct cable. [F] A Linux bridge forwards by destination address and floods a destination it has not learned, and other switches flood likewise. [G] So the card must also send from that address now and then, or its frames go to every port | [G] Program one of the three address filters the firmware leaves unused (the Filter step), and read the specific-address field from the descriptor, with no frame bytes, if that field tells the second filter from the first ("Where a frame could be claimed") | `bsp/xemacps_control.c:L73-87`; `bsp/xemacps_hw.h:L574`; `linux:net/bridge/br_input.c:L140-141, L197-215`; `rfc:2889:L104-106` |
| VLAN tag | [G] Only VLAN-aware switches; on a direct cable it adds nothing over the two rows above | [F] The vendored driver's VLAN option does not add tagged frames to what is received: it sets receive-only-VLAN. [G] So turning it on would discard the Amiga's untagged frames. [F] The descriptor has a VLAN-tagged bit, and the Amiga's driver takes frames of up to 1,518 bytes | `bsp/xemacps_control.c:L483-486`; `bsp/xemacps_hw.h:L377-378, L578`; `drivers:net/rx.h:L36` |
| UDP port, on the Amiga's own address | [G] Whatever IP crosses, routers and Wi-Fi included | [G] Parse the Ethernet, IPv4 and UDP headers of each frame, since the firmware has no TCP/IP code (the On the ARM step); the Amiga's stack keeps answering ARP | None |
| A separate IP address for the service | [G] As the UDP row | [G] As the UDP row, plus answering ARP for that address, or a fixed entry on the second computer | None |
| The controller's hash filter | [G] As a second hardware address | [F] The descriptor flags a multicast-hashed and a unicast-hashed frame, and one hash serves both. [G] With unicast-hash matching on (the Filter step), a service address admitted through a bucket would be flagged with no frame bytes read; so would any other single-station address in a set bucket, and the hash reset at each Amiga reset clears the service's bucket with the rest | `bsp/xemacps_hw.h:L571-572`; `bsp/xemacps_control.c:L200-209` |

- [G] Every row also needs receive buffers apart from the Amiga's ordered backlog, or a rework of the in-order rule ("Where a frame could be claimed").
- [G] Row 2e of `topics/link-and-address.md` needs none of this table: every frame on the socket is the second computer's.

## Sharing the link

- [F] A standard maximum frame is 1,518 bytes, and the gap between frames is 96 bits (`rfc:2889:L155, L1047`).
- [F] The preamble is 7 bytes, before a start delimiter (`ksz9031` p14).
- [F] An IP datagram on Ethernet is at most 1,500 octets (`rfc:894:L37-38`); an IP header is at least 5 words (`rfc:791:L867`); a TCP header has options only when its data offset is above 5 words (`rfc:9293:L469-470`).
- [G] So a full-size frame takes 1,518 + 8 + 12 = 1,538 byte-times on the wire and carries 1,500 − 20 − 20 = 1,460 bytes of TCP payload without options.
- [G] At the 100 Mb/s the firmware asks for (`topics/network.md`, "The card's Ethernet today") the wire carries 12.5 MB/s, which is 12.5 × 1,460 ÷ 1,538 = 11.9 MB/s of such payload.
- [G] The Amiga receiving 2.9 MB/s of payload, the most that `topics/target-config-rates.md`, "Network receive", has for a 68060 at 50 MHz, with the conditions given there, occupies 2.9 × 1,538 ÷ 1,460 = 3.05 MB/s of the wire and leaves 12.5 − 3.05 = about 9.4 MB/s for the second computer's frames.
- [G] That is not a floor: at the backlog's pause threshold (`sections/firmware-and-rtl.md`, "What the card offers today") the card arms no more descriptors, so when those already armed are used nothing more is received, the second computer's frames included.
- [F] A Linux bridge drops pause frames (`linux:net/bridge/br_input.c:L376-377`).
- [G] So in row 2b the card's pause frame reaches only the second computer's own port.
- [F] Whether a Linux port obeys a pause frame is a setting of each device (`ethtool` `ethtool.8.in` L611-622; `linux:include/uapi/linux/ethtool.h:L565-584`).

## One receive backlog

- When the backlog is rebuilt, and that everything waiting in it is then dropped: the Rebuild step.
- [G] So a rebuild drops whatever shares the backlog, the second computer's frames included, unless they have buffers of their own.
- [F] A third party reports that with 32 receive descriptors and a bigger TCP window every frame past the 32nd of a burst is lost in the controller, and nothing counts it (`anx@9a6f6fc:docs/plans/zz9000-ethernet.md:L147`).

## A second network card

Row 2e of `topics/link-and-address.md`.

- [F] A third party documents an A3000 with a ZZ9000 and an X-Surf 100 both up at once, with a priority set for each interface, on a 68030 at 25 MHz under AmiNetXDuo (`anx@9a6f6fc:docs/plans/zz9000-ethernet.md:L3-6, L41-47`).
- How many interfaces each stack carries: `topics/link-and-address.md`, "Through the Amiga's stack".
- A USB Ethernet adapter on the card's own USB port in place of a second Zorro card: `topics/other-attachments.md`, "Links".

## Services others ship for the card's ARM

- [F] One firmware line distributed apart from `fw` carries a service of its own: AmiNetXDuo's README says that its display server can move frame-buffer readback and delta encoding to the card's ARM, that the firmware this needs is a ready-to-flash image in its own firmware fork, and that its Amiga program detects the service and falls back when it is absent (`anx@9a6f6fc:README.md:L206-218`).
- [G] That service encodes the Amiga's own screen for a viewer elsewhere, the opposite direction to a feed of browser pixels.
- A second such line, which loads ARM programs at run time: `topics/arm-hosted-engine.md`, "A firmware line that loads ARM programs (XACP)".
- [G] A card runs one firmware image at a time: the image is one boot file on the card's SD card (`topics/arm-offload.md`, "Mechanisms in the firmware").
- The firmware's licence: `sections/overview.md`, "Licences".

## Exposure

- [G] In rows 2a to 2e the second computer's frames reach the card's firmware directly, so the row "The ARM firmware, over the control link" of `topics/security.md`, "Threat model", applies to the service's parser.
- [G] In rows 2b to 2d the second computer also carries all of the Amiga's own traffic.

## Not established

- The descriptor's address-match encoding, on which the second-address and hash-filter rows rest; type matching with checksum offload on; whether tagged frames are received with the receive-only-VLAN filter off, and to what length; receive queues: the controller's manual (`ug585`) would settle each, and it was not read.
- The ARM's rate of taking frames beside the Amiga's own traffic, and pause-frame behaviour with a given Linux port or switch: only hardware shows them.
- Which way of telling frames apart would be used, and whether the session must work without the service: design choices, and none is made.
- VLAN handling in an Amiga TCP/IP stack: no statement was found in Roadshow's home page, Miami's guide or AmiNetXDuo's README.
- Whether the Ethernet path of the firmware line that loads ARM programs matches the one read here: its source would settle it.

## Sources

`fw`, `drivers`, `linux`, `anx`, `rfc`, `ksz9031` and `ug585` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `zephyr` | Zephyr, its driver for the same Ethernet controller | `github.com/zephyrproject-rtos/zephyr` | `8469084dfae8` (tag v4.0.0) |
| `ethtool` | ethtool 6.11, manual page source `ethtool.8.in` | `https://mirrors.edge.kernel.org/pub/software/network/ethtool/ethtool-6.11.tar.xz` | 2026-10-11 |
