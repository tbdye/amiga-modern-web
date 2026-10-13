# Page pixels: JPEG and soft text

Scope: what JPEG does to the pixels of real web pages: ratios and PSNR by quality and kind of content, five pieces of page text coded exactly and as JPEG, and whether a browser draws letter edges coloured or grey.
Status: current

- [R] Every figure here is this project's own measurement, made on 2026-10-11 on a Windows 10 PC with Microsoft Edge 154.0.4258.37, headless, from the eleven pages of `topics/page-pixels.md`; the same method on fresh captures would verify any of them.
- Every statement below is `[R]` on those terms unless it opens with another label.
- Captures, pixel formats, units and the conditions of each page are in `topics/page-pixels.md`, "Method" and "Pages measured"; lossless ratios are there by page and in `topics/page-pixels-lossless.md` by class.
- It is a desk measurement of sizes and of error: no Amiga, card or link was involved, no decoder was timed, and no coding is recommended.
- The decision on compression is DEC-008 (`decisions.md`); published decode rates are in `topics/decode-rates.md`.
- "Exact" is the page's pixels in the screen's 16-bit format; "soft" is the same pixels after JPEG.

## Method

- JPEG is Pillow 12.3.0 with libjpeg-turbo 3.1.4.1: baseline, not progressive, 4:2:0 chroma, qualities 50, 75 and 90, coded from the 24-bit capture, each unit alone.
- The whole file is counted, including 623 bytes of header and the standard tables.
- A ratio is the raw 16-bit bytes ÷ the file's bytes; the file is the same for a 32-bit screen, so its ratio against 32-bit is twice the figure given.
- PSNR is in dB, higher is closer, and 99 means identical.
- At 16-bit the decoded picture is truncated to 5:6:5 and compared with the undithered 5:6:5 original, both expanded to 8 bits a channel; at 32-bit it is compared with the 24-bit capture.
- PSNR is a coarse error measure: it does not say how legible smeared text is.

## Ratio and PSNR by quality

Each ratio cell is byte-weighted; median (range), and each PSNR cell is median (range).
The range is lowest–highest for whole screens, and 10th–90th percentile; lowest for strips.
Pools are those of `topics/page-pixels-lossless.md`; "Photo, less blank" leaves out the photo gallery's 41 mostly blank strips.

Whole first screen:

| Pool | Quality | Ratio to 16-bit | PSNR at 16-bit, dB | PSNR at 32-bit, dB |
|---|---|---|---|---|
| Text | 50 | 20.8; 21.6 (16.0–33.6) | 28.1 (25.3–33.9) | 28.2 (25.2–34.4) |
| Text | 75 | 15.1; 15.9 (11.4–25.3) | 29.3 (26.4–35.5) | 29.4 (26.4–36.2) |
| Text | 90 | 10.1; 10.8 (7.49–17.7) | 30.2 (27.2–36.8) | 30.4 (27.3–37.5) |
| Application | 50 | 30.8; 29.6 (22.4–49.5) | 32.4 (31.1–33.9) | 33.0 (31.4–34.5) |
| Application | 75 | 22.4; 21.8 (16.2–36.4) | 34.1 (33.3–36.3) | 35.1 (34.0–37.2) |
| Application | 90 | 14.5; 14.1 (10.5–24.0) | 36.4 (35.0–39.0) | 37.6 (35.9–40.6) |
| Mixed | 50 | 22.3; 23.2 (16.6–30.1) | 27.5 (25.1–33.3) | 27.5 (25.1–33.2) |
| Mixed | 75 | 16.0; 16.8 (11.5–22.8) | 28.6 (26.2–36.2) | 28.7 (26.2–36.1) |
| Mixed | 90 | 10.8; 11.2 (7.57–16.2) | 29.5 (27.0–38.7) | 29.6 (27.1–38.8) |
| Photo | 50 | 24.6; 24.0 (22.4–26.0) | 31.2 (30.5–31.6) | 31.4 (30.6–31.8) |
| Photo | 75 | 17.8; 17.3 (16.4–18.7) | 32.8 (32.1–33.3) | 33.3 (32.4–33.8) |
| Photo | 90 | 11.4; 11.1 (10.9–11.9) | 34.7 (33.8–35.2) | 35.4 (34.2–36.0) |

