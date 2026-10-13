# Engine options

Scope: which browser engines meet the published browser requirements of two example sites, how each engine is released and patched, measured speed and memory on small Linux computers, hardware video decode by board, and the small computers that could run an engine.
Status: current

[D] DEC-020: a "modern web" browser is one on which nearly any website works; no engine is fixed.
This page takes two sites as its examples, YouTube and Discord's web application.
Nothing here was run or measured by this project: every figure is its source's, read on 2026-10-11.
Ways to put a control program on an engine: `topics/engine-control.md`.

## What the two example sites require

| Site | Published requirement | Source |
|---|---|---|
| YouTube | [F] The newest version of Google Chrome, Firefox or Safari; its upgrade page lists Chrome, Firefox, Edge, Safari and Opera | `yt-78358`; `yt-175292` |
| YouTube, paid films and television | [F] Listed apart, with the same three browsers and an operating-system list (Windows 7+, Mac OS X 10.7+, Ubuntu 10+) | `yt-78358` |
| Discord in a browser | [F] Chrome 108+, Firefox 142+, Opera 72+, Edge 86+, Safari 15.4+; a mobile browser is not supported; older browsers may lack newer features (article edited 2026-07-21) | `discord-req` |

- [G] The two lists name three engine families: Blink (Chrome, Edge, Opera), Gecko (Firefox) and WebKit as Safari; neither names WebKit's Linux ports, Servo or Ladybird.
- [F] Ladybird reports that Cloudflare Turnstile refused it until May 2026, which kept it out of many sites (`lb-news`, 2026-05-31).
- [G] So whether a site works depends on what gatekeeping services accept as well as on standards support; what those services publish: `topics/engine-control.md`, "What a site sees".

## Engine families

