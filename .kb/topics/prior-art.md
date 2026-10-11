# Prior art

Scope: what other projects shipped that bears on a native-feeling modern browser for Zorro Amigas: native Amiga browsers, fast-68k routes, remote and split-engine browsers, computers on cards inside retro machines, app SoCs paired with FPGAs, and the cost of carrying a Chromium port.
Status: draft

Each row states what a project shipped or published, cited at a commit or with an access date in `sources.md`; the lessons are `[G]`.
Why a particular approach is not under study here is in `sections/options-rejected.md`.

## Native Amiga browsers

| Browser | What it supports | Source |
|---|---|---|
| IBrowse 3.0a | HTML 4.01 and XHTML 1.0, a JavaScript 1.6 engine, TLS 1.3 through OpenSSL 3; released 2023-12-22 | [F] `ibrowse` |
| AWeb 3.6 | JavaScript 1.5 (ECMA-262 3rd edition); an experimental CSS1/CSS2 subset | [F] `aweb3@116516f:README.md:L44, L115, L127-129` |
| Voyager 3.5 | An HTML 3.2 layout engine; JavaScript 1.3, compiled to bytecode and interpreted | [F] `voyager@dd15a86:README.md:L27, L179` |
| NetSurf | HTML 4.01 and CSS 2.1; JavaScript support it calls "primitive and incomplete", disabled by default; release 3.11 for AmigaOS 4 is dated 2023-12-28; the source tree also has an AmigaOS 3 build target (m68k, 68020-60) and a readme for a 3.11 beta package of it | [F] `netsurf-web` (home; documentation/info; downloads/amiga); [F] `netsurf@39da3c3:frontends/amiga/pkg/netsurf_os3.readme:L5-12`, `netsurf@39da3c3:frontends/amiga/Makefile:L7-10` |
| Wayfarer (MorphOS) | MorphOS 3.16 (2022-03-15) ships it and retires the Odyssey browser; a WebKit-based engine | [F] `morphos-news` (release); [R] engine, which the Wayfarer project's own pages would verify |
| OWB (AmigaOS 4) | A WebKit port with a native GUI | [R] os4depot listing |

- [G] The 68k engines in the table (IBrowse, AWeb, Voyager) stop at roughly ES3-era JavaScript, and NetSurf, which also has a 68k target, pairs CSS 2.1 with primitive JavaScript; the ceiling is set by the engines' features, not by CPU speed.
- [G] Wayfarer shows that native feel (fonts, windows, clipboard, menus) comes from the front end around a modern engine, but it needs a PowerPC host OS that a Zorro Amiga does not run.

## Fast-68k routes

- [F] PiStorm with the Musashi emulator performs at roughly a 100-125 MHz 68030 and offers a virtual RTG card (`pistorm@88937a6:README.md:L25, L42`).
- [F] Emu68 runs bare metal on the Raspberry Pi (`emu68@0ba3a89:README.md:L56`), so that Pi cannot also host Linux and Chromium [G].
- [G] Fast 68k CPUs do not change the engine verdict above; they make native chrome snappier and occupy the CPU slot or trapdoor, so they complement a Zorro card rather than compete with it.

## Remote and split-engine browsers

| System | What crosses the wire | What it shows | Source |
|---|---|---|---|
| Browservice | CEF renders off-screen; the view plus a control bar goes to an old browser as PNG or JPEG over HTTP, and input rides in the image-request URLs | Full Chromium compatibility; usable on a 100 Mbit/s LAN; clipboard through Ctrl+C/V plus a form; AltGr fails on some clients | [F] `browservice@02601b0:README.md:L65-67, L73-74, L143` |
| Browservice vice plugins | Browser core and client front end are split by a C plugin API, so a server for native clients could be written as a plugin | No Amiga client is listed | [F] `browservice@02601b0:README.md:L358` |
| WRP | A screenshot proxy: a GIF/PNG/JPEG with a clickable imagemap, or pages converted to simplified HTML | Every interaction reloads a page | [F] `wrp@549d324:README.md:L16-19` |
| Chrome DevTools screencast | `Page.startScreencast` (experimental) sends full frames, JPEG or PNG only | Frame metadata carries scroll offset and page scale, but no damage rectangles | [F] `cdp@c3ed21b:json/browser_protocol.json`, `Page.startScreencast`, `ScreencastFrameMetadata` |
| Opera Mini | Servers run the page's JavaScript and send OBML, an interactive snapshot similar in form to a PDF; elements with mouse listeners become hotspots that cost a server round trip | Timers pause after about 5 s; animations work poorly if at all | [F] `opera-mini-js` |
| Chromium's own pipeline | Paint ops (PaintRecord, its counterpart of SkPicture) go to raster; the compositor thread handles scroll and pinch without Blink; software-raster tiles are about 256×256 | Exact rendering; scroll never waits on the page | [F] `chromium-docs@3078967c68c4:docs/how_cc_works.md:L18, L128, L298` |
| Skia remote glyph cache | `SkStrikeServer` serializes the glyph data a draw needs; `SkStrikeClient` replays it, with discardable handles keeping entries cached | Exact glyphs without a font engine on the client | [F] `skia@3136abe:include/private/chromium/SkChromeRemoteGlyphCache.h:L31-60, L82` |
| RDP GDI acceleration | Encodes the drawing operations that produce an image instead of the image | Lossless UI at lower bandwidth | [F] `ms-rdpegdi` |
| RDP RemoteApp (RAIL) | Presents each remote application as a local window | Native window handling around remote content | [F] `ms-rdperp` §1.3 |
| SPICE | Separate channels: display (commands, images, video streams), inputs, cursor (position, visibility, shape), playback, record; the server drops hidden commands and detects video regions | Lossy only where video is detected | [F] `spice` |
| Citrix browser content redirection | Only the browser viewport is redirected to the client, whose engine renders it | The chrome stays on the server: the inverse cut | [F] `citrix-bcr` |
| Carbonyl | A Chromium-based browser that renders to a terminal | WebGL, video and audio work; runs over SSH | [F] `carbonyl@ab80a27:readme.md:L18-22` |

