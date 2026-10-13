# Scroll redraw: what real sites resend when scrolled

Scope: how much of an 800×600 window sixteen real pages change at each 48-row scroll step, measured over 883 steps under two models of what a sender resends, and the updates a second those bytes give on the target configuration at 50 MHz.
Status: current

- [R] The bytes and shares here are this project's own measurement, made on 2026-10-12, 02:29 to 02:49 UTC, on a Windows 10 PC with Microsoft Edge 154.0.4258.37, headless and with its user agent unchanged: 16 pages, one signed-out visit each, 883 steps; the same method on fresh captures would verify them.
- Every statement below is `[R]` on those terms unless it opens with another label.
- [D] DEC-035: the target configuration is a 68060 at 50 MHz on Zorro III with a ZZ9000; the updates a second here are stated for it.
- [G] Every updates-a-second figure is arithmetic on those bytes with third parties' published rates ("Updates a second at 50 MHz"); no Amiga was measured and no sending program was run.
- The 16 pages were picked by hand, and the shares are of these 883 steps, 180 of them YouTube's, not of the web.
- The bytes are 16-bit pixels, uncompressed; what coding does to them is in `topics/page-pixels.md`.

## Method

- Each site is loaded in a fresh browser context, with no cookies and no login, in an 800×600 window at device scale factor 1; nothing was clicked.
- Two unscrolled frames are taken, 8 s after the load event and 2 s later, as an idle check.
- Then come 60 steps, or as many as reach the page's end, each a script's `scrollBy` of 48 rows with `behavior: 'instant'`.
- After each step frames are taken 0.3 s apart until two are equal as 16-bit pixels, for at most 4 s, and that rested frame is kept.
- Every site scrolled its window and none a pane.
- Each pixel of a rested frame is classed against the frame before, as 16-bit pixels, in this order: slid, equal to it moved up 48 rows; strip, the bottom 48 rows; fixed, equal to it in the same place; changed, anything else.
- Class shares are neither costs nor areas: the blank background inside a fixed bar equals itself 48 rows down and counts as slid, so "fixed" undercounts what stays put.
- Cost is counted in whole 16×16 tiles, a tile being sent if any pixel in it must be, on a grid that starts at the window's bottom edge: the strip is 76,800 bytes and the window 960,000.
- Whole-window slide: the whole window is moved up, and what is sent is strip + fixed + changed.
- Region-aware slide: only what moved is moved, and what is sent is strip + changed.
- [G] Above the strip the region-aware figure is a floor for a real sender, each pixel being taken as free to move or to stay; in the strip it is not, since both models send the strip whole ("Conditions").
- [G] Both models take the sender to know what moved; servers that find a scroll from the frames themselves are in `topics/remote-display-servers.md`, "How a scroll becomes a copy".

## Updates a second at 50 MHz

- [G] One update is the card moving the pixels it holds, then the 68k receiving the bytes sent and drawing them: updates a second = 1 ÷ (bytes ÷ pixel rate + move time).

| Input | Slow end | Fast end | Owner |
|---|---|---|---|
| Pixel rate: uncompressed 16-bit pixels from the network to the screen | 1.62 MB/s | 2.08 MB/s | `topics/target-config-rates.md`, "Pixel rate" |
| Time for a ZZ9000 to move an 800×600, 16-bit window's pixels vertically | 1.9 ms | 1.4 ms | `topics/bus-and-card-rates.md`, "Scrolls on the card" |

- [G] The pixel rate is derived there as 1 ÷ (1/receive + 1/copy), from 2.6 to 2.9 MB/s received through the ZZ9000 ("Network receive") and 4.3 to 7.3 MB/s copied into the card ("Copies into the card"): 1 ÷ (1/2.6 + 1/4.3) = 1.62 and 1 ÷ (1/2.9 + 1/7.3) = 2.08; MB is 10^6 bytes.
- [G] Slow inputs are paired with slow and fast with fast, so every figure is a bracket, slow to fast.
- [G] Worked on 171,008 bytes: ÷ 1,620,000 = 105.6 ms, + 1.9 = 107.5 ms, 9.3 a second; ÷ 2,080,000 = 82.2 ms, + 1.4 = 83.6 ms, 12 a second.

