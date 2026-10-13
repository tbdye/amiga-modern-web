# Sound paths on the target configuration

Scope: the paths by which sound can reach an output on a 68060 Amiga with a ZZ9000: each path's rates and buffers and what it asks of the 68k, what the card's mixer does when a producer is late, and what video with sound takes of the 68k, the card and the link each second.
Status: current

- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it.
- [D] DEC-036: it should support video with synchronised audio; where the sound plays is not decided.
- Nothing here was run, built or measured by this project, and no path is recommended; a measured figure is its source's own.
- `[F]` opens what a source states; `[G]` opens arithmetic or inference made here, shown beside it.
- A ZZ9000 has a sound output of its own only with its audio add-on, the ZZ9000AX ("the add-on"): the hardware, the card's mixer (the audio fabric) and the Replica's wiring are in `topics/audio-path.md`.
- How sound and picture are kept in step, and the published tolerances: `topics/av-sync.md`.
- AHI is AmigaOS's retargetable audio system; Paula is the Amiga's own sound chip; "the player" is ZZPlay, the media player in the firmware's SDK.
- Units: MB = 10^6 bytes; kB = 10^3 bytes.
- A citation with no source ID is `fw@cfbb910`; `os/` expands per `sources.md`; `lib.md` stands for `sdk/docs/zz9k-library.md` and `zzplay/` for `sdk/tools/zzplay/`.
- AHI's files: `ahiusr.guide` is in `aminet:driver/audio/m68k-amigaos-ahiusr` (AHI 6.0, 2005); `ahidev.guide` and `paula_audio.a`, the Paula driver's source at version 4.30 of 2003, are in `aminet:driver/audio/m68k-amigaos-ahidev`.

## Paths

| Path | Needs | Rates and format | Buffers and delay the source states | What the 68k does |
|---|---|---|---|---|
| AHI with the Paula driver, `paula.audio` | The driver, which the AHI 4.18 user archive holds and the 6.0 one does not | [F] 8-bit, and 14-bit with calibration (`ahiusr.guide` L835-845); the rates: "AHI with the Paula driver" | [F] Each Paula stream is double-buffered in chip memory (`paula_audio.a` L2450-2460); no latency figure | [G] AHI mixes on the 68k, and the driver writes the result to chip memory |
| AHI with the add-on's driver, `zz9000ax.audio` 4.32 | The add-on's audio chip | [F] 8, 12, 24, 32, 44.1 and 48 kHz; 16-bit stereo; up to 8 software-mixed channels (`drivers@cb6a1c4:ahi/driver/zz9000ax-ahi.c:L65, L74, L90, L179-188`) | [F] Periods of 20 ms; playback starts after a runway of two periods, 40 ms; paced by an absolute 50 Hz timer (same file, `L91-93, L628-632, L1401`) | [F] AHI mixes every allocated channel in software on the Amiga's processor; the README's guidance for a 68060 is 8 channels, and overload shows as period skips, an audible stutter; it gives no percentage (`drivers@cb6a1c4:ahi/README.md:L37-59`) |
| A direct PCM ring on the card, without AHI | The add-on's audio chip; firmware that advertises the audio fabric | [F] 16-bit stereo, little-endian; 48 kHz, or 8, 12, 16, 22.05, 24, 32 or 44.1 kHz converted by the card (`lib.md:L955-987`; `sdk/include/zz9k/audio.h:L32-42`) | [F] Periods of 3,840 bytes, 20 ms; on Zorro III two rings of 16 periods; the card returns the bytes the DMA has retired as ring credit, and reports starvation for each slot (`lib.md:L963, L969, L989-993`; `os/audio_fabric_internal.h:L77-79`); [G] 16 periods are 61,440 bytes, 320 ms at 48 kHz | [F] A producer writes PCM, makes the range visible and commits its write cursor, and the steady path makes no mailbox copy (`lib.md:L989`); [G] so the 68k's work is the write into card memory, with no AHI mixer; no figure |
| Compressed sound decoded by the card and played on the add-on | The add-on's audio chip | [F] The firmware advertises MP3, as a stream service, and MPEG Layer II inside a program stream; FLAC, Ogg Vorbis and WebM's Opus and Vorbis are built in and not advertised (`os/sdk_service_catalog.h:L32-55, L130-153, L179-197`) | [F] An MP3 stream bound to the add-on's output is pumped as decoded PCM straight to the audio hardware (`lib.md:L1823-1831`); which paths report a played position: `topics/av-sync.md`, "Which sound paths report a played position" | [G] The 68k carries only the compressed bytes ("What each second takes") |
| The card decodes and the 68k plays through AHI | Nothing beyond the card | [F] On its AHI path the player decodes on the card, reads the PCM back from a shared ring of 128 KiB and writes it to AHI as 16-bit big-endian samples (`zzplay/zzplay.c:L70, L1424`) | [F] Two AHI requests of 1/10 s each, chained (`zzplay/zzplay.c:L73`; `zzplay/zzplay-ahi.h:L17`; `ahidev.guide` L969-977); a pause through AHI takes effect after the queued sound finishes, "up to about 0.4 seconds" (`sdk/docs/zzplay.md:L269-271`) | [G] It reads the PCM across the bus, then pays AHI's cost as in the first or second row |
| Another sound card through AHI | The card | [F] AHI's guide lists Concierto, Delfina, Maestro Pro, Melody, Prelude, Repulse, Toccata and Wavetools among the cards it supports (`ahiusr.guide` L756-798) | Not read | Not read |

