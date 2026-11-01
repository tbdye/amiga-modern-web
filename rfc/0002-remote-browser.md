# RFC 0002: A remote browser in a native Amiga window

| | |
|---|---|
| Author | Thomas Dye |
| Status | Draft, in review; nothing is built or run yet. |
| Last updated | 2026-11-01 |
| Decision owner | Thomas Dye; for the firmware's decode service, the firmware's maintainers have the biggest say (§5). |
| Feedback | First, whether this can feel integrated rather than like a remote desktop (Q1); then the decode service (§5, Q7). Comment on this file's pull request. |
| Related | RFC 0001 ([#8](https://github.com/tbdye/amiga-modern-web/pull/8)) explores a native route, a new Zorro card that takes a browser computer's picture over HDMI. This RFC starts from the Amiga and graphics card people have, plus a Linux computer; both stay open. |
| Sources | This repository's `.kb/`; figures worked out here say "by calculation", and estimates are marked. Terms: Appendix A. |
| Licence | Not chosen yet; the project is not planned as closed-source. |

## 1. Summary

I want a big-box Amiga to reach nearly any website, YouTube and Discord's website included, in a Workbench window.
This RFC takes another point of view than RFC 0001: software first, on hardware people already have.

An ordinary browser runs, unmodified, on a Linux computer on the home network, drawing on a hidden display.
A small control program of the project's sits beside it and sends the page area to a new Amiga program over one TCP connection.
The Amiga program draws everything around the page: the window, toolbar, menus and requesters (Amiga dialogs).
Files download into Amiga drawers and upload from them through Amiga requesters, and the clipboard works both ways.
The Amiga keeps its own network address and its other network use.

```
 LINUX COMPUTER (PC or Pi-class)                       AMIGA (any RTG card; target in §4)
+-------------------------------------+               +--------------------------------------+
| Unmodified browser, from the        |  one TCP      | New Amiga program: window, toolbar,  |
|   distribution, on a hidden display | connection    |   menus, requesters, keymap,         |
| Control program (the project's):    | over the home |   clipboard, files to drawers,       |
|   changed areas, scrolls, sound,    |   network     |   sound through AHI                  |
|   input, address bar, dialogs,      | <-----------> | The Amiga's own TCP/IP stack and     |
|   downloads, clipboard              |  page area +  |   address                            |
| Its own connection to the web       |  everything   | ZZ9000, where fitted: decodes the    |
+-------------------------------------+  else         |   page stream, slides scrolls,       |
                                                      |   decodes pictures and video         |
                                                      +--------------------------------------+
```

The bar is a good integrated feel: it should not look like the Amiga is showing someone else's desktop.

Every speed here is by calculation, or marked as an estimate, from other people's published Amiga figures and from this project's measurements, on a PC, of what real sites change when scrolled and how far the firmware's own encoder compresses it.

What I'm asking:

- Everyone: is the split in §3.4 between Amiga-drawn and browser-drawn integrated enough (Q1), and are the speeds in §4 worth having (Q2, Q3)?
- ZZ9000 firmware maintainers: I'd like your support for a decode service, the inbound counterpart of the firmware's console encoder. The Amiga program receives the page as that encoder's own lossless tile stream on the session's TCP connection and copies it into a card shared buffer, and one new mailbox operation decodes it on the card. No Ethernet or hardware change; by calculation, a whole window paints in about 50 ms instead of about half a second, before the card's decode time, which only hardware shows. The project would write it and offer it upstream; whether and how it is accepted is yours to say (§5, Q7).
- Anyone with experience of Chromium on a hidden X display, WPE WebKit or fast 68k pixel paths: please comment.

## 2. Requirements and non-goals

Most rows restate the project's decisions ([`.kb/decisions.md`](../.kb/decisions.md)).

| Requirement | Measure |
|---|---|
| Modern web | Nearly any website works; YouTube and Discord's website are the examples. |
| A good integrated feel | The window, toolbar, menus and requesters are the Amiga's; the page inside is the browser's (§3.4). |
| Files | Downloads into and uploads from Amiga drawers, chosen in Amiga requesters, over the session's own connection; no shared or mounted drive. |
| Clipboard | Copy and paste both ways; text first, images later. |
| The Amiga keeps its own TCP/IP address | The session is an ordinary TCP connection ([`.kb/topics/link-and-address.md`](../.kb/topics/link-and-address.md), "The ways", row 1). |
| Video with sound in step | On the target (§4); about 15 frames a second is likely the floor, at no set size. |
| Scrolling | One to two updates a second is too slow; no acceptable rate is set (Q2). |
| Window size | Mostly 1024×768 or less; no size is set. |
| Support over performance | Working slowly beats not working. |
| Little browser-engine work | As little engine work as possible (a preference); with stock Chromium the project builds and patches no engine. |

This RFC needs no new hardware; whether a board is designed is Q4.
Not in scope: a full-screen 1080p60 browser.

## 3. The arrangement

### 3.1 The Linux side

Two engines go forward; the Amiga program and the connection are the same for both.

| | Stock Chromium (first) | WPE WebKit (tested early) |
|---|---|---|
| What it is | A Chromium package on a virtual X display; the control program reads changed rectangles, injects input, taps the sound server, and works navigation and dialogs through Chromium's remote-control interface | WebKit's embeddable engine, linked into the control program, which gets each frame's buffer and changed rectangles |
| Comes from | The distribution; the Debian 13 and Raspberry Pi packages are built with H.264 and AAC | The distribution, if it ships 2.54 or later (not established); otherwise the project builds it |
| What a site sees | A desktop Chromium; with a fixed debugging port the automation flag stays unset, and whether sites detect the open session another way is not published (Q5) | Safari on Linux; neither example site names it, and whether Discord works in it is not known; WebRTC, which Discord's calls are reported to use (not verified here), is off in 2.54 |

Sources: [`.kb/topics/engine-control.md`](../.kb/topics/engine-control.md), [`.kb/topics/engine-interfaces.md`](../.kb/topics/engine-interfaces.md), [`.kb/topics/hidden-display.md`](../.kb/topics/hidden-display.md), [`.kb/topics/engine-options.md`](../.kb/topics/engine-options.md); upkeep of each: [`.kb/topics/engine-control.md`](../.kb/topics/engine-control.md), "Upkeep by arrangement".

I propose stock Chromium first, because sites are written for it.
WPE WebKit is tried early on a PC against YouTube and Discord; if both work, it is adopted, since it hands over nearly everything that should become a requester.
Chromium's engine embedded in the project's own program (CEF) is not pursued: the project would build and ship every engine update itself, and Google says it may refuse sign-in from embedded browsers ([`.kb/topics/engine-control.md`](../.kb/topics/engine-control.md), "What a site sees", "Upkeep by arrangement").

### 3.2 The connection

The session is one TCP connection through the Amiga's own TCP/IP stack, so it needs no new hardware and nobody's agreement.
It shares the 68k with the Amiga's other network use: by calculation, each 1 MB/s of other incoming traffic takes 34 to 38% of what the 68k can receive ([`.kb/topics/link-and-address.md`](../.kb/topics/link-and-address.md), "Through the Amiga's stack").

Proposed:

- The base, on any RTG card: the page area travels as exact pixels, uncompressed to start, in VNC's published message forms (RFB), with its continuous-updates extension so the Linux side pushes unasked; any VNC viewer then serves as a test client on a PC.
- On a ZZ9000 with the decode service (§5), the page area travels instead as the firmware's own tile stream, which is not VNC's, so a VNC viewer cannot test it.
- The project's own messages carry the rest on the same connection: toolbar state, requesters, files, clipboard and sound.
- Pixels are exact either way; in the base they are already in the screen's format (on a ZZ9000 16-bit screen, 5-6-5, high byte first), so the 68k converts nothing.
- A scroll travels as "slide this region, then draw this strip", so the graphics card moves what it already holds; the control program finds it by comparing frames, as existing servers do ([`.kb/topics/remote-display-servers.md`](../.kb/topics/remote-display-servers.md), "How a scroll becomes a copy").

### 3.3 The Amiga program

A new program, in C.
It draws through RTG calls, so it reaches any RTG card.
The pointer is the Amiga's own, so its motion waits on no update.
Sound goes through AHI, kept in step by letting the picture follow the sound and dropping a late frame ([`.kb/topics/av-sync.md`](../.kb/topics/av-sync.md)).
No existing Amiga client read has page dialogs as requesters or a pixel path written for the ZZ9000; only the 68k Remote Desktop client has sound (through AHI, with no video to keep in step), and AmiFox, whose native shell round a remote browser is borrowed here as an idea, not code, fetches one picture per interaction ([`.kb/topics/prior-art-remote-clients.md`](../.kb/topics/prior-art-remote-clients.md); [`.kb/topics/prior-art.md`](../.kb/topics/prior-art.md), "Remote and split-engine browsers").

### 3.4 What is the Amiga's, and what stays the browser's

| Item | Stock Chromium | WPE WebKit |
|---|---|---|
| Window frame, toolbar (address, back, reload, title, loading state), menus | Amiga | Amiga |
| Alert, confirm, prompt; login | Requester (Chromium's own alert, confirm or prompt also shows in the page until answered) | Requester |
| File chooser for uploads | ASL requester | ASL requester |
| Downloads | ASL save requester, then the file crosses the session into the drawer; rests on experimental events (fallback, an estimate: watch the download folder) | Same, on the stable download interface |
| Clipboard, text both ways | Through the hidden X display's selection | Through WPE WebKit's clipboard interface; whether it carries text both ways is not established |
| Context menus | Browser-drawn | Amiga pop-up |
| Drop-down lists | Browser-drawn | Amiga list |
| Permission prompts | Browser-drawn | Requester |
| Page scrollbars | Browser-drawn | Browser-drawn |

Amiga text is Latin-1, so characters outside it do not survive a paste into the Amiga; images and rich text come later.
Which other surfaces Chromium draws in a window without its own bars has not been read.

## 4. What the target gets

The target is a 68060 at 50 MHz on Zorro III with a ZZ9000, on a 16-bit screen ([`.kb/topics/target-config-rates.md`](../.kb/topics/target-config-rates.md)).
Uncompressed pixels reach its screen from the network at 1.62 to 2.08 MB/s, by calculation from a receive benchmark on firmware later than release v2.8.1 and from copy figures taken on an 8-bit screen standing in for a 16-bit one ([`.kb/topics/target-config-rates.md`](../.kb/topics/target-config-rates.md), "Pixel rate").
No source measures one program doing both, and a real program may fall well short.
The decode-service column applies the same rate to compressed bytes, plus a 0.28 ms mailbox call per update ([`.kb/topics/arm-offload.md`](../.kb/topics/arm-offload.md), "Per-call cost"), without the card's decode time, which nothing has measured.
On a 32-bit screen, every uncompressed rate halves ([`.kb/topics/sound-paths.md`](../.kb/topics/sound-paths.md), "What each second takes"), and the tile stream has forms for 8- and 16-bit screens only ([its formats](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/ZZ9000_proto.sdk/ZZ9000OS/src/rfb/rfb_encode.h#L31-L45)).

| What | Today, by calculation | With the decode service, by calculation | Source |
|---|---|---|---|
| Painting a whole 800×600 window; 1024×768 | 0.46 to 0.59 s; 0.76 to 0.97 s | 42 to 54 ms; 67 to 86 ms | The pixel rate above |
| Scrolling an 800×600 window by 48 rows, a page with little or nothing fixed | 15 to 25 a second | 160 to 207 a second, the median step of all 883 | [`.kb/topics/scroll-redraw.md`](../.kb/topics/scroll-redraw.md), "Results" |
| The same, with a bar or column fixed to the window | 4.1 to 12; up to 19 to 26 if the sender slides only the part that moved, which nobody has built | Included in the median above | Same |
| Pages that play by themselves: Discord's landing page; a YouTube watch page with its video in view | At most 4.3 to 5.5; at most 2.1 to 6.7 | 24 to 35; 7 to 10, though video should not take this path | Same |
| Video at 320×180 with 48 kHz stereo through AHI, the 68k drawing | 12.4 to 16.4 frames a second; 5.5 to 7.3 at 480×270 | Unchanged | [`.kb/topics/sound-paths.md`](../.kb/topics/sound-paths.md), "What each second takes" |
| Typing, key to character | 26 to 105 ms, an estimate | Unchanged | The sum of the Amiga noticing the key, 0 to 20 ms; sending it, 2 to 10; one or two of the Linux computer's frames, 17 to 66; the return, 7 to 9 |

The compressed bytes were measured on a PC, the firmware's encoder run unmodified on this project's captures: still 800×600 pages shrink about 11 to 12 times (4.7 for a photo wall, 50 for YouTube's home page), and scroll steps, sent as slides, carry 6.4 to 6.7 times fewer bytes than the uncompressed base.
A playing video's tiles shrink only about 3 times, so video keeps the card's video paths.
None of 883 measured scroll steps on 16 sites needed the whole window resent.
Video clears about 15 frames a second at 480×270, by calculation, only where the ZZ9000 decodes each frame, which rests on a conversion pass on the card that nobody has timed; 640×360 is open ([`.kb/topics/decode-rates.md`](../.kb/topics/decode-rates.md), "What the card's ARM decodes today"; [`.kb/topics/sound-paths.md`](../.kb/topics/sound-paths.md), "What each second takes").
The Linux computer's own time to load a site comes first in every case.
Other Amigas get the same program through any RTG card, at rates no source gives; only a ZZ9000 adds decoding ([`.kb/topics/audience.md`](../.kb/topics/audience.md)).

## 5. The ZZ9000 decode service

The base works without firmware changes; the decode service is what takes page pixels off the 68k.
The project would write it and offer it upstream; the firmware's maintainers have the biggest say on whether and how it is accepted.

In the base, every page pixel crosses the card's network port, the Zorro bus and the 68k, then the bus again into the screen.
With the decode service, the Linux side sends the page as the firmware's own tile stream: lossless tiles and slides of what the card already holds, with zlib over the lot, as the console encoder emits it ([its wire format](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/ZZ9000_proto.sdk/ZZ9000OS/src/rfb/rfb_encode.h); [its deflate step](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/ZZ9000_proto.sdk/ZZ9000OS/src/sdk_mailbox.c#L8618-L8644)).
The Amiga program receives it on its ordinary TCP connection, copies it into a card shared buffer and makes one new mailbox call, which decodes it into a page surface of the service's own; the program puts the visible part on screen with the existing surface copy.
The surface is needed because tiles and slides build on the previous picture, which the screen loses when the window is covered.
Compressed bytes still cross the 68k; pixels do not, and no Ethernet code or address changes.
The card's decode rate is unknown until hardware shows it.

The firmware already has the outbound counterpart, the AmiNetXDuo console encoder, which turns the displayed framebuffer into this stream ([its service](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/sdk/include/zz9k/abi.h#L153-L155) and [encode call](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/sdk/include/zz9k/abi.h#L658-L663)) and came in the shape the decode service would take ([PR #152](https://github.com/BlitterStudio/zz9000-firmware/pull/152)).
The new operation can sit beside the encoder's, since a vendor service may add one at the end of its range ([vendor services](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/sdk/docs/zz9k-vendor-services.md#L17-L24)), or under a new vendor ID; that is the maintainers' call.
It runs only when called; without it, the program falls back to RTG writes.
The encoder's source is MIT-licensed ([its licence line](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/ZZ9000_proto.sdk/ZZ9000OS/src/rfb/rfb_encode.c#L7)), so it can serve as the Linux-side sender, at a cost on a Pi-class computer not yet measured; the Linux side sends scroll moves as slides itself, since the encoder's scroll detection does not try a 48-row move ([its candidates](https://github.com/BlitterStudio/zz9000-firmware/blob/a71459f9/ZZ9000_proto.sdk/ZZ9000OS/src/rfb/rfb_encode.c#L424-L441)).
Nothing uses the encoder yet, so its integration is untested in use; the decode service would be its first partner, tested with it.

A later step, proposed only if a card shows the 68k's byte path is still the limit, delivers the same stream to the same decoder from the card's network port: in Ethernet frames to a second hardware address of the card's own, in an address filter the firmware leaves unused, kept in buffers apart from the Amiga's receive backlog, so the Amiga's own traffic and address are unchanged ([`.kb/topics/card-ethernet-sharing.md`](../.kb/topics/card-ethernet-sharing.md), "Telling the two kinds of frame apart"; [`.kb/topics/link-and-address.md`](../.kb/topics/link-and-address.md), "The ways", row 2a).
A UDP port on the Amiga's own address would also work, at the cost of parsing Ethernet, IPv4 and UDP headers on the card's ARM.
Either way it is one cable on the card's existing port, with a ceiling of about 12 MB/s by calculation, shared with the Amiga's own traffic ([`.kb/topics/card-ethernet-sharing.md`](../.kb/topics/card-ethernet-sharing.md), "Sharing the link"); it comes second because it changes the receive path every Amiga network user depends on.

In this arrangement the card's ARM would also slide scrolled pixels and decode JPEG and PNG, both of which it does today, and play video in step on its video service, with or without the audio add-on.

## 6. Security on a home network

I assume a web page eventually takes over the Linux computer, so everything it sends is hostile.
AmigaOS has no memory protection (general knowledge, not verified here), so the Amiga program's parser is the boundary.

| Concern | Proposed |
|---|---|
| Messages from the Linux side | Fixed header and length; over-length and unknown messages dropped; no paths, pointers or Amiga names from the Linux side; rectangles clamped to the window ([`.kb/topics/security.md`](../.kb/topics/security.md), "Proposed parser rules") |
| The card's decoder (§5) | The 68k forwards the stream unchecked and the ARM has no memory protection ([`.kb/topics/arm-offload.md`](../.kb/topics/arm-offload.md), "ARM-side capacity"), so the decoder checks every length against the message and the page surface; the later Ethernet step would face any host on the network |
| Downloads | Each confirmed in an ASL requester; a sanitised name (no `:`, `/` or `.info`); never run or unpacked; whether to confine them to one drawer is open |
| Clipboard | Text only, size-capped; Amiga to Linux only when the user pastes |
| The remote-control interface | Listens on the Linux computer's loopback only, since it gives full control of the browser (general knowledge, not verified here) |
| Network placement | A guest network for the Linux computer can cut it off from the Amiga ([`.kb/topics/link-and-address.md`](../.kb/topics/link-and-address.md), "Safety on the home network") |

Not designed yet: how the two programs know each other, and whether the session is encrypted (Q8).
No speed in §4 includes encryption.

## 7. Order of work

1. The Linux side on a PC, with a VNC viewer as its client: stock Chromium's changed rectangles and capture cost on a hidden display, finding which part of a window moved, and YouTube and Discord in WPE WebKit.
2. The Amiga program: exact uncompressed pixels and PCM sound through AHI.
3. The ZZ9000's help: sliding scrolls from the start, then decoding video frames, then the card's video service; that a program can feed it a stream is an inference.
4. The decode service; asking the firmware maintainers runs alongside step 1.

Every step can be built and tested without a real Amiga: in the Amiberry emulator, which emulates the ZZ9000 from release 8.3.0 ([its ZZ9000 notes](https://github.com/BlitterStudio/amiberry/blob/v8.5.0/docs/zz9000.md)), and, for the decode service, in the firmware's own host tests, which already build the console encoder on a PC ([its test](https://github.com/BlitterStudio/zz9000-firmware/tree/a71459f9/test/console)).
Once the decode service is in the firmware, the project offers Amiberry an emulation of it.
Rates and acceptance come from a real card.

## 8. Open questions

| # | Question | Options | Proposed | What it changes |
|---|---|---|---|---|
| Q1 | Is the split of §3.4 a good integrated feel? | Yes with either engine; only with WPE WebKit's | Open | Whether WPE WebKit must work |
| Q2 | Floors for scrolling and for painting a window | A rate; none | None set; one to two a second is too slow | Whether a smarter sender or the decode service is required |
| Q3 | Which Amigas count as supported, at whatever speed they get? | Any with an RTG card, below the target too; only above a floor; chipset (non-RTG) screens as well | Open | Who the program is for |
| Q4 | Where the Linux computer lives | On the network; an off-the-shelf board in the case; a co-processor board designed for it | Open; the software is the same either way | Whether any hardware is designed |
| Q5 | Do sites treat Chromium with its remote-control port open as automated? Google's sign-in help names browsers "controlled through software automation" among those it may refuse ([`.kb/topics/engine-control.md`](../.kb/topics/engine-control.md), "What a site sees"). | — | Only use shows | If yes, stock Chromium loses the toolbar's navigation and the requesters, and the engine question reopens, WPE WebKit first |
| Q6 | Does a Pi-class computer report small changed areas cheaply on a hidden display? | — | Desk work on one shows | If not: a Wayland compositor's capture, or WPE WebKit's own reports |
| Q7 | The firmware's help (§5) | Decode service; decode service, then the Ethernet step; neither | Decode service first; the base ships without it | What the 68k carries, and its load |
| Q8 | How the two ends know each other; encryption | A paired key; TLS; neither on a home network | Open | Speed on the 68k, and set-up |
| Q9 | Soft text: may page text ever be sent lossy? | Exact always; lossy where it saves more | Exact: the base and the decode service are both lossless, so text stays exact on the card's path too; beyond that, open | Whether a lossy page form is ever added |
| Q10 | Video larger than 320×180 | The card decodes each frame; the card's video service, fed by a real-time re-encode nobody has designed (that a program can feed it a stream is an inference) | Both, chosen at run time; a proposal, not settled | Video size on a ZZ9000 |

## Appendix A. Glossary

| Term | Meaning |
|---|---|
| AHI | The Amiga's standard sound system |
| ASL requester | The standard Amiga file requester |
| Hidden display | A display that exists only in memory, such as a virtual X display |
| Remote-control interface | Chromium's DevTools protocol, made for developer tools and automated testing |
| RTG | Retargetable graphics: Amiga screens drawn by a graphics card, not the chipset |
| Tile stream | The ZZ9000 firmware's own lossless picture format, from its console encoder; not VNC's |
