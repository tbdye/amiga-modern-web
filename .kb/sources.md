# Sources

Scope: every repository whose pin `_manifest.yaml` tracks and every other source the KB cites, except a source that one topic alone cites and defines in its own closing `## Sources` table; for each, its short ID, visibility, link template and pin or access date; also the path abbreviations and the pin checks.
Status: current

Citations elsewhere use these IDs (`AGENTS.md`, "Labels, status and citations").
Pins are as-of: a citation is true at its pin, not necessarily at HEAD.
Re-verify against HEAD before relying on a pinned line ("Pin checks").

## Repositories

| ID | Source | Visibility | Link template | Pin (verification dates in `_manifest.yaml`) |
|---|---|---|---|---|
| `fw` | ZZ9000 firmware, FPGA RTL and SDK (`BlitterStudio/zz9000-firmware`) | Public | `https://github.com/BlitterStudio/zz9000-firmware/blob/<commit>/<path>#L<a>-L<b>` | `cfbb910` (`v2.8.1-172`), on `origin/master` |
| `drivers` | AmigaOS drivers and tools (`BlitterStudio/zz9000-drivers`) | Public | `https://github.com/BlitterStudio/zz9000-drivers/blob/<commit>/<path>#L<a>-L<b>` | `cb6a1c4` (`v2.8.1-32`), on `origin/master` |
| `linux` | Linux kernel (`torvalds/linux`) | Public | `https://github.com/torvalds/linux/blob/<commit>/<path>#L<a>-L<b>` | `6c377d19d4a5` (master) |
| `cef` | Chromium Embedded Framework (`chromiumembedded/cef`) | Public | `https://github.com/chromiumembedded/cef/blob/<commit>/<path>#L<a>-L<b>` | `a875f407e36b` (master) |
| `replica` | ZZ9000 Replica board (KiCad schematic, netlist, datasheets) | **Not public** | None | `96bdef0` |
| `addon` | ZZ9000 VGA-USB add-on (KiCad schematic, netlist) | **Not public** | None | `faf99db` |

**`fw` path abbreviations** (expand before building a link):

| Prefix | Expands to |
|---|---|
| `os/` | `ZZ9000_proto.sdk/ZZ9000OS/src/` |
| `xdc/` | `ZZ9000_proto.srcs/constrs_1/new/` |
| `rtl/` | `ZZ9000_proto.srcs/sources_1/new/` |
| `bsp/` | `ZZ9000_proto.sdk/zz9000_bsp_new/ps7_cortexa9_0/libsrc/emacps_v3_8/src/` (the vendored Ethernet controller driver) |

Files at the `fw` root (`video_source_sync.v`, `video_formatter.v`, `mntzorro.v`, `videocap_sampler.v`, `zz9000_project.tcl`, `README.md`) carry no prefix.

`linux` paths: `adv7604.c` = `drivers/media/i2c/adv7604.c`; `drm_hdmi_state_helper.c` and `drm_bridge_connector.c` are in `drivers/gpu/drm/display/`; `intel_hdmi.c` = `drivers/gpu/drm/i915/display/intel_hdmi.c`; `vc4_hdmi.c` = `drivers/gpu/drm/vc4/vc4_hdmi.c`; `dw_hdmi_qp-rockchip.c` = `drivers/gpu/drm/rockchip/dw_hdmi_qp-rockchip.c`; `hdptx.c` = `drivers/phy/rockchip/phy-rockchip-samsung-hdptx.c`; `motorcomm.c` = `drivers/net/phy/motorcomm.c`; `rk3588-base.dtsi`, `rk3588-extra.dtsi`, `rk3588.dtsi` and `rk3588s.dtsi` are in `arch/arm64/boot/dts/rockchip/`.

## Pin checks

A citation is true at its pin forever; what can change is its truth at HEAD.
Re-pin a citation only when its fact changed at HEAD; a line shift alone is no reason to edit it.
To check a source that moved:

