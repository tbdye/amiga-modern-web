# A remote-display client on the target configuration

Scope: what an Amiga client of a remote-display protocol would do for each pixel on a 68060 at 50 MHz with a ZZ9000, by the form the data arrives in; the facts that bear on delay and on integration; what stays un-native with a stock browser behind such a protocol; and what a website sees.
Status: current

- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; other Amigas vary from it.
- Nothing here was built, run or measured: every rate is `[G]`, arithmetic on other pages' published figures, and each input carries the conditions stated under its own heading.
- `[F]` opens what a source states; a line that ends in a page and heading restates a fact that page owns.
- The protocols: `topics/remote-display-protocols.md`; the Linux servers: `topics/remote-display-servers.md`; the calls that put pixels in a window: `topics/rtg-layer.md`.
- Existing Amiga clients: `topics/prior-art.md`, "Remote and split-engine browsers".
- MB = 10^6 bytes; an 800×600 window of 16-bit pixels is 960,000 bytes.

## Per-pixel work on a 68060

Inputs, each by pointer:

| Input | Value | Owner |
|---|---|---|
| Receive through the ZZ9000 at 50 MHz | 2.6 to 2.9 MB/s | `topics/target-config-rates.md`, "Network receive" |
| Copy from memory into the card | 4.3 to 7.3 MB/s | Same page, "Copies into the card" |
| Pixel rate: uncompressed 16-bit pixels from the network to the screen | 1.62 to 2.08 MB/s | Same page, "Pixel rate" |
| The graphics system's converting write to a 16-bit screen, which is its 8-bit palette path | 1.12 to 1.2 Mpix/s, 2.2 to 2.4 MB/s | Same page, "Copies into the card" |
| Deflate's output rate | 1.49 to 1.56 MB/s | `topics/decode-rates.md`, "68k lossless decoders" |
| JPEG decode, a 100 MHz measurement halved | 0.39 to 1.46 MB/s of 16-bit pixels | `topics/decode-rates.md`, "68k JPEG" |
| The card moving an 800×600, 16-bit window's pixels | 1.4 to 1.9 ms | `topics/bus-and-card-rates.md`, "Scrolls on the card" |
| Ratios on text whole screens: zlib; run-length | 16.6; 6.0 | `topics/page-pixels.md`, "At a glance" |

- [G] Slow inputs are paired with slow and fast with fast, as on the pages that own them.
- [G] The receive rate is a benchmark into memory with no TLS, the copies are 8-bit runs standing in for a 16-bit write, and the card's move time is scaled from whole-screen scrolls; no source measures one program doing all three.
- The ZZ9000's screen layouts, 16-bit `rrrrrggg gggbbbbb` high byte first and 32-bit bytes B, G, R, A: `topics/rtg-layer.md`, "Putting pixels into a window".

Every figure below is `[G]`.

