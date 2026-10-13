# Remote-display servers on Linux: what each sends

Scope: what Linux servers of RDP, VNC, xpra and Guacamole send a client that offers no codec: pixel depth and byte order, screen copies and how a scroll becomes one, update pacing, per-window mode, sound, clipboard and drives, security and listening defaults, and the versions Debian 13 packages.
Status: current

- Nothing here was built, run or measured; a statement of what a server does is for its source at the commit in "Sources", read on 2026-10-11.
- `[F]` opens what a source states; `[G]` opens arithmetic or inference made here; a "none" names the search it rests on, case-insensitive, over the tree at that commit.
- Under each heading a path with no source ID is in the repository that heading's first line names.
- What each protocol asks of a client: `topics/remote-display-protocols.md`; what each form costs a 68060, and what bears on delay and integration: `topics/remote-display-client.md`.
- A server as the hidden display behind a stock browser, and Microsoft's Weston fork: `topics/hidden-display.md`, "Existing remote-display servers".

## RDP servers

A path with no ID is `xrdp@9cd64936f53e`, as is one that opens `xrdp:`; `xorgxrdp:` paths are at `59d0735c4321`.
[F] xrdp has two back ends: its README says a Linux desktop "requires" the xorgxrdp X module, and "If xorgxrdp is not provided, use Xvnc server" (`README.md:L33-34, L58-61`; `xrdp/xrdp.ini.in:L274-276`).

| Aspect | xrdp with its X module, xorgxrdp | xrdp with an Xvnc |
|---|---|---|
| Depths accepted | [F] 8, 15, 16, 24 and 32 bits (`libxrdp/xrdp_sec.c:L1717-1726, L1789`) | The same front end |
| Sent when no codec is offered | [F] No codec (JPEG, H.264, RemoteFX) is used below 24 bits (`xrdp/xrdp_encoder.c:L206-209`); [F] a 16-bit client is sent 16-bit bitmaps: the X module converts each captured area to 5-6-5, and xrdp writes each pixel low byte first, last row first (`xorgxrdp:module/rdpCapture.c:L271, L889-891`; `xorgxrdp:module/rdpClientCon.c:L1533-1535`; `xrdp:libxrdp/libxrdp.c:L755-763`); [F] 64×64 tiles go through the bitmap cache, or plain Bitmap Updates of the dirty region when the client lacks any of four basic orders (`xrdp:xrdp/xrdp_painter.c:L100-131`; `xrdp:libxrdp/xrdp_caps.c:L248-254`); [F] with `bitmap_compression` on, run-length coding below 32 bits and planar coding at 32 (`xrdp:libxrdp/libxrdp.c:L559, L598-616`) | [F] The VNC server's raw rectangles, painted the same way, and its copies (`xrdp:vnc/vnc.c:L1501-1510`) |
| Screen copies | [F] None: every X drawing hook, `CopyArea` included, only adds to a dirty region, and the function that would send a screen copy has no caller (`xorgxrdp:module/rdpCopyArea.c:L91-95`; `xorgxrdp:module/rdpClientCon.c:L2737`; "ScreenBlt" occurs at its definition only, and "scroll" only in keyboard and mouse input code) | [F] The module always asks its VNC server for copy rectangles and turns each into xrdp's screen copy: a screen-copy order to a client that listed the four orders, otherwise a copy inside xrdp's own buffer sent on as a bitmap (`xrdp:vnc/vnc.c:L2372, L1512-1522`; `xrdp:xrdp/xrdp_mm.c:L4187-4204`; `xrdp:xrdp/xrdp_painter.c:L1195-1298`); [G] it forwards what the VNC server recorded ("How a scroll becomes a copy") |
| Update pacing | [F] At most one capture every 40 ms, and only on a change: 4 ms after it, longer only to keep 40 ms since the last update; the interval is the setting `normal_frame_interval` (`xrdp/xrdp.ini.in:L272`; `common/xrdp_constants.h:L116`; `xorgxrdp:module/rdpClientCon.c:L71, L1496, L4020-4031`); [F] no new capture while one is unacknowledged; xrdp acknowledges after painting, and stops reading its X module while output for the client is still buffered, which its source calls back-pressure for a much slower link (`xorgxrdp:module/rdpClientCon.c:L3934-3939`; `xrdp:xrdp/xrdp_mm.c:L4419-4422`; `xrdp:common/trans.h:L66-87`) | Not read |
| Per-window mode | [F] In the channel server, allowed by default (`sesman/chansrv/rail.c`; `xrdp/xrdp.ini.in:L247`); [F] the project's wiki says it was written to draw window borders locally, where the specification's mode draws them on the server, and that this leaves the general support incomplete (`xrdp-wiki@cde66a77c465:RAIL-support-in-xrdp.md:L9-10`); [F] xorgxrdp has no window messages ("rail" and "window_new_update" occur in no file) | Not read |
| Sound | [F] PCM at 44.1 and 22.05 kHz, 16-bit stereo, always; AAC, Opus and MP3 at 44.1 kHz only when built in (`sesman/chansrv/sound.c:L112-196`); [F] sound "requires to build additional modules" (`README.md:L41`) | The same |
| Clipboard, drives, size | [F] Clipboard "text, bitmap, file"; "Session resizing (both on-connect and on-the-fly)" (`README.md:L36, L40`); [F] the client's drives are mounted under `thinclient_drives` in the user's home through FUSE, with no hard or soft links and no POSIX locking, every file taking the logged-in user's UID and GID under a umask of 077 (`README.md:L43`; `sesman/sesman.ini.in:L201-205`; `xrdp-wiki@cde66a77c465:Drive-redirection-features.md:L4-6, L12-14`) | The same |