1. List KB citations to it, e.g. `rg -n "fw@" .kb/` (pass `.kb/` explicitly; it is hidden).
2. Run `git diff <pin>..<HEAD> --stat -- <cited paths>`; a claim whose cited paths did not change needs no further check.
3. For each changed path, re-read each claim that cites it at HEAD.
   Fact unchanged, even if its lines moved: leave the citation at its pin.
   Fact changed: re-derive the claim and cite it at the new commit; until then, the file is `stale`.
4. Record the commit checked and its `verified_on` date under `pins` in `_manifest.yaml`.

A public-repo pin must exist on the public remote.
For fw and drivers, run `git fetch` in a clone, then `git branch -r --contains <commit>`; no branch listed fails the pin.
For Linux and CEF, which have no local checkout here, confirm the commit exists at `https://github.com/<owner>/<repo>/commit/<sha>`; a 404 fails the pin.
Triggers: a firmware or driver release tag; a Linux mainline release tag (Linux only); a Replica revision the project relies on; any KB change that cites a source other than Linux whose manifest pin is older than its HEAD.

## Documents

Datasheets are cited, never committed.
SHA-256 is of the copy that was read; a vendor may replace a file under the same URL.

| ID | Document | Where | SHA-256 | Access note |
|---|---|---|---|---|
| `ds187` | AMD DS187 v1.21 (2020-12-01), Zynq-7000 DC and AC switching characteristics (Z-7007S to Z-7020) | `docs.amd.com`, by document ID | `61e245380c01d2b9cc1350d529265d185e04c1c0379b0fdb3adcba76585c8dac` | Table 18 p15; Tables 50, 51 p33; Table 73 p55 (text extraction misaligns its rows; read the rendered page) |
| `ds190` | AMD DS190 v1.10 (2016-09-27), Zynq-7000 overview | `docs.amd.com`, by document ID | `9645d24599147afd989c89f19f50ff2d4c4e142db73fb4fa8fb77d53c7194097` | Resources p3; packages p4 (Tables 2, 3) |
| `sii9022a` | Lattice SiI9022A/SiI9024A HDMI transmitter, SiI-DS-1076-E.01 | Lattice website | `3654d67aabee107820761e0804e52664c60edf42866b76fbfe04c6f870868766` | Copy read from `replica@96bdef0:Docs/datasheets/SiI9022A.pdf` |
| `lvc8t245` | TI SN74LVC8T245, SCES584D (revised May 2026) | `https://www.ti.com/lit/ds/symlink/sn74lvc8t245.pdf` | `c14e874982491aadeb329649325a038a3d1e8a759d2035b08ddb13acc372ad1d` | §5.3 p7, §5.6 p9, §5.7 p10, §5.9 p11, Table 7-1 p15; TI stamps each download, so a fresh copy of the same revision hashes differently |
| `adv7611` | Analog Devices ADV7611 datasheet, Rev. D, ADI's Chinese-language edition | `https://datasheet.lcsc.com/datasheet/pdf/d944f827e87cafee093b0fb111927fee.pdf?productCode=C146553` (LCSC C146553, `ADV7611BSWZ`) | `3fad618d4110ee7f9eb89335155f8f4cc2794d4ed58ac773cfb4e09c27059f69` | Features p1; Table 2 and its note 1 p5 (text extraction garbles p5; read the rendered page); fetched 2026-10-10 |
| `cm5-ds` | Raspberry Pi Compute Module 5 datasheet, Release 3 (build date printed 08/06/2026) | `https://datasheets.raspberrypi.com/cm5/cm5-datasheet.pdf` | `80070fefd8db6e8abc6e146c8b7b5fb318ba129cc1e28826936d547fde79c863` | Features p6; PCIe p9; USB p10; GPIO functions p12-13; power consumption and regulator outputs p16 (§3.3, §3.4); carrier connectors p17 |
| `rpi-zero2w` | Raspberry Pi Zero 2 W product brief | `https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-product-brief.pdf` | `503f348880c00c543e99383ca8759a0b60c1b511cc3c27f216720866159a2bff` | Read 2026-10-11 |
| `rpi-3aplus` | Raspberry Pi 3 Model A+ product brief | `https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-a-plus-product-brief.pdf` | `d253dcedae53f055ac2f08240ee7d8240f6d9001fd391c6437eefe6c56c18904` | Read 2026-10-11 |
| `rpi4-brief` | Raspberry Pi 4 Model B product brief | `https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-product-brief.pdf` | `7e18898418a47cdbab2f6184ae93fbe6e4943c45475cecbe1db8eb11d32f4328` | Read 2026-10-11 |
| `rpi-cm4` | Raspberry Pi Compute Module 4 datasheet, Release 4 (build date printed 30/06/2026) | `https://datasheets.raspberrypi.com/cm4/cm4-datasheet.pdf` | `d6946f8bb3e0276defa95b99b9d402a01a4805d3de02d53f835e93044ea7af97` | Read 2026-10-11; pages are the PDF's |
| `tfp401a` | TI TFP401/TFP401A PanelBus digital receiver, SLDS120H (revised March 2022) | `https://www.ti.com/lit/ds/symlink/tfp401a.pdf` | `b4e30688f4be01f01fdb1841944f9522724fb8ec8d63c780c72f94c2ab036d95` | Features p1; fetched 2026-10-10 |
| `myir-7015-pinmap` | MYIR MYC-C7Z015 pin map V1.0 (2023-03-09) | `https://www.myirtech.com/download/Zynq7000/MYC-C7Z015_PINMAP.pdf` | `1b6127569b0026f91b61d5fc0ed1e0f47435318ffbb25c962f554b3e869a31d4` | Matched live 2026-10-08 |
| `myir-7020-pinout` | MYIR MYC-C7Z010/20 pin-out | `https://www.myirtech.com/download/Zynq7000/MYC-C7Z010_20_PinOuts.pdf` | `4f859609c63c341d09b974fc1d214123671a4fc5e79fa160aeb442e21565b74a` | Matched live 2026-10-08; identical to the copy in `replica` |
| `ug470`, `ug472`, `ug585` | AMD 7-series configuration, clocking, and Zynq-7000 TRM | `docs.amd.com` | Not fetched | Cited only by `[R]` claims |
| `zorro3` | Commodore, The Zorro III Bus Specification, revision 1.10 (1991-03-20) | No vendor URL; copies circulate | `ea68997c74a992c6e88e5e802f8162a2ca0b708e7ce57418299f5200a3a91c13` | PDF pages read: §2.2 p23, §2.3.1 p24, §2.3.2 p25, §2.3.3-§2.3.6 pp26-30, §3.1 p31, §3.1.1 p32, §3.1.2-§3.4 pp33-38, §3.6 p40, §4.1-§4.7 pp44-50, Table 6-1 p62 (from the rendered page), §6.1-§6.2 pp62-63, Appendix A.1 pp76-78 (rows rebuilt from word positions); other citations to it are `[R]` |
| `zz9000-manual-r1` | MNT ZZ9000 Quickstart Manual; page 2 is the schematic, title block "MNT ZZ9000", Rev R-1, 2019-08-04, Id 1/3 | `https://mntre.com/documentation/zz9000-manual-r1.pdf` | `90f9ba269a1135ae9395d1a16c62fc1b4e18e4cc762d2b8f63e34c20f660fe80` | Schematic p2: a vector drawing with outlined lettering and no text layer, read from renders at 450-620 dpi; fetched 2026-10-12 |
| `zz9000-manual-r3` | MNT ZZ9000 R-3 Quickstart Manual; page 2 is the schematic, which has no title block | `https://mntre.com/media/ZZ9000_info_md/zz9000-manual-r3.pdf` | `a924759964507307472cff6d3d101565c0207eba89f2460e3b6eb4cca89cd7b2` | Schematic p2, read the same way; page 2 of the R-4 manual in the same folder (`zz9000-manual-r4.pdf`, SHA-256 `a6b62cc1d542f9d02e0d60760e2adb91382754d37e81905c64a5346fdc4a3286`) renders pixel-identical to it at 300 dpi; fetched 2026-10-12 |
| `a4000-sm` | Commodore A4000 service manual, text-layer scan | No vendor URL; copies circulate | `009e3d5ab3fc9c277705cfb91e33ff9e9920d3c602fc3bd5d91ed622a861b86a` | Power-supply requirements p52 (functional specification 6-14); the text layer misreads "+5", read the rendered page |
| `atx12v` | Intel ATX12V Power Supply Design Guide, version 2.2 (March 2005) | No stable vendor URL; copies circulate | `9e32967d69623ca72f9553c5d613f0260c1746d01e3687d87ffc34a2b32e8cb8` | §4.5.5 p39 |
| `adau1701` | Analog Devices ADAU1701 SigmaDSP, Rev. C | `https://www.analog.com/media/en/technical-documentation/data-sheets/ADAU1701.pdf` | `417167d2fd3dd07771cf9de606b9017e81b2802bd57ed587dd0a09368a60dc33` | Copy read from `replica@96bdef0:Docs/datasheets/ADAU1701JSTZ-RL.pdf`; pin table p11, Table 64 p46 |
| `lvc06a` | TI SN74LVC06A, SCAS596N | `https://www.ti.com/lit/ds/symlink/sn74lvc06a.pdf` | `70171e649d8706f0a1f6956767d366adb6643273a0015ce5d53fbde8abdd7713` | Copy read from `replica@96bdef0:Docs/datasheets/SN74LVC06APWR.pdf`; recommended operating conditions p3 |
| `jk-nsmd350l` | JK-SMD1206 (L) series PPTC datasheet (JK-nSMD350L-12) | Vendor PDF | `4cb4a96dd0832e6c2cdcfd9dc67f6a72061c92e72f9ac4f44404f12b6e805292` | Copy read from `replica@96bdef0:Docs/datasheets/JK-nSMD350L-12.pdf`; thermal derating chart pp3-4 |
| `lutefuse-1206l` | Lutefuse 1206L series PPTC datasheet (1206L250/16AR), revision 2020 | Vendor PDF | `9b5eae932a00b0947da930f441730842a8b315f1e7d76675c3e9453d2bd4e1c3` | Copy read from `replica@96bdef0:Docs/datasheets/1206L250_16AR.pdf`; ratings table p4 |
| `te-171826` | TE Connectivity 171826-4 product data | TE website, by part number | `01115b5280220528241758b932d5814e0ffd79e55df8e4c85f0684290f68edec` | Copy read from `replica@96bdef0:Docs/datasheets/171826-4_product-data.pdf`; contact rating p2 |
| `ksz9031` | Microchip KSZ9031RNX gigabit Ethernet transceiver data sheet, DS00002117F | `https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/00002117F.pdf` | `f7c402264e7b9b65e09f88242a0e8269e4c01e051cd515dbdbabb66dfff4f408` | Preamble p14; auto MDI/MDI-X p16; auto-negotiation p17; fetched 2026-10-11 |

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
| `aminet` | `https://aminet.net/package/<path>` (an Aminet package; cited as `aminet:<path>`, with the file inside its archive; the readme alone is at `https://aminet.net/<path>.readme`) | 2026-10-11 |
| `aminet-rview` | `https://aminet.net/docs/rview/<name>.txt` (archived Usenet reviews; cited as `aminet-rview:<name>`) | 2026-10-11 |
| `zz9000-bench` | `http://www.gregdonner.org/zz9000/benchmarks.html` and the images `bench_gfx_<suffix>.png` beside it (P96Speed 1.2 screenshots on ZZ9000 firmware 1.4 to 1.13; the page gives 2026-05-17 as its last update) | 2026-10-11 |
| `rfc` | `https://www.rfc-editor.org/rfc/rfc<n>.txt` (an RFC as plain text; cited as `rfc:<n>:L<a>-<b>`, by the lines of that file) | 2026-10-11 |