| Form | Where it occurs | Work for each pixel or run | Figure |
|---|---|---|---|
| Raw, in the screen's own 16-bit layout | RFB from TigerVNC; not from wayvnc's library | Copy 2 bytes from the network buffer to the card; no arithmetic | The pixel rate itself, 1.62 to 2.08 MB/s; an 800×600 window in 0.96 ÷ 1.62 = 0.59 s to 0.96 ÷ 2.08 = 0.46 s |
| Raw 16-bit, low byte first | RDP's Bitmap Update as xrdp sends it, which is also bottom-up with rows padded to four bytes; RFB from wayvnc's library; xpra's `BGR565` | As above, plus one byte swap for each pixel | No published figure; below the row above; if the swap cost what the converting write costs, which is a stand-in and not a bound: 1 ÷ (1/2.6 + 1/2.2) = 1.19 to 1 ÷ (1/2.9 + 1/2.4) = 1.31 MB/s |
| Raw 32-bit, bytes B, G, R, X | RDP at 32 bits, as Weston's raw form; RFB at 32 bits from either server read | The layout of a 32-bit ZZ9000 screen: a copy of 4 bytes | Half the pixels of the first row for the same bytes: 800×600 is 1.92 MB, 1.92 ÷ 1.62 = 1.19 s to 1.92 ÷ 2.08 = 0.92 s, taking the copy rate in bytes as unchanged |
| Screen copy | RFB's CopyRect; RDP's screen-copy order; xpra's `scroll`; Guacamole's `copy`; SPICE's `copy_bits` | One move by the card, and nothing crosses the bus (`topics/rtg-layer.md`, "Scroll-copy"); xpra copies from a snapshot, so one more card-side copy | For a 48-row strip, 76,800 bytes, in the screen's own layout: 20 to 26 updates a second (`topics/scroll-redraw.md`, "Updates a second at 50 MHz"); byte-swapped, at the stand-in rate above: 76,800 ÷ 1.19 MB/s + 1.9 ms = 66.4 ms to 76,800 ÷ 1.31 MB/s + 1.4 ms = 60.0 ms, 15 to 17 a second; Guacamole's strip arrives as PNG, JPEG or WebP: no figure |
| Solid rectangles | RFB's RRE and Hextile; RDP's fills | One fill call for each sub-rectangle | None published |
| RDP's run-length coding | RDP below 32 bits | By kind of run (`topics/remote-display-protocols.md`, "RDP"); it reads the row above, so it decodes in memory and then copies; a colour run stores one value many times, so a decoder swaps bytes once for each value read, not for each pixel written | None published; it beats raw only if the 68060 decodes faster than receive × ratio ÷ (ratio − 1) (`topics/target-config-rates.md`, "Pixel rate"): with 6.0, a ratio measured for another run-length coding and so an assumption, 2.6 × 6 ÷ 5 = 3.1 to 2.9 × 6 ÷ 5 = 3.5 MB/s |
| zlib-based | RFB's ZRLE and Tight; PNG in Guacamole and xpra | Inflate, then copy | 1 ÷ (1/(16.6 × 2.6) + 1/1.49 + 1/4.3) = 1.08 to 1 ÷ (1/(16.6 × 2.9) + 1/1.56 + 1/7.3) = 1.25 MB/s, below the raw row |
| JPEG | RFB's Tight; Guacamole; xpra; xrdp's JPEG codec, at 24 bits and up for a client that offers it | A full decode | 0.39 to 1.46 MB/s of 16-bit pixels, before conversion and copy |

- [G] The deflate rate is for data that halves, and its rate on page-like data is unmeasured (`topics/decode-rates.md`, "68k lossless decoders"), so the zlib row holds at the published rate only.
- [G] At xrdp's default level a client on classic RDP security, without TLS, decrypts every received byte with RC4, a pass that no figure above includes; at the `low` level it does not (`topics/remote-display-servers.md`, "Security and listening defaults"; `topics/remote-display-protocols.md`, "What a minimal RDP client must speak"); no RC4 rate on a 68060 was looked for.
- [G] A client that widens each 16-bit pixel to 32-bit ARGB and writes it with `WritePixelArray`, which has no 16-bit source format, converts twice on a 16-bit screen, where the low-byte-first row above needs one swap (`topics/rtg-layer.md`, "Putting pixels into a window"); which published clients draw this way: `topics/prior-art.md`, "Remote and split-engine browsers".
- [G] JPEG and PNG, the forms the card's ARM decodes (`topics/decode-rates.md`, "What the card's ARM decodes today"), are what RFB's Tight, Guacamole and xpra can send; none of RDP's own codings (run-length, planar, NSCodec, RemoteFX, H.264) is among them; on a 16-bit screen the card needs the second pass that heading describes.
- [G] Sound: xrdp's two PCM formats are 44,100 × 4 = 176,400 and 22,050 × 4 = 88,200 bytes a second; if a sound byte costs the 68k what a pixel byte does, that is 176,400 ÷ 2,080,000 = 8.5% to 176,400 ÷ 1,620,000 = 10.9% of the pixel rate, and 4.2% to 5.4% (`topics/remote-display-servers.md`, "RDP servers").
- RDP's 16-bit samples arrive low byte first, so a big-endian client swaps them (`topics/remote-display-protocols.md`, "Reference clients").
- [F] One published comparison of such systems, on PCs with 1024×768 clients on a 100 Mb/s LAN in 2005, found that "most of the systems did well in both LAN and WAN environments, having latencies below the one second threshold" for a web page; it covered VNC, RDP, X, NX and Citrix's system (`thinc` §8.1, §8.3).
- No figure for a client of these protocols on a 68k was found (`topics/decode-rates.md`, "Not established").

## Delay and integration

Each line restates a fact with the page and heading that own it; `p` is `topics/remote-display-protocols.md` and `s` is `topics/remote-display-servers.md`; a bare `p` is that page's table under the heading of each protocol the line names.
The lines are facts on either side of each property, and none is weighed against another.