The other three servers; a path with no ID is in the row's own repository.

| Server | Requires of the client | Sent when no codec is offered | Screen copies; per-window mode | Sound, clipboard, drives, size |
|---|---|---|---|---|
| Weston's RDP back end, `weston-git@a440a7bed4d5` | [F] Surface commands, without which it refuses the client (`libweston/backend-rdp/rdp.c:L1186-1189`) | [F] The repaint damage as "Set Surface Bits" at 32 bits a pixel, raw, NSCodec or RemoteFX; it sets the colour depth to 32 (`libweston/backend-rdp/rdp.c:L249-321, L1987`) | [F] No screen copy ("scrblt" occurs nowhere in the back end) and no per-window mode ("rail" occurs only inside the word "trailing") | [F] Clipboard and resizing "to the dimensions of the client's announced resolution" (`libweston/backend-rdp/rdpclip.c`, `rdpdisp.c`; `man/weston-rdp.man:L68-71`); the back end's directory holds no file for drives |
| GNOME Remote Desktop, `grd@bb44752f785d` | [F] The pipeline, desktop resizing, dynamic channels and fast-path output, each on pain of closing the connection (`src/grd-session-rdp.c:L1261-1266, L1294, L1300, L1392`) | Nothing: [F] "Client did not advertise support for the Graphics Pipeline, closing connection" (`src/grd-session-rdp.c:L1263-1264`) | Not read | Not read |
| FreeRDP's shadow server, which shows an existing X display, `freerdp@87baff6c80e1` | None read | [F] Bitmap Updates in 64×64 tiles where the client has neither the pipeline nor surface commands: run-length coding below 32 bits and planar coding at 32; a 24-bit request becomes 16 (`server/shadow/shadow_client.c:L546-548, L2028-2132, L2336-2370`) | [F] Neither ("scrblt" and "rail" occur in no file of `server/shadow`) | [F] Sound out and in (`server/shadow/shadow_rdpsnd.c`, `shadow_audin.c`); no clipboard or drive file among its sources |

- [G] Of the four servers, two serve a 16-bit client at all: xrdp and the shadow server.
- [G] One path passes a screen copy on to the client for what an application draws: xrdp with an Xvnc, for the copies that VNC server records.
- [G] No other drawing order, nor the glyph cache, is used for application content by any of the four, and of the three that serve a client without the pipeline xrdp alone uses the bitmap cache; the specification's side of both is `topics/prior-art.md`, "Remote and split-engine browsers".
- [F] xrdp's `bitmap_compression`, `bulk_compression`, `bitmap_cache`, `max_bpp` and `use_fastpath` are server settings (`xrdp/xrdp.ini.in:L104-113`).
- [F] The video-region channel that RDP's sound time stamp pairs with has no server here: its channel name occurs nowhere in xrdp, xorgxrdp or Weston's back end, in GNOME Remote Desktop only in a list of reserved names (`grd@bb44752f785d:src/grd-rdp-dvc-camera-enumerator.c:L148, L165-166`), and in FreeRDP only in its client and its proxy's pass-through (`freerdp@87baff6c80e1:channels/video/client`; `server/proxy/pf_config.c:L1511-1516`; search for "RDS::Video").

## VNC servers