| Engine, and how it is obtained | State, by its own project | YouTube | Discord's web application |
|---|---|---|---|
| Blink: Chrome, Chromium, the Chromium Embedded Framework (CEF), Electron, Qt WebEngine | [F] Google's apt repository carried an ARM64 Linux package of Chrome stable, `google-chrome-stable` 155.0.8059.39, at the index read (`chrome-arm64`); [F] Chrome's Linux requirement is an SSE3-capable Intel Pentium 4 or later, or an ARM processor (`chrome-req`) | Named | Named |
| Gecko: Firefox | [F] Linux ARM64 builds since Firefox 136, by APT and tarball (`ff-136`); [F] Raspberry Pi OS ships a Firefox that Raspberry Pi describes as optimised for its boards (`rpi-bookworm`) | Named | Named, from version 142 |
| WebKit: WPE WebKit, WebKitGTK | [F] The 2.54 release series was announced on 2026-09-16 (`wpe-254`); [F] the project calls WPE widely adopted in signage, set-top boxes and automotive (`wpe-site`, about), and its launcher's FAQ says WPE is not a full web browser to be compared with Chrome or Safari (`wpe-site`, FAQ) | Not named; Safari is; [F] WebKit's shared site-quirk code has YouTube-specific entries (`webkit@f0fdd66b6957:Source/WebCore/page/Quirks.cpp:L218, L242-250`) | Not named; Safari is; [F] neither `Quirks.cpp` nor `UserAgentQuirks.cpp` matches "discord" at that commit; no primary statement that it works or fails was found |
| Servo 0.7.0 (2026-10-05) | [F] Its README calls it a prototype web browser engine (`servo@82eb041cbeb2:README.md:L3`); [F] Servo has no 1.0 release, and its long-term-support page says production use should be carefully evaluated (`servo-lts`) | [F] A report that YouTube's search page did not render its results, filed 2026-09-10 (`servo-issues`, #47963) | [F] Reports that Discord login is broken (#36964, filed 2025-05-11) and that Discord does not work (#20815) (`servo-issues`) |
| Ladybird | [F] Its README describes a pre-alpha state, suitable only for developers (`ladybird@32c11f700f0e:README.md:L6`); [F] its newsletter says the engine will not be finished when its alpha starts (`lb-news`, 2026-08-31) | [F] Its newsletters report adaptive streaming on by default since May 2026, and that YouTube already played (`lb-news`, 2026-05-31, 2026-08-31); [F] reports of a crash opening YouTube on Ubuntu 26.04 (#11411) and of Google sign-in on YouTube (#8067) (`lb-issues`) | [F] Its newsletters of May and September 2026 list rendering, interaction and text-input fixes (`lb-news`) |
| Cobalt, YouTube's runtime for televisions | [F] It implements a subset of HTML5, CSS and JavaScript to run applications, the YouTube TV application among them (`cobalt`) | The television application only | Not a general browser |

- [G] By the sites' own lists, two families pass on Linux without qualification: Blink and Gecko; WebKit's Linux ports belong to a named family but are not the named product; Servo and Ladybird do not pass, by their own status statements and the reports on their trackers.
- [F] WebRTC is disabled in WPE 2.54, whose release notes say the old backend is being replaced by one based on LibWebRTC (`wpe-254`); [F] the old backend stays usable in 2.52 and 2.54 through a build option, off by default, incomplete and unsupported (`wpe-site`, FAQ).
- [R] Discord's voice and video calls use WebRTC and its text chat does not; Discord's developer documentation would verify it.
- [F] Servo provides a WebView API for embedding (`servo-site`, home); its frame hand-off was not examined, since it does not pass.
- What WebKit's Linux ports send sites as their identity: `topics/engine-control.md`, "How WebKit's Linux ports identify themselves".
- Not examined: the commercial Flow engine [R].

## Release policy by engine

A policy is stated as its publisher states it; no version here is given as current.

| Engine | Releases | Security fixes | How an update reaches a device | Licence |
|---|---|---|---|---|
| Chrome, Chromium, CEF | `topics/security.md`, "Patching" | Same | Chrome: [F] Google's apt repository, ARM64 included (`chrome-arm64`); Chromium, CEF: `topics/engine-control.md`, "Upkeep by arrangement" | `sections/overview.md`, "Licences" |
| Firefox | [G] Every two weeks on the calendar read: 158 on 2026-10-13, 159 on 2026-10-27, 160 on 2026-11-10 (`ff-calendar`) | [F] The extended-support branches (153 and 115 on that calendar) get a point release with each of those dates (`ff-calendar`) | [F] APT or tarball on ARM64 (`ff-136`); [F] Raspberry Pi states that it has released its Firefox packages on the day Firefox released them (`rpi-bookworm`, comments) | MPL 2.0 [R]; Firefox's licence file would verify it |
| WPE WebKit, WebKitGTK | [F] Two feature releases a year, typically in March and September, with bug-fix releases between; a patch release is compatible at API and ABI level (`wpe-site`, release schedule) | [F] Joint advisories: 6 in 2026 up to 2026-09-29, 10 in 2025, 8 in 2024 (`wpe-site`, security); [F] Debian 13 covers applications built on its `webkit2gtk` package with security support, in a passage that does not name the WPE package (`debian-13-relnotes`, §5.2.3.1) | [G] The distribution's package, or the builder of the device image | [F] A mix of LGPLv2 and BSD (`wpe-site`, FAQ) |
| Servo | [F] Monthly releases; a long-term branch every six months, supported for about nine months with security fixes only, on a best-effort basis and with no specific guarantees (`servo-lts`) | Same | [G] The embedder rebuilds | MPL 2.0 [R]; Servo's licence file would verify it |
| Ladybird | [F] Pre-alpha (`ladybird@32c11f700f0e:README.md:L6`) | — | — | [F] BSD 2-clause (`README.md:L54`) |

- WPE's platform interface and its standing: `topics/engine-interfaces.md`, "WPE WebKit".
- [F] Debian 13 states that applications using its `qtwebengine` package are not covered by security support, and recommends Firefox or Chromium for general browsing (`debian-13-relnotes`, §5.2.3.1).
- Electron and Qt WebEngine: `topics/engine-control.md`, "Upkeep by arrangement".

## Speed and memory on small Linux computers

Speedometer 2.0 and 2.1 scores for Chromium across Raspberry Pi boards are in `topics/prior-art.md`, "App SoC plus FPGA", and are not repeated here.

### Three engines on Raspberry Pi 4 test hosts

[F] The WPE project's public dashboard runs benchmarks continuously on Raspberry Pi 4 devices (`wpe-254`); its API returned the runs below (`wpe-dash`).
Conditions of every row:

- [F] Chrome and Servo ran on one host; the WPE runs are spread over eight other hosts of the same naming, and no WPE run on the Chrome host is in the data read.
- [F] All rows carry the same benchmark version hash.
- [F] The WPE data read is one page of the API, its newest 40 runs, not the whole history.
- [G] The memory fields carry no unit in the API; megabytes is assumed.
- [F] The API's schema says only that memory is "per browser process kind" and names the kinds `wpe`, `minibrowser`, `chrome` and `servo`; what each sums is not documented.
- The memory size of the boards is not stated.

| Browser | Speedometer 3 score | Runs | Resident memory during the run | Private memory |
|---|---|---|---|---|
| Chrome 155.0.8059.39 | 2.36 | 1 (2026-10-08) | 1,500 | 618 |
| WPE WebKit, 39 successive `main` builds (323204-323391) | 1.62 median (1.61-1.63) | 39 (2026-10-09 to 2026-10-11) | 499 (`wpe`) + 137 (`minibrowser`) | 284 + 24 |
| WPE WebKit 2.54 stable branch (`317695.433@webkitglib/2.54`) | 1.53 | 1 (2026-10-09) | 509 + 134 | 295 + 23 |
| Servo 0.7.0, three builds | 0.97 median (0.84-1.00) | 3 (2026-10-08 to 2026-10-10) | 1,362 (2 of the 3 runs; the third has no memory fields) | 1,107 (the same 2 runs) |

- [G] Chrome scores 2.358 / 1.623 = 1.45 times WPE `main`, and 2.358 / 1.527 = 1.54 times the 2.54 branch, each side of the second ratio being one run.
- [G] WPE `main`'s resident memory is (499 + 137) / 1,500 = 42% of Chrome's, and its private memory (284 + 24) / 618 = 50%.
- [G] Private memory is the safer comparison: a resident figure summed over several processes can count shared pages more than once, and the API does not say how it sums.
- [G] Servo scores 0.97 / 1.62 = 0.60 of WPE `main`.
- [F] Speedometer 3 has no bad-run check in this dashboard (the field is null on every row), so the Chrome run is unvetted; the same host's Chrome MotionMark and JetStream runs that day are flagged bad (`wpe-dash`).
- [G] If the Pi 5 to Pi 4 ratio of the Speedometer 2.1 scores in `topics/prior-art.md` (62.5 / 20.5 = 3.05) held for Speedometer 3, the table would give about 7.2 for Chrome and 4.9 for WPE `main` on a Pi 5; the two benchmark versions differ, so this is an extrapolation.

### Other benchmarks

- [F] MotionMark 1.3.1 at 30 fps: WPE's default configuration scores 348 and the dashboard's `skiacpu` variant 258, each the median of its newest 20 runs (2026-10-11, `main` builds, one group of twelve hosts that does not include the Chrome host) (`wpe-dash`).
- [G] 258 / 348 = 74%; the variant's name suggests CPU rasterisation and nothing read defines it, and the GPU is still loaded in those runs (median `average_gpu_load` 28.4 against 37.6, a field with no unit), so this is not a figure without a GPU.
- [F] JetStream 2, split subtests: WPE 42.1 (19 runs on seven hosts), Servo 26.5 (3 runs on the Chrome host) (`wpe-dash`).
- [F] Ladybird's newsletters report about 3.9 on Speedometer 3 and about 64 on Speedometer 2 at the end of August 2026 on the project's own continuous benchmark, and rises of about 50% and 30% across September (`lb-news`, 2026-08-31, 2026-09-30).
- [G] That is about 3.9 × 1.5 = 5.9 and 64 × 1.3 = 83 at the end of September, every input being the source's own rounding; neither post states the runner's hardware, and neither figure is for a small computer.
- [F] Raspberry Pi describes Chromium as probably the most memory-intensive application in Raspberry Pi OS, with one process per tab (`rpi-64bit`).

## Hardware video decode

| Board | Decoders its maker lists | Source |
|---|---|---|
| Pi Zero 2 W, Pi 3A+ | [F] H.264 and MPEG-4, 1080p30 | `rpi-zero2w` p3; `rpi-3aplus` p3 |
| Pi 4, Compute Module 4 | [F] H.265 at 4Kp60; H.264 at 1080p60 | `rpi4-brief` p3; `rpi-cm4` p4 |
| Pi 5, Compute Module 5 | [F] A 4Kp60 HEVC decoder only | `rpi5-brief` p3; `cm5-ds` p6 |
| Radxa ROCK 5B+ (RK3588) | [F] H.265, H.264, VP9, AV1 and AVS2, up to 8K60 | `radxa-5bp` |

- [F] Ladybird's newsletter states that every YouTube video is available as VP9 with Opus in WebM, that some older videos have several quality levels only as H.264, and that the highest qualities are often served only as AV1 (`lb-news`, 2026-08-31); it is a secondary source for YouTube's formats.
- [G] On that statement a Pi 5 lists a decoder for none of YouTube's formats, so YouTube video is decoded in software there whatever the engine, and a Pi 4 has a hardware path for H.264 only.
- A decoder a board lists serves a browser only if the browser's build uses it: `topics/engine-control.md`, "Codecs by build".
- [F] Raspberry Pi's Firefox has V4L2 codec support for the boards' hardware H.264 decoder, which Raspberry Pi says significantly improves performance and reduces CPU load on older models when playing HD video (`rpi-bookworm`).
- [F] Raspberry Pi stated in 2022 that its Chromium package used the V4L2 stateless decoders (`rpi-64bit`, comments).
- [F] WPE decodes through GStreamer and reports decoding limits to pages; a limit can be set per device with `WEBKIT_GST_VIDEO_DECODING_LIMIT` (`wpe-254`).
- [R] Which GStreamer hardware decoders work on a Pi 4, a Pi 5 or an RK3588 board; the GStreamer plugin documentation for each board would verify it.
- Widevine by engine and by build: `topics/engine-control.md`, "Widevine".

## Candidate computers

Identity and durable characteristics only; "—" means the page read does not state it.

| Board | Processor | Memory | Network | USB | Video out | Other | Power input | Typical bare-board current at 5 V | Maker's dated production statement | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Raspberry Pi Zero 2 W | 4 × Cortex-A53, 1 GHz | 512 MB | 2.4 GHz Wi-Fi; no Ethernet | 1 × USB 2.0 with OTG | Mini HDMI; composite | 1 CSI-2; 40-pin header footprint | 5 V, 2.5 A | 350 mA | Until at least January 2030 | [F] `rpi-zero2w` p3; `rpi-power` L30-112 |
| Raspberry Pi 4 Model B | 4 × Cortex-A72, 1.8 GHz | 1, 2, 3, 4 or 8 GB | Gigabit Ethernet; dual-band Wi-Fi | 2 × USB 3.0, 2 × USB 2.0 | 2 × micro HDMI | 2-lane DSI, 2-lane CSI; 40-pin header | 5 V by USB-C or by the header, 3 A minimum | 600 mA | Until at least January 2034 | [F] `rpi4-brief` p3; `rpi-power` L30-112 |
| Raspberry Pi 5 | 4 × Cortex-A76, 2.4 GHz | 1, 2, 4, 8 or 16 GB | Gigabit Ethernet; dual-band Wi-Fi | 2 × USB 3.0, 2 × USB 2.0 | 2 × HDMI, 4Kp60 | 2 × 4-lane MIPI; 40-pin header; PCIe 2.0 ×1 | 5 V, 5 A by USB-C | 800 mA | Until at least January 2036 | [F] `rpi5-brief` p3; `rpi-power` L30-112 |
| Raspberry Pi Compute Module 4 | 4 × Cortex-A72, 1.5 GHz | 1, 2, 4 or 8 GB | Gigabit Ethernet PHY | 1 × USB 2.0, usable as OTG, for which the datasheet says there is no official documentation | 2 × HDMI 2.0 | PCIe Gen 2 ×1; 55 × 40 × 4.7 mm | — | — | Until at least January 2034 | [F] `rpi-cm4` p4-p5, p8; `cm5-ds` p5 |
| Raspberry Pi Compute Module 5 | 4 × Cortex-A76, 2.4 GHz | 2, 4, 8 or 16 GB | Gigabit Ethernet PHY | 1 × USB 2.0, 2 × USB 3.0 | 2 × HDMI 2.0 | 2 × 4-lane MIPI; PCIe Gen 2 ×1; 55 × 40 × 4.7 mm | `topics/power-domains.md`, "Per browser-chip class" | Same | — | [F] `cm5-ds` p6 |
| Radxa ROCK 5B+ | Rockchip RK3588: 4 × Cortex-A76, 4 × Cortex-A55 | — | 2.5 Gb Ethernet | 2 × USB 2.0 host; USB 3.1 host and OTG; USB-C | HDMI out; also an HDMI input, 4Kp60 | 2 × 4-lane CSI; 2 × M.2 with PCIe 3.0, 2 lanes each | USB-C power delivery | — | — | [F] `radxa-5bp` |
| Radxa X4 | Intel N100, with an RP2040 microcontroller on the board | LPDDR5; sizes — | 2.5 Gb Ethernet | 3 × USB 3.2 Gen 2, 1 × USB 2.0 | Dual 4K | 40-pin header; M.2 with PCIe 3.0, 4 lanes | — | — | — | [F] `radxa-x4` |

- [F] Measured board current from Raspberry Pi's documentation, in amps at 5 V: Pi 4B idle 0.6, H.264 playback 0.78 average, stress 1.2 average and 1.25 maximum; Pi 3B idle 0.30, stress 0.85 average and 1.34 maximum; Pi Zero idle 0.10, stress 0.23 average; the table has no Pi 5 or Zero 2 W column (`rpi-power` L129-139).
- [F] Recommended supply: Zero 2 W 2 A; Pi 4B 3 A; Pi 5 5 A, of which up to 1.6 A is for USB peripherals (`rpi-power` L30-112).
- A Raspberry Pi that runs Emu68 as a PiStorm cannot also be this computer: `topics/prior-art.md`, "Fast-68k routes".
- Other RK3588 and x86 modules, by identity: `sections/sourcing.md`.

## Mounting and power in a big-box case

- What a drive lead and a Zorro slot supply: `topics/power-domains.md`, "Zorro slot limits" and "Browser-chip domain: PSU-lead inlets".
- [G] Typical draw at 5 V, from the table and the measured currents above: Zero 2 W 0.35 A = 1.75 W; Pi 4 0.6 A = 3 W idle and 1.25 A = 6.25 W at the measured stress maximum; Pi 5 0.8 A = 4 W typical.
- [G] Each is under the 2.0 A a Zorro slot offers at +5 V.
- The Pi 5's draw under load is not in the table read; its supply rating is 5 A with peripherals.
- [F] A Pi 4 accepts 5 V on its 40-pin header as well as on USB-C (`rpi4-brief` p3).

## Not established

- Whether Discord's web application works in WPE WebKit or WebKitGTK, and whether YouTube does without a user-agent override: a primary statement from either site or from WebKit would settle it.
- Speed and memory of Firefox on any Raspberry Pi, and of any engine on a Pi Zero 2 W, an RK3588 board or a low-end x86 board: a published benchmark from a primary source.
- YouTube playback at 480p, 720p and 1080p (frames dropped, CPU load) on any of these boards, with any engine: no published measurement was found.
- Whether YouTube serves H.264 to an engine that advertises VP9: no source read says.
- The memory size of the dashboard's Pi 4 hosts, the unit of its memory fields and what each process kind sums: the dashboard's own documentation.
- The memory floor of each engine: Chrome's only memory figure here has an assumed unit and comes from a benchmark run.
- Page-load time for YouTube or Discord on any board or engine: none was found.
- The rate at which an engine produces frames for an embedding program on these boards, with the cost of capture and readback: `topics/engine-interfaces.md`, "Not established".
- Power draw of a Pi 5 or an RK3588 board under browser load (for the Compute Module 5: K16 in `unknowns.md`), and power draw and a dated production statement for the Radxa boards: not on the pages read.
- Mechanical mounting, cooling inside the case, and whether a given machine has a spare drive lead (K37 in `unknowns.md`): not researched.

## Sources

Pages and indexes were read on 2026-10-11; a repository is cited at the commit given.
A SHA-256 is of the copy read.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `yt-78358`, `yt-175292` | YouTube Help: system requirements; browser upgrade page | `https://support.google.com/youtube/answer/78358`, `/answer/175292` | 2026-10-11 |
| `discord-req` | Discord: supported browsers and system requirements | `https://support.discord.com/hc/en-us/articles/213491697` | 2026-10-11 |
| `chrome-arm64` | Google's apt repository, stable, ARM64 package index | `https://dl.google.com/linux/chrome/deb/dists/stable/main/binary-arm64/Packages` | 2026-10-11 |
| `chrome-req` | Chrome system requirements | `https://support.google.com/chrome/a/answer/7100626` | 2026-10-11 |
| `ff-136` | Firefox 136.0 release notes | `https://www.mozilla.org/en-US/firefox/136.0/releasenotes/` | 2026-10-11 |
| `ff-calendar` | Firefox release calendar | `https://whattrainisitnow.com/calendar/` | 2026-10-11 |
| `wpe-dash` | WPE performance dashboard API: results for Speedometer 3, MotionMark 1.3.1 and JetStream 2, and its schema | `https://wpe-perf-dashboard.igalia.com/api/v1/` | 2026-10-11 |
| `servo` | Servo | `github.com/servo/servo` | `82eb041cbeb2` |
| `servo-site`, `servo-lts`, `servo-issues` | Servo home page; long-term-support page; issue tracker | `https://servo.org/`; `https://book.servo.org/embedding/lts-release.html`; `github.com/servo/servo/issues` | 2026-10-11 |
| `ladybird` | Ladybird | `github.com/LadybirdBrowser/ladybird` | `32c11f700f0e` |
| `lb-news`, `lb-issues` | Ladybird newsletters of 2026-05-31, 2026-08-31 and 2026-09-30; issue tracker | `https://ladybird.org/newsletter/<date>`; `github.com/LadybirdBrowser/ladybird/issues` | 2026-10-11 |
| `cobalt` | Cobalt home page | `https://cobalt.dev/` | 2026-10-11 |
| `rpi-64bit` | Raspberry Pi news post of 2022-02-02, with its comments | `https://www.raspberrypi.com/news/raspberry-pi-os-64-bit/` | 2026-10-11 |
| `rpi-power` | Raspberry Pi documentation, `documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc` | `github.com/raspberrypi/documentation` | `62ba0a0c2dd5` |
| `rpi-zero2w` | Raspberry Pi Zero 2 W product brief | `datasheets.raspberrypi.com` | SHA-256 `503f348880c00c543e99383ca8759a0b60c1b511cc3c27f216720866159a2bff` |
| `rpi-3aplus` | Raspberry Pi 3 Model A+ product brief | `datasheets.raspberrypi.com` | SHA-256 `d253dcedae53f055ac2f08240ee7d8240f6d9001fd391c6437eefe6c56c18904` |
| `rpi4-brief` | Raspberry Pi 4 Model B product brief | `datasheets.raspberrypi.com` | SHA-256 `7e18898418a47cdbab2f6184ae93fbe6e4943c45475cecbe1db8eb11d32f4328` |
| `rpi5-brief` | Raspberry Pi 5 product brief | `https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf` | SHA-256 `944fc1d70da50f0b8d5947dd4263078f698c79586f29c07f35fcd4b87077dd3f` |
| `rpi-cm4` | Raspberry Pi Compute Module 4 datasheet, Release 4 (build date printed 30/06/2026) | `datasheets.raspberrypi.com` | SHA-256 `d6946f8bb3e0276defa95b99b9d402a01a4805d3de02d53f835e93044ea7af97` |
| `radxa-5bp`, `radxa-x4` | Radxa ROCK 5B+ and X4 product pages | `https://radxa.com/products/rock5/5bp`; `https://radxa.com/products/x/x4` | 2026-10-11 |
