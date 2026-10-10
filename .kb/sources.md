# Sources

Scope: every source the KB cites, with its short ID, visibility, link template and pin or access date.
Status: current

Citations elsewhere use these IDs (`AGENTS.md`, "Labels, status and citations").
Pins are as-of: a citation is true at its pin, not necessarily at HEAD.
Re-verify against HEAD before relying on a pinned line (procedure in `_index.md`, "Keeping pins current").

## Repositories

| ID | Source | Visibility | Link template | Pin (verification dates in `_manifest.yaml`) |
|---|---|---|---|---|
| `fw` | ZZ9000 firmware, FPGA RTL and SDK (`BlitterStudio/zz9000-firmware`) | Public | `https://github.com/BlitterStudio/zz9000-firmware/blob/<commit>/<path>#L<a>-L<b>` | `bdfd8b0` (`v2.8.1-146`), on `origin/master` |
| `drivers` | AmigaOS drivers and tools (`BlitterStudio/zz9000-drivers`) | Public | `https://github.com/BlitterStudio/zz9000-drivers/blob/<commit>/<path>#L<a>-L<b>` | `ad9606b` (`v2.8.1-22`), on `origin/master` |
| `linux` | Linux kernel (`torvalds/linux`) | Public | `https://github.com/torvalds/linux/blob/<commit>/<path>#L<a>-L<b>` | `6c377d19d4a5` (master) |
| `cef` | Chromium Embedded Framework (`chromiumembedded/cef`) | Public | `https://github.com/chromiumembedded/cef/blob/<commit>/<path>#L<a>-L<b>` | `a875f407e36b` (master) |
| `replica` | ZZ9000 Replica board (KiCad schematic, netlist, datasheets) | **Not public** | None | `96bdef0` |

**`fw` path abbreviations** (expand before building a link):

| Prefix | Expands to |
|---|---|
| `os/` | `ZZ9000_proto.sdk/ZZ9000OS/src/` |
| `xdc/` | `ZZ9000_proto.srcs/constrs_1/new/` |
| `rtl/` | `ZZ9000_proto.srcs/sources_1/new/` |

Files at the `fw` root (`video_source_sync.v`, `video_formatter.v`, `mntzorro.v`, `videocap_sampler.v`, `zz9000_project.tcl`, `README.md`) carry no prefix.

`linux` paths: `adv7604.c` = `drivers/media/i2c/adv7604.c`; `drm_hdmi_state_helper.c` and `drm_bridge_connector.c` are in `drivers/gpu/drm/display/`; `intel_hdmi.c` = `drivers/gpu/drm/i915/display/intel_hdmi.c`; `vc4_hdmi.c` = `drivers/gpu/drm/vc4/vc4_hdmi.c`; `dw_hdmi_qp-rockchip.c` = `drivers/gpu/drm/rockchip/dw_hdmi_qp-rockchip.c`; `hdptx.c` = `drivers/phy/rockchip/phy-rockchip-samsung-hdptx.c`; `motorcomm.c` = `drivers/net/phy/motorcomm.c`; `rk3588-base.dtsi`, `rk3588-extra.dtsi`, `rk3588.dtsi` and `rk3588s.dtsi` are in `arch/arm64/boot/dts/rockchip/`.

## Documents

Datasheets are cited, never committed.
SHA-256 is of the copy that was read; a vendor may replace a file under the same URL.

