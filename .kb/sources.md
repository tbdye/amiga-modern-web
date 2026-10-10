# Sources

Scope: every source the KB cites, with its short ID, visibility, link template and pin or access date.
Status: current

Citations elsewhere use these IDs (`AGENTS.md`, "Labels, status and citations").
Pins are as-of: a citation is true at its pin, not necessarily at HEAD.
Re-verify against HEAD before relying on a pinned line (procedure in `_index.md`, "Keeping pins current").

## Repositories

| ID | Source | Visibility | Link template | Pin (verified 2026-10-08) |
|---|---|---|---|---|
| `fw` | ZZ9000 firmware, FPGA RTL and SDK (`BlitterStudio/zz9000-firmware`) | Public | `https://github.com/BlitterStudio/zz9000-firmware/blob/<commit>/<path>#L<a>-L<b>` | `8778ef3` (`v2.8.1-64`), on `origin/master` |
| `drivers` | AmigaOS drivers and tools (`BlitterStudio/zz9000-drivers`) | Public | `https://github.com/BlitterStudio/zz9000-drivers/blob/<commit>/<path>#L<a>-L<b>` | `ad9606b` (`v2.8.1-22`), on `origin/master` |
| `linux` | Linux kernel (`torvalds/linux`) | Public | `https://github.com/torvalds/linux/blob/<commit>/<path>#L<a>-L<b>` | `6c377d19d4a5` (master) |
| `cef` | Chromium Embedded Framework (`chromiumembedded/cef`) | Public | `https://github.com/chromiumembedded/cef/blob/<commit>/<path>#L<a>-L<b>` | `2d4a38cec5a6` (master) |
| `cef-issue` | CEF issue tracker | Public | `https://github.com/chromiumembedded/cef/issues/<n>` | Accessed 2026-10-08 |
| `replica` | ZZ9000 Replica board (KiCad schematic, netlist, datasheets) | **Not public** | None | `96bdef0` |
| `addon` | ZZ9000 VGA-USB Add-On board | **Not public** | None | `faf99db` as reported; facts from it are `[R]` |

**`fw` path abbreviations** (expand before building a link):

| Prefix | Expands to |
|---|---|
| `os/` | `ZZ9000_proto.sdk/ZZ9000OS/src/` |
| `xdc/` | `ZZ9000_proto.srcs/constrs_1/new/` |
| `rtl/` | `ZZ9000_proto.srcs/sources_1/new/` |

Files at the `fw` root (`video_source_sync.v`, `video_formatter.v`, `mntzorro.v`, `videocap_sampler.v`, `zz9000_project.tcl`, `README.md`) carry no prefix.

`linux` paths: `adv7604.c` = `drivers/media/i2c/adv7604.c`; `drm_hdmi_state_helper.c` and `drm_bridge_connector.c` are in `drivers/gpu/drm/display/`; `intel_hdmi.c` = `drivers/gpu/drm/i915/display/intel_hdmi.c`; `vc4_hdmi.c` = `drivers/gpu/drm/vc4/vc4_hdmi.c`; `dw_hdmi_qp-rockchip.c` = `drivers/gpu/drm/rockchip/dw_hdmi_qp-rockchip.c`; `hdptx.c` = `drivers/phy/rockchip/phy-rockchip-samsung-hdptx.c`; `motorcomm.c` = `drivers/net/phy/motorcomm.c`.

## Documents

Datasheets are cited, never committed.
SHA-256 is of the copy that was read; a vendor may replace a file under the same URL.