| Server | Pixel bytes | Copy rectangles | Sound | Clipboard, size, other |
|---|---|---|---|---|
| wayvnc `wayvnc@b286ab91d0f4` on its library `neatvnc@a4c67ec07a34` | [F] Encoders for raw, Tight, ZRLE and H.264 (`neatvnc:src/enc/`); [F] the client's byte-order flag is read in one place, where it mirrors each colour's shift, and every 15- or 16-bit pixel is then written low byte first (`neatvnc:src/pixels.c:L503-509, L321-322`) | [F] None: the encoding is parsed and named, and no encoder exists for it, at this commit and at the three packaged versions, 0.9.1, 0.9.5 and 1.0.3 (`neatvnc:src/server.c:L846, L980`; `neatvnc@v0.9.1:src/enc/interface.c:L36-44`, `src/server.c:L636, L746`; `neatvnc@v0.9.5:src/server.c:L646, L756`; `neatvnc@v1.0.3:src/server.c:L846, L981`) | [F] None ("audio" occurs in no source file of either tree) | [F] Extended clipboard; a size set by the client; two pseudo-encodings of its own that carry a frame time stamp (`neatvnc:include/rfb-proto.h:L80-84`; `neatvnc:src/server.c:L957-971, L2067`) |
| TigerVNC's X server, Xvnc, `tigervnc@8c5eb64cc522` | [F] It writes the high byte first when the client asks for big-endian (`common/rfb/PixelFormat.inl:L55-67`) | [F] Its X server records a copy for `CopyWindow` and for `CopyArea`, the second only when the source is on screen (`unix/xserver/hw/vnc/vncHooks.c:L372-380, L540, L1462-1465, L1494`) | [F] The QEMU sound extension is in its viewer's classes only ("audio" occurs in no server class of `common/rfb` and nowhere under `unix`) | [F] Extended clipboard; size requests accepted by default (`unix/xserver/hw/vnc/Xvnc.man:L87-88`) |
| x11vnc, manual only, `x11vnc@e2b726a8c046` | Not read | [F] An option that will "use heuristics to try to guess if a window has scrolled its contents"; it needs the RECORD extension to watch other applications' `XCopyArea` and `XConfigureWindow` requests, names a web browser window among its examples, and "will not always detect scrolls" (`x11vnc.1:L4200-4225`) | Not read | Not read |

- [G] The 16-bit bytes wayvnc's library delivers: asked for 16 bits, big-endian, red at shift 11, green at 5 and blue at 0, which is the ZZ9000's screen layout `rrrrrggg gggbbbbb` (`topics/rtg-layer.md`, "Putting pixels into a window"), it mirrors the shifts to 16 − 11 − 5 = 0, 16 − 5 − 6 = 5 and 16 − 0 − 5 = 11 and writes low byte first, giving `gggrrrrr bbbbbggg`: neither the layout asked for nor its byte swap.
- [G] A little-endian request with the same shifts gives `gggbbbbb rrrrrggg`, one byte swap from the screen's layout, as with xrdp's bitmaps; no request with the flag clear gives the screen's bytes.
- [G] At 32 bits the mirror is a true byte swap: a big-endian request for blue at 24, green at 16 and red at 8 yields bytes B, G, R, X, the ZZ9000's 32-bit layout.
- [F] Weston's VNC back end hands each repaint's damage region to the same neatvnc library (`weston-git@a440a7bed4d5:libweston/backend-vnc/vnc.c:L751-788`).
- Not read at source level, so the "none" cells above do not cover them: x11vnc and libvncserver; TigerVNC's two other servers, `x0vncserver` and `w0vncserver`; RealVNC's server.

## xpra and guacd

- [F] xpra's sessions run applications on a virtual X display (`topics/hidden-display.md`, "Existing remote-display servers").
- [F] Its seamless mode "supports bit depths 16,24 and 30"; the server names 16-bit pixels `BGR565` on a little-endian machine and passes them unconverted to a client that lists that name (`xpra@de195aac2dda:docs/Features/Image-Depth.md:L18`; `xpra/x11/bindings/ximage.pyx:L191-196`; `xpra/codecs/argb/encoder.py:L47-48`).
- [F] "16-bit mode has no real native encoders and so the pixels are often upsampled to 24-bit" (`xpra@de195aac2dda:docs/Features/Image-Depth.md`).
- [F] The server chooses encodings from, among other things, network performance and available processing power (`xpra@de195aac2dda:docs/Usage/Encodings.md:L7-9`).
- [F] guacd is a daemon that speaks RDP, VNC or SSH to a server and the Guacamole protocol to its client (`guac-man@482ac54f15ae:src/guacamole-architecture.md:L30-37`); [G] here it would sit between an RDP or VNC server on the Linux computer and the Amiga.
- [F] guacd keeps a processing lag for each user (`guacd@ae12b8e51aa6:src/libguac/guacamole/user.h:L175-184`).
- [F] Its RDP side emulates a drive whose files are kept after the session ends, and a file dropped into that drive's "Download" folder is sent to the client (`guac-man@482ac54f15ae:src/using-guacamole.md:L288-302`).