### Delay

| What bears on it | Fact | Owner |
|---|---|---|
| Who starts an update | RDP and xpra servers push; base RFB needs a request for every update, and an extension removes it | `p`, each protocol's table |
| | [F] Of a client that must ask, one paper says it adds "an update delay of at least half the round-trip time" | `thinc` §5 |
| The pointer | RDP, xpra and RFB each send the pointer's shape for the client to draw; [G] pointer motion then waits for no update | `p`, each protocol's table |
| The round trip | [G] A network round trip remains in every interaction by construction | — |
| Pixel layout | TigerVNC writes the byte order the client asks for, and at 32 bits wayvnc's library yields the card's layout; xrdp and wayvnc's library deliver 16-bit pixels low byte first whatever the client asks; [G] a swap for each pixel | `s`, "RDP servers", "VNC servers" |
| Servers that set a floor on the client | GNOME Remote Desktop refuses a client without the pipeline; Weston's back end sends 32-bit pixels only; xpra's 16-bit mode is often upsampled to 24-bit | `s`, "RDP servers", "xpra and guacd" |
| Coded bitmaps | An RDP client cannot decline them and decodes them through memory; xrdp can be set not to send them | `p`, "What a minimal RDP client must speak"; `s`, "RDP servers" |
| Scrolls | xpra, guacd and the Web Rendering Proxy's VNC mode find a scroll from the frames, so only the exposed strip travels; two more pass on only the copies an application asks of the X server, and Chromium's software path asks for none; xrdp with its X module and wayvnc never send a copy, so a scroll arrives as bitmaps of the whole changed area | `s`, "How a scroll becomes a copy" |
| Pacing to a slow client | xrdp with its X module captures no new frame while one is unacknowledged and stops reading while output is buffered; xpra has decode-time acknowledgements, Guacamole `sync`, RDP's pipeline its acknowledgements, TigerVNC congestion control | `s`, "RDP servers", "Security and listening defaults"; `p` |
| Capture interval | xrdp's X module captures a change 4 ms after it; its ceiling of 25 updates a second is a setting | `s`, "RDP servers" |
| Encryption | At xrdp's default level a client on classic security receives every byte RC4-encrypted | `s`, "Security and listening defaults"; `p`, "What a minimal RDP client must speak" |
| The network path | xpra's documentation calls it sensitive to jitter and latency from queueing on the path | `p`, "xpra" |

### Integration

| What bears on it | Fact | Owner |
|---|---|---|
| Files | RDP serves the client's drives to the server, and xrdp mounts them in the user's home; [G] Amiga volumes would then show in the Linux file chooser and could be the browser's download folder | `p`, "RDP"; `s`, "RDP servers" |
| | The client must itself implement the file service: ten kinds of request, 1,360 + 1,444 = 2,804 lines in rdesktop | `p`, "Reference clients" |
| | xrdp's mount has no links and no locking; Guacamole sends a file saved into one folder to its client; xpra sends single files and has no drive; RFB defines no file transfer | `s`, "RDP servers", "xpra and guacd"; `p` |
| Sound | RDP: PCM mandatory, a time stamp on each block and a confirmation; xrdp offers two PCM rates and needs an extra module; xpra: named codecs and time-stamp metadata; RFB's extension and Guacamole: PCM with no time stamp; neither VNC server read sends sound | `p`; `s`, "RDP servers", "VNC servers" |
| Windows | xpra: every remote window, pop-ups included, is a client window that the client's own window manager frames, moves and resizes | `p`, "xpra" |
| | RDP's per-window channel also gives one client window for each remote window, but as specified the server draws the frame; xrdp's variant, made to draw borders locally, is incomplete by its own wiki; upstream Weston and the shadow server have none | `p`, "RDP"; `s`, "RDP servers" |
| | RFB and Guacamole carry one desktop rectangle | `p` |
| Clipboard | RDP: Unicode text and files; xpra: by type; RFB: Latin-1, with UTF-8 in an extension | `p` |
| Screen size | With RDP and RFB the remote screen can follow the client's size: xrdp on connection and on the fly, Weston to the client's announced resolution, TigerVNC by default; under xpra each window is the client's to resize | `s`, "RDP servers", "VNC servers"; `p`, "xpra" |
| Other channels | xpra: a URL opened on the other side, notifications, printing; RDP: printing | `p` |
| Keys | RDP sends PC scancodes with a layout identifier, or Unicode; RFB sends keysyms | `p` |
| Inside the browser's window | [G] No channel of any protocol here reaches it: toolbar, menus, page dialogs, permission prompts, drop-down lists and the file chooser are drawn on Linux and arrive as pixels | "What stays un-native" |