| ID | Document | Where | SHA-256 | Access note |
|---|---|---|---|---|
| `ds187` | AMD DS187 v1.21 (2020-12-01), Zynq-7000 DC and AC switching characteristics (Z-7007S to Z-7020) | `docs.amd.com`, by document ID | `61e245380c01d2b9cc1350d529265d185e04c1c0379b0fdb3adcba76585c8dac` | Table 18 p15; Tables 50, 51 p33 |
| `ds190` | AMD DS190 v1.10 (2016-09-27), Zynq-7000 overview | `docs.amd.com`, by document ID | `9645d24599147afd989c89f19f50ff2d4c4e142db73fb4fa8fb77d53c7194097` | Resources p3; packages p4 (Tables 2, 3) |
| `sii9022a` | Lattice SiI9022A/SiI9024A HDMI transmitter, SiI-DS-1076-E.01 | Lattice website | `3654d67aabee107820761e0804e52664c60edf42866b76fbfe04c6f870868766` | Copy read from `replica@96bdef0:Docs/datasheets/SiI9022A.pdf` |
| `lvc8t245` | TI SN74LVC8T245, SCES584D (revised May 2026) | `https://www.ti.com/lit/ds/symlink/sn74lvc8t245.pdf` | `c14e874982491aadeb329649325a038a3d1e8a759d2035b08ddb13acc372ad1d` | §5.3 p7, §5.7 p10, §5.9 p11; TI stamps each download, so a fresh copy of the same revision hashes differently |
| `adv7611` | Analog Devices ADV7611 datasheet, Rev. D, ADI's Chinese-language edition | `https://datasheet.lcsc.com/datasheet/pdf/d944f827e87cafee093b0fb111927fee.pdf?productCode=C146553` (LCSC C146553, `ADV7611BSWZ`) | `3fad618d4110ee7f9eb89335155f8f4cc2794d4ed58ac773cfb4e09c27059f69` | Features p1; Table 2 and its note 1 p5 (text extraction garbles p5; read the rendered page); fetched 2026-10-10 |
| `cm5-ds` | Raspberry Pi Compute Module 5 datasheet, Release 3 (build date printed 08/06/2026) | `https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf` | `80070fefd8db6e8abc6e146c8b7b5fb318ba129cc1e28826936d547fde79c863` | Features p6; PCIe p9; USB p10; GPIO functions p12-13; carrier connectors p17 |
| `tfp401a` | TI TFP401/TFP401A PanelBus digital receiver, SLDS120H (revised March 2022) | `https://www.ti.com/lit/ds/symlink/tfp401a.pdf` | `b4e30688f4be01f01fdb1841944f9522724fb8ec8d63c780c72f94c2ab036d95` | Features p1; fetched 2026-10-10 |
| `myir-7015-pinmap` | MYIR MYC-C7Z015 pin map V1.0 (2023-03-09) | `https://www.myirtech.com/download/Zynq7000/MYC-C7Z015_PINMAP.pdf` | `1b6127569b0026f91b61d5fc0ed1e0f47435318ffbb25c962f554b3e869a31d4` | Matched live 2026-10-08 |
| `myir-7020-pinout` | MYIR MYC-C7Z010/20 pin-out | `https://www.myirtech.com/download/Zynq7000/MYC-C7Z010_20_PinOuts.pdf` | `4f859609c63c341d09b974fc1d214123671a4fc5e79fa160aeb442e21565b74a` | Matched live 2026-10-08; identical to the copy in `replica` |
| `ug470`, `ug472`, `ug585` | AMD 7-series configuration, clocking, and Zynq-7000 TRM | `docs.amd.com` | Not fetched | Cited only by `[R]` claims |
| `zorro3` | Zorro III bus specification | — | Not fetched | Cited only by `[R]` claims |

## Web pages

| ID | Page | Accessed |
|---|---|---|
| `myir-order` | `https://en.myir.cn/order.html` | 2026-10-08 |
| `myir-7015` | `https://www.myirtech.com/list.asp?id=552` and `https://en.myir.cn/Zynq7015/69.html` | 2026-10-10 |
| `myir-7020v2` | `https://en.myir.cn/Zynq701020/43.html` and `https://www.myirtech.com/list.asp?id=694` | 2026-10-10 |
| `myir-lifecycle` | `https://en.myir.cn/lifecycle.html` | 2026-10-10 |
| `myir-7020v1` | `https://www.myirtech.com/list.asp?id=525` | 2026-10-08 |
| `amd-vivado-editions` | `https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-buy.html` | 2026-10-08 |
| `jlc-capabilities` | `https://jlcpcb.com/capabilities/pcb-assembly-capabilities` | 2026-10-10 |
| `amd-zynq7000` | `https://www.amd.com/en/products/adaptive-socs-and-fpgas/soc/zynq-7000.html` | 2026-10-10 |
| `radxa-cm5` | `https://radxa.com/products/cm/cm5` (hardware specification table) | 2026-10-10 |
| `lcsc` | `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=<C-number>` (JSON; the HTML search is client-rendered) | 2026-10-08; connector rows 2026-10-10 |
| `pishop` | `https://www.pishop.us/product/raspberry-pi-compute-module-5-<n>gb-ram-lite-<part>/`, `<part>` the lower-case CM5 part number (e.g. `cm5004000`) | 2026-10-10 |
| `dfrobot` | `https://www.dfrobot.com/product-2820.html`, `product-2901.html` | 2026-10-10 |
| `arace` | `https://arace.tech/products/<handle>` (Radxa store; product JSON at `<handle>.js`): `radxa-cm5-radxa-cm5-lite`, `radxa-x4` | 2026-10-08 |
| `chromium-release-cycle` | `https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_cycle.md` (Chrome release cycle; "Extended Stable") | 2026-10-10 |
| `chromium-linux-sandbox` | `https://chromium.googlesource.com/chromium/src/+/HEAD/sandbox/linux/README.md` ("Overall Design") | 2026-10-10 |
| `cef-branches` | `https://chromiumembedded.github.io/cef/branches_and_building` (branch support channels and builds) | 2026-10-10 |
| `cef-builds` | `https://cef-builds.spotifycdn.com/index.json` (platform keys) | 2026-10-10 |
| `debian-13-relnotes` | `https://www.debian.org/releases/trixie/release-notes/issues.en.html` (§5.2.3.1, security status of web browsers) | 2026-10-10 |
| `debian-chromium` | `https://qa.debian.org/madison.php?package=chromium&table=debian&text=on` (suites and architectures) | 2026-10-10 |
| `debian-contents` | `https://packages.debian.org/search?searchon=contents&keywords=libcef.so&mode=filename&suite=trixie&arch=any` (only match: syslog-ng's unrelated `libcef.so`) | 2026-10-10 |

TI and Lattice PDFs fetch directly; some vendors block scripted downloads, and the LCSC JSON endpoint above returns the datasheet link for a C-number.
