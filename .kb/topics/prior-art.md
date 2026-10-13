# Prior art

Scope: what other projects shipped that bears on a native-feeling modern browser for Zorro Amigas: native Amiga browsers, fast-68k routes, remote and split-engine browsers with the Amiga programs that an engine elsewhere feeds, computers on cards inside retro machines, app SoCs paired with FPGAs, Speedometer scores by Raspberry Pi board, and the cost of carrying a Chromium port.
Status: draft

Each row states what a project shipped or published, cited at a commit or with an access date in `sources.md`; the lessons are `[G]`.
Nothing here was built or run: a row gives what a source at its pin contains or says, and whether a program works as its documentation says is not established.
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

- [G] IBrowse, AWeb and Voyager, which run on the 68k, stop at roughly ES3-era JavaScript, and NetSurf, which also has a 68k target, pairs CSS 2.1 with primitive JavaScript (rows above); for each of these engines the limit is its features, which a faster CPU does not add.
- [G] Wayfarer shows that native feel (fonts, windows, clipboard, menus) comes from the front end around a modern engine, but it needs a PowerPC host OS that a Zorro Amiga does not run.

## Fast-68k routes

- [F] PiStorm with the Musashi emulator performs at roughly a 100-125 MHz 68030 and offers a virtual RTG card (`pistorm@88937a6:README.md:L25, L42`).
- [F] Emu68 runs bare metal on the Raspberry Pi (`emu68@0ba3a89:README.md:L56`), so that Pi cannot also host Linux and Chromium [G].
- [F] Musashi PiStorm is instead a Linux program (`emulator`) on 32-bit Raspberry Pi OS; on the repository's `main` branch it runs on a Pi 3A+, 3B+ or Zero 2 (a Pi 4 cannot be used), in a 68000 DIP socket, confirmed only on the A500, A500+, A1000 and A2000 (`pistorm@88937a6:README.md:L24, L26-27, L47, L86`).
- [F] The same repository's `pistorm32-lite` branch is for the PiStorm32-lite board alone, lists "Pi4,CM4,Pi3,PiZero2" as compatible boards and needs 32-bit Raspberry Pi OS (`pistorm@cc0244c:README.md:L14-16, L30`); that board is an accelerator for the A1200 (`pistorm32-hw@f6b69cd:README.md:L1-2`); the branch's README states no 68k speed.
- [G] So one Pi can host both the 68k and Chromium only where these boards fit: on `main` at about 68030 class, in 68000-socket machines, on a Pi 3-class board, below the Pi 4-class floor for current Chromium (`sections/overview.md`); on the `pistorm32-lite` branch on a Pi 4 or CM4, in an A1200, at a 68k speed that README does not state.
- [G] Fast 68k CPUs add no features to IBrowse, AWeb, Voyager or NetSurf ("Native Amiga browsers"); they make native chrome snappier and occupy the CPU slot or trapdoor, so they complement a Zorro card rather than compete with it.

## Remote and split-engine browsers