| ID | Document | Where | SHA-256 | Access note |
|---|---|---|---|---|
| `ds187` | AMD DS187 v1.21 (2020-12-01), Zynq-7000 DC and AC switching characteristics (Z-7007S to Z-7020) | `docs.amd.com`, by document ID | `61e245380c01d2b9cc1350d529265d185e04c1c0379b0fdb3adcba76585c8dac` | Table 18 p15; Tables 50, 51 p33 |
| `ds190` | AMD DS190 v1.10 (2016-09-27), Zynq-7000 overview | `docs.amd.com`, by document ID | `9645d24599147afd989c89f19f50ff2d4c4e142db73fb4fa8fb77d53c7194097` | Resources p3; packages p4 (Tables 2, 3) |
| `sii9022a` | Lattice SiI9022A/SiI9024A HDMI transmitter, SiI-DS-1076-E.01 | Lattice website | `3654d67aabee107820761e0804e52664c60edf42866b76fbfe04c6f870868766` | Copy read from `replica@96bdef0:Docs/datasheets/SiI9022A.pdf` |
| `lvc8t245` | TI SN74LVC8T245, SCES584D (revised May 2026) | `https://www.ti.com/lit/ds/symlink/sn74lvc8t245.pdf` | `c14e874982491aadeb329649325a038a3d1e8a759d2035b08ddb13acc372ad1d` | §5.7 p10, §5.9 p11; TI stamps each download, so a fresh copy of the same revision hashes differently |
| `cm5-ds` | Raspberry Pi Compute Module 5 datasheet, Release 3 (build date printed 08/06/2026) | `https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf` | `80070fefd8db6e8abc6e146c8b7b5fb318ba129cc1e28826936d547fde79c863` | Features p6; PCIe p9 |
| `myir-7015-pinmap` | MYIR MYC-C7Z015 pin map V1.0 (2023-03-09) | `https://www.myirtech.com/download/Zynq7000/MYC-C7Z015_PINMAP.pdf` | `1b6127569b0026f91b61d5fc0ed1e0f47435318ffbb25c962f554b3e869a31d4` | Matched live 2026-10-08 |
| `myir-7020-pinout` | MYIR MYC-C7Z010/20 pin-out | `https://www.myirtech.com/download/Zynq7000/MYC-C7Z010_20_PinOuts.pdf` | `4f859609c63c341d09b974fc1d214123671a4fc5e79fa160aeb442e21565b74a` | Matched live 2026-10-08; identical to the copy in `replica` |
| `ug470`, `ug472`, `ug585` | AMD 7-series configuration, clocking, and Zynq-7000 TRM | `docs.amd.com` | Not fetched | Cited only by `[R]` claims |
| `zorro3` | Zorro III bus specification | — | Not fetched | Cited only by `[R]` claims |

## Web pages

Prices and stock are as shown to an anonymous visitor on the access date.

| ID | Page | Accessed |
|---|---|---|
| `myir-order` | `https://en.myir.cn/order.html` | 2026-10-08 |
| `myir-7015` | `https://www.myirtech.com/list.asp?id=552` and `https://en.myir.cn/Zynq7015/69.html` | 2026-10-08 |
| `myir-7020v2` | `https://en.myir.cn/Zynq701020/43.html` and `https://www.myirtech.com/list.asp?id=694` | 2026-10-08 |
| `myir-7020v1` | `https://www.myirtech.com/list.asp?id=525` | 2026-10-08 |
| `amd-vivado-editions` | `https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/vivado/vivado-buy.html` | 2026-10-08 |
| `jlc-capabilities` | `https://jlcpcb.com/capabilities/pcb-assembly-capabilities` | 2026-10-08 |
| `findchips` | `https://www.findchips.com/search/<MPN>` | 2026-10-08 |
| `lcsc` | `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=<C-number>` (JSON; the HTML search is client-rendered) | 2026-10-08 |
| `pishop` | `https://www.pishop.us/product/raspberry-pi-compute-module-5-<n>gb-ram-lite-cm50<n>000/` | 2026-10-08 |
| `dfrobot` | `https://www.dfrobot.com/product-2820.html`, `product-2901.html` | 2026-10-08 |
| `arace` | `https://arace.tech/products/<handle>` (Radxa store; product JSON at `<handle>.js`): `radxa-cm5-radxa-cm5-lite`, `radxa-x4` | 2026-10-08 |

Bot-blocked sources: Mouser, DigiKey, Octopart and Arrow refused automated access; their figures are not in this KB.
TI and Lattice PDFs fetch directly; some vendors block scripted downloads, and the LCSC JSON endpoint above returns the datasheet link for a C-number.
