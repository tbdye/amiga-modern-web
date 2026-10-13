# Remote-display protocols: what a client must speak

Scope: for each published remote-display protocol that could carry a stock browser from a Linux computer to a 68k Amiga (RDP, xpra, VNC's RFB, Guacamole, and others in brief): what reaches a client and in what form, who starts an update and how the two ends pace each other, the channels beside pixels, what a minimal client must implement, and the size of reference clients.
Status: current

- Nothing here was built, run or measured; specifications and sources were read on 2026-10-11, at the revisions and commits in "Sources".
- `[F]` opens what a source states; `[G]` opens arithmetic or inference made here; a line count is `[G]`, by `wc -l` over the files named.
- "Pixels" means drawn on Linux and received as a picture; "the pipeline" is RDP's newer graphics channel (`ms-rdpegfx`).
- What each Linux server does with these protocols: `topics/remote-display-servers.md`.
- What each form costs a 68060, what bears on delay and integration, and what stays un-native: `topics/remote-display-client.md`.
- Existing Amiga clients of these protocols, a VNC client and a 68k port of an RDP client among them: `topics/prior-art.md`, "Remote and split-engine browsers".

## At a glance

| Protocol | What reaches the client | Linux servers read | A client for 68k AmigaOS |
|---|---|---|---|
| RDP | Bitmap rectangles, raw or coded, at the client's depth; drawing orders if the client lists them; codecs, which xrdp uses only at 24 bits and up | xrdp, Weston's RDP back end, GNOME Remote Desktop, FreeRDP's shadow server | `topics/prior-art.md` |
| xpra | Per-window draw packets: raw, scroll vectors, PNG, JPEG, WebP, video | xpra | [F] None on Aminet (`aminet-search`, "xpra": 2 unrelated packages) |
| VNC (RFB) | Rectangles in a pixel format the client sets; raw is always allowed | TigerVNC, wayvnc; x11vnc's manual only | `topics/prior-art.md` |
| Guacamole | Text instructions carrying PNG, JPEG or WebP | guacd, placed in front of an RDP or VNC server | [F] None on Aminet (`aminet-search`, "guacamole": no package) |
| SPICE, NX and X2Go, plain X11, Waypipe | "Other protocols" | None at source level | "Other protocols" |

The Aminet searches cover Aminet alone: the projects' own client lists and the wider web were not searched.

## RDP

Section numbers are those of `ms-rdpbcgr` unless another ID is named.

| Aspect | What the specifications say |
|---|---|
| Depth | [F] The client names 4, 8, 15, 16, 24 or 32 bits a pixel; 16 is 5-6-5 (§2.2.1.3.2) |
| Raw bitmaps | [F] Rectangles whose data is a bottom-up, left-to-right series of pixels, each row a multiple of four bytes; the passage gives no byte order for a pixel (§2.2.9.1.1.3.1.2.2) |
| Coded bitmaps | [F] Run-length coding below 32 bits, whose codes are little-endian, and planar coding at 32; support for the coded form "is required for a connection to proceed" (§2.2.9.1.1.3.1.2.2, §2.2.9.1.1.3.1.2.4, §2.2.7.1.2) |
| Drawing orders | [F] Screen-to-screen copy, cached bitmaps, cached glyphs and fills, each sent only if the client lists it; pointer shapes for the client to draw (§2.2.7.1.3, §2.2.9.1.1.4; `ms-rdpegdi` §1.3.1, §3.3.5.1.1.1.7) |
| Codecs | [F] Bitmap codecs are used with the Set Surface Bits surface command and with the third revision of the cache-bitmap order, whose support a client states in its order capabilities (§2.2.7.2.10; `ms-rdpegdi` §2.2.2.2.1.2.8); [F] the pipeline's two pixel formats are both 32-bit (`ms-rdpegfx` §2.2.1.4) |
| Who starts an update | [F] The server pushes; there is no request per update; [F] a plain Bitmap Update carries a count and, for each rectangle, bounds, size, depth, flags, length and data, with no frame identifier (§2.2.9.1.1.3.1.2.1, §2.2.9.1.1.3.1.2.2); [G] so a client has nothing to acknowledge |
| Pacing | [F] Acknowledgements exist for surface-command frames and for the pipeline, the second with the client's queue depth; round-trip and bandwidth probes; a client message that stops all display updates; a confirmation for each sound block (`ms-rdprfx` §2.2.1.3, §2.2.3.1; `ms-rdpegfx` §2.2.2.13; §2.2.14, §2.2.11.3; `ms-rdpea` §2.2.3.8) |
| Sound | [F] PCM is mandatory for both ends; each block carries a time stamp, which the client returns in its confirmation with the milliseconds from receiving the block to confirming it added (`ms-rdpea` §2.2.2.1.1, §2.2.3.3, §2.2.3.8, §3.2.5.2.1.6) |
| Clipboard | [F] Text, Unicode included, and files by stream (`ms-rdpeclip` §1.3.1, §1.3.1.1.1, §2.2.2.1.1.1) |
| Drives | [F] The client's drives are served to the server, each under a name of at most 7 characters (`ms-rdpefs` §1.3, §2.2.1.3) |
| Printing; screen size | [F] A printing channel; the remote screen can follow the client's size (`ms-rdpepc` §1.3; `ms-rdpedisp` §1.3) |
| Keys | [F] Scancodes, with a keyboard layout identifier in the client's settings, or Unicode characters (§2.2.8.1.1.3.1.1.1, §2.2.8.1.1.3.1.1.2, §2.2.1.3.2) |
| One window for each remote window | [F] A per-window channel gives one client window for every remote window, with title, icon, visibility and client-side move and resize; those windows "exactly mimic the appearance of their corresponding remote windows/icons" (`ms-rdperp` §1.3, §1.3.2.5, §2.2.1.3.1.2.1, §2.2.1.3.1.2.2); [G] so the window frame arrives as pixels |

- [F] The run-length coding has six kinds of order and four single-byte codes: a background run copies the pixel above, or black on the first row; a foreground run is the pixel above XOR a colour; a dithered run alternates two colours; a colour run stores one value; a colour image copies pixels from the stream; in a mixed image one mask bit for each pixel chooses between the first two; and the single-byte codes are two short mixed images, a white pixel and a black pixel (§2.2.9.1.1.3.1.2.4, §3.1.9).
- [F] rdesktop's README says it "has implemented the RDP version 4 and 5 protocols" and is "no longer maintained" (`rdesktop@f8a478568bc6:README.md:L1-13`).

### What a minimal RDP client must speak

- [F] A connection has ten phases: connection initiation; basic settings exchange; channel connection; RDP security commencement; secure settings exchange; optional connect-time auto-detection; licensing; optional multitransport bootstrapping; capabilities exchange; connection finalization (§1.3.1.1).
- [F] The section "Mandatory Capability Sets" holds eleven: General, Bitmap, Order, Bitmap Cache, Pointer, Input, Brush, Glyph Cache, Offscreen Bitmap Cache, Virtual Channel and Sound (§2.2.7.1.1 to §2.2.7.1.11).
- [F] rdesktop sends ten of them and no Offscreen Bitmap Cache set (`rdesktop@f8a478568bc6:rdp.c:L1143-1168`; "offscreen" occurs in none of its sources).
- [F] Static virtual channels are a list the client requests (§2.2.1.3.4); [G] sound, clipboard, drives and display size each ride a channel, so each is optional, and pixels and input need none.
- [F] A client cannot refuse coded bitmaps (table above); it can decline bulk compression and every drawing order (§2.2.1.11.1.1, §2.2.7.1.3).
- [G] So the smallest set is the eight phases not named optional, the mandatory capability sets, a decoder for the run-length coding, and input; whether a server then sends raw or coded bitmaps is the server's setting (`topics/remote-display-servers.md`, "RDP servers").
- [F] Classic RDP security has four levels: at Low only client-to-server data is encrypted, and at the other three data is encrypted in both directions (§5.3.1).
- [F] It costs the client one RSA operation, the client random encrypted with the server's public key, and then, below the FIPS level, RC4 over the data stream with a MAC generated for each block; the FIPS level uses Triple DES (§5.3.4.1, §5.3.6, §5.3.6.1).
- [F] On receive rdesktop skips the 8-byte signature and decrypts (`rdesktop@f8a478568bc6:secure.c:L894-900, L925-931`).
- [F] rdesktop takes hashing, RC4 and RSA from the nettle and GnuTLS libraries (`rdesktop@f8a478568bc6:configure.ac:L153-184`); its line counts below leave them out.
- TLS on the Amiga is AmiSSL's: `topics/arm-offload.md`, "How the TLS offload is built".
- Which levels a server asks for by default: `topics/remote-display-servers.md`, "Security and listening defaults".

### Reference clients

[G] rdesktop at `f8a478568bc6`, GPLv3: 40,686 lines in its top-level `*.c` and `*.h` files; the parts below are its `.c` files, and the third column is `[G]`, from what the capability and channel negotiation let a client decline.

| Part (files) | Lines | What the protocol lets a client leave out |
|---|---|---|
| Transport, security, licensing, session (`tcp iso mcs secure licence rdp rdp5 ssl asn stream channels`) | 6,536 | Nothing |
| Bitmap run-length decoder, orders, caches (`bitmap orders cache pstcache`) | 3,061 | All but the decoder, `bitmap.c`, 918 lines: orders and the persistent cache can be declined |
| Bulk decompression (`mppc`); network-level authentication (`cssp pkix_asn1_tab`) | 379; 1,817 | Both, where the server does not insist on the second |
| X11 window, keymap, clipboard glue, window hints, control (`xwin xkeymap xclip ewmhints ctrl`) | 8,633 | Specific to X11 |
| Sound channel and mixing (`rdpsnd rdpsnd_dsp`); six output drivers | 1,208; 3,651 | The channel is optional; the drivers are per sound system |
| Clipboard channel (`cliprdr`) | 194 | Optional |
| Device redirection core (`rdpdr`); disk (`disk`); printer; serial and parallel; smart card | 1,360; 1,444; 490; 1,290; 2,790 | Optional, each by device kind |
| Its own seamless mode (`seamless`); dynamic channels and display size (`dvc rdpedisp`) | 551; 626 | Optional |

- [F] Serving a drive means answering ten kinds of request: create, close, read, write, query information, set information, query volume information, directory control, device control and lock control (`rdesktop@f8a478568bc6:rdpdr.c:L490-793`).
- [F] rdesktop's seamless mode is a channel of its own that needs a helper program on the Windows side; it is not the per-window channel of the table above (`rdesktop@f8a478568bc6:doc/seamlessrdp-channel.txt`).
- [F] On a big-endian host rdesktop swaps the bytes of 16-bit sound samples, which arrive low byte first (`rdesktop@f8a478568bc6:rdpsnd_dsp.c:L203-205, L391-393`).
- [G] FreeRDP at `87baff6c80e1`, Apache-2.0, has the per-window channel in 5,128 lines (`channels/rail`, `*.c` and `*.h`); its `libfreerdp/core` alone is 98,382 lines, against rdesktop's 6,536 for transport and session.

## xpra

A path with no ID is `xpra@de195aac2dda`; `Protocol.md` stands for `docs/Network/Protocol.md`.

| Aspect | xpra |
|---|---|
| Record and coding | [F] An eight-byte header, then a `rencodeplus` list; a client "MUST implement rencodeplus and SHOULD implement LZ4" (`Protocol.md:L70-73, L167-180`) |
| What reaches the client | [F] Draw packets for each window, whose encoding the client must have advertised: `rgb` (raw, optionally LZ4), `scroll` (copy vectors), PNG, JPEG, WebP, video; the cursor as image data (`Protocol.md:L438, L455-457, L492-500`; `docs/Usage/Encodings.md:L33-34, L46-47, L56-60, L82-91`) |
| The `scroll` encoding | [F] Its rectangles "are relative to the same reference picture", so a client must copy from a snapshot of the window taken before the first of them (`docs/Subsystems/Window.md:L146-151`); [G] a client needs a second copy of the window to apply them |
| 16-bit pixels | `topics/remote-display-servers.md`, "xpra and guacd" |
| Who starts an update; pacing | [F] The server pushes; the client acknowledges every draw with its decode time, and ping echoes carry latency (`Protocol.md:L364-365, L452-453`); [F] of queueing on the network path its documentation says xpra "is sensitive to jitter and latency" (`docs/Network/README.md:L209-210`) |
| Windows | [F] Every remote window, pop-ups included, is a client window with title, icon and size hints, which the client moves, resizes and closes; "Remote windows are managed by your local operating system and window manager", and decorations are a window state in its client tables (`Protocol.md:L427-448`; `docs/Usage/Seamless.md:L69`; `docs/Usage/Clients.md:L117, L210-211, L240-241`) |
| Sound | [F] Sound packets carry a codec name and metadata with a time stamp, and a `sync` control exists; codec names include `mp3`, `flac`, `opus`, `vorbis` and `wav` (`Protocol.md:L533-548`; `docs/Subsystems/Audio.md:L75`; `xpra/audio/common.py:L17-43`) |
| Clipboard, files, URLs, printing | [F] Clipboard by type; files both ways; `open-url`; printing as a forwarded file; notifications (`Protocol.md:L502-578`); [F] no client drive: file transfer "is not meant to replace a network filesystem" (`docs/Features/File-Transfers.md:L5`) |
| Encoder service | [F] The server also offers a stateless service: pixels in, coded picture out (`Protocol.md:L294, L581-596`) |
| Security | [F] The record layer "provides no confidentiality, integrity or authentication"; plain TCP is allowed, and TLS, SSH or AES are options (`Protocol.md:L662-666`; `docs/Network/README.md:L49-51`) |
| Client size | [F] Its own table gives 9 thousand lines for its Rust client, 14 for its Go client and 18 for its browser client (`docs/Usage/Clients.md:L42-45`) |
| Versions | `topics/engine-control.md`, "Upkeep by arrangement"; [F] its list of defunct clients says they "will not work with the currently supported versions" of the server (`docs/Usage/Clients.md:L268-274`) |

- [G] The Go client at `go-xpra@eedcb81275a3` is 15,037 lines in its `*.go` files, tests excluded.
- [F] It handles RGB and PNG pictures, windows, keys and pointer, and has no sound, clipboard or file transfer in its feature table (`docs/Usage/Clients.md:L228-255`).

## VNC (RFB)

A path with no ID is `rfbproto@152107d:rfbproto.rst`, the community's specification.

| Aspect | RFB |
|---|---|
| What reaches the client | [F] The client sets the pixel format: bits a pixel, colour widths and shifts, and byte order (`L1676-1722`); [F] encodings are raw, CopyRect, RRE, Hextile, zlib-based forms and Tight, which can carry JPEG as "a JFIF stream"; a cursor shape; "Pixel data may always be sent in raw encoding" (`L1727-1729`, `L3050-3061`, `L3072`, `L3481-3540`) |
| Who starts an update; pacing | [F] In the base protocol the client asks for every update; extensions add continuous updates and a fence, a marker the other end echoes, described as a synchronisation of the data stream (`L2059-2150`); [G] the echo lets either end time the round trip |
| Sound | [F] The QEMU audio extension: a client that accepts pseudo-encoding -259 can set a sample format (8, 16 or 32 bits, signed or unsigned), one or two channels and a rate, and then receives raw audio data messages, which carry a length and data and no time value (`L2633-2700, L2997-3045, L3077, L4209-4216`) |
| Clipboard | [F] Latin-1 text; an extension adds UTF-8, RTF, HTML and bitmaps, and reserves a file format without defining it (`L2043, L4777-4860`) |
| Screen size; keys | [F] The client can set the screen size; keys travel as keysyms (`L1812, L2213-2232`) |
| Drives, printing, per-window mode | [G] None: the specification's message and encoding lists hold no such item |
| Versions | [F] The published versions are 3.3, 3.7 and 3.8; extensions are opt-in, and a server that lacks one "will simply ignore" the request (`L172, L277`) |

## Guacamole

`guac-man` paths are under `src/` at `482ac54f15ae`.

| Aspect | Guacamole |
|---|---|
| What reaches the client | [F] Text instructions; pictures only as PNG, JPEG or WebP, base64 in `blob` instructions; `copy` between layers, "often used for scrolling"; fills; a cursor (`guac-man:guacamole-protocol.md:L293-323`; `guac-man:protocol-reference.rst:L39, L94-132, L174, L654-668`) |
| Pacing | [F] `sync`: the client must answer each frame's time stamp, "or the server may stop sending updates until the client catches up" (`guac-man:protocol-reference.rst:L1024-1044`) |
| Handshake | [F] The client lists the image and audio types it takes and its size; connection parameters include `color-depth`, `force-lossless`, `resize-method`, `remote-app`, `enable-drive`, `drive-path` and `disable-audio` (`guac-man:guacamole-protocol.md:L113-121`; `guac-man:configuring-guacamole.md.j2:L1054-1210, L1440`) |
| Sound | [F] Raw PCM streams, `audio/L8` and `audio/L16`, with no time stamp (`guacd@ae12b8e51aa6:src/libguac/raw_encoder.c:L38-142`) |
| Clipboard, files | [F] Clipboard, file and named-pipe streams both ways; one display, its size from the client (`guac-man:protocol-reference.rst:L669-760, L947`) |
| Versions | [F] Protocol versions 1.0.0 to 1.5.0, negotiated from 1.1.0 (`guac-man:guacamole-protocol.md:L78-110`) |
| Size | [G] At `guacd@ae12b8e51aa6`, libguac is 16,776 lines (`src/libguac/*.c`) and guacd 3,161 (`src/guacd/*.c`), Apache-2.0; the reference client is JavaScript and was not counted |

- [G] Every picture byte is base64 text: 4 bytes on the wire for 3 of PNG or JPEG.

## Other protocols

| Protocol | What reaches the client | Channels beside pixels | An Amiga side |
|---|---|---|---|
| SPICE | [F] 16-bit surfaces (5-5-5, 5-6-5); raw bitmaps, lossless image codings, JPEG; `copy_bits`; video streams from MJPEG up; the client may state a preferred compression, `OFF` included (`spice-server@0.15.2:subprojects/spice-common/spice.proto:L346-390, L476-484, L727, L1010`) | [F] Sound raw or Opus; clipboard text and file transfer through a guest agent; a WebDAV channel for a directory of the client; no per-window mode (`spice-server@0.15.2:subprojects/spice-common/spice.proto:L1169-1174, L1363`; `spice-protocol@0.14.4:spice/vd_agent.h:L109, L280`; `spice-gtk@0.42:src/spice-session.c:L1459-1474, L1495-1505`) | [F] None on Aminet (`aminet-search`, "spice": 21 unrelated packages); [F] Debian 13 has `libspice-server1` and no `xserver-xspice`, its X server for a plain Linux machine (`topics/remote-display-servers.md`, "Packages") |
| NX, X2Go | [R] Compressed X11, which the projects' documentation would verify; [F] its proxy, `nxproxy`, runs at both ends (`nx-libs@58d42b6edf3b:README.md:L45`) | Not read | [F] No X2Go package on Aminet (`aminet-search`, "x2go") |
| Plain X11 to an X server on the Amiga | [G] The X server's own pixel format; [F] Chromium's software path sends images (`topics/remote-display-servers.md`, "How a scroll becomes a copy"); [R] today's toolkits expect extensions newer than X11R6, which their documentation would verify | [G] Each window is the Amiga X server's window | [F] AmiWin 2.22, 68k, X11R6, shareware: its demo offers 256 colours on CyberGraphX boards, and a Picasso96 driver for the registered version is on Aminet; AmiCygnix (X11R6.3) is a port for AmigaOS 4 (`aminet:misc/x11/AmiWin222d`, `aminet:misc/x11/AW-CGX223reg`, `aminet:misc/x11/amicygnix-x11-src`, readmes) |
| Waypipe | Forwards Wayland messages and must be installed at both ends (`topics/engine-control.md`, "Arrangements"); [G] the client end then needs a Wayland compositor | — | — |

- [R] Not examined: PCoIP, Citrix HDX, NoMachine's newer protocol and Chrome Remote Desktop, which are proprietary; RustDesk, Sunshine and Moonlight, which carry the screen as a video stream; each project's own documentation would verify it.
- Neko, Selkies and KasmVNC: `topics/hidden-display.md`, "Existing remote-display servers".

## Not established

- Whether a 68k client of xpra, SPICE, X2Go or Guacamole exists outside Aminet: the projects' own client lists and a wider search would settle it.
- SPICE's X server on arm64 and its TLS; NX and X2Go at source level; the size of the JavaScript Guacamole client: their sources.
- Parts of the specifications that were not read: `ms-rdprfx` beyond its message flows, its prerequisites and the two sections cited, the dynamic-channel and NSCodec documents, and the clipboard, drive, per-window, display and printing documents beyond their overviews and the sections cited.
- rdesktop beyond its README, counts, protocol negotiation and the lines cited, and FreeRDP's client code.

## Sources

`xpra`, `aminet`, `freerdp`, `guacd`, `guac-man`, `ms-rdpea`, `spice-server` and `spice-gtk` are defined in `sources.md`, with `ms-rdpegdi` and `ms-rdperp`, which were read as revision 34.0 of 2024-04-23 and revision 34.0 of 2026-07-14.
The Microsoft documents were read as PDF from `winprotocoldoc.z19.web.core.windows.net`; `spice-server`, `spice-protocol` and `spice-gtk` are release archives, cited at their version.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `ms-rdpbcgr`, `ms-rdpegfx`, `ms-rdprfx` | Microsoft Open Specifications [MS-RDPBCGR], [MS-RDPEGFX], [MS-RDPRFX] | `learn.microsoft.com`, Open Specifications | Revisions 62.0 (2026-03-09), 19.0 (2026-05-11) and 23.0 (2024-04-23); SHA-256 `77fae7d35a5cc4f3d0f4ab86ed752182ec675369655259cb999b7c41290d2d7d`, `ac6d4de488fcf92eacb8730cc6a76f3e5b1d2b95cb86f156f24c99bc8fef9077`, `84e9a1c07eb755b4224d486d6d25a356975173ce779c3a455f85d294a02b99db` |
| `ms-rdpeclip`, `ms-rdpefs`, `ms-rdpedisp`, `ms-rdpepc` | [MS-RDPECLIP], [MS-RDPEFS], [MS-RDPEDISP], [MS-RDPEPC] | `learn.microsoft.com`, Open Specifications | Revisions 16.0, 29.0, 10.0 and 13.0, each of 2024-04-23; SHA-256 `9863ff69319af5ff82f24f08a6ec3f67a309e46380a67665e9a2e842b0dcbf8e`, `d193f891d7a917797aed035d29aab6ca481519fc0a076ecbeff517660e2e199f`, `13763151c7fa57273e97ebda0dd244936bb2aba55ea08356017b081ccaac0079`, `ba863ecd4f3e71c25dab5a6fffd40334bb1006648c90c7de763f6106c43935e6` |
| `rdesktop`, `go-xpra` | rdesktop; the Go client of xpra | `github.com/rdesktop/rdesktop`; `github.com/Xpra-org/go-xpra` | `f8a478568bc6`; `eedcb81275a3` |
| `rfbproto` | The RFB protocol, community specification, `rfbproto.rst` | `github.com/rfbproto/rfbproto` | `152107d` |
| `spice-protocol` | SPICE release archives | `https://www.spice-space.org/download/releases/` | 0.14.4 |
| `nx-libs` | nx-libs, branch 3.6.x, `README.md` | `github.com/ArcticaProject/nx-libs` | `58d42b6edf3b` |
| `aminet-search` | Aminet's package search | `https://aminet.net/search?query=<term>` | 2026-10-11 |