## How a scroll becomes a copy

| Server | How it learns of a scroll | Source |
|---|---|---|
| xpra | [F] From the frames: for each new picture it checksums every row, keeps the checksums of the reference picture and of the latest, and counts hits for each distance; its change log calls this "window scrolling detection" | `xpra@de195aac2dda:xpra/server/window/motion.pyx:L46-51, L82-88, L130-133`; `docs/CHANGELOG.md:L840`; the rest of that file was not read |
| guacd | [F] From the frames: it searches the previous frame for content reused in the pending one, in cells of 64 pixels a side | `guacd@ae12b8e51aa6:src/libguac/display-priv.h:L98-109` |
| The Web Rendering Proxy's VNC mode | From the frames | `topics/prior-art.md`, "Remote and split-engine browsers" |
| TigerVNC's Xvnc; xrdp with an Xvnc | [F] From the application: only a copy the application asks of the X server is recorded | "VNC servers"; "RDP servers" |
| x11vnc | [F] From other applications' X copy requests, watched through the RECORD extension | "VNC servers" |
| xrdp with xorgxrdp; wayvnc; Weston's RDP back end; the shadow server | Never: none sends a copy | "RDP servers"; "VNC servers" |

- [F] Chromium's software presenter on X11 sends each damaged rectangle as an image, by a shared-memory `PutImage` or a `PutImage` through a pixmap; its one `CopyArea` copies the window into a temporary pixmap to read it back, on a path its comment limits to status-icon windows (`chromium@ceb8f3a65507:ui/base/x/x11_software_bitmap_presenter.cc:L91-92, L179-183, L209-273`; `ui/base/x/x11_util.cc:L94-151`).
- [G] So the servers that rest on X copy requests (TigerVNC's Xvnc, xrdp's Xvnc back end, x11vnc) get none from a scroll that Chromium draws this way, and a browser scroll reaches the client as bitmaps of the whole changed area, as it does from the servers that never send a copy.
- [G] With the three servers that find a scroll from the frames, only the newly exposed strip then travels as pixels; what real pages resend beyond that strip: `topics/scroll-redraw.md`.

## Security and listening defaults

| Server | Default | Source |
|---|---|---|
| xrdp | [F] Port 3389; `security_layer=negotiate` with TLS 1.2 and 1.3; to a client that asks for no TLS it selects classic RDP security; `crypt_level=high`, from `none`, `low`, `medium`, `high` and `fips` | `xrdp@9cd64936f53e:xrdp/xrdp.ini.in:L28, L60-72, L84`; `libxrdp/xrdp_iso.c:L193-209` |
| xrdp, classic levels | [F] `low` is "the only level that the traffic sent by the server to client is not encrypted"; at `medium` and `high` all data both ways is encrypted; `security_layer=rdp` is "for testing only"; `none` is in the code and the sample file and not the manual, and with it a client that offers no method gets no encryption | `xrdp@9cd64936f53e:docs/man/xrdp.ini.5.in:L120-143, L234-237`; `libxrdp/xrdp_rdp.c:L85-88`; `libxrdp/xrdp_sec.c:L1998-2009, L2329-2332` |
| Weston's RDP back end | [F] A TLS key and certificate, or an RDP key that its manual calls known to be insecure; 60 Hz by default | `weston-git@a440a7bed4d5:man/weston-rdp.man:L34-36, L76-80` |
| GNOME Remote Desktop | [F] Network-level authentication only | `grd@bb44752f785d:src/grd-session-rdp.c:L1655-1657` |
| FreeRDP's shadow server | [F] A `/sec:` option taking `rdp`, `tls`, `nla` or `ext`; authentication on by default | `freerdp@87baff6c80e1:server/shadow/cli/shadow.c:L82, L94` |
| TigerVNC's Xvnc | [F] Security types `TLSVnc,VncAuth`; at most 60 updates a second; congestion control "to avoid excessive latency" | `tigervnc@8c5eb64cc522:unix/xserver/hw/vnc/Xvnc.man:L137-141, L294-299`; `common/rfb/Congestion.cxx:L19-34` |
| wayvnc | [F] No authentication unless enabled, then TLS or RSA-AES; DES authentication only with `allow_broken_crypto`, "on a trusted network" | `wayvnc@b286ab91d0f4:wayvnc.scd:L143-181` |
| guacd | [F] Port 4822, TLS optional; authentication belongs to the web application in front of it | `guacd@ae12b8e51aa6:src/guacd/man/guacd.8.in:L56, L90-117`; `guac-man@482ac54f15ae:src/guacamole-architecture.md:L79` |

