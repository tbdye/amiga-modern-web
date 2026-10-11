# Gotchas

Scope: domain sharp edges an agent would otherwise trip on, one per bullet, with the evidence.
Status: draft

## Searching this KB

- `.kb/` is a hidden directory; ripgrep and tools built on it skip it unless given the path or `--hidden` [R]. Search with `.kb/` as the path argument.

## Firmware and RTL

- [F] Every mode init drops source sync before reprogramming, even when the output timing is unchanged (`fw@8778ef3:os/video.c:L1202-1207`); a V variant inheriting that path blinks the plane for about 5 frames on a colour-depth change [G] (E5, fix f5).
- [F] `MAX_TOTAL_LINES` (1152) and the 256-line delay are native-1080p values derived from the capture prefetch guard (`fw@8778ef3:video_source_sync.v:L25-37`); they are not RTG limits, and 1600×1200 and 2560×1440 exceed 1152 lines.
- [F] The pixel clock is `clk_wiz_0`, a PLLE2_ADV reprogrammed through DRP for every mode (`fw@8778ef3:xdc/runtime_pixel_timing.xdc:L6-11`); a PLLE2 has no dynamic phase shift [R `ug472`], so a phase-shift trim means an MMCM swap [G].
- [F] The default native profile is `filtered_60` (`fw@8778ef3:README.md:L129`), an 800×600 or 720×480 output, not a 1080p profile (`os/zz_config.c:L233-236`; `os/video.c:L491-520`); only a centred-1080p native profile with RTG at 1080p60 avoids a monitor retrain on native↔RTG switches (`README.md:L385-391`), and the tracker still relocks [G] (`sections/display-coupling.md`).
- [F] `ZZ9000.CFG` is read at power-on; a soft reset does not reload it, except `fast_ram`, which every reset re-reads (`fw@bdfd8b0:README.md:L118-121`), so test a profile change with a power cycle.
- [F] `docs/native-p96-pip.md` cites `c6341f8` for its scaling (`fw@8778ef3:docs/native-p96-pip.md:L3-7`), a commit that is not on `master` (`fw` `git cat-file -t c6341f8` fails after a fetch); the RTL on `master` is authoritative.
- [F] PS DDR above the linker-managed region (which ends at 0x18000000) is not free: it holds the task queue, the core-1 stack and card-pool ranges A1, A2, B (the Z3 fast-RAM window while fast RAM is not advertised) and C (`fw@bdfd8b0:docs/memory-map.md:L12-17`); take large buffers from the pool, not a fixed range (`sections/firmware-and-rtl.md`, "PS DDR map and card pool").

## Modules and pins

- [F] The 7015 pin map labels the module connectors J2/J3, the 7020 document J1/J2 (`myir-7015-pinmap`, `myir-7020-pinout`); this KB uses the 7020 numbering, so 7015 "J3.14" is J2.14 here.
- [F] On the 7015, PUDC_B moves to J2.14 (`myir-7015-pinmap`, ball K7), which the Replica wires to `HG0`, a live HDMI pixel line (`replica@96bdef0`, netlist, not public): it would float during configuration unless strapped [R `ug470`: PUDC_B must not float, and a strap is 1 kΩ or less].
- [G] So PUDC_B needs an on-module tie or a strap high, with the low level and edge rate then checked at every receiver on `HG0`.
- [F] On the 7020, J2.28 (the ADAU1701's output BCLK, `I2SO_BCLK`, `fw@8778ef3:xdc/zz9000.xdc:L270, L285`) is clock-capable pair L12; on the 7015 the same pin is pair L6, not clock-capable (`evidence/z20.json`, `evidence/z15.json`, section 2 pin 28).
- [F] MYIR labels GTP lanes 0 and 2 "Pcie", lane 1 "Sata" and lane 3 "Sfp", and reference clocks MGTREFCLK0 "Pcie" and MGTREFCLK1 "Sfp" (`myir-7015-pinmap` p1); a label is not a validation, and ×2/×4 PCIe on those pins is unvalidated [G].
- [F] The firmware's PHY check accepts any PHY whose register 2 reads `0x22` or `0x4f51` (`fw@8778ef3:os/ethernet.c:L1007-1024`); `0x0022` is Micrel's OUI word, so it accepts more than the KSZ9031 it names [R].

## Video path

- [F] The ADV7611 driver picks limited-range RGB for DVI input at CE timings in automatic mode (`linux@6c377d19d4a5:adv7604.c:L1153-1158`); bit-exact text needs an explicit pass-through setting.
- [F] An HDMI (not DVI) EDID at a CEA mode gets limited range by default from the shared DRM helper (`linux@6c377d19d4a5:drm_hdmi_state_helper.c:L392-395`).
- [G] 59.94 Hz is 1.67 lines per frame from the Zynq's 60.03 Hz 1080p, outside a ±1 cap: a SoC that falls back to 59.94 never locks (E19).

## Sourcing

- [F] MYIR's direct sample terms cover only the first 2 pieces per customer; above that is by quote (`myir-order`).
