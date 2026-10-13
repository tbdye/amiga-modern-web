# Audio path

Scope: the card's sound outputs as built, and how browser audio would reach the card's audio output: the ADAU1701 and its clocks, the A9 audio fabric, the candidate routes from the browser chip under each coupling, latency and A/V sync.
Status: draft

Replica facts come from its netlist at `replica@96bdef0` (not public).
The routes and the A/V sync mechanism are proposals under study, not decisions.

## The card's audio path today

- [G] A ZZ9000 has no sound output of its own without its audio add-on, the ZZ9000AX: the lines below are the basis, and for the HDMI output it holds only on the premise of the `[G]` on HDMI below.
- [F] The card's manual describes header J6 as breaking out the raw and filtered audio signals of the video slot "for use in future sound expansions", and from revision R-2 a header J7 as a digital audio input for the video encoder chip, "Reserved for later use" (`zz9000-manual-r1` p1; `zz9000-manual-r3` p1).
- [F] The FPGA's pin constraints carry sound pins for the add-on's audio chip only: the six `I2SO_` and `I2SI_` ports of "Replica wiring" (`fw@cfbb910:xdc/zz9000.xdc:L262-290`).
- [F] At boot the firmware probes that chip over I2C and reports when it is not detected; without it the video service does not offer audio binding and a bind request returns "unsupported" (`fw@cfbb910:os/ax.c:L787-795`; `os/main.c:L545-546`; `os/sdk_mailbox.c:L1467-1469, L5893-5894`).
- [F] The add-on carries the ADAU1701 with a 12.288 MHz crystal, a line output, two auxiliary jacks that jumpers set to input or output, and an input from the Amiga's Paula; its default DSP program mixes AHI and Paula sound and is included in the firmware (`zz9000ax-manual` p1, p2).
- [F] On the R-1 add-on the auxiliary input and the Paula input of each channel meet at the input of one buffer stage, U4, drawn as "Analog Input Mixer", whose outputs feed the ADAU1701's two ADC inputs through 18 kΩ (`zz9000ax-manual` p2).
- [F] The drivers' README says that early Revision 1 add-on boards carry an op-amp at U4 on the Paula path and that later revisions omit it (`drivers@cb6a1c4:ahi/README.md:L119-127`).
- Where the auxiliary input goes on add-on boards after R-1 is not established: a schematic of a later revision would settle it.
- [F] The release firmware writes the HDMI transmitter from one file, and only its registers `0xC7`, `0x1E`, `0x09`, `0x0A`, `0x60`, `0x3C`, `0x00` to `0x08` and `0x1A`; no line of that file matches "audio" or "i2s", and its only other I2C writes go to the add-on's audio chip on the second controller (`fw@6aa71d1:os/hdmi.c:L53-55, L66-72, L87-97, L160, L182, L194`; callers `os/video.c:L963, L1005, L1007, L1043`; `os/ax.c:L31`).
- [F] The Linux driver for this chip defines the transmitter's sound registers as `0x1F` to `0x28`, and its sound set-up also writes `0xBC` to `0xBE` and from `0xBF` on: the firmware writes none of them, and both programs use the register set that a write of 0 to `0xC7` selects (`linux@6c377d19d4a5:drivers/gpu/drm/bridge/sii902x.c:L74-143, L150-158, L699-756, L1081`; `sii9022a` p39).
- [F] In every mode the value it writes to register `0x1A` when it turns the output on is the mode's `hdmi` field, which is 0 in each of the 22 rows of the mode table and is set to 0 when a custom mode is committed (`fw@6aa71d1:os/zz_video_modes.c:L11-36`; `os/video.c:L900, L963, L1045, L1199`; `os/hdmi.c:L138, L183-184, L194`).
- [F] That value is DVI by three sources: the firmware's comment gives the register's 0 as DVI and 1 as HDMI, the Linux driver gives bit 0 of the same register as the output mode with those two values, and the firmware's README lists the board's video output as DVI (`fw@6aa71d1:os/hdmi.c:L126, L192-193`; `README.md:L621`; `linux@6c377d19d4a5:drivers/gpu/drm/bridge/sii902x.c:L59-66, L342-351`).
- [G] So no sound leaves on HDMI with this firmware: it rests on the premise, not verified here, that a transmitter in DVI mode with its sound registers unwritten sends none; the maker's register reference, which its data sheet says needs a non-disclosure agreement, would settle it (`sii9022a` p36, p37, p78).
- [F] The ADAU1701 is the clock master: its 12.288 MHz (256·Fs) output BCLK is the audio formatter's master clock (`fw@bdfd8b0:rtl/audio_clock.v:L22-30`).
- [F] Firmware sets the ADAU1701's serial output to 48 kHz, 16-bit TDM8 master mode with a 256·Fs BCLK; the two ADC capture channels ride in slots 0 and 1 of `SDATA_OUT0` (`fw@bdfd8b0:zz9000ax/README.md:L30-34`).
- [F] The FPGA divides that BCLK by 8 and drives the result, 1.536 MHz (32·Fs), out on port `I2SO_MCLK` as the clock for the ADAU1701's serial input (`fw@bdfd8b0:rtl/audio_clock.v:L46-47, L154, L172`; `zz9000_project.tcl:L1394`).
- [F] The FPGA receives the ADAU1701's LRCLK on input port `I2SO_LRCLK`, and playback leaves on `I2SO_D0` from an I2S transmitter fed by the audio formatter (`fw@bdfd8b0:zz9000_project.tcl:L608, L1312, L1401-1402`).
- [F] The capture side accepts a 256-bit TDM8 frame only when its LRCLK midpoint and closing edge are coherent (`fw@bdfd8b0:rtl/audio_clock.v:L82-86`).
- [F] The ADAU1701 runs 1024 instruction cycles per sample at 48 kHz, and its production graph is at that limit: adding a selector and one more input algorithm failed to compile for lack of DSP resources (`fw@bdfd8b0:docs/testing/zz9000ax-dig0-feasibility.md:L35-42`).
- [F] The production DSP project has one serial-input block, which carries FPGA playback into the mixer beside the analog Paula input (`fw@bdfd8b0:dsp/limiter-postvolume.dspproj`, one `SerialInputRegister`; `zz9000ax/README.md:L17-23`).

