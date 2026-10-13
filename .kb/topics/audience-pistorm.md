# PiStorm owners and what reaches them

Scope: owners of a PiStorm, a Raspberry Pi in place of an Amiga's 68k: its two software stacks, the mechanisms by which browser pixels and input could reach Workbench on each, and the Zorro machines it reaches.
Status: current

- This is one of the owner groups of `topics/audience.md`, which holds the other groups, the comparison across them and what the design under study gives each; like that page, this one ranks nothing and judges no mechanism against a decision.
- [D] DEC-024: a PiStorm by itself is not seen as a solution; a Raspberry Pi as a co-processor is a different case and is not chosen.
- Each variant's emulator, boards, Amigas and 68k speed are in `topics/prior-art.md`, "Fast-68k routes"; this page adds what bears on a browser.
- Nothing here was measured or run by this project: `[F]` opens what a cited source states, and `[G]` an inference made here.
- An engine is a current browser engine such as Chromium's.

## The two software stacks

They differ in whether Linux runs.

| | Linux emulator (Musashi) | Emu68 |
|---|---|---|
| Operating system on the Pi | [F] Linux: 32-bit Raspberry Pi OS (`topics/prior-art.md`, "Fast-68k routes") | [F] None: bare metal (same heading) |
| Amigas and boards beyond that heading | The `pistorm32-lite` branch, with its board, Pi boards, operating system and Amiga: `topics/prior-art.md`, "Fast-68k routes" | [F] PiStorm for the A500, A1000 and A2000 and PiStorm600 for the A600, each with a Pi Zero 2, 3A+, 3B or 3B+; PiStorm16 for the A600 with a CM4; PiStorm32-lite for the A1200 with those four boards or "Pi4B+", or with a CM4 through an adapter (`pistorm-site@fca047c:_pages/hardware.md:L9-19`); [F] no Pi 5 or CM5 is listed, and the site gives the Pi 5's GPIO, behind a bridge on PCIe, as too slow for a PiStorm (`_pages/faq-hardware.md:L37-45`) |
| 68k speed, as the project states it | `topics/prior-art.md`, "Fast-68k routes" | [F] A JIT "reaching up to 1 MIPS per MHz" (`pistorm-site@fca047c:_pages/home.md:L23`); the site's benchmark page shows charts, with no result figures in its text (`_pages/benchmarks.md`) |
| RTG | [F] PiGFX, a virtual RTG board for P96, with output on the Pi's HDMI (`pistorm@88937a6:README.md:L42`; `platforms/amiga/rtg/readme.md:L1-7`) | [F] `VideoCore.card`, a P96 driver for the Pi's HDMI port (`pistorm-site@fca047c:_pages/p96setup.md:L7-16`) |
| How RTG pixels reach HDMI | [F] A thread of the emulator opens a raylib window, uploads the RTG framebuffer, which is the emulator's own memory, as a texture and draws it; the pointer is a second textured rectangle (`pistorm@88937a6:platforms/amiga/rtg/rtg-output-raylib.c:L230, L343, L357, L384, L464`) | [F] The driver writes the VideoCore scaler's display list itself, the pointer being a further plane in that list (`emu68-tools@0f86e19:VideoCore.card/src/vc4.c:L547-563, L721`) |
| Native (chipset) video on the same monitor | [G] Not through the Pi: the quick start connects an HDMI display to the Pi and the Amiga to its own monitor (`pistorm@88937a6:README.md:L54-55`) | [F] With a Framethrower, which samples the video at Denise and sends it to the Pi's camera port, the driver switching the scaler between its RTG plane and that feed (`framethrower@d24348b:README.md:L3`; `setup.md:L27-33`; `emu68-tools@0f86e19:VideoCore.card/src/vc4.c:L378-384`) |
| On the project's site | [F] "a m68k emulator used with PiStorm which was mainly used before Emu68 became useful" (`pistorm-site@fca047c:_pages/faq-musashi.md:L9`) | [F] "The software side is handled by Emu68" (`_pages/about.md:L11`) |

- [F] The cells that cite `emu68-tools` describe `VideoCore.card` at `0f86e19`; the notes of two Emu68 1.1 pre-releases say that version requires `VideoCore.card` 1.5, distributed with the release and "not yet available in Emu68-tools package" (`emu68-releases`, v1.1.0-alpha.1, v1.1.0-beta.1).
- Version 1.5 was not read, so those cells, and the driver statements below, hold at the pin only.
- [F] On the `pistorm32-lite` branch `emulator.c` and `platforms/amiga/rtg/rtg-output-raylib.c` are not the files cited here at `88937a6`, which is on the `main` branch; the RTG, A314 and AHI readmes are the same files (`pistorm@cc0244c`).

## An engine on the same Pi (Linux emulator)

