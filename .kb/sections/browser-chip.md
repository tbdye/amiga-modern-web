# Browser chip

Scope: the browser-chip candidates, the pass criteria that choose between them, the EDID and colour path into the receiver, and the Chromium host.
Status: current

## Candidates

| SoC | Display path under V-tracked | Under PCIe fetch | Open |
|---|---|---|---|
| RK3588 | [F] RGB444, YCbCr444 and YCbCr422 up to 10 bpc (`linux@6c377d19d4a5:dw_hdmi_qp-rockchip.c:L602-606`); [F] a fractional PLL calculator for TMDS rates (`linux@6c377d19d4a5:hdptx.c:L1054-1120`), so arbitrary rates are plausible [G] | [F] A PCIe 3.0 ×4 controller (`pcie3x4`), plus `pcie3x2` and Gen2 ×1 controllers (`linux@6c377d19d4a5:rk3588-extra.dtsi:L344-372, L431-459`; `rk3588-base.dtsi:L2188-2266`); against a Zynq-7015's Gen2 ×4 block it trains Gen2 ×4 [G] | Chromium's GPU path on the panthor driver is young [R] (K15) |
| x86 (Intel N-series, Ryzen Embedded) | [F] i915 decides RGB range in `intel_hdmi_limited_color_range` (`linux@6c377d19d4a5:intel_hdmi.c:L2232-2257`) and attaches a Broadcast RGB property (`:L2718`) | Yes [G] | Power and thermals; likely its own supply [G] |
| Raspberry Pi CM5 | [F] Two HDMI 2.0 outputs (`cm5-ds` p6); [F] Broadcast RGB property attached (`linux@6c377d19d4a5:vc4_hdmi.c:L591`); [F] the pixel clock is set by `clk_set_rate` (`vc4_hdmi.c:L1524`), exact hits [R] | [F] One-lane PCIe Gen 2, host only (`cm5-ds` p6, p9): too narrow for 1080p60 fetch [G] (below) | Whether its GPU sustains full-screen 1080p60 is in doubt [G] (K15); a middle tier for users below 1080p [D] DEC-012 |

- [F] The RK3588S has only the two Gen2 ×1 controllers: `rk3588s.dtsi` includes `rk3588-base.dtsi` but not `rk3588-extra.dtsi` (`linux@6c377d19d4a5:rk3588s.dtsi:L7-8`; `rk3588-base.dtsi:L2188-2266`); so it cannot serve PCIe fetch [G].
- [F] CM5 power input: a single 5 V input, up to 5 A (`cm5-ds` p6).
- [F] i915 checks an HDMI clock only against a range and per-platform PLL holes (`linux@6c377d19d4a5:intel_hdmi.c:L1885-1922`); whether it then synthesises the Zynq's exact rates is [R], which R-SoC's readback settles.
- [F] The Radxa CM5 module is an RK3588S2 with one HDMI TX (up to 8K60), one eDP TX and one DP TX shared with USB 3.0; the Radxa CM5 Lite is an RK3582 with no GPU (`radxa-cm5`).
- [G] So the Radxa CM5 Lite is no browser chip, and the Radxa CM5, being RK3588S-class, cannot serve PCIe fetch (table above).
- [F] The Raspberry Pi CM5 Lite is a different part, the CM5 without eMMC (`cm5-ds` p6), and stays a candidate [G].
- [G] Fetch link load at 1080p60, 32 bpp: 518 MB/s averaged over active lines (7,680 B per 14.8 µs line, CEA-861 timing; 518.6 MB/s at the Zynq's 148.57 MHz, `fw@8778ef3:os/zz_video_modes.c:L18`), about 600 MB/s with ~15% read overhead (K9).
- [G] A Gen2 lane carries 500 MB/s after 8b/10b and about 400 MB/s usable [R], so ×1 cannot carry it and ×2 is the minimum; whether the ~400 MB/s already includes the read overhead is unverified, and if it does, the ~15% is counted twice.
- [G] The frame average (498 MB/s) applies only with a buffer about 43 lines (332 KB) deep, which the 45-line vblank refills at the frame-average rate; a 4-line FIFO is far smaller.
- [R] Jetson (Orin) has a PCIe root complex and a strong GPU, but Chromium GPU acceleration on L4T is unproven; i.MX95 and MediaTek Genio are unscreened (K19).

## Pass criteria (DC-B)

[G] Per SoC, at full-screen 1080p60 [D] DEC-010:

| Criterion | Pass |
|---|---|
| p95 frame time | ≤ 16.7 ms |
| Missed frames over a 60 s heavy-page scroll | ≤ 1% |
| Latency, p95, from input arriving at the Zynq to the vblank that latches the changed frame (`sections/architecture.md`, "Paths") | ≤ 2 frames + 1 ms (scroll), ≤ 3 frames + 1 ms (DOM change) |

Tie-breakers, in order: integration, price, power.
Under P1 the choice is the cheapest SoC that passes; under P2 the SoC is the user's choice.
[G] Under P1, a CM5 that passes only below full-screen 1080p would ship as a separate product, the middle tier for users below 1080p [D] DEC-012.
[G] R-SoC measures latency with a Chromium trace from input to presentation on the SoC, a proxy that omits the control-link transport the +1 ms covers and the line-FIFO offset; the SoC-side trace must come in at ≤ 2 frames (scroll) and ≤ 3 frames (DOM).
[G] This needs a measurement (R-SoC): published benchmarks report throughput, not p95 frame time [R], and GPU drivers change with each Mesa and Chromium release [R].

## EDID and colour into the receiver (K46)

The receiver must see bit-exact RGB 4:4:4, 8 bpc, full range, at the Zynq's exact timings.

- [F] The shared DRM HDMI helper (used by RK3588 and CM5) tries RGB first in AUTO (`linux@6c377d19d4a5:drm_hdmi_state_helper.c:L704-707`).
- [F] A DVI sink requires RGB at 8 bpc (`drm_hdmi_state_helper.c:L423-427`) and gets full range (`:L392-393`).
- [F] An HDMI sink at a CEA mode in AUTO gets the mode's default range, which is limited for CEA modes (`drm_hdmi_state_helper.c:L395`); limited range is not bit-exact.
- [F] The ADV7611 driver selects limited-range RGB on DVI input with CE timings in automatic mode (`linux@6c377d19d4a5:adv7604.c:L1153-1158`), so the A9 programs a pass-through colour conversion.
- [F] RK3588's bridge connector code attaches no Broadcast RGB property (`linux@6c377d19d4a5:drm_bridge_connector.c`, negative grep).
- [G] Default: a DVI-only EDID listing the Zynq's exact timings as DTDs (K5); its audio then goes over the control link: 48 kHz 16-bit stereo is about 1.92 Mbaud at 8N1, plus control traffic, so a UART route needs about 2 Mbaud or more on both ends, and 1.5 Mbaud is too slow (K7).
- [F] The ADV7611's TMDS clock is 165 MHz maximum (`adv7611` p1); 10 bpc at 1080p60 needs 185.6 MHz on the CEA 148.5 MHz basis (185.7 MHz on the Zynq's 148.57) [G], over that limit.
- [F] The Linux driver drives the ADV7611's hot-plug through an IO-map register, with automatic HPD control once the internal EDID is active, a cable is detected and manual HPD is set; its optional HPD GPIOs serve only the ADV7604 (`linux@6c377d19d4a5:adv7604.c:L523-537, L2897-2906, L3524-3531`).
- [F] TI's TFP401A, the DVI-only alternative, is DVI 1.0 compliant, takes pixel rates up to 165 MHz and outputs 24-bit RGB at one or two pixels per clock, with 3.3 V I/O (`tfp401a` p1); it has no EDID and no audio [R] (K4).