- [F] The card's mixer fills one transmit ring of 8 periods, 160 ms, and keeps its fill at most 6 periods, 120 ms, ahead of the DMA position (`os/memorymap.h:L13-19`; `os/audio_fabric.c:L52-55, L1136-1140`).
- [F] A conversion to 48 kHz has a group delay of 50 input samples (`docs/audio-conversion.md:L29-35`); [G] that is 1.1 ms at 44.1 kHz.
- [F] On firmware without the audio fabric only one of the AHI driver and the MHI library owns the add-on at a time (`drivers@cb6a1c4:ahi/README.md:L17-21`); which producers play together with the fabric: `topics/audio-path.md`, "The A9 audio fabric".
- [F] MP3 decode to PCM is a capability of its own, which the SDK's document calls no promise that the add-on is fitted (`lib.md:L832-835`).

## AHI with the Paula driver

- [F] The AHI 6.0 user archive holds `device.audio`, `emu10kx.audio` and `filesave.audio` and no `paula.audio`; the AHI 4.18 user archive holds `paula.audio`, dated 1998-12-06, and a 68060 build of `ahi.device` (the file lists of `aminet:driver/audio/m68k-amigaos-ahiusr` and `aminet:driver/audio/ahiusr_4.18`).
- The 4.18 archive was listed and not unpacked, so every line below is the 4.30 source and the 6.0 guide, and the 4.18 driver's own limits are not read.
- [F] The add-on's manual tells its user to install AHI 4.18, and advises against version 6 for its higher processor use and audio stuttering (`zz9000ax-manual` p1).
- [F] The rate is Paula's clock ÷ a whole period: the clock is 3,546,895 Hz (PAL) or 3,579,545 Hz (NTSC), and the smallest period is 62, or 124 unless a test of the screen passes (`paula_audio.a` L202-204, L1262-1301).
- [G] So at period 124 the most is 28,604 Hz (PAL) or 28,867 Hz (NTSC); with the test passed, a request for 48,000 Hz plays at 47,931 or 47,727 Hz and one for 44,100 Hz at 44,336 or 44,192 Hz, which is −0.57% to +0.54% of the rate asked for.
- [F] The mode list has 17 rates up to 27,429 Hz, or 23 up to 48,000 Hz (`paula_audio.a` L1472-1497, L2982-2994).
- [F] The test, by the guide: the driver allows up to 48 kHz when the current screen mode is a 31 kHz one, and the variable `AHIpaulaSampleLimit` lifts the limit when set to 1 and keeps it when set to 0 (`ahiusr.guide` L864-879).
- [F] The test, by the source: with that variable unset and the front screen a graphics card's under Picasso96, the limit lifts only if the variable `Picasso96/AmigaVideo` begins "31" (`paula_audio.a` L1316-1329, L1355-1358, L1386-1410).
- [F] By default the driver stores the real rate as AHI's mixing rate and reports it; with `AHIpaulaFakeMixFreq` set to 1 it reports the rate asked for, which the guide says can make the sound "a little false" (`paula_audio.a` L1113-1121; `ahiusr.guide` L908-919).
- [F] A program that writes to AHI's device gives its stream's own rate with each request (`ahidev.guide` L959-964); [G] so the conversion between that rate and the real one is AHI's, and the difference between the two is not in itself drift.
- [F] A buffer holds `AHIpaulaBufferLength` (0 by default) plus AHI's largest mixing pass plus 4 samples, and one run of the driver's interrupt code repeats mixing passes until at least `AHIpaulaBufferLength` samples exist (`paula_audio.a` L931-935, L2450-2460, L3616-3623, L3678-3679).
- [F] The guide warns that a 68060 "might run into trouble" with that default of 0, because of chip memory's bandwidth (`ahiusr.guide` L921-928).
- [F] Only the mode "Paula:DMA 8 bit stereo" has no software mixing; a processor-use limit exists for some drivers; "Fast" modes are described as useful for 16-bit audio streams (`ahiusr.guide` L847-852, L627-633, L1036-1040).
- [G] In 14-bit stereo the driver writes 4 bytes a sample frame to chip memory: at 28,604 Hz that is 114,416 bytes a second, 1.6% of the one published write rate into chip memory, 7.0 MB/s on an A3000 with a 68060 at 50 MHz (`paula_audio.a` L2450-2457; `topics/bus-and-card-rates.md`, "Bus ceilings").

