# Owner groups and what reaches each

Scope: groups of Amiga owners by the hardware they have (a stock ZZ9000, a PiStorm, another RTG card, an emulator): what each has, the mechanisms by which browser pixels and input could reach its Workbench, and what the design under study gives each.
Status: current

- [D] DEC-020, DEC-022: the design under study, a new Zorro card (`sections/overview.md`, "The design under study"), is one proposal; no approach is chosen, and the order of preference is software, a co-processor board, then a full card, with something existing cards can use preferred, not required.
- [D] DEC-031: no single machine is named as the one the result is for, and what "supported" means is open.
- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it.
- An owner group is a set of Amiga owners with the same kind of hardware; those here are the ones examined, not every Amiga owner.
- The page ranks no group, places no machine in a level of support, estimates nothing by class of Amiga and judges no mechanism against a decision; what native feel asks is in `topics/look-and-feel.md`, "What native feel means".
- Nothing here was measured or run by this project: `[F]` opens what a cited source states, and `[G]` an inference made here.
- An engine is a current browser engine such as Chromium's.
- The PiStorm group has its own page, `topics/audience-pistorm.md`.

## At a glance

Each cell is `[G]`, a summary of the heading named in its row, where the labels, citations and conditions are.

| Group, and where it is described | Between the 68k and the monitor | Where browser pixels could come from | Input, clipboard, files | The design under study |
|---|---|---|---|---|
| Stock ZZ9000 ("Stock ZZ9000") | A Zorro card with RTG, two ARM cores and Ethernet | The 68k, across the bus; the card's ARM, in card memory; a second computer, through the card's Ethernet and the 68k | AmigaOS's own | Nothing on the stock card |
| PiStorm with the Linux emulator (`topics/audience-pistorm.md`, "An engine on the same Pi (Linux emulator)") | A Raspberry Pi as the 68k, under Linux; RTG on its HDMI | The same Pi: the RTG framebuffer is the emulator's memory | A314 services to Linux; none carries the clipboard, or input from the Amiga | Only in a machine with Zorro slots |
| PiStorm with Emu68 (`topics/audience-pistorm.md`, "Emu68: no Linux on the Pi") | A Raspberry Pi as the 68k, with no Linux; RTG on its HDMI | A 68k program on the JIT; a second computer into the Pi's camera port, as a whole screen | AmigaOS's own; none through the camera port | Only in a machine with Zorro slots |
| Another RTG card ("Other RTG cards") | A Zorro card with a display chip and no processor | The 68k, across the bus; a second computer only through the Amiga's network card and the 68k | AmigaOS's own | Only beside the card already fitted |
| Emulator; WinUAE read ("Emulators") | The host runs the 68k and the RTG board | The host: an overlay composed from emulated card memory; host libraries that 68k code can call | Calls into a host library | Nothing: no slot |

## What the design under study gives each group

- [G] The design reaches an Amiga only through a card made for it: each packaging option is a new card or a redesigned Replica (`sections/zynq-and-board.md`, "Packaging options").
- [G] So a stock ZZ9000 gets nothing from it as that card stands; whether its owners get a path at all is K54 (`unknowns.md`).
- [G] Beside another RTG card the new card, itself an RTG card (`sections/overview.md`, "The design under study"), duplicates the one fitted.
- [G] A PiStorm owner could add it only where there are Zorro slots, which among PiStorm machines is the A2000 (`topics/audience-pistorm.md`, "PiStorm and Zorro machines").
- [G] An emulator has no slot to take it.

## Stock ZZ9000

- [F] The card is a Zynq-7020 with a dual Cortex-A9 at 666 MHz and 1 GB of DDR3 (`sections/overview.md`, "Problem and goal"); what its firmware offers is in `sections/firmware-and-rtl.md`, "What the card offers today".
- [F] Its maker lists it for the Amiga 500, 2000, 3000 and 4000, as Zorro II and Zorro III compatible, and tests with an Amiga 2000 Rev 6.2, 3000D, 4000D and 500 Rev 5 (`mnt-zz9000`).
- [F] The firmware's release variants cover Zorro III, Zorro II and the A500 family (`sections/firmware-and-rtl.md`, "Native-video regression").
- [G] So the group spans all three, the target configuration being one case; on Zorro II the firmware offers less ("What the card offers today": no general offscreen bitmaps, a smaller overlay source pool).

A cell with no label restates what the pages named in its row state.

| Mechanism | How pixels reach the window | Limits, and where the figures are |
|---|---|---|
| The 68k writes them | A 68k program copies them into card memory through P96 | [G] Every pixel crosses the bus: `topics/target-config-rates.md`, "Copies into the card"; `topics/bus-and-card-rates.md`, "Bus ceilings" |
| The card moves them | A scroll or copy inside card memory | `topics/bus-and-card-rates.md`, "Scrolls on the card" |
| The card's ARM draws or decodes them | Firmware services fill, copy and scale in card memory, and decode JPEG or PNG into a program's window | `sections/firmware-and-rtl.md`, "What the card offers today"; `topics/decode-rates.md`, "What the card's ARM decodes today" |
| The overlay window | P96's overlay window (PIP): a second bitmap in card memory, shown over the screen | [F] Packed YUV 4:2:2 by design (`sections/firmware-and-rtl.md`, same heading); [G] pixels a 68k program writes into it cross the bus |
| From the network | The card's Ethernet is bridged to the Amiga as raw frames; a 68k program receives, then copies | `topics/network.md`, "The card's Ethernet today"; `topics/target-config-rates.md`, "Network receive", "Pixel rate" |