TI and Lattice PDFs fetch directly; some vendors block scripted downloads, and the LCSC JSON endpoint above returns the datasheet link for a C-number.

## Engine and display-server sources

Sources that two or more topics cite; a source that one topic alone cites is in that topic's `## Sources` table.
Web pages and package indexes were read on 2026-10-11.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `chromium` | Chromium source | `github.com/chromium/chromium` (mirror of `chromium.googlesource.com/chromium/src`) | `ceb8f3a65507`; `media/gpu/args.gni` at `4afca57b57f5` |
| `firefox` | Firefox source | `github.com/mozilla-firefox/firefox` | `8e9ac3e12bba` |
| `webkit` | WebKit | `github.com/WebKit/WebKit` | `f0fdd66b6957` |
| `electron` | Electron | `github.com/electron/electron` | `04449e9846ed` |
| `xpra` | xpra | `github.com/Xpra-org/xpra` | `de195aac2dda` |
| `portal` | Desktop portal, `data/org.freedesktop.portal.ScreenCast.xml` | `github.com/flatpak/xdg-desktop-portal` | `ee298d1817fe` |
| `wl-proto` | Wayland protocols | `gitlab.freedesktop.org/wayland/wayland-protocols` | `682ae76bccd6` |
| `wlroots` | wlroots | `gitlab.freedesktop.org/wlroots/wlroots` | `2f08303d3c09`; tags 0.18.2, 0.19.0, 0.20.0; `@0.18.2` and `@0.20.2` are the source packages 0.18.2-3 (Debian 13) and 0.20.2-1+rpt4 (Raspberry Pi archive) |
| `xorgproto` | X.Org protocol documents: `damageproto.txt`, `fixesproto.txt`, `compositeproto.txt`, and `xtest.xml` in the `xextproto` folder of its `specs` directory | `gitlab.freedesktop.org/xorg/proto/xorgproto` | `6d3907b6d5dc` |
| `pkg-index` | arm64 `Packages` and `Sources` indexes with their `Release` files: Debian 13 (main, contrib, non-free, updates, backports, security), Debian testing, and the Raspberry Pi archive's suite trixie | `deb.debian.org/debian/dists/`; `security.debian.org/debian-security/dists/trixie-security/`; `archive.raspberrypi.com/debian/dists/trixie/` | 2026-10-11 |
| `qt` | Qt 6 documentation: Qt WebEngine features, overview and licensing; `QWebEnginePage` | `https://doc.qt.io/qt-6/` | 2026-10-11 |
| `chrome-ext` | Chrome extensions documentation: `tabCapture`, `debugger`, `downloads`, native messaging, Manifest V2 timeline | `https://developer.chrome.com/docs/extensions/` | 2026-10-11 |
| `wpe-site` | WPE WebKit site: about, FAQ, release schedule, security | `https://wpewebkit.org/` | 2026-10-11 |
| `wpe-254` | WPE WebKit 2.54 release post (2026-09-16) | `https://wpewebkit.org/blog/2026-09-16-wpewebkit-2.54.html` | 2026-10-11 |
| `rpi-bookworm` | Raspberry Pi news post of 2023-10-11, with its comments | `https://www.raspberrypi.com/news/bookworm-the-new-version-of-raspberry-pi-os/` | 2026-10-11 |