| System | What crosses the wire | What it shows | Source |
|---|---|---|---|
| Browservice | CEF renders off-screen; the view plus a control bar goes to an old browser as PNG or JPEG over HTTP; a JavaScript client there requests the images and sends input in their URLs | Full Chromium compatibility; usable on a 100 Mbit/s LAN; clipboard through Ctrl+C/V plus a form; AltGr fails on some clients | [F] `browservice@02601b0:README.md:L65-67, L73-74, L143` |
| Browservice vice plugins | Browser core and client front end are split by a C plugin API, so a server for native clients could be written as a plugin | No Amiga client is listed | [F] `browservice@02601b0:README.md:L358` |
| WRP | A screenshot proxy: a GIF/PNG/JPEG with a clickable imagemap, or pages converted to simplified HTML | In these two modes every interaction reloads a page | [F] `wrp@549d324:README.md:L16-19` |
| WRP's VNC mode | At the same commit the proxy also has a VNC server (flags `-vnc`, `-vncfps`, `-vncpage`): screencast frames arrive as whole JPEGs and are hashed in 64×64 tiles, and only the tiles a client lacks are encoded; a vertical scroll is found from the frames themselves, by matching sampled rows, and sent as a copy-rectangle with the remainder repainted | A live view of the browser under a tab bar and a navigation bar that the server paints into the frame; at that commit the mode is in no tagged release, and the README names it only in a note on saved sessions | [F] `wrp@549d324:wrp.go:L49-51`; `vncenc.go:L1-7, L50, L294-388`; `vnc.go:L1-6, L71-80, L2504-2525`; `README.md:L201` |
| VncFox | A container recipe with no program code of its own: Firefox ESR under the ratpoison window manager on a TigerVNC server, port 5900, 1024×768 by default | Firefox's own interface, served over VNC; VNC password authentication only, with the password printed in its README; the repository has no licence file | [F] `vncfox@d9c879e:Dockerfile:L1-16, L32-33`; `xinitrc`; `vncserver-config-defaults:L2`; `README.md:L16, L42` |
| AmiFox, with its server (a fork of WRP) | One image of the page per interaction, as PNG, GIF, JPEG or IFF ILBM, fetched over HTTP from a server that drives Chrome and takes one screenshot per request; a click, a click-and-drag or typed text goes back as a request | A native Amiga program on the MUI toolkit, whose own window shell surrounds the image; the image is decoded by AmigaOS DataTypes, remapped to the window's screen, and redrawn at the new offset on a scroll; its guide says "You cant watch YouTube clips with AmiFox" | [F] `amifox@c8b2d36:AmiFox.guide:L56, L78, L286-287, L412-416`; `threadunit.pas:L411-437`; `mainwinunit.pas:L1087, L1190-1225, L1263-1267, L1302-1305`; `amifox-server@07c7972:README.md:L16`; `wrp.go:L410-420, L465-501` |
| AmiTube | A server downloads a YouTube video and converts it to a file: CDXL 160 or 320 pixels wide, or MPEG-1 320 pixels wide with MP2 sound | A native MUI program that searches, downloads the converted file to disk and hands it to an external player; that file is not a live stream, and the guide also describes starting an external player, such as mplayer or ffplay, on a video's address | [F] `amitube@ab6140f:AmiTube.guide:L9-13, L42-43, L349-354, L372-378`; `server/src/prg/atconvert.sh:L44` |
| TwinVNC | VNC (RFB 3.3 to 3.8): rectangles in Raw, RRE, CoRRE, Hextile, Zlib, ZlibHex, ZRLE and Tight, copy-rectangle and cursor shapes; keys, pointer and clipboard text go back | A native Amiga VNC client on GadTools, by default on its own screen, showing whatever desktop the server has; it decodes into a frame buffer in RAM and, on a CyberGraphX screen, writes a 16- or 32-bit frame buffer with `WritePixelArray` as 32-bit ARGB, widening the 16-bit one first; `p96WritePixelArray` and `LockBitMap` do not occur in its source; a copy-rectangle is a `ClipBlit` only on its own screen, and in a window on another screen a copy in RAM and a rewrite | [F] `twinvnc@86a5721:twinvnc/rfb.h:L7-11`; `twinvnc/server.c:L292-349`; `twinvnc/config.c:L171`; `twinvnc/gfxnormal.c:L466-517`; `twinvnc/decodercopyrect.c:L33-61`; `twinvnc/input.c:L311-420`; `twinvnc/client.c:L247-273` |
| amifleet68 | Its VNC window is an RFB 3.3 client that asks for Raw and CopyRect only | A MUI console for administering other Amigas, built for a plain 68000; it keeps a frame buffer of 32-bit pixels in RAM, writes it with `WritePixelArray` as ARGB or with `WriteChunkyPixels`, and makes no blit call | [F] `amifleet68@e5abc10:README.md:L3-7, L29-34`; `src/vnc.c:L2-11`; `src/view.c:L4-13, L149-153`; `Makefile:L3` |
| A 68k Remote Desktop client (a port of rdesktop) | RDP: bitmaps at 8, 15, 16 or 24 bits and the drawing orders it lists; sound; clipboard text | A remote desktop in an Intuition window on a public screen, or on its own screen; it reads 15-, 16- and 24-bit pixels low byte first, converts each to 32-bit ARGB and writes with CyberGraphX's `WritePixelArray`, making no Picasso96 call; its site announces a 68k build for AmigaOS 3.x on 2005-03-02; `base/` is the archive's `rdesktop-2004-04-17-0600/` directory | [F] `rd68k:amiga.c:L633-708, L1336-1381, L1481-1550`; `base/rdp.c:L428-456`; `rdpsnd_ahi.c:L79-81`; `amiga_clipboard.c:L197-269`; `rd-pages` |
| Chrome DevTools screencast | `Page.startScreencast` (experimental) sends full frames, JPEG or PNG only | Frame metadata carries scroll offset and page scale, but no damage rectangles | [F] `cdp@c3ed21b:json/browser_protocol.json`, `Page.startScreencast`, `ScreencastFrameMetadata` |
| Opera Mini | Servers run the page's JavaScript and send OBML, an interactive snapshot similar in form to a PDF; elements with mouse listeners become hotspots that cost a server round trip | Timers pause after about 5 s; animations work poorly if at all | [F] `opera-mini-js` |
| Chromium's own pipeline | Paint ops (PaintRecord, its counterpart of SkPicture) go to raster; the compositor thread handles scroll and pinch without Blink; software-raster tiles are about 256×256 | Exact rendering; scroll never waits on the page | [F] `chromium-docs@3078967c68c4:docs/how_cc_works.md:L18, L128, L298` |
| Skia remote glyph cache | `SkStrikeServer` serializes the glyph data a draw needs; `SkStrikeClient` replays it, with discardable handles keeping entries cached | Exact glyphs without a font engine on the client | [F] `skia@3136abe:include/private/chromium/SkChromeRemoteGlyphCache.h:L31-60, L82` |
| RDP GDI acceleration, as specified | Encodes the drawing operations that produce an image instead of the image | Lossless UI at lower bandwidth | [F] `ms-rdpegdi` §1.3.1 |
| RDP RemoteApp (RAIL), as specified | Presents each remote application as a local one: a client window for every remote window, which a client that declares the option moves and resizes locally | The client's windows "exactly mimic the appearance" of the remote ones | [F] `ms-rdperp` §1.3, §1.3.2.5 |
| SPICE | Separate channels: display (commands, images, video streams), inputs, cursor (position, visibility, shape), playback, record; the server drops hidden commands and detects video regions | Lossy only where video is detected | [F] `spice` |
| Citrix browser content redirection | Only the browser viewport is redirected to the client, whose engine renders it | The chrome stays on the server: the inverse cut | [F] `citrix-bcr` |
| Carbonyl | A Chromium-based browser that renders to a terminal | WebGL, video and audio work; runs over SSH | [F] `carbonyl@ab80a27:readme.md:L18-22` |