## When a producer is late

- The card's mixer and its three slots: `topics/audio-path.md`, "The A9 audio fabric".
- [F] A late, absent or paused producer contributes silence without stalling the others, and only its own underrun counter moves (`os/audio_fabric.h:L18-27`).
- [F] An underrun is counted when the DMA has caught up with or passed the fill frontier, which is a period that nobody filled (`os/audio_fabric.c:L1082-1110`).
- [F] The firmware's qualification record, for a "PAL A4000 / R1 card" on 2026-08-28 with MP3 decode on the card and a full-screen window being dragged, lists four mixes of producers, each with underruns "0, stable", and says that the numeric reports for each stage were not kept (`docs/audio-fabric.md:L110-119, L152-173`).
- [F] It does not name the Amiga's processor, and the load it describes for those four rows has no network traffic (`docs/audio-fabric.md:L110-119`).
- [F] A further pass, two streams listened to "under RTG/network load", is recorded as passed with no audible drops: it was judged by ear, no counter is given, and neither the load nor the processor is described (`docs/audio-fabric.md:L175-177`).
- [F] The card's cost, by the same document's analysis: one conversion from 44.1 to 48 kHz is 193,920 multiply-adds a period, put at 0.19 to 0.39 million cycles, about 1.5 to 3% of the period's 13.33 million, and called an estimate derived on a host (`docs/audio-fabric.md:L40-66`).
- The one published run of picture with sound, and its 13 underruns: `topics/av-sync.md`, "How the card's own player keeps step".

## What each second takes

Every figure under this heading is `[G]` unless its line opens with another label, and each input is its owner's, at the value given:

| Input | Value used | Owner |
|---|---|---|
| What the 68k receives from the network at 50 MHz | 2.6 to 2.9 MB/s | `topics/target-config-rates.md`, "Network receive" |
| Copy from memory into the card | 4.3 to 7.3 MB/s; 5.3 and 5.8 MB/s on firmware 2.8 | `topics/target-config-rates.md`, "Copies into the card" |
| Pixel rate, 1 ÷ (1/receive + 1/copy) | 1.62 to 2.08 MB/s; 1.74 to 1.93 MB/s on the firmware 2.8 copies | `topics/target-config-rates.md`, "Pixel rate" |
| JPEG's ratio to 16-bit pixels on scroll strips, quality 75, 4:2:0 | 11.8 on the photo gallery's strips and 9.30 on strips across video thumbnails, both byte-weighted; 7.64 at the 10th percentile of the gallery's strips less the mostly blank ones | `topics/page-pixels-lossy.md`, "Ratio and PSNR by quality" |
| The card's JPEG decode rate at 4:2:0 | 13.0 to 18.1 million pixels a second | `topics/decode-rates.md`, "Cortex-A9 JPEG" |
| One call from the 68k to the card | 0.28 to 0.39 ms | `topics/arm-offload.md`, "Per-call cost" |
| TCP payload on the card's 100 Mb/s link | 11.9 MB/s | `topics/card-ethernet-sharing.md`, "Sharing the link" |