What classic RDP security asks of a client: `topics/remote-display-protocols.md`, "What a minimal RDP client must speak".

## Packages

[F] In Debian 13's arm64 index (13.7, Release of 2026-09-12) as read on 2026-10-11 (`pkg-index`):

| Package | Version | Note |
|---|---|---|
| `xrdp`; `xorgxrdp` | 0.10.1; 0.10.2 | `xrdp` recommends `xorgxrdp` and `fuse`, and depends on `libfuse2t64`, `libopus0` and `ssl-cert` |
| `pipewire-module-xrdp` | 0.2 | The sound module; no `pulseaudio-module-xrdp` in the index |
| `tigervnc-standalone-server`; `tigervnc-scraping-server` | 1.15.0 | The second is `x0vncserver` |
| `wayvnc`; `libneatvnc0`; `x11vnc`; `libvncserver1` | 0.9.1; 0.9.1; 0.9.17; 0.9.15 | The Raspberry Pi archive has `wayvnc` 0.10.2, `libneatvnc0` 0.9.5 and `libneatvnc1` 1.0.3, whose own changes were not read |
| `weston`; `gnome-remote-desktop`; FreeRDP | 14.0.2; 48.1; 3.15.0 | |
| `rdesktop` | 1.9.0 | Depends on `libnettle8t64`, `libhogweed6t64`, `libgmp10` and `libgnutls30t64` |
| `libspice-server1`; `nxproxy`; `x2goserver`; `waypipe` | 0.15.2; 3.5.99.27; 4.1.0.6; 0.9.2 | No `xserver-xspice` |
| `xpra`; `guacd` | Absent | xpra.org's own repository: `topics/hidden-display.md`, "Which packaged compositor offers what" |

- [G] `xrdp`'s dependencies name an Opus library and neither an MP3 nor an AAC one, so of its three optional sound codecs Debian's build has Opus alone; its certificate comes with the `ssl-cert` package.

## Not established

- What xrdp sends a 16-bit client that lists no orders for a browser scroll, typing and video, with each back end: bytes, rectangles, copies and updates a second; running the server against such a client would show it.
- Whether xrdp's per-window code works with xorgxrdp, and the Xvnc back end's pacing: their sources beyond the lines cited.
- Whether Chromium's GPU presentation path, or Firefox, asks the X server for copies when scrolling: their sources.
- A Linux VNC server that sends sound: the sources of x11vnc, libvncserver, RealVNC's server and TigerVNC's two other servers.
- xpra with only `rgb` and `scroll` advertised at 16 and 24 bits, whether its big-endian 16-bit name can be requested, and which window manager its session reports to a browser: running it, or its server code beyond the files cited.
- Guacamole's bytes for a page with `force-lossless`, and its use of `copy` on a scroll: running guacd.
- Whether a browser's file chooser lists the mounted client drives, and how a download behaves there: running xrdp with a client that serves a drive.
- Whether sound and picture stay in step through xrdp at 25 bitmap updates a second: unmeasured.
- xrdp's handling of Unicode key events and keyboard layouts: its keyboard documentation.

## Sources

`xpra`, `chromium`, `pkg-index`, `freerdp`, `guacd` and `guac-man` are defined in `sources.md`; `xrdp`, `wayvnc` and `neatvnc` in `topics/hidden-display.md`, "Sources".

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `xorgxrdp`, `xrdp-wiki` | xrdp's X module; xrdp's wiki | `github.com/neutrinolabs/xorgxrdp`; `github.com/neutrinolabs/xrdp.wiki.git` | `59d0735c4321`; `cde66a77c465` |
| `weston-git`, `grd` | Weston, upstream; GNOME Remote Desktop | `gitlab.freedesktop.org/wayland/weston`; `gitlab.gnome.org/GNOME/gnome-remote-desktop` | `a440a7bed4d5`; `bb44752f785d` |
| `tigervnc`, `x11vnc` | TigerVNC; x11vnc's manual, `x11vnc.1` | `github.com/TigerVNC/tigervnc`; `github.com/LibVNC/x11vnc` | `8c5eb64cc522`; `e2b726a8c046` |
