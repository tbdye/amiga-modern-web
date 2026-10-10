# Display coupling

Scope: how browser pixels reach the Zynq's output without the monitor depending on the browser chip: V-tracked, the tracker, the line FIFO, lock times, the event list, mitigations and the R-TRIM monitor test.
Status: current

## Routes

| Route | Monitor clock | DEC-013 | Status |
|---|---|---|---|
| V-tracked: receiver into the Zynq; the Zynq keeps its clock and trims frame length by ±1 line per frame to follow the SoC; async line FIFO | Zynq, always | Meets it; residual risk is monitor acceptance (K49) | Design under study [G] |
| PCIe fetch (copy as fallback) | Zynq, always | Meets it | Alternative; needs Gen2 ×2 or more at 1080p60 [G] |
| Frame-buffered V: free-running SoC, one frame in memory | Zynq, always | Meets it | Fallback if K49 fails and no trim works; +≤1 frame latency [G] |
| SoC locks to the Zynq's VSYNC | Zynq, always | Meets it | Expected unsupported on all three SoC families [R] (K1) |
| V-locked: the Zynq's output runs from the SoC's pixel clock | SoC | Fails | Out [D] DEC-013 |

## The precedent in shipping firmware

- [F] The opt-in `centered_1080p_match` native profile tracks the captured source cadence by adjusting vertical blanking, and monitor sync continues while the phase converges (`fw@8778ef3:README.md:L395-402`).
- [F] It entered the firmware in `1116f97`, which is in tags v2.8.0 and v2.8.1 (`fw` `git tag --contains 1116f97`).
- [F] It was hardware-tested on one A4000 with a default Z3 card; the README states that this qualifies that setup, not monitor acceptance on every machine (`fw@8778ef3:README.md:L403-407`).
- [F] The tracker decides each output frame's last line inside vertical blanking: not before VSYNC and active video end, and not beyond `min(nominal_last + 27, 1151)` (`fw@8778ef3:video_source_sync.v:L50-63`).
- [F] Constants: `DELAY_LINES` 256, `EXT_LINES` 27, `MAX_TOTAL_LINES` 1152, `PERIOD_TOL` 27, `LOCK_INTERVALS` 4, `WATCHDOG_LINES` 256, `MIN_FRAME_LINES` 512 (`fw@8778ef3:video_source_sync.v:L122-128`).
- [F] Source cadences outside ±27 lines of nominal are rejected and fall back to nominal free-running sync (`fw@8778ef3:video_source_sync.v:L50-54`).
- [F] The native module hides the picture until the phase is safe (`video_hidden`, `picture_ok`) (`fw@8778ef3:video_source_sync.v:L43-48, L264-288, L446-457`).
- [F] At 1080p the frame can run from 1091 to 1152 lines against 1125 nominal; the ramp is about −34 or +27 lines per frame (VEND 1089 at `fw@8778ef3:os/zz_video_modes.c:L18`; clamp at `video_source_sync.v:L198-199`).

## What V-tracked adds

- [G] A tracker variant anchored on the receiver's VSYNC/DE, capped at ±1 line per frame in acquisition and steady state, that never hides RTG and goes to nominal frames on unlock (K2).
- [G] An async line FIFO from the receiver clock to the output clock: 4 lines at 1920 × 32 bpp ≈ 8 BRAM36, absorbing phase, not rate (K3).
- [G] Per-mode tracker constants; today's are native-1080p values tied to the capture read-after-write guard (K48).
- [F] `MAX_TOTAL_LINES` 1152 was derived for the native single-buffer prefetch guard (`fw@8778ef3:video_source_sync.v:L25-37`).
- [G] Read from the RTL, today's tracker would still engage on an RTG mode with Vtotal above 1152 (`nominal_valid` accepts up to 4030, `video_source_sync.v:L152-155`) and then cap every frame at 1152 lines (`:L197-199`), cutting frames short: 1600×1200 (1242) and 2560×1440 (1465) (Vtotals at `os/zz_video_modes.c:L23-24`).