| Bytes sent | Share of the window | Updates a second [G] |
|---|---|---|
| 76,800, the bare strip | 8% | 20 to 26 (49.3 and 38.3 ms) |
| 124,800, the strip and 5% of the window | 13% | 13 to 16 (78.9 and 61.4 ms) |
| 480,000 | 50% | 3.4 to 4.3 (298.2 and 232.2 ms) |
| 960,000, the whole window | 100% | 1.7 to 2.2 (594.5 and 462.9 ms) |

- [G] The inputs carry the conditions stated under their headings: the receive rate is a benchmark into memory, the copies are 8-bit runs standing in for a 16-bit write, the move time is scaled from whole-screen scrolls, and no source measures one program doing all three.
- [G] The move time is charged in full in both models, and the sender's work to find what moved is not counted.
- [G] Only bytes are counted: each separate area sent is one more draw call and message, and the copy rate rests on calls of 9,090 pixels (`topics/target-config-rates.md`, "Copies into the card"), so many small areas cost more per byte than counted here.

## Results

No step of the 883 resent the whole window: the costliest sent 79% of it under the whole-window slide and 71% under the region-aware slide.

Steps sorted by bytes sent: clean is the strip and at most 5% of the window, so at most 124,800 bytes; half or more is 480,000 bytes or more; partial is everything between.

| Model | Clean | Partial | Half or more |
|---|---|---|---|
| Whole-window slide | 314 (36%) | 564 (64%) | 5 (0.6%) |
| Region-aware slide | 787 (89%) | 92 (10%) | 4 (0.5%) |