### Replica wiring

[F] `replica@96bdef0`, netlist; FPGA ports from `fw@bdfd8b0:xdc/zz9000.xdc:L285-290` and module balls from `myir-7020-pinout`, J2.18-30; MP pin functions from `adau1701` Table 64, p46:

| Net (header pin) | ADAU1701 pin | FPGA port | Direction |
|---|---|---|---|
| `Free2_AX_INPUT_BCLK` (J10.4) | MP5, serial-input BCLK | `I2SO_MCLK` | FPGA → ADAU, 1.536 MHz |
| `Free3_AX_SDATA_IN0` (J10.6) | MP0, `SDATA_IN0` | `I2SO_D0` | FPGA → ADAU, playback |
| `Free4_AX_OUTPUT_LRCLK` (J10.8) | MP10, output LRCLK; also MP4, input LRCLK, through R132 (0 Ω) | `I2SO_LRCLK` | ADAU → FPGA, 48 kHz |
| `Free5_AX_OUTPUT_BCLK` (J10.10) | MP11, output BCLK | `I2SO_BCLK` | ADAU → FPGA, 12.288 MHz |
| `Free1_AX_SDATA_OUT0` (J10.2) | MP6, `SDATA_OUT0` | `I2SI_D0` | ADAU → FPGA, capture |
| `Free6_AX_RESET` (J10.1) | `RESET` | `I2SO_RESETn` | FPGA → ADAU |
| `AX_SDATA_IN1` (J111.5) | MP1, `SDATA_IN1` | none | Unused input; no other load |

- [F] MP0 is `SDATA_IN0` (also the TDM input) and MP1 is `SDATA_IN1` (`adau1701` Table 64, p46); the pin table on p11 swaps the two labels, and the Replica's net names follow Table 64.
- [F] The ADAU1701's `SDATA_OUT1`, output BCLK and output LRCLK also feed the SiI9022A's I2S inputs through 0 Ω links R41-R43, and header J7 exposes the SiI9022A's audio pins (`replica@96bdef0`, netlist).
- [F] `SDATA_OUT2` and `SDATA_OUT3` reach header J110 (`replica@96bdef0`, netlist).

## The A9 audio fabric

- [F] The fabric compositor mixes bounded producers into the formatter's transmit ring once per formatter period of 20 ms (`fw@bdfd8b0:docs/audio-fabric.md:L3-5, L40`).
- [F] It has three slots: slot 0 is the pump, never leaseable, and slots 1-2 form the lease plane (`fw@bdfd8b0:os/audio_fabric.h:L42-46, L236-243`).
- [F] MHI and ZZPlay play through the pump; the AHI driver takes a rate-bearing lease and mixes alongside it (`fw@bdfd8b0:docs/audio-fabric.md:L19-25`).
- [F] Zorro III grants two leaseable slots; Zorro II grants one, and only under an acknowledged generation-2 aperture layout; a legacy Zorro II layout has no grant map (`fw@bdfd8b0:os/audio_fabric.h:L236-243`).
- [F] The SDK plan gives the reason for the Zorro II single slot: its 64 KiB host-visible window cannot hold a safe two-slot reserve (`fw@bdfd8b0:sdk/docs/plans/2026-08-27-1453-feat-direct-audio-rings-plan.md:L38`).
- [F] 48 kHz bypass producers are always admissible; any other rate needs one of the two qualified converter slots (`fw@bdfd8b0:os/audio_fabric.h:L229-234`).
- [F] A lease ring holds whole periods of 3840 bytes (`fw@bdfd8b0:os/audio_fabric.h:L221`), which is 20 ms of 48 kHz 16-bit stereo [G: arithmetic].
- [F] Hardware row B4 of `fw` `docs/audio-fabric.md`, a converting 44.1 kHz pump plus two 48 kHz direct-ring producers, passed with no underruns (`fw@bdfd8b0:docs/audio-fabric.md:L138, L167`); the conditions of that record, and its other rows: `topics/sound-paths.md`, "When a producer is late".
- [G] The Zorro II limit is an aperture limit on 68k-side producers; a producer inside the A9, fed from the browser chip rather than the 68k, needs no Zorro aperture.