- Each input keeps its owner's conditions: the receive figure is a benchmark into memory on an A3000 with firmware later than the release; the copies are A4000s, with an 8-bit screen standing in for a 16-bit one; the decode rate is another maker's chip scaled by clock; the call time's machine clock is not named.
- No source measures one program that receives, draws and plays sound at once.
- A sound byte is taken to cost the 68k what a pixel byte does where it is set against the pixel rate, and less where it is only received.
- A frame is 16-bit pixels, width × height × 2 bytes: 115,200, 259,200 and 460,800 bytes at the three sizes; on a 32-bit screen every uncompressed rate halves.
- [D] DEC-033 gives about 15 frames a second as the likely floor for video, at no stated picture size; the rows at 15 frames a second take that rate and judge no size by it.

Sound alone, as bytes a second ÷ the rate:

| Sound | Bytes a second | Of the 68k at the pixel rate (÷ 2.08 to ÷ 1.62 MB/s) | Of the 68k, received only (÷ 2.9 to ÷ 2.6 MB/s) | Of the link (÷ 11.9 MB/s) |
|---|---|---|---|---|
| 48 kHz, 16-bit stereo | 192,000 | 9.2 to 11.9% | 6.6 to 7.4% | 1.6% |
| 44.1 kHz stereo | 176,400 | 8.5 to 10.9% | 6.1 to 6.8% | 1.5% |
| 32 kHz stereo | 128,000 | 6.2 to 7.9% | 4.4 to 4.9% | 1.1% |
| 22.05 kHz mono | 44,100 | 2.1 to 2.7% | 1.5 to 1.7% | 0.4% |
| Compressed at 128 or 192 kbit/s, example rates, decoded by the card | 16,000 or 24,000 | 0.8 to 1.0%; 1.2 to 1.5% | 0.6%; 0.8 to 0.9% | 0.1%; 0.2% |