## Remote-display and RTG sources

Sources that a remote-display or RTG topic and at least one other file cite; a source that one topic alone cites is in that topic's `## Sources` table.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `freerdp` | FreeRDP | `github.com/FreeRDP/FreeRDP` | `87baff6c80e1` |
| `guacd`, `guac-man` | Apache Guacamole's server; its manual | `github.com/apache/guacamole-server`; `github.com/apache/guacamole-manual` | `ae12b8e51aa6`; `482ac54f15ae` |
| `xrdp` | xrdp | `github.com/neutrinolabs/xrdp` | `9cd64936f53e` |
| `wayvnc` | wayvnc | `github.com/any1/wayvnc` | `b286ab91d0f4` |
| `prism` | PrismRTG | `github.com/lainejones/PrismRTG` | `d62ee32` |
| `p96-wiki` | P96 on its publisher's wiki, one page with the release notes | `https://wiki.icomp.de/wiki/P96` | 2026-10-11; last modified 2026-06-20 by the page |
| `p96-drv` | P96 driver development, same wiki | `https://wiki.icomp.de/wiki/P96_Driver_Development` | 2026-10-11; last modified 2026-10-11 by the page |

## Prior-art sources

GitHub repositories use `https://github.com/<owner>/<repo>/blob/<commit>/<path>#L<a>-L<b>`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `browservice` | Browservice | `github.com/ttalvitie/browservice` | `02601b0`; tag v0.9.12.2 at `3824e81` |
| `wrp` | Web Rendering Proxy | `github.com/tenox7/wrp` | `549d324` |
| `vncfox` | VncFox | `github.com/tenox7/vncfox` | `d9c879e` |
| `amifox` | AmiFox, the Amiga client | `github.com/alb42/AmiFox` | `c8b2d36` |
| `amifox-server` | AmiFox's server, a fork of the Web Rendering Proxy | `github.com/alb42/wrp` | `07c7972` |
| `amitube` | AmiTube | `github.com/alb42/AmiTube` | `ab6140f` |
| `twinvnc` | TwinVNC | `github.com/JohnG4489/amiga-twinvnc` | `86a5721`; earlier commits `b478477`, `0190d43` |
| `amifleet68` | amifleet68 | `github.com/thomas-luebker/amifleet68` | `e5abc10` |
| `carbonyl` | Carbonyl | `github.com/fathyb/carbonyl` (releases at `/releases`) | `ab80a27`; releases read 2026-10-10 |
| `a314` | A314 | `github.com/niklasekstrom/a314` | `7e19215` |
| `a314-cp` | A314-cp, the clock-port interface | `github.com/niklasekstrom/clockport_pi_interface` | `a6711deacb55` |
| `a314rtg` | A314RTG, an RTG driver over the A314 clock-port interface | `github.com/lainejones/a314RTG` | `da1b9fe59504` |
| `pistorm` | PiStorm | `github.com/captain-amygdala/pistorm` | `88937a6` on `main`; `cc0244c`, dated 2023-12-12, on branch `pistorm32-lite` |
| `pistorm32-hw` | PiStorm32-lite hardware | `github.com/PiStorm/pistorm32-lite-hardware` | `f6b69cd` |
| `emu68` | Emu68 | `github.com/michalsc/Emu68` | `0ba3a89` |
| `aweb3` | AWeb 3 | `github.com/amigazen/aweb3` | `116516f` |
| `voyager` | Voyager | `github.com/amigazen/Voyager` | `dd15a86` |
| `netsurf` | NetSurf source | `github.com/netsurf-browser/netsurf` | `39da3c3` |
| `mistex` | MiSTeX hardware | `github.com/MiSTeX-devel/MiSTeX-hardware` | `ccf697c` |
| `skia` | Skia | `github.com/google/skia` | `3136abe` |
| `cdp` | Chrome DevTools Protocol | `github.com/ChromeDevTools/devtools-protocol` | `c3ed21b` |
| `chromium-docs` | Chromium design docs `docs/how_cc_works.md`, `docs/ozone_overview.md` | `github.com/chromium/chromium` (mirror of `chromium.googlesource.com/chromium/src`) | `3078967c68c4` |
| `netsurf-web` | NetSurf home, about, documentation/info and downloads/amiga pages | `https://www.netsurf-browser.org/<page>/` | 2026-10-10 |
| `ibrowse` | IBrowse home page | `https://www.ibrowse-dev.net/` | 2026-10-10 |
| `morphos-news` | MorphOS team news | `https://www.morphos-team.net/news` | 2026-10-10 |
| `opera-mini-js` | Opera Mini and JavaScript | `https://dev.opera.com/articles/opera-mini-and-javascript/` | 2026-10-10 |
| `spice` | SPICE for newbies | `https://www.spice-space.org/spice-for-newbies.html` | 2026-10-10 |
| `ms-rdpegdi` | [MS-RDPEGDI] RDP GDI Acceleration Extensions, revision 34.0 | `learn.microsoft.com`, Open Specifications | 2026-10-10 |
| `ms-rdperp` | [MS-RDPERP] RDP Remote Programs Virtual Channel Extension, revision 34.0 | `learn.microsoft.com`, Open Specifications | 2026-10-10 |
| `citrix-bcr` | Citrix browser content redirection | `https://docs.citrix.com/en-us/citrix-virtual-apps-desktops/multimedia/browser-content-redirection.html` | 2026-10-10 |
| `mnt-modularity` | MNT Reform modularity | `https://mntre.com/modularity.html` | 2026-10-10 |
| `rpi5-launch` | Raspberry Pi 5 launch post | `https://www.raspberrypi.com/news/introducing-raspberry-pi-5/` | 2026-10-10 |
| `rpi5-bench` | Raspberry Pi post "Benchmarking Raspberry Pi 5" (2023-10-20): the table of Core Electronics' results | `https://www.raspberrypi.com/news/benchmarking-raspberry-pi-5/` | 2026-10-11 |
| `magpi-pi4-bench` | Raspberry Pi's magazine, "Raspberry Pi 4 specs and benchmarks" (2019-06-24) | `https://magpi.raspberrypi.com/articles/raspberry-pi-4-specs-benchmarks` | 2026-10-11; figures read from the chart images |
| `twinvnc-site` | TwinVNC's site: news, future improvements and known bugs pages | `http://twinvnc.free.fr/` (no HTTPS) | 2026-10-11 |
| `twinvnc-aminet` | Readme of TwinVNC 0.8 beta on Aminet | `https://aminet.net/comm/tcp/TwinVNC0.8beta.readme` | 2026-10-11 |
| `rd-pages` | The 68k Remote Desktop port's site and change log, and rdesktop's ports list, as archived; Aminet and OS4Depot searches for "rdesktop" | Wayback Machine copies of `www.hd-zone.com/rdesktop/rdesktop.htm` (2007-02-10), `www.hd-zone.com/rdesktop/changelog.html` (2007-08-17) and `www.jacco2.dds.nl/rdesktop/index.html` (2005-12-14) | 2026-10-11 |
| `rd68k` | `RDesktop-2005-02-05.src.tar.gz`, source of that port; cited as `rd68k:<path>` | `web.archive.org/web/20060715195151id_/http://www.hd-zone.com:80/rdesktop/dloads-aos/RDesktop-2005-02-05.src.tar.gz` | 2026-10-11; 331,305 bytes; SHA-256 `297f1c9b5d6a1f71b69592d5d29ed4c27159d47c894d0c4fcf2cd9eb39534d95` |
| `xacp` | XACP-ZZ9000, a third-party ZZ9000 firmware line with its Amiga programs and documents | `github.com/Xanxi-Amiga/XACP-ZZ9000` | `cca1f3c`; read as data, nothing built or run |
| `anx` | AmiNetXDuo | `github.com/tinic/AmiNetXDuo` | `9a6f6fc` |
| `roadshow` | Roadshow's home page | `http://roadshow.apc-tcp.de/index-en.php` | 2026-10-11 |