- [F] At `02601b0` the Browservice README declares the project unmaintained, names v0.9.12.2 (2026-02-09) as the final release, and states that its security model rests on the embedded Chromium being kept current (`browservice@02601b0:README.md:L3-7`).

**Lessons [G]:**

- Pixel streaming (Browservice, WRP, the screencast) sends whole frames, so scroll and text pay latency and compression; it fails native feel by construction.
- Production engines already split at the paint-op and glyph-cache level, and scroll on a compositor thread from cached tiles; that is the split a remote viewport would need.
- SPICE's channel split (cursor, display, video regions, input, audio) is the cleanest template for keeping the pointer local and only video lossy.
- Opera Mini shows server-side layout reaching weak clients, but paused scripts and hotspot round trips break modern web apps; it suits at most a reader mode.
- Client models that need a modern DOM and CSS engine on the client (DOM-diff frameworks, Citrix's redirection) do not fit an Amiga, which has none.

## Display lists and small renderers

- [F] NetSurf front ends draw everything through one `plotter_table` of twelve calls (clip, arc, disc, line, rectangle, polygon, path, bitmap, text, group start and end, flush) (`netsurf@39da3c3:include/netsurf/plotters.h:L102-329`) and three font calls (width, position, split) (`include/netsurf/layout.h:L37-88`).
- [F] NetSurf started on RISC OS, whose common hardware is a 200 MHz StrongARM, and its framebuffer front end ran on a 400 MHz ARM9 (`netsurf-web`, about page).
- [D] DEC-003: rendering Chromium paint ops as a display list on the ZZ9000's A9 is not under study (`sections/options-rejected.md`).

## A computer on a card

- [F] A314 joins a Raspberry Pi to an Amiga through shared memory on the board, with `a314.device` and `a314d` multiplexing logical channels to services (`a314@7e19215:README.md:L8-15`).
- [F] Its services are Amiga-native: a filesystem volume (`PI0:`), a command runner, PiAudio (samples from the Pi into chip memory for Paula, integrated with ALSA), a SANA-II Ethernet driver, disk images, USB input forwarded to `input.device`, RemoteWB and a video player (`a314@7e19215:README.md:L42-66`).
- [G] A314 never shows the Pi's desktop; it exposes the Pi's capabilities as AmigaOS services, which is the model for a browser built as viewport, clipboard, download, file-requester and audio services.
- [R] The A2088/A2286 Bridgeboard showed a PC in an Amiga window, a compatibility box rather than a native experience.

## App SoC plus FPGA

- [F] MiSTeX pairs a Raspberry Pi Zero-class SBC with a separate FPGA board over SPI and GPIO; its rev2 baseboard is manufactured and tested (`mistex@ccf697c:README.md:L4-8, L20`).
- [F] MNT Reform offers swappable processor modules, among them RKX7 (an FPGA) and RCORE RK3588 (`mnt-modularity`).
- [F] Raspberry Pi 5 has two to three times the CPU and GPU performance of the Pi 4 (`rpi5-launch`).
- [R] Speedometer 2.x scores, approximately: quad Cortex-A53 (Pi 3 class) low teens or below; Pi 4 about 20-35; Pi 5 or RK3588 (Cortex-A76) about 60-100.

## Carrying a Chromium port

- [F] Carbonyl carries its Chromium changes as 14 patches (`carbonyl@ab80a27:chromium/patches/chromium/`); v0.0.3 was released 2023-02-18 (`carbonyl` releases).
- [F] The Ozone overview lists easy out-of-tree platforms among its guiding principles, supported by patching one `ozone_extra.gni`, and warns that ports which are hard to keep current ship outdated and potentially insecure Chromium-derived code (`chromium-docs@3078967c68c4:docs/ozone_overview.md:L42-49`).
- [G] Upkeep, tracking Chromium's security releases, is the recurring cost of a fork whatever its patch count (Ozone warning above); a CEF embedder carries the same need (`browservice@02601b0:README.md:L3-7`).
- [G] A CEF embedder or an Ozone platform is the low-upkeep tier; a patch at the compositor or Skia level needs a standing rebase budget.

## Dead ends [G]

- A native modern engine on the 68k at any accelerator speed: the engines' features, not the CPU, set the ceiling.
- Pixel streaming as the main path: it fails scroll and lossless text.
- Client models that need a modern DOM and CSS engine on the Amiga.
- Bulk drawing by the 68k over Zorro: every pixel crosses the bus, so Zorro II falls behind Zorro III.