The 68k draws uncompressed frames: frames a second at 50 MHz = (pixel rate − the sound's bytes a second) ÷ frame bytes.

| Size | No sound | 48 kHz stereo PCM | 22.05 kHz mono PCM | 128 kbit/s compressed | On the firmware 2.8 copies: no sound; 48 kHz stereo PCM |
|---|---|---|---|---|---|
| 320×180 | 14.1 to 18.1 | 12.4 to 16.4 | 13.7 to 17.7 | 13.9 to 17.9 | 15.1 to 16.8; 13.4 to 15.1 |
| 480×270 | 6.3 to 8.0 | 5.5 to 7.3 | 6.1 to 7.9 | 6.2 to 8.0 | 6.7 to 7.4; 6.0 to 6.7 |
| 640×360 | 3.5 to 4.5 | 3.1 to 4.1 | 3.4 to 4.4 | 3.5 to 4.5 | 3.8 to 4.2; 3.4 to 3.8 |

- Worked, 320×180 with 48 kHz stereo: (1,620,000 − 192,000) ÷ 115,200 = 12.4, and (2,080,000 − 192,000) ÷ 115,200 = 16.4.
- Uncompressed video at 15 frames a second is 1.73, 3.89 and 6.91 MB/s at the three sizes, which is 15%, 33% and 58% of the link, against the 2.6 to 2.9 MB/s that the 68k receives.

The card decodes photograph-like frames as JPEG, at 15 frames a second: compressed bytes a second = frame bytes × 15 ÷ 11.8 to ÷ 9.30 (÷ 7.64 in brackets); the 68k's share = that ÷ 2.08 to ÷ 1.62 MB/s; the card's share = pixels a second ÷ 18.1 to ÷ 13.0 million.

| Size | Compressed kB/s | 68k, frames only | With 48 kHz stereo PCM through the 68k | With 128 kbit/s compressed sound | The card's decoding core | Link |
|---|---|---|---|---|---|---|
| 320×180 | 146 to 186 (226) | 7.0 to 11.5% (14.0%) | 16.3 to 23.3% | 7.8 to 12.5% | 864,000 pixels a second: 4.8 to 6.6% | 1.2 to 1.6% |
| 480×270 | 329 to 418 (509) | 15.8 to 25.8% (31.4%) | 25.1 to 37.7% | 16.6 to 26.8% | 1,944,000: 10.7 to 15.0% | 2.8 to 3.5% |
| 640×360 | 586 to 743 (905) | 28.2 to 45.9% (55.8%) | 37.4 to 57.7% | 28.9 to 46.9% | 3,456,000: 19.1 to 26.6% | 4.9 to 6.2% |

- Worked, 640×360: 460,800 × 15 ÷ 11.8 = 585,763 bytes a second, and ÷ 2,080,000 = 28.2%; 460,800 × 15 ÷ 9.30 = 743,226, and ÷ 1,620,000 = 45.9%; 230,400 × 15 = 3,456,000 pixels a second, ÷ 18,100,000 = 19.1%.
- The ratios stand in for video: no video frame was measured on its own, and live action would compress less (`topics/page-pixels-lossy.md`, "Ratio and PSNR by quality").
- Not in any cell: the calls; AHI's mixing; the card's second pass on a 16-bit screen, whose rate is unmeasured (`topics/decode-rates.md`, "What the card's ARM decodes today"); the one worker on the card's second core being shared by picture decode, sound decode and TLS (`topics/arm-offload.md`, "Which core runs what"); and how far a real program falls short of a benchmark's rate (`topics/target-config-rates.md`, "Network receive").
- One call a frame is 15 × 0.28 to 0.39 ms = 4.2 to 5.9 ms a second, 0.4 to 0.6% of the 68k; how many calls a frame of each size takes is not counted here.

The card's own video session, with picture and sound decoded on the card and shown in the P96 overlay:

- Of the 68k: a stream of 1 to 2 Mbit/s is 125,000 to 250,000 bytes a second, and ÷ 2.08 to ÷ 1.62 MB/s = 6.0 to 15.4%; the stream rate is an example and not a measured one, and the session's calls are not counted.
- [F] Of the card: a 640×480 file of 4,405 frames, played with pacing off, ran at 69.095 frames a second, on a machine and at a bit rate that are not stated (`docs/native-p96-pip.md:L336-337`; its decode calls a second: `topics/decode-rates.md`, "Cortex-A9 JPEG").
- 30 frames a second is 43% of that rate (30 ÷ 69.095).
- What release firmware plays in such a session: `sections/firmware-and-rtl.md`, "What the card offers today".

## Not established

- AHI's mixing share of a 68060 at 50 MHz for one 16-bit stereo stream, by driver and AHI version: no figure is in AHI's two guides, its two autodocs or the two driver READMEs; an instruction count of the mixing loop from AHI's source would bound it, and only a machine would show it.
- A latency figure for any AHI driver: none is in the same files; what is above are buffer sizes in source code.
- The length of AHI's own mixing pass for a program that writes to its device, and the 4.18 Paula driver's limits: AHI's source and the 4.18 archive's guide would settle them.
- Rates and buffers of the other sound cards' drivers: not read.
- Whether a direct ring, the player's sound and AHI can all play together, as the three slots suggest: the firmware's lease code would settle it.
- Underruns while the 68k is saturated with receiving and drawing frames: the four qualification rows had no network load, and the pass that had it was judged by ear; only hardware would show it.
- The number of calls a frame takes at each size: the SDK's image tools would settle it.
- The cost and the added delay of encoding MPEG-1 video with Layer II sound in real time, at 320×180 to 640×480, on a small Linux computer: no published figure was found.
- The size of real video frames as JPEG: `topics/page-pixels-lossy.md`, "Not established".
- The card's second pass, and the call time under display load: `topics/decode-rates.md` and `topics/arm-offload.md`, "Not established" in each.

## Sources

`fw`, `drivers`, `aminet` and `zz9000ax-manual` are defined in `sources.md`; this page defines no source of its own.
