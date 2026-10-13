# Page pixels: how they compress

Scope: how the pixels of eleven real web pages were captured and coded, what each page showed, the headline ratios, lossless ratios by page, 16-bit against 32-bit and dithered pixels, and what changes on a page left alone.
Status: current

- [R] Every figure here is this project's own measurement, made on 2026-10-11 on a Windows 10 PC with Microsoft Edge 154.0.4258.37, headless and with its user agent unchanged, from eleven pages as served that day; the same method on fresh captures would verify any of them.
- Every statement below is `[R]` on those terms unless it opens with another label.
- It is a desk measurement of sizes: no Amiga, card or link was involved, no decoder was timed on a 68k or on the card's ARM, and no coding is recommended.
- The decision on compression is DEC-008 (`decisions.md`); published decode rates are in `topics/decode-rates.md`.
- Lossless ratios by class of content, for every coding and pixel format, are in `topics/page-pixels-lossless.md`; JPEG, PSNR and soft text are in `topics/page-pixels-lossy.md`; what sites resend when scrolled is in `topics/scroll-redraw.md`.
- A ratio is raw bytes ÷ coded bytes: higher is smaller, and under 1 the coded unit is larger than raw.
- Two figures describe every set of screens or strips, and they differ.
- The byte-weighted ratio is the raw bytes of all the units ÷ their coded bytes; the bytes on a link follow it, and with them the time to repaint or scroll through a page.
- The median ratio is the middle of the per-unit ratios; it describes a typical single screen or strip and nothing more.
- On the text pages most scroll strips are largely blank and a few are costly, so the median sits above the byte-weighted figure: at 16-bit under zlib 6 they are 22.4 and 14.7, and the least compressible 305 of the 1,973 strips (15%) carry half of all the coded bytes; on the photo gallery's scroll strips the median is the lower of the two, 2.30 against 2.47.

## At a glance

All against 16-bit pixels and byte-weighted; lossless figures are under zlib 6 unless a coding is named.