- [F] At `02601b0`, dated 2026-09-11, the Browservice README declares the project unmaintained, names v0.9.12.2 (2026-02-09) as the final release, and states that its security model rests on the embedded Chromium being kept current (`browservice@02601b0:README.md:L3-7`).
- [F] That notice records a gap of several months in the project's builds and gives no reason for stopping; the README at release v0.9.12.2 carries an earlier notice, dated 2024-06-27, that development time is very limited and that the main focus will be builds with the latest Chromium, as critical for security (`browservice@02601b0:README.md:L3-9`; `browservice@3824e81:README.md:L5-7`).
- [F] AmiFox's guide, whose header reads version 0.3 (2023-03-21), gives "4 to 8 seconds loading time" on an Amiga 1200 with a 68060 at 100 MHz (RTG) and "9 to 29 seconds" on an Amiga 4000 with a 68040 at 25 MHz (AGA), naming no page, image format, size or network (`amifox@c8b2d36:AmiFox.guide:L4, L69-73`).
- The Amiga programs among these rows part by part, TwinVNC's licence notices and the Remote Desktop client's source: `topics/prior-art-remote-clients.md`.

**Lessons [G]:**

- Browservice, WRP's two image modes and the screencast send whole frames, so a scroll resends the view; WRP's VNC mode cuts the same screencast into changed tiles and scroll copies on the server, from frames the screencast has already coded as JPEG (rows above).
- Production engines already split at the paint-op and glyph-cache level, and scroll on a compositor thread from cached tiles; that is the split a remote viewport would need.
- SPICE's channel split (cursor, display, video regions, input, audio) is the cleanest template for keeping the pointer local and only video lossy.
- Opera Mini shows server-side layout reaching weak clients, but paused scripts and hotspot round trips break modern web apps; it suits at most a reader mode.
- Client models that need a modern DOM and CSS engine on the client (DOM-diff frameworks, Citrix's redirection) do not fit IBrowse, AWeb, Voyager or NetSurf, whose features stop short of one ("Native Amiga browsers").

## Display lists and small renderers

- [F] NetSurf front ends draw everything through one `plotter_table` of twelve calls (clip, arc, disc, line, rectangle, polygon, path, bitmap, text, group start and end, flush) (`netsurf@39da3c3:include/netsurf/plotters.h:L102-329`) and three font calls (width, position, split) (`include/netsurf/layout.h:L37-88`).
- [F] NetSurf started on RISC OS, whose common hardware is a 200 MHz StrongARM, and its framebuffer front end ran on a 400 MHz ARM9 (`netsurf-web`, about page).
- [D] DEC-003: a networked browser computer is not ruled out, nor is any role chosen for it.
- [G] Rendering Chromium paint ops as a display list on the ZZ9000's A9 belongs to the remote tier (family A, DC-F), which is not part of the design under study (`sections/options-rejected.md`).

## A computer on a card

- [F] A314 joins a Raspberry Pi to an Amiga through shared memory on the board, with `a314.device` and `a314d` multiplexing logical channels to services (`a314@7e19215:README.md:L8-15`).
- [F] Its services are Amiga-native: a filesystem volume (`PI0:`), a command runner, PiAudio (samples from the Pi into chip memory for Paula, integrated with ALSA), a SANA-II Ethernet driver, disk images, USB input forwarded to `input.device`, RemoteWB and a video player (`a314@7e19215:README.md:L42-66`).
- [F] A314-cp, the variant for "Any Amiga with clockport", shares a 64 kB memory between the Amiga and the Pi through an interface 8 bits wide with four registers (`a314@7e19215:README.md:L30`; `a314-cp@a6711deacb55:README.md:L3-9, L22-38`).
- [F] Its link rate is published only as a third party's statement: the README of A314RTG, a Picasso96 driver that sends changed pixels from the Amiga to the Pi over that link, calls it "a ~70–120 KB/s byte-at-a-time link" and gives no method (`a314rtg@da1b9fe59504:README.md:L10-13`).
- [G] A314 never shows the Pi's desktop; it exposes the Pi's capabilities as AmigaOS services, which is the model for a browser built as viewport, clipboard, download, file-requester and audio services.
- [R] The A2088/A2286 Bridgeboard showed a PC in an Amiga window, a compatibility box rather than a native experience.

## App SoC plus FPGA

- [F] MiSTeX pairs a Raspberry Pi Zero-class SBC with a separate FPGA board over SPI and GPIO; its rev2 baseboard is manufactured and tested (`mistex@ccf697c:README.md:L4-8, L20`).
- [F] MNT Reform offers swappable processor modules, among them RKX7 (an FPGA) and RCORE RK3588 (`mnt-modularity`).
- [F] Raspberry Pi 5 has two to three times the CPU and GPU performance of the Pi 4 (`rpi5-launch`).
- [F] Speedometer scores by Raspberry Pi board (`magpi-pi4-bench`; `rpi5-bench`):

| Raspberry Pi | Speedometer 2.0 | Speedometer 2.1 |
|---|---|---|
| A; B; B+ | 0.667; 0.596; 0.623 | |
| Zero; Zero W | 1.04; 0.961 | |
| 2 | 4.138 | |
| 3; 3B+; 3A+ | 7.56; 8.55; 6.35 | |
| 4 | 16.91 | 20.5 |
| 5 | | 62.5 |

- [F] The 2.0 column is a chart in a 2019 article in Raspberry Pi's magazine, labelled runs per minute and read from the chart image; the article says the test measures the Chromium browser, names no Chromium version or operating system for it, and says that it "hinges not only on CPU performance but on memory speed and capacity" and "proved too much for Raspberry Pi A+" (`magpi-pi4-bench`).
- [F] The 2.1 column is from a table of Core Electronics' results that a Raspberry Pi post of 2023-10-20 reproduces, which gives the increase as 3.05 times and names no browser, browser version or operating system for those two scores (`rpi5-bench`).
- [G] The columns differ in benchmark version, year and source, so a 2.0 score is not comparable with a 2.1 score.

## Carrying a Chromium port

- [F] Carbonyl carries its Chromium changes as 14 patches (`carbonyl@ab80a27:chromium/patches/chromium/`); v0.0.3 was released 2023-02-18 (`carbonyl` releases).
- [F] The Ozone overview lists easy out-of-tree platforms among its guiding principles, supported by patching one `ozone_extra.gni`, and warns that ports which are hard to keep current ship outdated and potentially insecure Chromium-derived code (`chromium-docs@3078967c68c4:docs/ozone_overview.md:L42-49`).
- [G] Upkeep, tracking Chromium's security releases, is the recurring cost of a fork whatever its patch count (Ozone warning above); a CEF embedder carries the same need (`browservice@02601b0:README.md:L3-7`).
- [G] A CEF embedder or an Ozone platform is the low-upkeep tier; a patch at the compositor or Skia level needs a standing rebase budget; on record against the first, the two notices of one CEF embedder, Browservice ("Remote and split-engine browsers").

## Dead ends [G]

- IBrowse, AWeb, Voyager or NetSurf on a faster accelerator as the way to the current web: the limit of each is its features, which CPU speed does not add ("Native Amiga browsers").
- Client models that need a modern DOM and CSS engine in IBrowse, AWeb, Voyager or NetSurf: the features of each stop short of one ("Native Amiga browsers").
- Bulk drawing by the 68k over Zorro: every pixel crosses the bus, so Zorro II falls behind Zorro III (`topics/bus-and-card-rates.md`, "Bus ceilings").
