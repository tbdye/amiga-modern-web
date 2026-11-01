# RFC 0002: A remote browser in a native Amiga window

| | |
|---|---|
| Author | Thomas Dye |
| Status | Draft, in review; nothing is built or run yet. |
| Last updated | 2026-11-01 |
| Decision owner | Thomas Dye; for the firmware function, the firmware's maintainers have the biggest say (§5). |
| Feedback | First, whether this can feel integrated rather than like a remote desktop (Q1); then the firmware function (§5, Q7). Comment on this file's pull request. |
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
| Its own connection to the web       |  everything   | ZZ9000, where fitted: slides scrolls,|
+-------------------------------------+  else         |   decodes pictures and video         |
                                                      +--------------------------------------+
```

The bar is a good integrated feel: it should not look like the Amiga is showing someone else's desktop.

Every speed here is by calculation, or marked as an estimate, from other people's published Amiga figures and from this project's measurements, on a PC, of what real sites change when scrolled.

What I'm asking:

- Everyone: is the split in §3.4 between Amiga-drawn and browser-drawn integrated enough (Q1), and are the speeds in §4 worth having (Q2, Q3)?
- ZZ9000 firmware maintainers: I'd like your support for a firmware function that takes page pixels off the card's existing network port, the one cable the Amiga already uses, and draws them on the card; the Amiga's own traffic is unaffected, and no hardware changes. It lifts the pixel ceiling from about 2 to about 12 MB/s, by calculation, and takes the 68k out of the pixel path. The project would write it and offer it upstream; whether and how it is accepted is yours to say (§5, Q7).
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

- The page area travels in VNC's published message forms (RFB), with its continuous-updates extension so the Linux side pushes unasked; any VNC viewer then serves as a test client on a PC.
- The project's own messages carry the rest on the same connection: toolbar state, requesters, files, clipboard and sound.
- Pixels are exact, uncompressed to start, and already in the screen's format (on a ZZ9000 16-bit screen, 5-6-5, high byte first), so the 68k converts nothing.
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
On a 32-bit screen, every uncompressed rate halves ([`.kb/topics/sound-paths.md`](../.kb/topics/sound-paths.md), "What each second takes").

| What | By calculation | Source |
|---|---|---|
| Painting a whole 800×600 window; 1024×768 | 0.46 to 0.59 s; 0.76 to 0.97 s | The pixel rate above |
| Scrolling an 800×600 window by 48 rows, a page with little or nothing fixed | 15 to 25 a second | [`.kb/topics/scroll-redraw.md`](../.kb/topics/scroll-redraw.md), "Results" |
| The same, with a bar or column fixed to the window | 4.1 to 12; up to 19 to 26 if the sender slides only the part that moved, which nobody has built | Same |
| Pages that play by themselves: Discord's landing page; a YouTube watch page with its video in view | At most 4.3 to 5.5; at most 2.1 to 6.7 | Same |
| Video at 320×180 with 48 kHz stereo through AHI, the 68k drawing | 12.4 to 16.4 frames a second; 5.5 to 7.3 at 480×270 | [`.kb/topics/sound-paths.md`](../.kb/topics/sound-paths.md), "What each second takes" |
| Typing, key to character | 26 to 105 ms, an estimate | The sum of the Amiga noticing the key, 0 to 20 ms; sending it, 2 to 10; one or two of the Linux computer's frames, 17 to 66; the return, 7 to 9 |

None of 883 measured scroll steps on 16 sites needed the whole window resent.
Video clears about 15 frames a second at 480×270, by calculation, only where the ZZ9000 decodes each frame, which rests on a conversion pass on the card that nobody has timed; 640×360 is open ([`.kb/topics/decode-rates.md`](../.kb/topics/decode-rates.md), "What the card's ARM decodes today"; [`.kb/topics/sound-paths.md`](../.kb/topics/sound-paths.md), "What each second takes").
The Linux computer's own time to load a site comes first in every case.
Other Amigas get the same program through any RTG card, at rates no source gives; only a ZZ9000 adds decoding ([`.kb/topics/audience.md`](../.kb/topics/audience.md)).

## 5. The ZZ9000 firmware function

The base works without firmware changes; this function is what lifts it past the 68k's limit.
The project would write it and offer it upstream; the firmware's maintainers have the biggest say on whether and how it is accepted.

In the base, every page pixel crosses the card's network port, the Zorro bus and the 68k, then the bus again into the screen.
The function would receive page pixels on the card's existing network port, the one the Amiga already uses, and draw them on the card, so they never cross Zorro or the 68k; the Amiga's own traffic, such as file shares, still reaches the Amiga unchanged ([`.kb/topics/card-ethernet-sharing.md`](../.kb/topics/card-ethernet-sharing.md), "Telling the two kinds of frame apart").
It needs no second port and no hardware change, only firmware.
The card and the Linux computer both stay on the home switch, so the Amiga keeps its address and its own traffic ([`.kb/topics/link-and-address.md`](../.kb/topics/link-and-address.md), "The ways", row 2a).

| | Today's path | With the function |
|---|---|---|
| Pixel ceiling | 1.62 to 2.08 MB/s | About 12 MB/s by calculation, the 100 Mb/s link's payload, shared with the Amiga's own traffic, and a ceiling, not a floor ([`.kb/topics/card-ethernet-sharing.md`](../.kb/topics/card-ethernet-sharing.md), "Sharing the link") |
| The 68k | Busy with every pixel | Out of the pixel path |
| Unknown | — | How fast the card's ARM receives and draws; only hardware shows |

What it would meet in the firmware as built ([`.kb/topics/card-ethernet-sharing.md`](../.kb/topics/card-ethernet-sharing.md)):

- A way to tell the session's frames from the Amiga's on the one port. One option is a second hardware address of the card's own, on one of the address filters the firmware leaves unused; another is a UDP port on the Amiga's own address. The choice is the maintainers' (Q7).
- Its frames need receive buffers apart from the Amiga's receive backlog, which stops being refilled when 96 frames are waiting.
- Its parser faces the Linux computer directly, so the rules of §6 apply to it.

In this arrangement the card's ARM would slide scrolled pixels and decode JPEG and PNG, both of which it does today; play video in step on its video service, with or without the audio add-on; and, with this function, receive and draw page pixels.

## 6. Security on a home network

I assume a web page eventually takes over the Linux computer, so everything it sends is hostile.
AmigaOS has no memory protection (general knowledge, not verified here), so the Amiga program's parser is the boundary.

| Concern | Proposed |
|---|---|
| Messages from the Linux side | Fixed header and length; over-length and unknown messages dropped; no paths, pointers or Amiga names from the Linux side; rectangles clamped to the window ([`.kb/topics/security.md`](../.kb/topics/security.md), "Proposed parser rules") |
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
4. The firmware function; asking the firmware maintainers runs alongside step 1.

Every step can be built and tested without a real Amiga: in the Amiberry emulator, which emulates the ZZ9000 from release 8.3.0 ([its ZZ9000 notes](https://github.com/BlitterStudio/amiberry/blob/v8.5.0/docs/zz9000.md)), and, for the firmware function, in the firmware's own tests, which already run its Ethernet receive code on a PC.
Once the function is in the firmware, the project offers Amiberry an emulation of it.
Rates and acceptance come from a real card.

## 8. Open questions

| # | Question | Options | Proposed | What it changes |
|---|---|---|---|---|
| Q1 | Is the split of §3.4 a good integrated feel? | Yes with either engine; only with WPE WebKit's | Open | Whether WPE WebKit must work |
| Q2 | Floors for scrolling and for painting a window | A rate; none | None set; one to two a second is too slow | Whether a smarter sender or the firmware function is required |
| Q3 | Which Amigas count as supported, at whatever speed they get? | Any with an RTG card, below the target too; only above a floor; chipset (non-RTG) screens as well | Open | Who the program is for |
| Q4 | Where the Linux computer lives | On the network; an off-the-shelf board in the case; a co-processor board designed for it | Open; the software is the same either way | Whether any hardware is designed |
| Q5 | Do sites treat Chromium with its remote-control port open as automated? Google's sign-in help names browsers "controlled through software automation" among those it may refuse ([`.kb/topics/engine-control.md`](../.kb/topics/engine-control.md), "What a site sees"). | — | Only use shows | If yes, stock Chromium loses the toolbar's navigation and the requesters, and the engine question reopens, WPE WebKit first |
| Q6 | Does a Pi-class computer report small changed areas cheaply on a hidden display? | — | Desk work on one shows | If not: a Wayland compositor's capture, or WPE WebKit's own reports |
| Q7 | The firmware function (§5) | Support it; not | Support it; the base ships first | The pixel ceiling, and the 68k's load |
| Q8 | How the two ends know each other; encryption | A paired key; TLS; neither on a home network | Open | Speed on the 68k, and set-up |
| Q9 | Soft text: may page text be sent lossy where the ZZ9000 decodes? | Exact always; soft on the card's path | A first version sends exact pixels; beyond that, open | Whether the card decodes page areas as well as video |
| Q10 | Video larger than 320×180 | The card decodes each frame; the card's video service, fed by a real-time re-encode nobody has designed (that a program can feed it a stream is an inference) | Both, chosen at run time; a proposal, not settled | Video size on a ZZ9000 |

## Appendix A. Glossary

| Term | Meaning |
|---|---|
| AHI | The Amiga's standard sound system |
| ASL requester | The standard Amiga file requester |
| Hidden display | A display that exists only in memory, such as a virtual X display |
| Remote-control interface | Chromium's DevTools protocol, made for developer tools and automated testing |
| RTG | Retargetable graphics: Amiga screens drawn by a graphics card, not the chipset |