- Four text pages: 16.6 whole screen and 14.7 scroll strip; by page 9.4 to 32.6 and 7.6 to 33.3, the low end being a news front page full of photographs.
- The same under LZ4: 11.7 and 9.9; Hextile: 7.5 and 6.0; run-length: 6.0 and 4.6.
- Photographs, as the scroll strips of a wall of photographs without its mostly blank strips: 2.28, with the 10th-percentile strip at 1.53 and the worst at 1.22; LZ4 1.64; run-length 1.14.
- Strips across video thumbnails: 1.99.
- JPEG at quality 75: text pages 15.1 whole screen and 11.0 scroll strip, with the text smeared (median PSNR 29.3 dB over whole screens and 26.7 dB over scroll strips, margins and headings included, against 22.6 dB on a piece of dense text with coloured letter edges and 36.3 dB on one with grey edges); the photo wall's scroll strips 11.1, without its mostly blank strips; strips across thumbnails 9.3 (`topics/page-pixels-lossy.md`).
- Three application-style pages, all signed out: 6.7 to 13.9 whole screen; the two of them that scroll are 9.0 (the YouTube watch page at 640 and 800 wide) and 12.5 (Discord's landing page) by scroll strip.
- Scroll-strip figures assume scroll-copy ("Method"); without it the whole-screen figures apply to every scroll.

## Method

Capture:

- A script drives the browser and uses its own screenshot call; each page and window size is a first visit in a fresh isolated context: no cookies, cache or login, default settings, nothing clicked.
- Window sizes are 640×480, 800×600 and 1024×768 at device scale factor 1: 33 captures, and every load event fired.
- Each capture holds the first screen 8 s after the page's load event, the same view 2 s later, and the scrollable page from the top, cut off at 9,600 rows.
- The full page is one screenshot, taken after scrolling through the page once so that content that loads on approach is present.
- The forum thread draws only the posts near the window and came out blank that way; its full page is assembled from scroll steps of 240 rows, keeping the rows each step newly exposes.
- Two first-choice sites, a search engine and a photo site, refused the headless browser and were replaced by another site of the same kind; nothing was done to get past either check.
- The 800×600 first screen of every page was looked at by eye: no consent wall hid any page's content.
- The browser's 15-pixel scrollbar is in 30 of the 33 first screens and in the forum thread's full pages, and in no other full page.
- Where a full page's right-hand 15 columns are a single colour (12 captures), those scroll strips' ratios would be at most 2.3% lower without them (1.5% at 1024 wide).
- No capture records the page's HTTP status.

Pixel formats:

- 16-bit: RGB565 by truncation, bytes in big-endian order, 2 bytes a pixel.
- 16-bit dithered: the same after a 4×4 ordered (Bayer) dither.
- 32-bit: bytes B, G, R and a constant fourth byte, 4 bytes a pixel; one raw byte in four carries nothing, so a 32-bit ratio is not comparable with a 16-bit one ("16-bit against 32-bit, and dithering").

Units:

- Whole first screen: a full repaint.
- First-screen strip: each full 48-row strip of the first screen; at 800×600 the last 24 rows of the screen are in no strip.
- Scroll strip: each 48-row strip of the full page below the first screen, which is what scrolling down 48 rows newly exposes.
- A scroll strip stands for the cost of a scroll only if the client moves the pixels it already has (scroll-copy) and is sent just the new strip; without scroll-copy a 48-row scroll resends the whole window, and the whole-screen figures apply.
- It also leaves out whatever stays fixed to the window and must be repainted after the move, which `topics/scroll-redraw.md` measures.

Codings, each unit coded alone:

| Coding | What was measured |
|---|---|
| Run-length | The measuring tool's own, not a VNC encoding: runs of whole pixels in raster order; a record is one length byte (1 to 256) plus the pixel |
| Hextile | An encoder and decoder written for the measurement to `rfc6143` §7.7.4: 16×16 tiles, a background colour plus sub-rectangles found by a greedy search |
| TRLE | The same, to §7.7.5: 16×16 tiles, each the smallest of raw, solid, packed palette, palette run-length and plain run-length; palette reuse between tiles is not used |
| ZRLE | The same, to §7.7.6: that tile coder on 64×64 tiles, then zlib level 6, with the 4-byte length; one fresh zlib stream per unit |
| zlib 1, zlib 6 | zlib 1.3.1 on the raw pixel bytes |
| LZ4, LZ4 HC | The LZ4 block format (library 1.9.4): default mode, and the library's default high-compression level |
| PNG | Pillow 12.3.0 with zlib-ng 1.3.1: truecolour, compression level 6, adaptive row filters; the whole file is counted, 57 bytes of container with one data chunk and 12 more for each further chunk |

- [F] The specification gives Hextile and TRLE 16×16 tiles, and ZRLE 64×64 tiles under zlib behind a 4-byte length, with one zlib stream for the whole connection (`rfc6143` §7.7.4 to §7.7.6).
- The three VNC coders produce the actual byte streams and decode them again; their sizes were checked against cases worked out by hand from the specification, not against another VNC implementation.
- At 16-bit the PNG carries the 5:6:5 pixels expanded to 8 bits a channel, and its ratio is against the 16-bit raw size; the 32-bit to 16-bit pass a ZZ9000 needs afterwards (`topics/decode-rates.md`, "What the card's ARM decodes today") is outside the measurement.

Two selection rules choose which strips a figure covers and change no measured size; a pixel is near-white when all three 8-bit channels of the capture are 240 or more:

- A scroll strip of the photo gallery that is more than 50% near-white is mostly blank: 41 of 561, of which 36 are blank placeholders at the end of the page and 5 are 53% to 87% near-white.
- A scroll strip of the YouTube watch page that is less than 20% near-white lies across the thumbnails of the recommended videos: 29 of 358, all at 640 and 800 wide.

## Pages measured

| Page | Class | What was shown | Scroll strips at 640 / 800 / 1024 wide |
|---|---|---|---|
| Encyclopedia article | Text | The article, under a site notice | 190 / 187 / 184 |
| News front page | Text | Many photographs; a subscription bar fixed to the window bottom; advertisement slots empty | 183 / 143 / 113 |
| Code-hosting project page | Text | The project page as a signed-out visitor sees it | 135 / 148 / 129 |
| Documentation page | Text | The article; an advertisement banner above it and one in the sidebar, both filled | 190 / 187 / 184 |
| YouTube home, signed out | Application | No video grid: nearly empty, and not scrollable | None |
| YouTube watch page | Application | The video, an animated film, playing by itself at every size; the recommended videos' thumbnails are stacked below the video at 640 and 800 wide and sit beside the comments at 1024 wide, where the full-page capture shows them blank | 111 / 113 / 134 |
| Discord landing page | Application | A marketing page with animated decoration | 152 / 115 / 120 |
| Discord login page | Application | The login form, nothing entered; not scrollable | None |
| Forum thread | Mixed | The thread, under a guidelines notice; its progress widget, fixed in the window's bottom rows, is in one or two of every five scroll strips | 190 / 185 / 180 |
| Search results | Mixed | The results page | 28 / 24 / 22 |
| Photo gallery | Photo | A wall of photographs, each smaller than the window, with thin light gaps; navigation and an empty advertisement area above; a cookie notice fixed to the window bottom; the last 14 strips at 800 wide and 22 at 1024 wide are blank placeholders, the photographs not having loaded | 190 / 187 / 184 |

- Every page gives three whole first screens, one for each window size, and 38 first-screen strips.
- A class pools its pages and the three window sizes, so its scroll strips are weighted by page length.
- The class names are loose labels: "Text" includes the news front page, which sets the low end of every text figure, and the two "Mixed" pages are mostly text and compress better than the text pool.
- The news front page is itself flattered: its advertisement slots were empty, and 62 of its 439 scroll strips are a single colour.
- [G] A visitor's browser may fill advertisement slots with pictures, which compress like photographs and often animate.
- The signed-out YouTube home page is nearly empty and is left out of every application figure.
- All four application pages were signed out: none is Discord's application, and none is a YouTube page full of thumbnails.
- [G] Both would compress far less than the application figures here; the nearest measured stand-in for thumbnails is the 1.99 of "By page, 16-bit".
- Anything fixed to the window appears once in a full-page capture, so no scroll strip includes the repaint a bar, header or notice needs after a scroll-copy.
- Pictures can be missing from a full page taken as one screenshot: that was seen twice, on the photo gallery and the watch page, both flattering the figures, and the other full pages were not checked picture by picture.
- A whole-screen figure rests on 3 screens of one page, or on 6 to 12 screens of 2 to 4 pages.

## By page, 16-bit

Byte-weighted ratios over the three window sizes together; the second column is the median under zlib 6, and the last is the byte-weighted zlib 6 ratio at 32-bit.

Whole first screen, three screens a page:

| Page | zlib 6 | zlib 6, median | ZRLE | LZ4 HC | LZ4 | PNG | Hextile | Run-length | zlib 6 at 32-bit |
|---|---|---|---|---|---|---|---|---|---|
| Encyclopedia article | 18.3 | 19.1 | 18.3 | 17.3 | 12.2 | 12.1 | 7.04 | 5.30 | 23.3 |
| News front page | 9.39 | 9.66 | 9.41 | 8.38 | 6.61 | 8.48 | 4.89 | 4.13 | 7.24 |
| Code-hosting project page | 32.6 | 31.4 | 35.2 | 30.5 | 21.4 | 20.4 | 13.8 | 10.6 | 47.9 |
| Documentation page | 20.3 | 20.4 | 23.8 | 21.2 | 16.0 | 14.0 | 8.64 | 6.84 | 27.0 |
| YouTube home, signed out | 83.5 | 70.4 | 97.8 | 69.6 | 55.0 | 50.8 | 37.5 | 28.3 | 109 |
| YouTube watch page | 6.68 | 7.04 | 6.73 | 5.99 | 4.68 | 5.76 | 4.14 | 3.40 | 5.50 |
| Discord landing page | 7.61 | 7.72 | 7.33 | 6.84 | 5.30 | 6.82 | 4.24 | 3.98 | 5.58 |
| Discord login page | 13.9 | 13.5 | 15.8 | 12.4 | 7.30 | 10.5 | 4.61 | 4.17 | 6.30 |
| Forum thread | 28.3 | 25.7 | 27.9 | 25.5 | 16.3 | 17.7 | 9.03 | 6.49 | 41.4 |
| Search results | 29.6 | 28.4 | 32.7 | 26.5 | 20.9 | 17.6 | 11.4 | 8.93 | 39.7 |
| Photo gallery | 5.61 | 5.40 | 5.57 | 4.93 | 4.02 | 5.28 | 3.22 | 2.84 | 4.40 |

Scroll strip, which assumes scroll-copy:

| Page | zlib 6 | zlib 6, median | ZRLE | LZ4 HC | LZ4 | PNG | Hextile | Run-length | zlib 6 at 32-bit |
|---|---|---|---|---|---|---|---|---|---|
| Encyclopedia article | 15.5 | 18.0 | 14.6 | 13.2 | 8.93 | 10.2 | 4.88 | 3.49 | 19.9 |
| News front page | 7.64 | 16.2 | 7.50 | 6.72 | 5.65 | 6.88 | 4.11 | 3.44 | 6.77 |
| Code-hosting project page | 33.3 | 35.7 | 33.7 | 29.8 | 19.1 | 21.4 | 12.3 | 8.04 | 49.9 |
| Documentation page | 19.3 | 19.5 | 19.4 | 18.8 | 14.8 | 14.2 | 7.46 | 6.05 | 29.2 |
| YouTube watch page | 13.5 | 36.1 | 14.1 | 11.8 | 10.2 | 10.6 | 7.41 | 6.24 | 13.1 |
| YouTube watch page, 640 and 800 wide only | 9.02 | 29.5 | 9.14 | 7.90 | 6.83 | 7.74 | 5.18 | 4.42 | 8.26 |
| YouTube watch page, strips across thumbnails | 1.99 | 1.98 | 1.98 | 1.76 | 1.55 | 2.00 | 1.31 | 1.11 | 1.69 |
| Discord landing page | 12.5 | 16.1 | 12.3 | 10.5 | 7.52 | 9.92 | 6.27 | 5.61 | 8.28 |
| Forum thread | 27.9 | 30.5 | 27.8 | 23.6 | 15.9 | 17.6 | 8.89 | 6.34 | 39.6 |
| Search results | 29.0 | 36.7 | 27.5 | 24.6 | 19.6 | 16.7 | 10.9 | 8.45 | 40.0 |
| Photo gallery | 2.47 | 2.30 | 2.52 | 2.12 | 1.78 | 2.32 | 1.46 | 1.24 | 2.00 |
| Photo gallery, less blank | 2.28 | 2.22 | 2.32 | 1.95 | 1.64 | 2.14 | 1.35 | 1.14 | 1.84 |

- The watch page's scroll strips at 1024 wide, 31.8 under zlib 6, are too high, because the thumbnails beside the comments are blank in that capture; at 640 and 800 wide the figure is 9.02.
- The 29 strips across thumbnails are the nearest measured stand-in for a page of thumbnails; thresholds from 8% to 40% in their selection rule give 1.83 to 2.11 under zlib 6.
- [G] Those thumbnails are of cartoons and animated films, and the watch page's video is an animated film; photographic thumbnails and live-action frames would compress less.
- The photo gallery's whole screens are navigation, two photographs and a cookie notice: 5.61 is not a figure for a photograph.
- A photograph that fills the window was not measured; the nearest figure is the 10th-percentile strip of the gallery without its mostly blank strips, 1.53 under zlib 6.
- The worst text strip, 1.49 under zlib 6, is a strip of the news front page filled by photographs.

## 16-bit against 32-bit, and dithering

- [G] Coded bytes per pixel are 2 ÷ ratio at 16-bit and 4 ÷ ratio at 32-bit, so equal ratios mean twice the bytes at 32-bit.
- Text whole screens under zlib 6 are 16.6 at 16-bit and 16.7 at 32-bit, which is 0.120 and 0.239 bytes a pixel: 32-bit costs 2.0 times the bytes, and the medians, 19.8 and 26.9, point the other way.
- Under zlib 6, 32-bit costs 1.4 times the bytes of 16-bit on the mixed whole screens, 1.8 times on the text scroll strips, 2.4 to 4.4 times on the three application pages' whole screens, and 2.5 times on the photo gallery's scroll strips.
- Of the lossless codings PNG differs least, 1.1 to 2.5 times: at 16-bit the PNG already carries three bytes a pixel.
- Dithering lowers every pool's figure, byte-weighted and median, for every unit and coding; of the 39,231 single results at 16-bit (4,359 units × 9 codings), 316 are smaller dithered.
- On text whole screens, byte-weighted, dithering takes zlib 6 from 16.6 to 13.5 and run-length from 5.96 to 2.26; on the three application pages' whole screens it takes run-length from 3.82 to 0.87, larger than raw.

## What changes with nothing touched

The share of 16×16 tiles that differ, as 16-bit pixels, between the two first-screen frames taken 2 s apart:

| Page | 640×480, 1,200 tiles | 800×600, 1,900 tiles | 1024×768, 3,072 tiles |
|---|---|---|---|
| YouTube watch page, one video playing | 686 (57.2%) | 1,372 (72.2%) | 920 (29.9%) |
| Discord landing page, no video | 0 | 113 (5.9%) | 200 (6.5%) |

- The other nine pages did not change at any size.
- The share is the area that changed between two samples, not how often it changes: two samples cannot tell a region repainted sixty times a second from one that changed once.
- Two frames 2 s apart catch animation running at that moment, and not slower timers such as a carousel that advances every few seconds.

## Not established

Each would be settled by the same method on captures that hold it, unless the line says otherwise.

- Pages behind a login: Discord's application, a signed-in YouTube home page, a page full of thumbnails.
- A photograph that fills the window; a video frame on its own; live-action video; the watch page before playback, since the video started by itself at every size.
- A scrolled view: every capture is of the top of a page, or of the page laid out from the top, so which pages keep a bar fixed to the window top was not checked here.
- 8-bit screens; the VNC Tight, RRE and CoRRE encodings; encoding time on the host.
- A real protocol's overhead: per-rectangle headers, update bookkeeping and the transport; a real ZRLE connection shares one zlib stream across rectangles, where every unit here starts a fresh one, which costs small strips a little.
- Decode speed on a 68k or on the card's ARM: nothing here measures it; published rates are in `topics/decode-rates.md`.
- How far one day's eleven pages, one of each kind, stand for the web: more pages and more days would show it.

## Sources

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `rfc6143` | RFC 6143, The Remote Framebuffer Protocol (March 2011) | `https://www.rfc-editor.org/rfc/rfc6143.txt` | 2026-10-12; SHA-256 `6550cbe29ce79b1d7349c0474d036fae3ef2dba84979b0850326e972f5096eb7` |