## Where browser audio enters [G]

- The DSP has no cycles left, so browser audio enters as an A9 fabric producer, mixed with Amiga audio before `SDATA_IN0`, and not as a new DSP input.
- It then needs no harness and no DSP change, stays sample-locked to the ADAU1701's crystal, and puts no load on the 68k.
- Which slot it takes is open (K32):

| Slot | Consequence |
|---|---|
| Share the pump | Contends with ZZPlay and MHI; whether a producer inside the A9 can bind there is unverified |
| Take a lease slot | Shares the lease plane with AHI; on Zorro II, with one lease, the browser and AHI are exclusive |
| Add a fourth slot | Keeps Zorro II equal to Zorro III; the B rows of `fw` `docs/audio-fabric.md` would be re-run on hardware |

- Proposed: a fourth slot as the target and a lease slot for bring-up.

## Routes from the browser chip

| Route | Coupling | What it needs | Notes |
|---|---|---|---|
| PCM over the control link into a fabric producer | V-tracked with a DVI EDID (the default, `sections/browser-chip.md`) | A link carrying 1.536 Mb/s of payload plus control traffic | [G] A UART needs about 2 Mbaud or more on both ends, so 1.5 Mbaud is too slow (K7); Ethernet carries it |
| Receiver I2S through an ASRC into the fabric | V-tracked with an HDMI EDID | +4 PL pins (`topics/zynq-pin-budget.md`) | [G] The ASRC moves the SoC-clocked stream onto the ADAU1701's clock (K7) |
| Audio ring in the PCIe control window | PCIe options | The SoC writes 48 kHz S16LE into a ring in PL BRAM; an A9 producer drains it | [G] The ring lives in the control BAR window that SR1 allows (`topics/plane-safety.md`) |
| I2S harness into `SDATA_IN1` (J111.5) | Any; a Replica option | The browser chip as I2S slave on J10.4 (32·Fs BCLK) and J10.8 (LRCLK), 16-bit, 48 kHz | [G] Conditional on a SigmaStudio compile with a second serial input (K33); a stub on J10.8 loads the LRCLK the FPGA samples, and a corrupted edge drops whole frames (see the coherence check above); [R] x86 boards rarely expose I2S |
| Stock ZZ9000 with the ZZ9000AX audio add-on | No new card | The same fabric producer, fed over Ethernet | [G]; a stock-board path is open (K54) |
| Stock ZZ9000 without AX | No new card | PCM played through Paula by a 68k-side player | [G] Unlike A314's PiAudio, which writes shared chip memory directly (`topics/prior-art.md`, "A computer on a card"), the samples reach chip memory through the 68k; [R] costs 68k load and tens of ms; a stock-board path is open (K54) |

## Latency and A/V sync [G]

- Audio latency La is the SoC sink buffer (about 20 ms) plus the ring fill, one fabric period (20 ms [F `fw@bdfd8b0:docs/audio-fabric.md:L40`]) and the formatter and ADAU1701 pipeline.
- Video lateness Lv is the excess of the hand-off and latch over the presentation deadline Chromium already assumes; it is at most one frame.
- [F] Chromium takes its media clock from its audio renderer when there is one, that renderer is told the output device's latency on every render call, and its video follows that clock (`topics/av-sync.md`, "Times the engine gives").
- A custom sink works only if it is the one Chromium actually uses; which sink it prefers on Linux: `topics/cef-frame-path.md`, "Audio".
- Primary mechanism: an ALSA ioplug plugin writes the ring and reports `snd_pcm_delay` = La − Lv, from the ring fill and a fixed pipeline delay the Zynq publishes, so Chromium renders each frame Lv early and it lands with its audio.
- No-patch alternative: `CefAudioHandler` packets carry a `pts`, which the code takes from Chromium's monotonic clock, so the embedder can time each packet and, with its own record of when each frame arrived, measure the offset; it works with Alloy-style browsers only and mutes normal output (`topics/cef-frame-path.md`, "Audio").
- Correcting that offset means holding video by about 2 frames, which delays all plane content during playback and misses the scroll latency target (`sections/architecture.md`, "Paths") while video plays.
- [G] Proposed: |A/V offset| ≤ 40 ms on a flash-and-beep clip (K34), with scroll latency recorded during playback if a video hold is in use.
- [D] DEC-036: no tolerance for the synchronisation is set; the published tolerances: `topics/av-sync.md`, "Published tolerances".