Where an engine's pixels could come from:

- [G] The 68k, as a native Amiga browser's do (`topics/prior-art.md`, "Native Amiga browsers"), with or without the services above.
- [G] The card's ARM cores, which run bare-metal firmware and no operating system (`sections/architecture.md`, "What each side runs"; `sections/firmware-and-rtl.md`, "Why the Zynq cannot host the browser").
- [G] A second computer on the network, as in the shipped projects of `topics/prior-art.md`, "Remote and split-engine browsers"; every byte then passes the Amiga's TCP/IP stack and the 68k.
- [G] Input, clipboard and files start in AmigaOS in each case; they would reach an engine on the card through the firmware's mailbox ("What the card offers today"), or one on a second computer through the network.

## PiStorm

- A PiStorm puts a Raspberry Pi in place of the 68k; its two software stacks, what an engine on that Pi would meet, and the Zorro machines it reaches are in `topics/audience-pistorm.md`.
- [D] DEC-024: a PiStorm by itself is not seen as a solution; a Raspberry Pi as a co-processor is a different case and is not chosen.

## Other RTG cards

- [F] P96's release notes name drivers for the Cirrus GD542x of the GVP Spectrum and Picasso II, the GD5434 of the Piccolo SD64 and the GD5446 of the Picasso IV, the CyberVision's Trio64 and the CyberVision 3D's ViRGE, the Tseng ET4000W32 of the Merlin and oMniBus, the Retina in its Zorro II version and the Retina BLT Z3, the Altais, Visiona, GVP EGS 110, Rainbow II and A2410, and Voodoo cards behind a PCI bridge board; they also record fixes to Radeon, Rage XL and Matrox drivers (`p96-wiki`, the updates from V2.3 to V3.6.3).
- [F] P96's `emulation.library` is "responsible for emulation of the villageTronic API and the cybergraphics API" (`p96-wiki`, "Update September 2021 (V3.1.2)"); [G] so a program written to the cybergraphics API can run on P96.
- [G] As `p96-wiki` describes them, none of the Zorro cards named carries a processor that a program can be loaded onto: each is a display chip with, at most, a blitter; the A2410 is the open case ("Not established").
- [F] Adjacent: Z3660 is an Amiga 4000 CPU accelerator board that, with a Z-turn FPGA board (MYS-7Z020-V2) fitted, adds 16-bit RTG, Ethernet, AHI and MHI, the RTG, AHI and MHI being based on the ZZ9000's, and can run a 68040 emulation with a JIT on one of that board's ARM cores (`z3660@7385d31:README.md:L3, L11, L20, L28-30, L38`).

A cell with no label describes the mechanism; its facts are where the row points.

| Mechanism | How | Limits |
|---|---|---|
| The 68k writes the window | An ordinary P96 or graphics call copies pixels into card memory | [G] Every pixel crosses the bus: `topics/bus-and-card-rates.md`, "Bus ceilings"; copies by card in `topics/target-config-rates.md`, "Copies into the card" |
| The card's blitter moves it | [F] P96 leaves some graphics operations to an on-board blitter, and then also keeps off-screen bitmaps in card memory (`p96-wiki`, "Update V3.6.0"; `p96-drv`, `BIB_BLITTER`) | [G] A scroll done that way needs only the newly exposed strip to cross the bus; times by card in `topics/bus-and-card-rates.md`, "Scrolls on the card" |
| P96 overlay window (PIP) | [F] A "special feature" of a card: an overlay that shows a fixed region of card memory, in which the chip may offer YUV colour spaces (`p96-drv`, `BIB_VIDEOWINDOW`, `SFT_MEMORYWINDOW`) | [G] Its pixels still cross the bus to get into card memory; support by card below |
| A processor on the card draws | The card fills its own framebuffer | [G] Only a card that has one: the ZZ9000 ("Stock ZZ9000") and the Z3660, with the A2410 open ("Not established") |
| A second video source mixed in after the card | A browser computer's own video output | [G] What is mixed in is not drawn by Workbench; not researched here, and a card that does it is among the pruned approaches (`sections/options-rejected.md`, "Why each pruned approach lost", the downstream HDMI compositor card) |

- [G] With no processor and no input but the bus, such a card shows pixels that come from the 68k itself, as a native Amiga browser's do, or from another computer through the Amiga's network card, its TCP/IP stack and the 68k (`topics/target-config-rates.md`, "Network receive").

### P96 overlay windows by card