- The clean counts move with the 5%: at 1% they are 160 (18%) and 606 (69%); at 2%, 179 (20%) and 701 (79%); at 10%, 464 (53%) and 819 (93%).
- The 5 and 4 steps of half or more are the YouTube watch page's first four steps (its first three under the region-aware slide) and one step of the encyclopedia article.
- [G] Those steps give 2.1 to 3.9 a second.
- [G] At the slow end 3 steps under the whole-window slide and 2 under the region-aware slide give 2.5 a second or under, and at the fast end none: the watch page's first one or two steps and that encyclopedia step.
- [G] Under 5 a second at the slow end means more than 320,922 bytes, a third of the window ((1/5 s − 1.9 ms) × 1,620,000): 113 steps (13%) under the whole-window slide, 106 of them on the documentation page and Discord's landing page, and 10 (1.1%) under the region-aware slide.
- Where a page keeps nothing fixed to the window and nothing plays (the file archive, the Amiga news site and the code-hosting page's first 41 steps: 119 steps), every step sent 8 to 9% of the window.
- [G] That is 19 to 26 a second under either model.
- [G] On the 14 pages where every step came to rest, the median step gives 10 to 26 a second under the region-aware slide, 17 to 26 on 12 of them.
- [G] Under the whole-window slide it gives 4.1 to 25: 15 to 25 on the six pages with little or nothing fixed, and 4.1 to 12 on the eight with a bar, a column or a floating box.
- The other two pages, Discord's landing page and the YouTube watch page, play by themselves.

By page; eight of the sixteen are pages of `topics/page-pixels.md`, visited again.
A model's cell gives the bytes sent and, after the colon, the updates a second `[G]`, slow–fast, for the median step (with its share of the window), then the worst tenth of the steps (the 90th percentile of their bytes), then the worst step.
Steps are clean / partial / half or more, whole-window then region-aware.

| Page | What it did when scrolled | Whole-window slide | Region-aware slide | Steps |
|---|---|---|---|---|
| YouTube channel page, a grid of video thumbnails | A top bar and a narrow left menu stay put; the row of tabs sticks under the bar from step 7. Thumbnails slide cleanly | 239,360 (25%): 6.7–8.6; 240,384: 6.7–8.5; 240,384: 6.7–8.5 | 78,336 (8%): 20–26; 78,848: 20–25; 133,120: 12–15 | 0/60/0; 59/1/0 |
| YouTube search results | The same bar and menu. Here the bar is faintly see-through: where thumbnails pass under it its pixels change at every step, by at most 20 levels of 256 (at most 8 in 49 of the 60 steps) | 181,760 (19%): 8.8–11; 185,754: 8.6–11; 188,928: 8.4–11 | 118,784 (12%): 13–17; 126,336: 13–16; 130,304: 12–16 | 0/60/0; 50/10/0 |
| YouTube watch page, all 60 steps | The video started by itself: 71% of tiles changed in 2 s before any scroll. With the video playing in the window (steps 1 to 7, none of which came to rest) a step sent 79% falling to 32% of the window, 71% to 24% region-aware | 155,392 (16%): 10–13; 316,006: 5.1–6.5; 753,920: 2.1–2.7 | 78,848 (8%): 20–25; 236,442: 6.8–8.7; 680,960: 2.4–3.0 | 0/56/4; 52/5/3 |
| The same, steps 8 to 60: no playing video in the window | The top bar stays put; titles, rows of thumbnails and comments slide cleanly. At step 8, the costliest, the player's last 48 rows are still in the window, as a blank dark band | 153,344 (16%): 10–13; 156,928: 10–13; 233,728: 6.8–8.8 | 78,336 (8%): 20–26; 78,848: 20–25; 154,624: 10–13 | 0/53/0; 52/1/0 |
| Discord landing page, all 60 steps | A one-colour top bar stays put. Video clips play by themselves in the window in 51 steps and decorations drift: 58 steps never came to rest, and 6% of tiles changed in 2 s before any scroll | 376,832 (39%): 4.3–5.5; 424,960: 3.8–4.9; 478,464: 3.4–4.3 | 261,376 (27%): 6.1–7.9; 298,547: 5.4–6.9; 358,400: 4.5–5.8 | 0/60/0; 5/55/0 |
| The same, the first 9 steps, before a playing clip is in the window | The bar, and the drifting decorations | 215,808 (22%): 7.4–9.5; 291,379: 5.5–7.1; 331,520: 4.8–6.2 | 92,160 (10%): 17–22; 220,979: 7.2–9.3; 275,456: 5.8–7.5 | 0/9/0; 5/4/0 |
| Encyclopedia article | Nothing fixed until step 3, when the contents button detaches to float at the top left and the article re-lays out: the text moved 53 rows, not 48, and that one step costs 71% and 70% of the window ("What caused the costly steps"). Every other step is clean | 86,272 (9%): 18–23; 86,784: 18–23; 685,056: 2.4–3.0 | 79,104 (8%): 20–25; 79,616: 20–25; 671,232: 2.4–3.1 | 59/0/1; 59/0/1 |
| Documentation page | Two top bars and a left contents column with an advertisement stay put; together they cover about two-fifths of the window. An advertisement banner on the first screen scrolls away by step 2, which re-seats them once (29%) | 389,632 (41%): 4.1–5.3; 391,168: 4.1–5.3; 391,680: 4.1–5.3 | 78,336 (8%): 20–26; 78,336: 20–26; 280,832: 5.7–7.3 | 1/59/0; 59/1/0 |
| News front page | A top bar stays put and shrinks once, at step 2, where the scroll position moved 32 rows and the content 48. Photographs slide cleanly; advertisement slots were empty | 171,008 (18%): 9.3–12; 180,736: 8.8–11; 194,048: 8.2–11 | 78,080 (8%): 20–26; 78,848: 20–25; 142,848: 11–14 | 0/60/0; 59/1/0 |
| News article, same site | The same bar and the same step 2. At step 43 the lines under an empty advertisement slot moved by a different amount than the page | 171,008 (18%): 9.3–12; 184,832: 8.6–11; 234,496: 6.8–8.8 | 78,336 (8%): 20–26; 78,336: 20–26; 145,920: 11–14 | 0/60/0; 58/2/0 |
| Forum thread | A top bar stays put (its text changes once, at step 5) and a small page counter floats at the bottom right | 184,320 (19%): 8.6–11; 186,368: 8.6–11; 186,880: 8.5–11 | 82,688 (9%): 19–24; 87,654: 18–23; 126,976: 12–16 | 0/60/0; 59/1/0 |
| Question-and-answer page | A top bar and a left menu column stay put; step 1 re-seats the menu as a notice scrolls away. No robot check and no cookie notice appeared | 275,968 (29%): 5.8–7.5; 275,968: 5.8–7.5; 278,016: 5.8–7.4 | 76,800 (8%): 20–26; 77,824: 20–26; 149,504: 11–14 | 0/60/0; 59/1/0 |
| Code-hosting project page | Nothing fixed for 41 steps; from step 42 the README's row of tabs sticks to the window top | 81,664 (9%): 19–25; 128,307: 12–16; 133,888: 12–15 | 78,336 (8%): 20–26; 78,336: 20–26; 125,696: 13–16 | 46/14/0; 59/1/0 |
| Search results | 25 steps to the page's end. From step 11 a follow-up box floats over the bottom left, with a soft edge the page shows through: 14 to 20% a step region-aware in steps 11 to 24. Wider than the window | 220,416 (23%): 7.2–9.3; 238,643: 6.7–8.6; 246,016: 6.5–8.4 | 158,208 (16%): 10–13; 175,923: 9.1–12; 188,416: 8.5–11 | 10/15/0; 11/14/0 |
| Shopping search listing | Nothing of the site's is fixed; product pictures slide cleanly. Wider than the window. 2.4% of tiles changed in 2 s before any scroll | 103,424 (11%): 15–20; 106,752: 15–19; 107,264: 15–19 | 91,136 (9%): 17–22; 97,997: 16–21; 102,912: 15–20 | 60/0/0; 60/0/0 |
| Amiga file archive, front page | Nothing fixed; a table of text slides cleanly | 82,176 (9%): 19–24; 82,176: 19–24; 82,176: 19–24 | 78,336 (8%): 20–26; 78,336: 20–26; 78,848: 20–25 | 60/0/0; 60/0/0 |
| Amiga news site, front page | Nothing fixed; 18 steps to the page's end | 83,200 (9%): 19–24; 84,224: 19–24; 84,224: 19–24 | 78,848 (8%): 20–25; 79,872: 20–25; 79,872: 20–25 | 18/0/0; 18/0/0 |
| Amiga community portal, front page | Nothing of the site's is fixed; its top banner picture did not load. Wider than the window | 107,264 (11%): 15–19; 107,264: 15–19; 107,776: 15–19 | 87,552 (9%): 18–23; 102,912: 15–20; 103,936: 15–19 | 60/0/0; 60/0/0 |

- On a page that plays by itself, which is Discord's landing page and the watch page while its video is in the window, the playing area is sent again at every frame, scrolled or not, so those rows' rates are upper limits.
- Four other sites refused the headless browser, with a robot check, an error page, a block notice and a bot filter's denial; nothing was done to get past them, and none is in any figure.
- Another search engine, another shopping site and two other Amiga sites were measured as sites of the same kinds; the fourth, a discussion site, has no stand-in.
- [G] A browser run for a real user is not headless and may be served where this one was refused.

## What caused the costly steps

Read from the frames and from maps of the pixel classes.

- Bars and columns fixed to the window cost under the whole-window slide only.
- Under both models: something see-through over moving content, at every step (YouTube search's top bar, the search page's follow-up box); video or animation in the window, redrawn whether or not the user scrolls (the watch page's player, Discord's clips); a one-off re-layout, for one step.
- The encyclopedia article's 70% is mostly the models' fixed 48-row slide and not a redraw: slid by the 53 rows the text moved, that step costs 186,112 bytes under the whole-window slide and 185,344 under the region-aware slide, 19% of the window under both.
- [G] That is 8.6 to 11 a second under either model (116.8 and 90.9 ms, and 116.3 and 90.5 ms).
- Not seen: a background fixed behind moving content; a late picture costing a partial step; a bar fixed to the window bottom; a cookie or sign-in wall.
- Discord's decorations were not told apart from parallax.

## Conditions

- One visit to each site, on one day, signed out, from a United States network, by headless Edge on Windows; not Discord's application and not a signed-in YouTube.
- The news site's advertisement slots were empty and the documentation page's filled.
- Visits differ: the watch page's video started by itself here and in the captures of `topics/page-pixels.md`, and not in a trial run minutes earlier.
- Both models charge the whole bottom strip at every step; a sender that compares tiles would skip the strip tiles already right on the screen: 0.1% (Discord) to 5.0% (the community portal) of the window at a site's median step, and 2.9% over all steps.
- The strip tiles that never change in a whole run, such as a fixed column's foot or a blank margin, are 0 to 2% of the window.
- Under a bar fixed across the window bottom the rows really exposed lie above the bar and are charged as well: on a local test page with such a bar the models count 153,600 bytes where 76,800 are needed (region-aware) and 204,800 where 128,000 are (whole-window), if the move leaves the strip's old pixels in place.
- The tile grid starts at the bottom edge, the one anchor under which the strip is exactly three rows of tiles; started at the top, the plain strip is 89,600 bytes.
- [G] That is 17 to 22 a second in place of 20 to 26.
- Taken step by step, that difference has a median by site of 0.9 to 1.9% of the window more under the region-aware slide, and from 0.9% less (the documentation page) to 3.6% more under the whole-window slide.
- The browser's own scrollbars are in the frames: the vertical one costs at most 7,424 bytes a step, 0.8% of the window.
- On pages wider than the window a horizontal scrollbar, 15 rows high, is fixed to the window bottom: the shopping listing and the community portal cost 9 to 11% of the window a step where the file archive and the Amiga news site cost 8 to 9%.
- The scroll was a script's instant 48-row jump, left to come to rest.
- [G] Smooth scrolling gives more frames for every 48 rows, and under the whole-window slide what is fixed is sent again at each.
- A step is the difference between two rested frames, and frames in between are not counted.
- The first frame, 0.3 s after the step, differed from the rested one in 74 steps (Discord 60, YouTube watch 9, others 5), and 65 steps never came to rest within 4 s (Discord 58, YouTube watch 7).
- A self-animating area is in a step once and is sent at every frame.
- Pixels are compared as 16-bit values, exactly: any difference counts as changed, however faint, and one that vanishes in 16 bits does not count.
- Compared as 24-bit, the search page's median step is 38% whole-window and 19% region-aware (23 and 16% here), YouTube search's 20 and 15% (19 and 12%), the other 14 sites' within one point, and 740 region-aware steps are clean, not 787.
- Text is drawn with the capturing PC's Windows fonts and subpixel antialiasing, as desktop Edge draws it.
- [G] A Linux computer would draw other glyphs.

## Not established

- What a signed-in page resends, Discord's application and a signed-in YouTube among them: the same method on signed-in visits would settle it.
- A wheel, a dragged scrollbar, a page key, smooth scrolling, and pages that take over the wheel: the same method with those inputs would settle each.
- Window sizes other than 800×600, and steps other than 48 rows: the same method at those sizes would settle each.
- What a self-animating area costs between rested frames: every frame of a run, kept and compared, would show it.
- What a page with a bar fixed to the window bottom, a cookie or sign-in wall, or a background fixed behind moving content resends: none was served on these visits.
- What a real sending program finds and sends: neither model was run as a program; a sender run on such frames would show it.
- What the four sites that refused would resend.
- The updates a second with the bytes compressed: not derived here; the ratios are in `topics/page-pixels.md`.
- The rates on a machine: every figure is derived, and its inputs' own open points are in `topics/target-config-rates.md` and `topics/bus-and-card-rates.md`, "Not established".

## Sources

No outside source is cited: the bytes are this project's measurement by the method above, and the rates come from the two pages named under "Updates a second at 50 MHz", which carry their own sources.