First-screen strip (Text, 152 strips; Application, 114; Mixed, 76; Photo, 38):

| Pool | Quality | Ratio to 16-bit | PSNR at 16-bit, dB | PSNR at 32-bit, dB |
|---|---|---|---|---|
| Text | 50 | 18.2; 18.5 (11.3–36.2; 7.66) | 28.6 (23.9–38.1; 21.0) | 28.7 (23.8–38.2; 20.9) |
| Text | 75 | 13.7; 14.2 (8.02–30.0; 5.44) | 29.8 (25.0–42.1; 22.0) | 30.0 (25.0–42.2; 21.9) |
| Text | 90 | 9.49; 10.1 (5.33–22.9; 3.63) | 30.9 (25.8–44.6; 22.6) | 31.1 (25.8–46.3; 22.5) |
| Application | 50 | 25.2; 26.0 (16.0–47.4; 12.4) | 32.3 (29.7–38.4; 28.3) | 32.9 (30.1–43.3; 28.7) |
| Application | 75 | 19.3; 20.3 (11.6–39.6; 9.44) | 34.6 (31.5–40.4; 30.0) | 35.4 (32.3–45.6; 30.2) |
| Application | 90 | 13.1; 14.1 (7.67–28.8; 6.13) | 37.1 (33.6–41.8; 31.1) | 38.7 (34.3–48.0; 31.4) |
| Mixed | 50 | 19.4; 20.4 (12.5–36.5; 8.04) | 29.9 (24.4–37.5; 21.2) | 29.8 (24.4–37.2; 21.2) |
| Mixed | 75 | 14.5; 15.4 (9.17–28.8; 5.61) | 31.5 (25.4–41.4; 22.2) | 31.5 (25.5–41.0; 22.2) |
| Mixed | 90 | 10.1; 10.7 (6.25–22.3; 3.67) | 32.8 (26.2–47.4; 22.9) | 32.8 (26.3–47.5; 22.9) |
| Photo | 50 | 20.9; 19.1 (14.3–39.1; 12.4) | 31.1 (28.5–37.6; 27.3) | 31.3 (28.9–36.6; 27.5) |
| Photo | 75 | 15.7; 14.6 (10.6–32.6; 8.85) | 32.8 (30.2–38.6; 28.7) | 33.3 (30.7–38.6; 28.9) |
| Photo | 90 | 10.5; 10.2 (6.71–24.6; 5.54) | 34.8 (32.5–40.4; 30.2) | 35.5 (32.6–41.0; 30.6) |

Scroll strip, which assumes scroll-copy:

| Pool | Quality | Ratio to 16-bit | PSNR at 16-bit, dB | PSNR at 32-bit, dB |
|---|---|---|---|---|
| Text | 50 | 15.1; 15.7 (8.68–36.3; 7.00) | 25.6 (21.8–34.8; 20.6) | 25.6 (21.8–35.8; 20.6) |
| Text | 75 | 11.0; 11.6 (6.14–30.2; 4.86) | 26.7 (22.8–36.4; 21.6) | 26.8 (22.8–37.3; 21.6) |
| Text | 90 | 7.43; 7.78 (4.01–23.6; 3.17) | 27.5 (23.5–38.1; 22.2) | 27.6 (23.5–39.1; 22.3) |
| Application | 50 | 25.7; 31.3 (14.6–51.8; 6.99) | 34.3 (29.1–40.1; 22.7) | 35.0 (29.5–44.5; 22.9) |
| Application | 75 | 19.9; 24.8 (10.9–46.9; 5.16) | 37.6 (31.2–44.2; 24.0) | 38.2 (31.8–47.5; 24.3) |
| Application | 90 | 14.0; 17.3 (7.22–36.1; 3.62) | 41.2 (33.5–51.1; 25.2) | 43.4 (34.5–51.4; 25.5) |
| Mixed | 50 | 17.9; 20.3 (8.94–47.1; 7.51) | 28.2 (21.9–40.4; 21.2) | 28.2 (22.0–40.1; 21.2) |
| Mixed | 75 | 13.2; 15.3 (6.34–40.5; 5.36) | 29.5 (22.9–42.8; 22.1) | 29.6 (23.0–42.6; 22.1) |
| Mixed | 90 | 9.01; 10.5 (4.17–33.8; 3.54) | 30.5 (23.6–46.1; 22.7) | 30.6 (23.7–46.5; 22.7) |
| Photo | 50 | 16.6; 16.3 (11.1–34.7; 7.71) | 31.4 (27.9–36.8; 24.7) | 32.3 (28.4–39.8; 24.9) |
| Photo | 75 | 11.8; 11.7 (7.76–26.6; 5.24) | 33.1 (29.8–38.3; 27.0) | 34.2 (30.5–42.2; 27.2) |
| Photo | 90 | 7.40; 7.18 (4.76–17.7; 3.30) | 35.5 (32.6–40.8; 29.2) | 37.3 (33.7–45.5; 29.9) |
| Photo, less blank | 50 | 15.7; 15.8 (11.1–25.6; 7.71) | 31.1 (27.9–35.0; 24.7) | 31.9 (28.3–36.9; 24.9) |
| Photo, less blank | 75 | 11.1; 11.2 (7.64–19.0; 5.24) | 32.8 (29.8–36.6; 27.0) | 33.8 (30.4–39.2; 27.2) |
| Photo, less blank | 90 | 6.89; 6.96 (4.70–11.8; 3.30) | 35.2 (32.5–38.6; 29.2) | 37.0 (33.6–42.1; 29.9) |

- JPEG smears text: across units and qualities the median PSNR at 16-bit is 25.6 to 30.9 dB on the text pages, against 31.1 to 35.5 dB on the photo gallery.
- At quality 75 the text pages' median is 29.3 dB over whole first screens and 26.7 dB over scroll strips, in round figures 27 to 29 dB.
- Each of those is a median over whole screens or full-width strips, margins and headings included; it is not a figure for dense text.
- On single pieces of text at the same setting the figure runs from 22.6 dB, dense text with coloured letter edges, to 36.3 dB, text with grey edges ("Exact against soft").
- [G] On whole text screens at quality 75 the JPEG is 17% smaller than the PNG: 15.1 against 12.5 times (`topics/page-pixels-lossless.md`, "Whole first screen"), and 12.5 ÷ 15.1 = 0.83.

Quality 75 by page, against 16-bit, over the three window sizes together; each cell is byte-weighted / median:

| Page | Whole first screen | Scroll strip |
|---|---|---|
| Encyclopedia article | 11.8 / 12.1 | 8.02 / 7.58 |
| News front page | 19.8 / 19.6 | 13.4 / 14.1 |
| Code-hosting project page | 18.1 / 17.0 | 14.1 / 14.7 |
| Documentation page | 13.4 / 12.2 | 12.0 / 12.1 |
| YouTube home, signed out | 47.3 / 42.7 | None |
| YouTube watch page | 18.2 / 19.5 | 18.7 / 24.5 |
| YouTube watch page, 640 and 800 wide only | Not applicable | 16.4 / 20.5 |
| YouTube watch page, strips across thumbnails | Not applicable | 9.30 / 9.25 |
| Discord landing page | 20.9 / 20.3 | 21.3 / 25.1 |
| Discord login page | 32.0 / 30.9 | None |
| Forum thread | 13.3 / 11.6 | 12.8 / 14.5 |
| Search results | 20.2 / 18.1 | 17.8 / 24.8 |
| Photo gallery | 17.8 / 17.3 | 11.8 / 11.7 |
| Photo gallery, less blank | Not applicable | 11.1 / 11.2 |

- No video frame on its own was measured: the YouTube watch page's first screen is part page and part moving frame of an animated film, and single screens of it gave 16.2 to 21.8.
- [G] Live action would compress less.
- The watch page's two further rows and the photo gallery's last row are selections of scroll strips (`topics/page-pixels.md`, "Method").