Each line is `[F]` from the update of `p96-wiki` that it names, unless it opens with another label.

- Picasso IV: video and memory windows, disabled on 32-bit screens ("Update V3.4.1"; "Update December 2021 (V3.2.0)").
- CyberVision 3D (ViRGE): a memory window, disabled on interlaced modes and not available on double-clocked or double-scan modes ("Update to V3.1.0 (June 2021)").
- Tseng ET4000W32: a memory overlay through the PIP interface, in the screen's own pixel format and not planar, which appears only if it is topmost and neither overlapped nor clipped ("Update V3.2.4").
- Voodoo: video overlays ("Update V3.5.0"); overlay fixes are recorded for the Radeon and Rage XL drivers ("Update V3.6.1") and the Matrox and Radeon drivers ("Update V3.6.3").
- Neither `p96-wiki` nor `p96-drv` names an overlay for the Picasso II's GD542x.
- [G] Neither names one for the CyberVision's Trio64 either, but a note on "The hardware overlays of the S3 and PicassoIV" ("Update V3.3.0") does not name the S3 chip, so this absence is the weaker.
- The ZZ9000's overlay is under "Stock ZZ9000"; the PiStorm's Emu68 driver implements none at its pin (`topics/audience-pistorm.md`, "Emu68: no Linux on the Pi").

## Emulators

Only WinUAE was read.

- [F] Its RTG board sets P96's video-window flag when the `rtg_overlay` setting is on, and the host composes the overlay by scaling rows from a bitmap in emulated card memory into its own frame (`winuae@016a9d1:od-win32/picasso96_win.cpp:L2745-2746, L5107-5148`).
- [G] So as read, the overlay shows what is in emulated card memory.
- [F] The ZZ9000 driver's overlay helpers state that their contract is modelled on that code, "the only public reference for how P96 drives these hooks" (`drivers@cb6a1c4:rtg/overlay_feature.h:L6-8`).
- [F] The UAE native interface lets 68k code open a host library, look up a function in it and call it, synchronously or on a thread, when the `native_code` setting is on, and the Windows build defines it (`winuae@016a9d1:include/uaenative.h:L17-25`; `uaenative.cpp:L252, L289, L435-466`; `od-win32/sysconfig.h:L108`).
- [G] The computer that runs the emulator is the one that would run an engine, so the pixels need not leave it; a 68k program would get input from the emulated AmigaOS, and the native interface is a way from it to host code.

## What differs by group

- [G] Every group on these two pages has a P96 driver for its RTG, so the part of a 68k program that owns the Workbench window and its requesters through Intuition and P96 need not differ by group; no source states this, and it is untested.
- [G] Three parts do differ: the pixel path, the computer the engine runs on, and the transport for input, clipboard and files between the program and the engine, which would be a firmware service or the network on a ZZ9000, an A314 service on a Linux PiStorm, and a host library under an emulator.
- [D] DEC-028: that P96 is what RTG cards have in common is raised, not adopted.

## Not established

What is open for the PiStorm group is in `topics/audience-pistorm.md`, "Not established".

- Any group not on these two pages, and any emulator but WinUAE: not examined.
- The size of any group: no figure is given here; a published total would settle it for a card.
- A path for owners of a stock ZZ9000: K54 (`unknowns.md`).
- Whether one machine can hold a stock ZZ9000 and a card of the design under study together, and what the stock card would then do: not examined.
- Whether programs written to P96's own API run under CyberGraphX, the RTG system whose API P96 emulates: not checked; CyberGraphX's documentation would settle it.
- Overlay support on the Picasso II and the CyberVision's Trio64: an absence in two pages, not a statement by the drivers' authors.
- Whether a program can be loaded onto the A2410's TMS34010: [R] the chip is a programmable graphics processor, which `p96-wiki` describes as a chip with blitter functions ("Update V3.4.0"); the chip's data sheet and the card's documentation would settle it.
- How an emulator's RTG modes and its host's display bound size and rate, and any path from host memory into the overlay: not read in WinUAE's source.
- The first statement under "What differs by group" is an inference from the P96 drivers alone: no source states it, and no trial stands behind it.

## Sources

`drivers` is defined in `sources.md`; GitHub rows take the link template of its "Prior-art sources".

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `mnt-zz9000` | The maker's ZZ9000 resources page | `https://mntre.com/media/ZZ9000_info_md/2019-08-09-ZZ9000-resources.html` | 2026-10-11; dated 2024-03-25 by the page |
| `p96-wiki` | P96 on its publisher's wiki, one page with the release notes | `https://wiki.icomp.de/wiki/P96` | 2026-10-11; last modified 2026-06-20 by the page |
| `p96-drv` | P96 driver development, same wiki | `https://wiki.icomp.de/wiki/P96_Driver_Development` | 2026-10-11; last modified 2026-10-11 by the page |
| `z3660` | Z3660 | `github.com/shanshe/Z3660` | `7385d31` |
| `winuae` | WinUAE | `github.com/tonioni/WinUAE` | `016a9d1` |
