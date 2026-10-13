# Attaching a second computer without the card's Ethernet

Scope: links between an Amiga and a second computer other than the ZZ9000's Ethernet socket (another network card, USB, the parallel and serial ports, a clock port, SCSI): what each needs on the Amiga, and each link's own published rate.
Status: current

- These are row 5 of `topics/link-and-address.md`, "The ways", with Ethernet through an Amiga network card that is not the ZZ9000; that page has what each way does to the Amiga's own address.
- Nothing here was run or measured; a figure is its source's own, on its machine.
- `drivers` citations are at `cb6a1c4`.
- MB = 10^6 bytes; KB = 10^3 bytes, with the unit of each quoted figure as its source writes it.

## Links

| Link | What the Amiga side needs | The link's rate | Notes |
|---|---|---|---|
| Ethernet to another Amiga network card | A SANA-II card and a TCP/IP stack | [F] X-Surf 100, a 100 Mb/s card for Zorro II and Zorro III slots: its maker reports data-port transfers of "up to 22.8 MBytes per second" with `movem.l` and 14 with plain longword moves, reached only with 0 wait states (`icomp-wiki-xsurf100`). What the 68k receives through it: `topics/target-config-rates.md`, "Network receive" | The Zorro II ceiling: `topics/bus-and-card-rates.md`, "Bus ceilings" |
| USB, with the second computer as a device on the ZZ9000's port under Poseidon | Poseidon and a class driver for what the second computer presents | [F] Mass storage through the card: about 4 MB/s write and 3 MB/s read on a Zorro III-capable Amiga, which the README calls a historical baseline (`drivers:usb-poseidon/README.md:L25-27`) | [F] The driver lists the transfers behind "HID and Ethernet status" as supported, with hardware tests pending (same file, L18). [F] The open-source Poseidon tree has class drivers named `cdcacm`, `cdceth`, `rndis`, `massstorage` and `asixeth` (`aros@949d6834f898:rom/usb/classes/`). Which boards can be a USB device: `topics/engine-options.md`, "Candidate computers" |
| Parallel port | A PLIP driver | [F] plipbox, a microcontroller bridge to Ethernet, on an A500 with a 68030 at 33 MHz: 114 to 127 KB/s bridged, by UDP echo with 1,400-byte packets; 234 KB/s in the file's "PB Test", which it does not define (`plipbox@a7995d7cc918:doc/src/benchmark.md:L56-89`) | [G] Each bridged rate counts both directions of one round trip: 2 × 1,400 B ÷ 24.48 ms = 114.4 KB/s. No TCP figure is given |
| Serial port | A serial driver | [F] The hardware manual puts the maximum reliable rate "on the order of 150,000-250,000 bits per second" with a cable of reasonable length, says that it varies between machines, and says that at such rates interrupts cannot be handled, so that the receiving end must sit in a tight read loop (`amiga-hrm`). [G] At 10 bits a byte that is 15 to 25 KB/s, and 115,200 baud is 11.5 KB/s | None |
| Clock port (A314-cp) | `a314.device`, and a clock port, whose address is a configuration value (`a314@7e19215:Software/README.md:L53-60`) | [F] A third party states "~70–120 KB/s byte-at-a-time" and gives no method (`a314rtg@da1b9fe59504:README.md:L10-13`) | [R] Big-box motherboards have no clock port; a motherboard schematic would verify it. The project: `topics/prior-art.md`, "A computer on a card" |
| SCSI, with an emulated network adapter | A SCSI controller and a SANA-II driver for an emulated DaynaPORT adapter | [F] No rate is published; the driver's README only warns of less than 5 K/s with debug logging left on (`daynaport@3d728bac3b0d:README.md:L47`) | [F] The driver is written for microcontroller SCSI emulators, BlueSCSI v2 and ZuluSCSI (same file, L1-4). [F] PiSCSI is a SCSI device emulator that runs on a Raspberry Pi, in userspace (`piscsi@4f800bae944b:README.md:L11-12`) |

- [G] At those rates one 640×480 frame of 8-bit pixels, 307,200 B, takes 2.6 to 4.4 s over the clock-port link and 2.4 to 2.7 s over the parallel-port bridge.
- [G] None of the last five is shown faster than Ethernet through the ZZ9000 (`topics/target-config-rates.md`, "Network receive"): the USB figure is a storage rate, SCSI has none, and the rest are lower.
- [G] None of the last five touches the Amiga's network card, so the Amiga's address is kept in each.
- [G] A USB Ethernet adapter on the card's own USB port could stand in for the second network card of `topics/link-and-address.md`, row 2e; [F] the driver's README lists the hardware test of one such adapter, an AX88772C, as pending (`drivers:usb-poseidon/README.md:L18`).

## Not established

- Whether the 68k Poseidon ships class drivers for a second computer that presents itself as a network or serial device, and whether the card's USB port carries them: Poseidon's own documentation would settle the first, and only hardware shows the second.
- Whether an A314-cp works on the clock port of a Zorro card in a big-box machine: no source read tests one.
- Whether the SCSI driver works with a network adapter emulated by a Linux computer: neither README states it.
- A parallel-port link to a Linux computer, and any TCP rate over the parallel port: not found.
- The X-Surf 100's data-port rates on a named machine: the maker's page names none.

## Sources

`drivers` and `a314` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `icomp-wiki-xsurf100` | The maker's wiki page for the X-Surf 100 | `https://wiki.icomp.de/wiki/X-Surf-100` | 2026-10-11 |
| `amiga-hrm` | Amiga Hardware Reference Manual, "Setting The Baud Rate" | `http://amigadev.elowar.com/read/ADCD_2.1/Hardware_Manual_guide/node01A1.html` | 2026-10-11 |
| `aros` | AROS, directory `rom/usb/classes/` | `github.com/aros-development-team/AROS` | `949d6834f898` |
| `plipbox` | plipbox | `github.com/cnvogelg/plipbox` | `a7995d7cc918` |
| `a314rtg` | A314RTG, an RTG driver over the A314 clock-port interface | `github.com/lainejones/a314RTG` | `da1b9fe59504` |
| `daynaport` | DaynaPORT SANA-II driver for SCSI emulators | `github.com/RobSmithDev/daynaport-amiga` | `3d728bac3b0d` |
| `piscsi` | PiSCSI | `github.com/PiSCSI/piscsi` | `4f800bae944b` |