## Steady-state offsets

- [F] The Zynq's 1080p60 is 148.571429 MHz, 2200 × 1125, 60.029 Hz (`fw@8778ef3:os/zz_video_modes.c:L9-10, L18`).
- [F] Against CEA 148.5 MHz that is 0.048%, about 0.54 lines per frame (arithmetic on the above).
- [G] With the Zynq's exact timings published as EDID DTDs, the 10 kHz DTD resolution [R] leaves about 10 ppm (≈ 0.011 lines per frame), inside the ±1 cap.
- [G] 59.94 Hz needs 1.67 lines per frame and today's 720p preset against CEA clocks about 7.6, both outside the cap: the SoC must emit the Zynq's exact timings (K5).

## Lock arithmetic

[G] Phase Φ after an event is uniform on [0, Vtotal); with the ±1 cap and exact DTDs it closes at about 1 line per frame.
Vtotal and refresh are [F] from `fw@8778ef3:os/zz_video_modes.c:L13-24`; times are arithmetic on them.

| RTG mode (Vtotal, Hz) | One direction, worst | Shorter direction, worst | Shorter direction, mean |
|---|---|---|---|
| 1920×1080 (1125, 60.03) | 1124 fr, 18.7 s | **562 fr, 9.4 s** | 4.7 s |
| 1600×1200 (1242, 60.21) | 20.6 s | 10.3 s | 5.2 s |
| 1280×1024 (1066, 60.02) | 17.7 s | 8.9 s | 4.4 s |
| 1280×720 (750, 60.61) | 12.4 s | 6.2 s | 3.1 s |
| 640×480 (525, 59.52) | 8.8 s | 4.4 s | 2.2 s |
| 720×576 (625, 50.20) | 12.4 s | 6.2 s | 3.1 s |

- [F] Today's tracker qualifies lock over 4 plausible intervals, then one warm frame: add about 5 frames (`fw@8778ef3:video_source_sync.v:L126, L446-457, L531-537`).
- [F] Today's tracker has no direction choice: it wraps at the first legal line once the anchor age reaches 256, or is forced at the maximum (`fw@8778ef3:video_source_sync.v:L486-495`).
- [G] Shorter-direction picking is new V-variant RTL.
- [G] At today's +27/−34 ramp, 1080p closes in about 18 frames (0.3 s) worst case in the shorter direction; using it on a live screen depends on R-TRIM.
- [G] Showing the plane before lock does not work: without a frame buffer the picture sits Φ lines off and rolls.

## When the window is not live

[G] In steady use the tracker locks when the SoC's HDMI appears, before any window opens, so opening the window is a plane enable at the next vblank.
Baseline design: ±1 cap, shorter direction, no f1.
Waits are for RTG at 1080p60; other modes take their lock-table figure.

| Event | Monitor resyncs today? | Wait, baseline design, 1080p60 | Note |
|---|---|---|---|
| E16 window open or move, E17 resize | No | 0 (E17 adds 1-3 frames of Chromium relayout [G]) | The common case |
| E15 Amiga blanker | No: DPMS masks syncs only (`fw@8778ef3:video_formatter.v:L1700-1703`) [F] | 0 | Phase kept |
| E22 monitor power-cycle or replug | Monitor side only | 0 [G] | No HPD handling in `os/hdmi.c`, `os/main.c` or `os/video.c` [F, negative grep at `8778ef3`] |
| E5 colour depth, same resolution | No: unchanged output timing keeps the clock and TMDS (`fw@8778ef3:os/video.c:L1174-1192, L1232-1236`) [F] | ≈ 5 frames (≈ 80 ms) blink [G] | Mode init drops source sync (below); f5 removes it |
| E4 RTG resolution change | Yes; each RTG resolution has its own output timing (`drivers@ad9606b:rtg/mode_timing.h:L23-37`) [F] | SoC modeset + relock, ~0.1-0.5 s [G], hidden by the monitor's resync | User-requested, so DEC-013-exempt; needs an EDID DTD per mode |
| E2 cold boot, SoC up; E3 warm reboot; E6 native↔RTG; E20 watchdog | Yes | ≤ 9.4 s after RTG appears, plus the ~5-frame lock qualification | E2, E3, E6 DEC-013-exempt; see below |
| E1 joint cold boot, E7 SoC reboot, E21 firmware update | E1, E21: yes; E7: no | SoC boot (~15-30 s) plus ≤ 9.4 s lock, less if the SoC sets its final mode early [G] | Boot-bound; E1 DEC-013-exempt |
| E8 Chromium restart, no modeset | No | 1-3 s restart [G]; lock held | |
| E9 Chromium modeset, E11 SoC mode/EDID, E12 cable replug, E13 SoC DPMS, E14 tracker watchdog | No | ≤ 9.4 s, not exempt | f4 removes E9, E11, E13 |
| E10 SoC hang | No | Frozen until the heartbeat watchdog (SR9) turns the plane off | |
| E18 unsupported mode, E19 off-EDID timing | — | Never live | Placeholder shown |