## Exact against soft

Five pieces of the captured pages, each 272×200 pixels and not resampled, coded four ways.
A cell is times smaller than the piece's 108,800 uncompressed 16-bit bytes; a JPEG cell adds the PSNR of soft against exact, both as a 16-bit screen shows them.

| Piece | Letter edges as captured | JPEG 75, 4:2:0 | JPEG 75, 4:4:4 | Exact, PNG | Exact, zlib 6 |
|---|---|---|---|---|---|
| 1: article text, all small and dense | Coloured | 6.13; 22.6 dB | 4.16; 27.6 dB | 9.48 | 16.4 |
| 2: Discord's login form, light on dark | Grey | 19.6; 31.9 dB | 16.0; 35.5 dB | 17.4 | 30.4 |
| 3: a code-hosting page's coloured interface | Coloured | 12.9; 29.0 dB | 9.73; 32.5 dB | 14.6 | 24.8 |
| 4: YouTube's list of other videos, text beside pictures | Grey | 11.2; 33.1 dB | 9.87; 34.3 dB | 4.16 | 5.43 |
| 5: a YouTube comment, grey-edged text | Grey | 12.1; 36.3 dB | 11.4; 36.3 dB | 9.53 | 18.1 |

- Exact is 5 bits red, 6 green and 5 blue by dropping the low bits, undithered.
- Soft is a JPEG of the capture's 24-bit pixels at quality 75, decoded and then made 16-bit the same way; 4:2:0 stores colour at half detail and is the setting of the tables above, and 4:4:4 stores it whole.
- Piece 5 has no colour, so its two soft versions show the same pixels and differ only in coded size.
- Piece 1's 22.6 dB stands beside 27.17 dB for the whole screen it was cut from: the piece is all small text, and its letter edges are coloured, which storing colour at half detail blurs.
- The three grey-edged pieces are other content than the two coloured-edged ones: no piece was captured both ways, so the table does not show what the colour of the edges costs on one text.
- [G] Exact under zlib 6 is smaller than soft at 4:2:0 on four of the five pieces, and exact as PNG on two (pieces 1 and 3).
- PNG is a form the ZZ9000's ARM decodes today (`topics/decode-rates.md`, "What the card's ARM decodes today").
- The 4:4:4 setting was applied to these five pieces only: no whole screen or strip was coded with it.

## Letter edges: coloured or grey

- One browser run drew both kinds: coloured edges in pieces 1 and 3, grey in 2, 4 and 5.
- A check on the same browser build, 2026-10-11: a local test page with seven lines of text, each styled differently, was screenshot headless at device scale factor 1 in a 600×350 window, then again with `--disable-lcd-text` added, and reddish and bluish pixels were counted in each line.
- By default the edges are coloured on plain text and with `-webkit-font-smoothing: antialiased`.
- By default they are grey with `will-change: transform` (also with a white fill), `opacity: 0.99`, `transform: translateZ(0)` and `filter: brightness(1)`.
- With `--disable-lcd-text` the edges are grey in all seven cases.
- The check is one build on Windows, and it does not show why two captured sites came out grey.

## Not established

- Which letter edges a browser on a Linux computer draws by default: the same check on that build would settle it.
- What coloured edges cost in dB on the same text: one piece captured with and without the switch, coded both ways, would settle it.
- Why Discord's login form and the two YouTube pieces came out grey: reading those pages' styles against the seven cases would show it.
- How legible soft text is: PSNR does not say; only looking at such text on a 16-bit screen shows it.
- JPEG at 4:4:4, at other qualities than 50, 75 and 90, or progressive, over whole screens and strips: the same method with those settings would settle it.
- Whether the card's JPEG decoder accepts 4:4:4 files: the firmware's decoder source would settle it.
- A video frame on its own, and live-action video: the same method on such frames would settle it.
- Decode speed, and what the firmware's fast inverse transform does to text: `topics/decode-rates.md`, "Not established".

## Sources

No outside source is cited: every figure is this project's measurement by the method above, and the pages pointed to carry their own sources.
