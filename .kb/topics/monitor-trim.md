# Monitor trim

Scope: whether monitors accept the frame-length trim (K49): what is known, the trim each Amiga source needs, the acquisition ramp, and how to read R-TRIM results.
Status: draft

The R-TRIM steps are in `sections/display-coupling.md`, "R-TRIM"; the shipping precedent and its one tested setup are in the same file, "The precedent in shipping firmware".

## What is known

- [R] CTA-861 and VESA DMT define fixed timings, not frame-to-frame changes of the vertical total; the two standards would verify it.
- [R] The SiI9022A HDMI transmitter on the ZZ9000 and Replica sends no variable-refresh signalling, so a monitor gets no warning of a trimmed frame; the `sii9022a` datasheet would verify it.
- [R] Public reports on frame-lock features of other video processors (GBS-Control's Frame Time Lock, RetroTINK frame lock) can narrow K49 at the desk but not close it: they cover other trims, sources and monitors.
- [G] So K49 needs a physical test on real monitors: R-TRIM now, R-PLANE later (`unknowns.md`, "Test methods").

## Steady-state trim per source

[G] Lines per frame that the `centered_1080p_match` profile must absorb, from the Zynq's 148.571429 MHz clock at 2200 × 1125 (60.029 Hz) and 2640 × 1125 (50.024 Hz) (`fw@8778ef3:os/zz_video_modes.c:L18, L20`), and standard Amiga timings [R: PAL 3.546895 MHz ÷ 227 colour clocks per line, NTSC 3.579545 MHz ÷ 227.5; the Amiga Hardware Reference Manual would verify them].
[F] The profile outputs 1080p50 for PAL and 1080p60 for NTSC (`fw@8778ef3:os/video.c:L528-534`).

| Source | Source rate | Output | Trim, lines per frame |
|---|---|---|---|
| PAL non-interlaced (313 lines) | 49.920 Hz | 1080p50 | +2.34 |
| PAL interlaced (312.5 lines per field) | 50.000 Hz | 1080p50 | +0.53 |
| NTSC non-interlaced (263 lines) | 59.826 Hz | 1080p60 | +3.81 |
| NTSC interlaced (262.5 lines per field) | 59.940 Hz | 1080p60 | +1.67 |
| NTSC non-interlaced, if 262 lines | 60.054 Hz | 1080p60 | −0.48 |

Positive means the source is slower than the output, so output frames are lengthened.

- [G] NTSC non-interlaced is the harshest steady case; whether a machine sends 262 or 263 lines is read from the live capture line count (R-TRIM step 6).
- [F] `REG_ZZ_VIDEOCAP_STATS` (register `0x4e`) returns the ten-bit frame line count (`fw@bdfd8b0:README.md:L381-382`).
- [G] A fractional trim alternates the vertical total by one line (for example 1127 and 1128), so R-TRIM's steady state also exercises a ±1-line trim.
- [G] For comparison, V-tracked at 1080p60 trims 0.54 lines per frame against CEA timing, or about 0.011 with exact EDID timings (`sections/display-coupling.md`, "Steady-state offsets").

## The acquisition ramp

- [F] Today's tracker ends each 1080p frame between line 1091 and line 1152 against 1125 nominal (`sections/display-coupling.md`, "The precedent in shipping firmware").
- [G] So while acquiring, the phase ramps by about −34 lines per frame (frames shortened, vertical rate +3.1%) or +27 (frames lengthened, −2.3%).
- [G] Closing a full frame of phase then takes about 33 frames (0.55 s) shortening or about 42 (0.69 s) lengthening, and about 18 frames (0.3 s) worst case taking the shorter way.
- [G] An uncapped V variant would ramp like this on every SoC boot, reboot or replug while RTG is visible; that is why the V variant caps the trim at ±1 line per frame (K2).

## Reading R-TRIM results

- [G] R-TRIM is harsher than V-tracked in steady state (up to 3.81 lines per frame) and in acquisition (the −34/+27 ramp), so a pass covers the ±1 design.
- [G] A pass means the monitor holds sync: the picture returns within about 0.5 s of a tracking restart, with no mode banner.
- [G] A blank of 1-3 s, a "no signal" message or an on-screen mode banner counts as a resync.
- [F] The native profile hides the picture while the phase converges (`fw@8778ef3:video_source_sync.v:L43-48`), so a short hidden picture after an interlace toggle is expected; the monitor sees the same timing whether the picture is hidden or not [G].
- [G] A PAL↔NTSC switch changes the output between 1080p50 and 1080p60, a mode change exempt under DEC-013; a resync then is not a trim failure.
- [G] If a monitor objects even at ±1, the remedies are a frequency trim by MMCM dynamic phase shift, which keeps the frame length constant (an MMCM in place of today's PLLE2, `sections/gotchas.md`), or frame-buffered V (P5).