- E20, E21: not browser actions and not named in DEC-013.
- [F] A timing change powers TMDS down, so the monitor retrains (`fw@8778ef3:os/hdmi.c:L179-182`).
- [F] An Amiga reset forces native capture mode (`fw@8778ef3:mntzorro.v:L2212`, `videocap_mode_in <= 1`).
- [F] The default native profile is `filtered_60` (`fw@8778ef3:README.md:L129`), which outputs 800×600 for PAL or 720×480 for NTSC (`os/zz_config.c:L233-236`; `os/video.c:L491-520`), not 1080p60.
- [G] So a warm reboot retrains the monitor twice: to native, then back to RTG.
- [F] Exception: with RTG at 1080p60 and a centred-1080p60 native profile, the output timing is unchanged and the HDMI signal keeps running (`fw@8778ef3:README.md:L385-391`).
- [F] Every mode init, native↔RTG switches included, drops source sync before reprogramming, even when the output timing is unchanged (`fw@8778ef3:os/video.c:L1202-1207`).
- [G] So the exception avoids the monitor retrain but not the relock: the SoC lock is lost while the reset holds native capture mode (SR15) and is reacquired after RTG returns, up to 9.4 s at 1080p60.
- [F] The PS watchdog resets the whole PS after about 12.9 s of firmware wedge and the card reboots (`fw@8778ef3:os/watchdog.c:L8-10`).
- [G] The window shows its own RTG pixels while the plane is off; a placeholder ("Starting browser…", "Connecting…", "Not available in this mode") is better than black.
- [G] Raster alignment on entering RTG from native is open: it would cut the E2, E3, E6 waits to about a frame but needs an SR15 rewrite (SR15, a [G] rule, not a decision, bars SoC-derived timing during native↔RTG switches; `topics/plane-safety.md`).

## Mitigations

| ID | Mitigation | Effect [G] | Cost and condition |
|---|---|---|---|
| f1 | PS-DDR acquisition bridge: the receiver writes a 3-frame ring (≈ 18.7 MB at 1080p, 24 bpp) in PS DDR; a reader shows the newest complete frame until lock, then a vblank switch to the line FIFO | **About 1 frame after receiver lock [G]** for E2, E3, E5, E6, E9, E11-E14, E20, at up to +1 frame latency while acquiring. **Gated on the DDR headroom measurement (K25); if that fails, the wait stays ≤ 9.4 s at 1080p60** | No BOM. Yields to native PIP (then ≤ 9.4 s at 1080p60). Brings SR3, SR12 and SR13's frame clause into V-tracked, plus a no-stall read rule; HP1 excluded |
| a′ | Snap at RTG→RTG mode inits: hold TMDS down until the receiver shows the SoC's new mode, then start the raster aligned to it | E4 = SoC modeset + ~1 frame, hidden by the monitor's resync | RTG→RTG only (SR15); every RTG mode change then waits on the SoC, bounded by a timeout |
| f3 | Lock before the window opens | 0 for E16, E17 | Part of the design |
| f4 | SoC hygiene: a compositor holds the mode across Chromium restarts; no DPMS; fixed EDID; modesets only on command; never toggle HPD | Removes E9, E11, E13 | SoC image configuration |
| f5 | Keep the tracker engaged when the output timing is unchanged | Removes E5 | Do not drop source sync when `output_unchanged` |
| c | Use today's +27/−34 ramp | ≤ 0.3 s at 1080p | Only if R-TRIM passes on every monitor |
| b | Frame-buffered V in its own PL DDR3 | ≈ 1 frame after lock, always +≤1 frame | ×16 DDR3 bank; 7020 only (`topics/zynq-pin-budget.md`) |