## What stays un-native

- [D] DEC-014: window chrome, dialogs and downloads are Workbench-native; this section states what a channel can and cannot carry, and judges no protocol against that decision.
- Chromium's kiosk and application-window switches: `topics/hidden-display.md`, "Window mode and ways to be the hidden display".
- [F] In Chromium's window code kiosk mode is always fullscreen, and a normal window has its tab strip, toolbar and location bar only when not fullscreen (`chromium@ceb8f3a65507:chrome/browser/ui/startup/startup_browser_creator_impl.cc:L241-248`; `chrome/browser/ui/window_feature_controller/window_feature_controller.cc:L77-91`).
- [F] An application-type window without an app controller has no tab strip, toolbar, bookmark bar or location bar, and a title bar when not fullscreen; with an app controller the toolbar is always supported, the final say lying with that controller (`chromium@ceb8f3a65507:chrome/browser/ui/window_feature_controller/window_feature_controller.cc:L93-149, L166-187`).
- [F] On X11 Chromium asks the window manager for a frame or for none through the `_MOTIF_WM_HINTS` property; its default for drawing its own frame is off when the window manager does not offer `_NET_WM_MOVERESIZE` or when Chromium cannot name the window manager, and on for stacking window managers (`chromium@ceb8f3a65507:ui/base/x/x11_util.cc:L238-261, L361-376`).
- [G] Under xpra, whether the Amiga draws the browser's frame therefore turns on the window manager the session reports and on the browser's setting.

| Item | Can a channel make it the Amiga's? |
|---|---|
| Where files are: Amiga volumes in the Linux file chooser and as download folder | [G] Yes: RDP's drives; a download can also reach the client as a file through Guacamole's folder or xpra's file sending |
| Clipboard, sound, printing, window size | [G] Yes, by the channels of "Integration" |
| The window frame | [G] Under xpra, unless the window asks for none; under RDP's per-window channel only in xrdp's incomplete variant |
| Anything drawn inside a browser window: toolbar, menus, page dialogs, permission prompts, drop-down lists, the file chooser's look | [G] No, by any channel of the protocols read |
| Navigation and page state once the toolbar is removed: go to an address, back, the page's address, its loading state | [G] No, apart from xpra's `open-url`; a window title travels only in xpra and in RDP's per-window channel |

- Which of those items a stock browser reports as events, through an interface whose owner does not support third-party use: `topics/engine-control.md`, "What a stock Chromium reports" and "Who is supported".

## What a website sees

- [G] An ordinary desktop browser: none of the servers read touches the browser process, and a stock browser started with a window and no debugging switch differs from a desktop browser in none of the markers of `topics/engine-control.md`, "What a site sees".
- [G] The remote screen's size and software rendering are visible to a page as on any such desktop; this was not examined.

## Not established

- The rate of a byte-swapping copy and of RDP's run-length decoder on a 68060, and RC4's rate: unmeasured; an instruction count of each loop would bound them, and only a measurement on the machine would show them.
- The ratio of RDP's run-length coding on real pages' pixels: not measured; the 6.0 above is another coding's (`topics/page-pixels.md`).
- Throughput of a pixel stream through the Amiga's TLS library, with and without the card's acceleration: unmeasured.
- Sound played through AHI against RDP's sound time stamps: not examined.
- The rate of any existing Amiga client against any server of `topics/remote-display-servers.md`: no published figure.
- Where `--app` selects Chromium's window type; which of the browser's dialogs, prompts and file chooser exist in a kiosk or application window; Firefox's kiosk mode: their sources.
- What an xpra session reports as its window manager, and where Chromium applies its frame setting: their sources.
- What a page can tell from the remote screen's size and from software rendering: not examined.

## Sources

`chromium` is defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `thinc` | "THINC: A Virtual Display Architecture for Thin-Client Computing", ACM Symposium on Operating Systems Principles, 2005 | `https://www.cs.columbia.edu/~nieh/pubs/sosp2005_fordist.pdf` | 2026-10-11; SHA-256 `07b8aa1699bcc75b5bba85b20be47d6a12d9d66905a0ddc5ee24c88c5bec54c6` |