- [G] Possible in mechanism and bounded by the Pi; nothing below measures an engine there.
- [F] A Pi 3A+ has 512 MB and a Cortex-A53 at 1.4 GHz, a Zero 2 W 512 MB and four Cortex-A53 cores at 1 GHz, and a 3B+ 1 GB (`rpi-3aplus` p3; `rpi-zero2w` p2-p3; `rpi-3bplus` p3).
- [F] The emulator starts interrupt, keyboard and processor threads, and its RTG output a fourth (`pistorm@88937a6:emulator.c:L671-690`; `platforms/amiga/rtg/rtg-output-raylib.c:L464`); its readme recommends the operating system's Lite version, as a windowing system "adds a lot of extra system load which may impact performance" (`README.md:L47`).
- [F] A Pi 4 and a CM4 have four Cortex-A72 cores and 1 to 8 GB (`rpi4-brief` p3; `rpi-cm4` p4-p5); [G] on this stack only the `pistorm32-lite` branch takes them, in an A1200; [F] that branch's head is dated 2023-12-12 (`pistorm@cc0244c`).
- [G] The emulator owns the display, so a browser's frame could be drawn as one more textured rectangle over the window's place, or copied into the RTG framebuffer; either way the pixels stay uncompressed in the Pi's memory and cross no 68k bus, and no display mode changes.
- [F] The RTG readme says that for raylib to work in the console on a Pi 3 the OpenGL driver must not be enabled, and that a Pi 4 needs a distribution with an X window manager "for it to perform well at all" (`pistorm@88937a6:platforms/amiga/rtg/readme.md:L10-11`); [G] so the display stack an engine would share differs by board.
- [F] The emulator provides the A314's functions by emulating that device on the Pi side (`pistorm@88937a6:a314/README.md:L7`): `a314fs`, a Pi directory mounted as `PI0:`; the `pi` command, which runs a Pi program from the Amiga shell; and a SANA-II driver that forwards Ethernet packets to the Pi's network interface (`:L39-45, L87-91, L101-103`).
- [F] PiAudio, RemoteWB and VideoPlayer are not supported, the PiStorm lacking full access to the chip-memory bus (`:L236`).
- The A314 and its own services are in `topics/prior-art.md`, "A computer on a card"; [F] its list has no clipboard service, and the input its services carry is passed to the Amiga, not taken from it (`a314@7e19215:README.md:L42-66`).
- [G] So window geometry, input events and clipboard text would need a new service of that kind, while downloads and uploads could use `PI0:`.
- [F] Pi-AHI plays Amiga sound through the Pi's audio output and is marked as not working properly (`pistorm@88937a6:platforms/amiga/ahi/readme.md:L3-6, L16`); [G] an engine's sound would leave by the Pi itself, not through Paula.
- [G] The engine would share the Pi with the 68k emulation, so a fault that stops the Pi stops the Amiga.

## Emu68: no Linux on the Pi

- [G] With no Linux, that Pi cannot also host an engine as it stands (`topics/prior-art.md`, "Fast-68k routes").
- [F] The A314's readme names the Musashi version of PiStorm as the one its software was adapted to (`a314@7e19215:README.md:L37-38`); [G] its daemon on the Pi is a Linux program, with nowhere to run under Emu68.
- [F] Emu68 instead gives AmigaOS drivers access to the Pi's hardware (`pistorm-site@fca047c:_pages/about.md:L11-12`).
- [F] Emu68 starts the Pi's other three cores: in PiStorm builds the second runs a serial log writer only when `async_log` is among the boot arguments and the third the PiStorm's housekeeping routine, the fourth runs a PowerPC emulator only when that is enabled, and each otherwise waits for an event (`emu68@0ba3a89:src/aarch64/start.c:L418-489, L1494-1518`).
- [G] So up to two cores sit idle, with no operating system to give them to an engine.
- [F] On a Pi with more than 2 GB, part of the memory above 2 GB, which AmigaOS cannot use, serves Emu68's JIT caches and its own needs (`emu68-releases`, v1.1.0-alpha.1).
- [G] Pixels can therefore come from a 68k program on the JIT, or from a second computer whose video enters the Pi's camera port as the Framethrower's does.
- [F] At its pin the driver switches the scaler's whole display list to that input (`emu68-tools@0f86e19:VideoCore.card/src/vc4.c:L378-384`) and leaves P96's feature hooks, which overlays use, unset (`VideoCore.card/src/main.c:L541-553, L607-619`).
- [G] So what is shown is a whole screen and not a Workbench window, and a window-sized plane and a channel for input would be new work.
- [F] The 3A+, 3B+, Zero 2 W and Pi 4 briefs each list one camera port, 2-lane on the Pi 4, and the CM4 has two, of 2 and 4 lanes (`rpi-3aplus` p3; `rpi-3bplus` p3; `rpi-zero2w` p2-p3; `rpi4-brief` p3; `rpi-cm4` p5, p11); [G] on a one-port board a browser feed would take the port the Framethrower uses.
- [F] The Framethrower's set-up notes give HDMI output settings for 720p and 1080p, each at 50 Hz (`framethrower@d24348b:setup.md:L35-55`).

## PiStorm and Zorro machines