Dead ends [G]: MMCM phase-shift trim for acquisition (kept as a steady-state remedy for K49); a partial BRAM buffer; showing the plane unlocked (`sections/options-rejected.md`).

[G] The f1 ring would be a card-pool allocation, not a fixed range (`sections/firmware-and-rtl.md`, "PS DDR map and card pool").
[F] Capture writes are idle in RTG: the writeback state machine re-arms only when `videocap_mode_sync` is set (`fw@8778ef3:mntzorro.v:L2023, L2081`).

## EDID for every RTG mode

- [F] The RTG table has 13 rows and 11 distinct output timings: 640×400 shares 640×480's, and 640×512 shares 800×600's (`drivers@ad9606b:rtg/mode_timing.h:L23-37`).
- [G] Excluding 2560×1440 leaves 10; three are exact DMT modes (800×600, 1024×768, 1280×1024) that fit standard timings, leaving 7 DTDs.
- [R] A base EDID block holds 2-3 DTDs after the name and range descriptors, and one CTA-861 extension about 6, in the ADV7611's 256-byte EDID RAM; CTA-861 and the ADV7611 hardware manual would verify it.
- [G] Verdict: fits, with 1-2 slots spare; a user-defined custom mode can never have an entry (E18).

## R-TRIM: the monitor test anyone can run

It needs no new hardware or tools: the profile ships in firmware v2.8.0 and later.
Results are welcome as a GitHub issue on this repository: monitor make and model, sources tested, and anything below.

1. On an existing ZZ9000, install firmware v2.8.1 with its release bitstream, plus `ZZ9000.card` and ZZTop from drivers v2.8.1; the mode needs matching files (`fw@8778ef3:README.md:L403`).
   Releases: `https://github.com/BlitterStudio/zz9000-firmware/releases/tag/v2.8.1` and `https://github.com/BlitterStudio/zz9000-drivers/releases/tag/v2.8.1`.
2. Set `videocap_profile = centered_1080p_match` in `ZZ9000.CFG` beside `BOOT.bin` (`fw@8778ef3:README.md:L129`; sample `ZZ9000.CFG:L15-16`), or choose it in ZZTop under Scandoubler > Output and Save; then power-cycle, because the file is read at power-on (`fw@8778ef3:README.md:L118-122, L409-410, L420-422`).
3. On each monitor, run a PAL and an NTSC source, each in a non-interlaced and an interlaced mode, 10 minutes each.
4. Toggle interlace about 10 times per run; each toggle restarts the tracking (`fw@8778ef3:video_source_sync.v:L439-444`).
5. Record any "no signal" message, mode banner, HDMI audio drop, or blank longer than about half a second; a short hidden picture after a toggle is expected.
6. Record the live capture line count ZZTop shows (`drivers@ad9606b:ZZTop/Sources/ZZTop.c:L870-871`).

[G] R-TRIM is harsher than V-tracked in steady state (up to 3.81 lines per frame for NTSC non-interlaced against 1080p60) and in acquisition (the −34/+27 ramp), so a pass covers the ±1 design.
A blank of 1-3 s or an on-screen mode banner counts as a resync.
