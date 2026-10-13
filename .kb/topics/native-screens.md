# Browsing on native screens

Scope: whether the browser can show on native (chipset) screens such as an NTSC high-res interlaced Workbench, why frame tracking stays on RTG screens, and the proposed buffered path for native screens with its cost and new work.
Status: draft

## Status

| Statement | Standing |
|---|---|
| Frame tracking (the ±1-line tracker) runs only on RTG screens | [G] Follows from [D] DEC-005: tracking in a native mode would make native output take its timing from the browser chip; SR15 encodes it (`topics/plane-safety.md`) |
| The browser shows only on RTG screens at first | [G] A proposed design choice, deferred until RTG works; no decision records it |
| Browsing on native screens from the acquisition buffer | [G] Proposed extension, built only after RTG browsing works and only if DDR headroom allows with native capture, audio and Ethernet running (K67) |

[G] So on an NTSC high-res interlaced Workbench the browser does not show at first, but no decision rules it out.

## Who owns output timing in native modes

| Native profile | Output | Timing owner |
|---|---|---|
| `filtered_60` (the default) | 720×480 for NTSC input, 800×600 for PAL (`fw@bdfd8b0:README.md:L129, L320-321`) | [F] The Zynq: the firmware enables source sync only under `centered_1080p_match` (`fw@bdfd8b0:os/video.c:L943-945`) |
| `filtered_pal`, `filtered_pal_exact`, `filtered_ntsc_exact` | 720×576; the `_exact` variants select non-standard vertical timing presets (`fw@bdfd8b0:os/zz_config.c:L237-248`) | [F] The Zynq: the firmware enables source sync only under `centered_1080p_match` (`fw@bdfd8b0:os/video.c:L943-945`) |
| `full_60`, `full_exact` | 1280×1024 | [F] The Zynq: source sync is enabled only under `centered_1080p_match` (`fw@bdfd8b0:os/video.c:L943-945`); `full_exact` uses fixed PAL/NTSC approximations (about 49.93/59.95 Hz) and does not phase-lock to the input (`fw@bdfd8b0:README.md:L321-322, L393-394`) |
| `centered_1080p_60`, `centered_1080p_50` | 1920×1080, the native picture at (320,28) | [F] The Zynq, free-running, "not input-genlocked" (`fw@bdfd8b0:README.md:L341-349`) |
| `centered_1080p_match` | 1920×1080 | [F] The Amiga: output frame length follows the captured source cadence (`fw@bdfd8b0:README.md:L395-397`; source sync enabled only under this profile, `os/video.c:L943-945`) |

## Why the tracker cannot run in native modes

| Reason | Label |
|---|---|
| Native output would take its timing from the browser chip, which DEC-005 rules out and SR15 bars | [D] DEC-005; [G] SR15 |
| `centered_1080p_match` already follows the Amiga, and one raster cannot follow two sources | [G] |
| Native video must stay frame-for-frame identical (CRC) to today's ZZ9000 outside the browser window, and trimming frame lengths breaks that | [G] |
| The browser chip would have to emit every native preset exactly, the non-standard ~49.93 Hz ones included, and change mode at every PAL/NTSC or profile change | [G] |

[F] The tracker's `MAX_TOTAL_LINES` was derived for the native single-buffer prefetch guard (`sections/display-coupling.md`, "What V-tracked adds").

## The proposed buffered path

[G] Proposed: run the f1 acquisition ring (`sections/display-coupling.md`, "Mitigations") permanently in native modes with no tracking: the receiver writes the window's region into a PS-DDR ring, and a reader shows the newest complete frame at the native output's own timing, composited after the scan doubler in output coordinates.

| Aspect | Assessment [G] |
|---|---|
| DEC-005 | Output timing is never touched, and pixels outside the plane are unchanged; SR15 stands as written, and SR2's native-mode hard gate would narrow to "line-FIFO path RTG-only; the buffered reader may run in native modes" |
| DEC-013 | The monitor never sees the browser chip; in native modes the chip may even change mode freely, and only the plane blinks |
| Latency | +0 to 1 output frame |
| 60 Hz browser on a 50 Hz profile | About 1 frame in 6 dropped (judder) |
| Sharpness | In the full and centred profiles a high-res interlaced pixel spans 2×2 output pixels, so the page can render at twice Workbench's density, flicker-free |
| DDR load, worst case | Capture write ≈ 0.08 GB/s; native scanout read ≈ 0.32 GB/s for 1280×1024 at 32 bpp and 60 Hz, up to ≈ 0.50 GB/s if `centered_1080p` reads the whole 1920×1080 frame (unverified); plane write plus read ≤ 0.63 GB/s at 1280×1024; total ≈ 1.0-1.2 GB/s, permanent and alongside capture writes |
| DDR load, filtered profiles | ≈ 0.4 GB/s |
| Compared with RTG | Close to f1's RTG case (K25), but permanent rather than only while acquiring |
| PIP | No conflict in native modes: the overlay's present hook does not run while capture owns the scanout (below) |

[F] While native capture owns the scanout decisions, the overlay present hook does not run (`fw@bdfd8b0:os/overlay.h:L94-97`).
[G] So the overlay read channel is idle in native modes, and the plane has no present path there today.

## New work it needs

| Work | Basis |
|---|---|
| Native gating in the PL and firmware, including a plane present path that runs while capture owns the scanout | [F] none exists today (`fw@bdfd8b0:os/overlay.h:L94-97`) |
| Screen-to-output mapping from the live capture crop, row-class scaling (×1, ×2, ×4), interlace weave and centring offset | [F] the scaling and centring are per profile (`fw@bdfd8b0:README.md:L322-336`); [G] calibration is open: maths from the ViewPort and DisplayID, or the A9 finding corner markers in the captured buffer (K67) |
| Screen drags, autoscroll and occlusion tracked per vblank | [G] menus, requesters, other windows and screen-title drags punch holes in the plane; the 68k derives the visible region from the window's ClipRects, and the A9 moves the plane on the output frame that shows the matching captured frame, so a screen drag does not tear the plane from its screen |
| Pointer | [G] The Amiga pointer is a chipset sprite inside the captured picture, so a plane over the window hides it. A lo-res sprite pixel at 2× output scale spans 4 output pixels, so a 16-pixel pointer is 64 output pixels wide. [F] The formatter's own sprite is 32×48 (`fw@bdfd8b0:video_formatter.v:L239-242`), composites above the overlay (`:L1137-1140`), and is hidden whenever the firmware sets up native capture (`os/video.c:L741-756`). [G] So the formatter sprite needs re-enabling with pixel doubling or a larger buffer |
| 68k side | [G] The client reports the pointer position while over the window, sends the shape from Chromium, and swaps the Amiga pointer out and back at the window edge; the A9 maps the position to output coordinates. This adds a 68k → Zorro → A9 hop to pointer latency over the page |

## Regression it must pass

[G] Proposed, on top of the native-video regression every board carries (K30, K31):

1. Plane off: CRC identity per profile against today's firmware.
2. Plane on: CRC identity with the plane's rectangle masked, so every pixel outside it is unchanged.
3. A long run with the capture-overflow and prefetch-guard counters at zero.
4. A DDR test of the permanent native case: burst latency against the single-buffer read-after-write guard, with full-frame plane writes, interlaced capture, scan doubling, audio, Ethernet DMA and A9 calibration reads all running.

[G] The same buffered path could serve custom RTG modes and 59.94 Hz, but in RTG it would compete with PIP; it is not proposed for that.