- [F] The site names the 500/500+, 600 and 1200 as the Amigas the project supports and, in its table, the A500, A1000 and A2000 for the first PiStorm board (`pistorm-site@fca047c:_pages/hardware.md:L9-19, L28-32`); [G] of these only the A2000 has Zorro slots.
- [F] Two community boards address the A2000's processor slot: an adapter that relocates the PiStorm to that slot and calls itself "a work in progress, more testing needs to be done, but it should work as is" (`a2000-relocator@9b8d205:README.md:L3, L39`), and PiStorm2K, whose readme treats the 86-pin co-processor slot as its place and gives its status as "V2.0 not recommended for production" and "V2.1 Fixed issues with v2.0" (`pistorm2k@3bce983:README.md:L16-24, L84`).
- [F] The PiStorm's CPLD firmware does not handle the bus arbitration signals (`pistorm@88937a6:README.md:L24`), and a community list of Zorro cards reports the A2091 SCSI card as not working "due to DMA" and the ZZ9000 as working, without naming the machine (`pistorm-zorro-list@152a11f:README.md:L11, L18`); [G] in an A2000 that pairing would be on Zorro II.
- [F] For the A3000 and A4000 the one adapter found says "Do not build. Preliminary rev for test purposes only. May not work." (`ps32-a4000-adapter@ba1e140:README.md:L7`).
- [G] So this group is mostly owners of the A500, A600 and A1200, and meets the machines with Zorro slots only at the A2000.

## Not established

- Free memory and processor time on a Pi while either stack runs, and so whether a Pi 3-class board can run an engine beside the Linux emulator: unmeasured; only a measurement on such a board would show it.
- The 1920x1080 RTG modes of PiGFX and `VideoCore.card`: not read; their mode tables would settle it.
- `VideoCore.card` 1.5: not read; its source would show whether the display path and the unset feature hooks still hold.
- Whether Emu68 can share the Pi with a second operating system: not read in its source; its readme and the project's site describe it as bare metal.
- Whether native video reaches the Pi's HDMI under the Linux emulator: the `[G]` above rests on the quick start alone; the emulator's source would settle it.
- Whether the emulator's threads and its RTG output are the same on the `pistorm32-lite` branch: its two source files were not read, and every statement that cites them describes `main`; those files at `cc0244c` would settle it.
- What an HDMI-to-camera-port bridge carries over 2 or 4 lanes: not researched; a bridge's datasheet would settle it.
- Whether switching to the camera feed, or losing it, makes the monitor resync: only hardware would show it.
- A PiStorm for the A3000 or A4000 beyond the one adapter: none found, on the project's site and by GitHub repository search only.

## Sources

`pistorm`, `emu68` and `a314` are defined in `sources.md`, and GitHub rows take the link template of its "Prior-art sources".

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `pistorm-site` | The PiStorm project's site, as its source pages | `github.com/PiStorm/pistorm.github.io` | `fca047c` |
| `emu68-tools` | Emu68 tools, with `VideoCore.card` | `github.com/michalsc/Emu68-tools-old` | `0f86e19` |
| `emu68-releases` | Emu68 release notes, by tag | `https://github.com/michalsc/Emu68/releases` | 2026-10-11 |
| `framethrower` | Framethrower | `github.com/PiStorm/Framethrower_Denise` | `d24348b` |
| `a2000-relocator` | A2000 CPU-slot adapter for the PiStorm | `github.com/arananet/A2000CPUADAPTER-PISTORM` | `9b8d205` |
| `pistorm2k` | PiStorm2K | `github.com/Fastdruid/PiStorm2K` | `3bce983` |
| `pistorm-zorro-list` | Zorro cards tried with a PiStorm | `github.com/Sgw32/PiStorm_Zorro_Comp` | `152a11f` |
| `ps32-a4000-adapter` | A1200 to A3000/A4000 CPU adapter | `github.com/wiretap-retro/A1200-to-A3000-A4000-CPU-Adapter` | `ba1e140` |
| `rpi-3aplus` | Raspberry Pi 3 Model A+ product brief | `https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-a-plus-product-brief.pdf` | Read 2026-10-11; SHA-256 `d253dcedae53f055ac2f08240ee7d8240f6d9001fd391c6437eefe6c56c18904` |
| `rpi-3bplus` | Raspberry Pi 3 Model B+ product brief | `https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-b-plus-product-brief.pdf` | Read 2026-10-11; SHA-256 `345192be568ea8ab2f1f7bdb43ca5edf36e20bdd9b1bf96081299a91a2a88f3f` |
| `rpi-zero2w` | Raspberry Pi Zero 2 W product brief | `https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-product-brief.pdf` | Read 2026-10-11; SHA-256 `503f348880c00c543e99383ca8759a0b60c1b511cc3c27f216720866159a2bff` |
| `rpi4-brief` | Raspberry Pi 4 Model B product brief | `https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-product-brief.pdf` | Read 2026-10-11; SHA-256 `7e18898418a47cdbab2f6184ae93fbe6e4943c45475cecbe1db8eb11d32f4328` |
| `rpi-cm4` | Raspberry Pi Compute Module 4 datasheet, Release 4 (build date printed 30/06/2026) | `https://datasheets.raspberrypi.com/cm4/cm4-datasheet.pdf` | Read 2026-10-11; SHA-256 `d6946f8bb3e0276defa95b99b9d402a01a4805d3de02d53f835e93044ea7af97`; pages are the PDF's |