### EDID for every RTG mode

- [F] The RTG table has 13 rows and 11 distinct output timings: 640×400 shares 640×480's, and 640×512 shares 800×600's (`drivers@ad9606b:rtg/mode_timing.h:L23-37`).
- [G] Excluding 2560×1440 leaves 10; three are exact DMT modes (800×600, 1024×768, 1280×1024) that fit standard timings, leaving 7 DTDs.
- [R] A base EDID block holds 2-3 DTDs after the name and range descriptors, and one CTA-861 extension about 6, in the ADV7611's 256-byte EDID RAM; CTA-861 and the ADV7611 hardware manual would verify it.
- [G] Verdict: fits, with 1-2 slots spare; a user-defined custom mode can never have an entry (E18).
- [F] The Zynq's 1600×1200 is 2160 × 1242 at 161.538462 MHz, 60.21 Hz (`fw@8778ef3:os/zz_video_modes.c:L23`): a standard horizontal total with a shortened vertical, so it needs its own DTD; it is neither VESA DMT (2160 × 1250 at 162 MHz) nor a reduced-blanking timing [R], which the VESA DMT standard would verify.
- [G] That mode is also outside the Zynq's timed 150 MHz pixel clock and the datasheet's PLL range (`sections/firmware-and-rtl.md`, "Anchors for a browser plane").

## The Chromium host

- [G] The chip's operating system is assumed to be Linux, with no decision behind it: `sections/architecture.md`, "What each side runs".
- [G] Under V-tracked the SoC uses its own display path, so no off-screen rendering (OSR) copy path is needed.
- [G] Proposed (DEC-014 mechanism, open in K50): the host runs CEF in windowed mode, because CEF's dialog, file, JS-dialog and context-menu handlers map to Amiga ASL, EasyRequest and Intuition popups; stock Chromium does not expose them.
- [F] CEF exposes those handlers in `include/cef_dialog_handler.h`, `cef_jsdialog_handler.h`, `cef_context_menu_handler.h` and `cef_download_handler.h` (`cef@2d4a38cec5a6`).
- Under PCIe the frame path is CEF OSR: `topics/cef-frame-path.md`.
