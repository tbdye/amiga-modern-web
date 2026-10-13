# Native engine speed

Scope: evidence on how fast a script engine built for the Amiga side would run, on a 68k or on the ZZ9000's ARM: the script engines one could build on, an interpreter against a JIT, the card's ARM against other ARM hardware and against 68k CPUs, and an estimate for one card core.
Status: current

No figure on this page was measured for it, on the card or on a 68k; each estimate is `[G]` and shows its arithmetic.
A source ID that `sources.md` does not define is in "Sources" below; every web page there was read on 2026-10-11.
The native Amiga browsers, and what each supports: `topics/prior-art.md`, "Native Amiga browsers".
The call path to the card's ARM: `topics/arm-offload.md`; what hosting an engine there would take, the layout engines one could build on and what bounds a small engine by class of site: `topics/arm-hosted-engine.md`.

## Script engines one could build on

Relative speed is the geometric mean of eight V8-suite tests on one machine, an Apple M4 in a Linux VM, with QuickJS as 1.00; it is [G], computed from the scores `js-zoo` publishes, each engine at the revision benchmarked there.
MuJS has no RegExp score and JerryScript no Splay score, so their figures are over seven tests, against QuickJS on the same seven.
A licence, language level, implementation language, line count, JIT back end or "built for" statement with no other citation is `js-zoo`'s.
"None found" is scoped under "Not established".

| Engine | Licence | Language level | Relative speed | Runtime needs | 68k AmigaOS | Bare-metal ARMv7 [G] |
|---|---|---|---|---|---|---|
| QuickJS | [F] MIT | [F] ES2025 (`quickjs-web`) | 1.00 at its revision of 2025-12-22; [F] its release of 2026-06-04 is "42% faster" on that suite (`quickjs-web`) | [F] The C library only (`stdlib`, `stdio`, `string`, `math`, `fenv`, `sys/time`, `malloc`), with `pthread` only for `Atomics`, no `mmap`, no JIT, and no match for "wasm" or "WebAssembly" in the engine source; NaN-boxed values on 32-bit, and big-endian paths (`quickjs@9d01a96:quickjs.c:L25-40, L69-73, L116-118, L37871`; `quickjs.h:L56-65`) | None found | Plausible on a newlib-class C library |
| QuickJS-ng | [F] MIT | [F] ES2023 | 0.87 | [G] As QuickJS | None found | As QuickJS |
| MicroQuickJS | [F] MIT | [F] "a subset of JavaScript close to ES5", in a stricter mode with no `with` and no array holes (`mquickjs@6d4d7eb:README.md:L12-14, L69-84`) | Not benchmarked | [F] As little as 10 kB of RAM and about 100 kB of ROM (`mquickjs@6d4d7eb:README.md:L6-9`) | None found | [F] Built for embedded systems; [G] too restricted for web script |
| Duktape | [F] MIT | [F] ES5 and ES5.1, with part of ES2015 and ES2016 (`duktape-web`) | 0.63 | [F] "Minimal, retargetable platform dependencies"; 148 kB of code and 78 kB of RAM for a hello-world on Thumb (`duktape-web`) | [F] Supported: its configuration has a platform for AmigaOS on m68k (`duktape@3afa016:config/platforms/platform_amigaos.h.in:L1-7`) | Plausible |
| JerryScript | [F] Apache-2.0 | [F] ES5.1 in full, ES2025 at 70% (`jerryscript@b706935:README.md:L11-12`) | 0.28 over seven tests | [F] C99; runs in less than 64 KB of RAM (`jerryscript@b706935:README.md:L8, L16`) | None found | [F] Built for microcontrollers (same lines) |
| MuJS | [F] ISC (`mujs-web`) | [F] ES5 | 0.36 over seven tests | [F] Portable C (`mujs-web`) | None found | Plausible |
| XS | [F] Apache and LGPL | [F] ESnext | 0.29 | [F] An interface file and an implementation file per platform, over the C standard library (`moddable@5f215f7:documentation/xs/XS Platforms.md:L7, L37`) | None found | [F] Listed as an engine for microcontrollers |
| Hermes; Escargot | [F] MIT; LGPL-2.1 | [F] ES2023; ESnext | 1.38; 1.32 | [F] C++, 170,000 and 116,000 lines; operating-system needs not examined | None found | Not examined |
| V8; JavaScriptCore, JIT off | [F] BSD-3; LGPL-2.0 | [F] ESnext | 2.05; 1.40 | [F] 1.3 million and 0.77 million lines of C++; [G] they need an operating system (threads, virtual memory) | [G] No | No |
| V8; JavaScriptCore, JIT on | As above | As above | 38.6; 40.0 | [F] JIT back ends that include 32-bit ARM; [G] they need an operating system and executable-memory management | [G] No | No |

- [F] In `js-zoo` the only engine under 100,000 lines with a 32-bit ARM JIT is Qt's QV4, at 50,000 lines.
- [G] It depends on Qt.
- [G] The C engines (QuickJS, Duktape, MuJS, JerryScript, XS) fit the firmware's C-only newlib build as it stands; Hermes, Escargot and every JIT engine are C++, and would add a C++ toolchain and runtime to it (`topics/arm-offload.md`, "ARM-side capacity").

## Interpreter against JIT

- [G] On the eight-test mean, V8 and JavaScriptCore with their JIT score about 39 to 45 times QuickJS (38.6 and 40.0 on the M4; 45.2 and 43.4 on the data's second machine, an Intel i9), and with the JIT off 1.4 to 2.5 times (computed from `js-zoo`).
- [F] On web-application workloads the gap is smaller: V8 with its JIT off is "around 40% slower" on Speedometer 2.0, 80% slower on the Web Tooling Benchmark and 6% slower in script execution over a session of YouTube's living-room application, measured on an x64 Linux desktop (`v8-jitless`).
- [G] On Speedometer-like work an interpreter of QuickJS's class is 1.7 to 4.2 times slower than a JIT engine: 1 ÷ 0.6 = 1.67 for V8's own interpreter, times the ratio of V8 with its JIT off to QuickJS (2.05 to 2.50; 2.05 ÷ 1.42 = 1.44 if the "42% faster" release is taken) on whatever share of the benchmark's time is script.
- [G] That share is unknown: the factor is 1.67 if none of the time is script, and 2.4 to 4.2 if all of it is.
- [G] Neither input was measured on a Cortex-A9: one is Speedometer on an x64 desktop, the other a compute suite on an Apple M4 and an i9.
- [G] On compute-bound script (challenge pages, parsers, codecs) the gap is 27 to 45: 38.6 to 45.2, or 38.6 ÷ 1.42 = 27 with the "42% faster" release.
- [G] A SpiderMonkey 1.5 interpreter of 2004 scores 0.36 of QuickJS in the same data (computed from `js-zoo`).
- [F] V8 with its JIT off did not support WebAssembly when that mode was published, in 2019 (`v8-jitless`).

## The card's ARM against other ARM hardware

| Platform | Dhrystone 2.1, VAX MIPS | MIPS per MHz | Linpack double precision, MFLOPS | Source |
|---|---|---|---|---|
| Cortex-A9 at 800 MHz, Android build | 962 | 1.20 | | [F] `bench-rpi` |
| A Cortex-A9 tablet, Android, original build | 1,610 | 1.34 at 1,200 MHz; 1.24 at 1,300 MHz | 151 | [F] `bench-android` gives 1,200 MHz; `bench-rpi` lists the same score at 1,300 MHz |
| The same tablet, a later 32-bit build | 1,317 | 1.10 | 159 | [F] `bench-android` |
| Raspberry Pi 1 (ARM1176) at 700 MHz, Raspbian gcc | 847 | 1.21 | 35.7-37.3 (Pi A, B, A+, B+) | [F] `bench-rpi`; `magpi-pi4-bench` |
| The same core at 1 GHz | 1,226 | 1.23 | 40.4 (Pi Zero) | [F] `bench-rpi`; `magpi-pi4-bench` |
| Raspberry Pi 2 (four Cortex-A7) at 900 MHz, Raspbian gcc; gcc 4.8 | 1,538; 1,667 | 1.71; 1.85 | 145.7 | [F] `bench-rpi`; `magpi-pi4-bench` |
| Raspberry Pi 4 (four Cortex-A72) | | | 748.7 | [F] `magpi-pi4-bench` |
| Vendor figures | | ARM11 1.25; Cortex-A7 1.9; Cortex-A9 2.5 | | [R] `wiki-ips`, a table that cites third parties, which ARM's own documents would verify; the Cortex-A9 figure is also [F] `ds190` p1 |
| The card's core at 667 MHz, as one report from the card gives it | About 1,059 | 1.59 | | [F] `topics/arm-hosted-engine.md`, "A firmware line that loads ARM programs (XACP)": another firmware line, compiler not stated |
| The card's core at 667 MHz, scaled from the three Cortex-A9 rows | 730-895 | 1.10-1.34 | 77-88 | [G] each row's figure per MHz × 666.67; 675 if the 1,317 build ran at 1,300 MHz |
| The same, on the vendor figure | 1,667 | 2.5 | | [G] 2.5 × 666.67 |

- [F] The Cortex-A9 rows are Android builds and the Pi rows Raspbian gcc; their source notes that MIPS per MHz depends on compiler optimisation, and one tablet scores 1,610 or 1,317 by build alone (`bench-android`).
- [G] The Pi rows sit at the vendor figures (ARM11 1.21-1.23 against 1.25; Cortex-A7 1.71-1.85 against 1.9) and the Cortex-A9 rows at about half of theirs (1.10-1.34 against 2.5), so the two anchors for the card differ by about 2.
- [G] The one figure reported from the card falls between them, at 1.59 per MHz; it is a third party's approximate figure on another firmware line and compiler, and nothing measures the build of `fw`.
- [G] Per core the card's A9 is 0.44 to 1.08 of a Pi 2 core (730 ÷ 1,667 to 1,667 ÷ 1,538) and 0.86 to 1.97 of a Pi 1 (730 ÷ 847 to 1,667 ÷ 847); on the scaled rows it is about twice a Pi 1 on floating point (77-88 against 36-37).
- [G] On the reported figure it is 0.64 to 0.69 of a Pi 2 core (1,059 ÷ 1,667 to 1,059 ÷ 1,538) and 1.25 of a Pi 1.
- [G] It has two cores to the Pi 2's four: 0.22 to 0.54 of a Pi 2 in aggregate, and 0.32 to 0.34 on the reported figure.

## Browsers with a JIT on Cortex-A9 devices

Speedometer by Raspberry Pi board is in `topics/prior-art.md`, "App SoC plus FPGA"; the figures used below are that page's.

- [G] Dhrystone does not predict that scale: a Pi 2 over a Pi Zero is 4.0 on Speedometer 2.0 (4.138 ÷ 1.04) and 1.25 to 1.36 on Dhrystone; a Pi 2 over a Pi B+ is 6.6 (4.138 ÷ 0.623) and 1.8 to 2.0.

For named Cortex-A9 devices only SunSpider and Octane results were found.
Each CPU is as its source states it; no source names the SunSpider version.

| Device and CPU | Test, date published | Result | Source |
|---|---|---|---|
| Google Nexus 7 of 2012: "quad-core 1.3 GHz Cortex-A9", Tegra 3 | SunSpider, 2012-08-15 | 1,703 ms | [F] `gsmarena`, Nexus 7 review p4 |
| The same device, "1.2–1.3 GHz Tegra 3" | Octane v1, 2013-07-27 | 1,678 | [F] `anandtech-nexus7`, read from the chart image |
| Samsung Galaxy S III: "4x Cortex-A9 @ 1.4GHz" | SunSpider, 2012-05-20; 2012-12-21, in the device's stock browser | 1,447 ms; 1,192 ms | [F] `gsmarena`, Galaxy S III review p5; Nexus 4 comparison p5 |
| HTC One X (Tegra 3): "4x Cortex-A9 @ 1.5GHz" | SunSpider, 2012-05-20 | 1,757 ms | [F] `gsmarena`, Galaxy S III review p5 |
| Huawei Ascend P7: "Quad-core 1.8 GHz Cortex-A9" | SunSpider, 2014-05-07 | 1,307 ms | [F] `gsmarena`, Ascend P7 review p1, p5 |
| Huawei Ascend P6: "quad-core 1.5GHz Cortex-A9" | SunSpider, in the same 2014 table | 3,858 ms | [F] `gsmarena`, Ascend P7 review p5; CPU from the Ascend P6 review p1 |
| For comparison, Motorola Moto G: "quad-core 1.2GHz Cortex-A7" | SunSpider, in the same 2014 table | 1,308 ms | [F] `gsmarena`, Ascend P7 review p5; CPU from the Moto G review p1 |
| For comparison, Raspberry Pi 2; Pi B+ | SunSpider, 2015-02-05 | 4,452.1 ms; 23,692.7 ms | [R] `rpi-pi2-bench`: a third party's post quoted there, browser not named; a run with a named browser would verify |

- [F] SunSpider "mostly reflects the raw performance of a single core and how optimized the JavaScript engine itself is" (`gsmarena`, Galaxy S III review p5).
- [G] In one table a Cortex-A9 at 1.8 GHz ties a Cortex-A7 at 1.2 GHz (1,307 and 1,308 ms): 0.67 of the A7 per MHz, which by clock alone puts the card's core at 0.67 × 667 ÷ 900 = 0.49 of a Pi 2 core.
- [G] On the Octane chart the Nexus 7 leads a tablet at 1,285 by 1.21 per MHz, 0.89 of a Pi 2 core, or 0.97 with the Nexus 7 at 1.2 GHz; that tablet's CPU, [R] a Cortex-A7 at 1.2 GHz, is not on the chart, and its maker's specification would verify it.
- [G] Across sources, the four 2012 results scaled by clock to 667 MHz are 2,500 to 3,950 ms, 1.1 to 1.8 times faster than the Pi 2 figure and 6.0 to 9.5 times faster than the Pi B+ figure; browsers and years differ, the Pi figures are [R], and clock scaling is assumed linear.
- [G] Two Cortex-A9 phones in one table differ by 2.5 per MHz (3,858 ms at 1.5 GHz; 1,307 ms at 1.8 GHz): the browser build moves a result by more than the Dhrystone bracket above is wide.
- [G] None of this narrows the estimate below: the pairings (0.49, 0.89, 1.1 to 1.8) straddle the Dhrystone bracket of 0.44 to 1.08 and favour neither anchor.
- [G] The cross-source pairing shows only that a first-generation Pi is slower in a browser than its Dhrystone score predicts (6.0 to 9.5 against 0.86 to 1.97), so the lower end of the estimate's first link is more likely low than high.

## Estimate for one card core running an interpreter

Nothing in it is measured on the card.

| Link | Value | Not held constant |
|---|---|---|
| 1. Chromium on a Pi, Speedometer 2.0 | 0.60 (Pi B) to 4.14 (Pi 2) (`topics/prior-art.md`, "App SoC plus FPGA") | Four cores on the Pi 2, one ARMv6 core on the Pi B; memory speed and capacity, on which its source says the test also hinges (`magpi-pi4-bench`) |
| 2. The card's core in place of that board | × 1 against the Pi B (0.86 to 1.06 of it on the scaled Dhrystone rows); × 1.08 against a Pi 2 core (vendor figure) | Dhrystone does not predict Speedometer; the engine gets one core, run to completion and shared with TLS, image, audio and video work (`topics/arm-offload.md`, "Which core runs what"), where the Pi 2 had four; counted here as costing nothing |
| 3. An interpreter in place of the JIT | ÷ 1.67 to ÷ 4.2 ("Interpreter against JIT") | The CPU (x64 and M4, not a Cortex-A9); the workload (a compute suite, not a browser benchmark); the script share |
| 4. A document model and layout engine as efficient as Chromium's | × 1, assumed | No such engine exists for this target (`topics/arm-hosted-engine.md`, "Layout engines small enough to consider") |
| 5. Memory | Not counted | One heap for both cores (`sections/firmware-and-rtl.md`, "PS DDR map and card pool"); on the Pi boards the test "proved too much for Raspberry Pi A+" (`magpi-pi4-bench`) |

- [G] Low end: 0.60 ÷ 4.2 = 0.14; high end: 4.14 × 1.08 ÷ 1.67 = 2.7; with the figure reported from the card in link 2 (0.69 of a Pi 2 core), 4.14 × 0.69 ÷ 1.67 = 1.7.
- [G] So a Speedometer 2.0 equivalent of the order of 0.1 to 3 runs a minute: a band about twenty-fold wide whose ends are themselves guesses.
- [G] The upper end is a ceiling, not an expectation: it gives one shared core the score of a four-core board, and gives QuickJS the speed of V8's own interpreter.
- [G] The lower end is more likely low than high: its anchor is one ARMv6 core on a board where memory also limits the test.
- [G] Link 4 has no established direction: a small engine does less work per page than Chromium and is less optimised for the work it does.
- [G] Link 5 limits which pages load at all, not how fast they run.
- [F] The card cannot run the Chromium that links 1 and 2 imagine: its firmware is bare metal (`sections/architecture.md`, "What each side runs").
- [G] Against the Pi 4 class that `sections/overview.md`, "Problem and goal", gives as about the floor for current Chromium (16.9 on Speedometer 2.0 in the figures pointed to above), the estimate is 6 to 120 times lower (16.9 ÷ 2.7 to 16.9 ÷ 0.14).

## 68k CPUs

Every 68k figure in the table is [R] from an encyclopedia page, and so is each one marked [R] in the lines under it; a Motorola document would verify them, and none was retrieved.
The ratios are [G]: the card's core, as scaled above, over the 68k figure.

| 68k | Figure [R] | Unit as the source gives it | Card core, scaled rows (730-895) | Card core, vendor figure (1,667) |
|---|---|---|---|---|
| 68030 at 50 MHz | 18 MIPS | Unstated (`wiki-ips`) | 41-50 | 93 |
| 68040 at 40 MHz | 44 MIPS | Unstated (`wiki-ips`) | 17-20 | 38 |
| 68060 at 50 MHz | 67 MIPS | Unstated, uncited there (`wiki-68060`) | 11-13 | 25 |
| 68060 at 50 MHz in Amiga accelerator cards | "around 80,000 Dhrystones per second"; 80,000 ÷ 1,757 = 45.5 VAX MIPS [G] | Dhrystone 2.1 (`wiki-68060`, citing a magazine review) | 16-20 | 37 |

- [G] The ratio for interpreter code is unmeasured.
- [G] For compiled Dhrystone 2.1 the one report from a machine with this card gives about 20 (about 1,059 against about 52 on a 68060 at 50 MHz: `topics/arm-hosted-engine.md`, "A firmware line that loads ARM programs (XACP)"), which agrees with the table's last row.
- [G] The 18, 44 and 67 figures are of unstated unit, compiler and system and are not comparable with it; [R] the same page quotes a Motorola projection of "about 77 MIPS" for the 68060 at 50 MHz (`wiki-68060`).
- [G] Dhrystone says little about an interpreter with a heap of megabytes: [R] the 68060 has 8 KB instruction and 8 KB data caches (`wiki-68060`), against the A9's 32 KB each and 512 KB L2 (`topics/arm-offload.md`, "ARM-side capacity").
- A 68k emulated on a Raspberry Pi: `topics/prior-art.md`, "Fast-68k routes".

## Not established

Each point names what would settle it; none is a condition of anything.

- The speed of any script engine on the card's ARM, on a 68k, or the ratio between them: no published benchmark of a script engine on a real or emulated 68k was found, and none of a small interpreter on a Cortex-A9; only a measurement on both shows the ratio.
- Whether an engine in the table other than Duktape has a 68k AmigaOS port: on 2026-10-11 searches of Aminet for `quickjs` and `duktape`, and of GitHub repositories for QuickJS on the Amiga, on m68k and on MorphOS and for a JavaScript engine on 68k AmigaOS, found none; the other engines were not searched for by name, and this shows absence in those searches only.
- A result for a browser with a JIT on a Cortex-A9 under Speedometer, JetStream or Kraken, and any browser benchmark on a Zynq-7000 board: none was found in the review sites fetched on 2026-10-11.
- A primary figure for any 68k CPU, and any benchmark figure for a 68k emulated on ARM by Emu68 or implemented as the Apollo 68080: none was retrieved; what the Emu68 project itself states of its speed is in `topics/audience-pistorm.md`, "The two software stacks".
- The share of Speedometer's time that is script, and so where in 1.67 to 4.2 the third link lies.

## Sources

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `js-zoo` | JavaScript engines zoo: per-engine metadata and V8-suite scores on two machines ("arm64: Mac M4 4.5GHz - Linux VM"; "amd64: i9-10900K 3.7-5.3GHz - Linux") | `https://zoo.js.org/engines.json`; `github.com/ivankra/javascript-zoo` | `a17d4e0`; data read 2026-10-11, SHA-256 `f65f9f687f4940aae9db460b48981e380fc55c6da170424bba368a14d097dc6c` |
| `quickjs`, `quickjs-web` | QuickJS source; its home page | `github.com/bellard/quickjs`; `https://bellard.org/quickjs/` | `9d01a96`; 2026-10-11 |
| `mquickjs` | MicroQuickJS | `github.com/bellard/mquickjs` | `6d4d7eb` |
| `duktape`, `duktape-web` | Duktape source; its home page | `github.com/svaarala/duktape`; `https://duktape.org/` | `3afa016`; 2026-10-11 |
| `jerryscript` | JerryScript | `github.com/jerryscript-project/jerryscript` | `b706935` |
| `mujs-web` | MuJS home page | `https://mujs.com/` | 2026-10-11 |
| `moddable` | Moddable SDK, which holds the XS engine | `github.com/Moddable-OpenSource/moddable` | `5f215f7` |
| `v8-jitless` | V8 blog, "JIT-less V8" (2019-03-13) | `https://v8.dev/blog/jitless` | 2026-10-11 |
| `bench-android`, `bench-rpi` | Android benchmarks and Raspberry Pi benchmarks pages: Dhrystone 2.1 and Linpack results by device and build | `http://www.roylongbottom.org.uk/android%20benchmarks.htm`; `http://www.roylongbottom.org.uk/Raspberry%20Pi%20Benchmarks.htm` | 2026-10-11; served over HTTP only |
| `magpi-pi4-bench` | The MagPi, Raspberry Pi 4 specifications and benchmarks: Linpack chart (its legend prints MIPS for MFLOPS) and the Speedometer note | `https://magpi.raspberrypi.com/articles/raspberry-pi-4-specs-benchmarks` | 2026-10-11; figures read from the chart image |
| `wiki-ips`, `wiki-68060` | Wikipedia, "Instructions per second" (table of Dhrystone MIPS by processor); "Motorola 68060" | `https://en.wikipedia.org/wiki/Instructions_per_second`; `https://en.wikipedia.org/wiki/Motorola_68060` | 2026-10-11 |
| `gsmarena` | GSMArena reviews, by address: `asus_google_nexus_7-review-797`, `samsung_i9300_galaxy_s_iii-review-761`, `google_nexus_4_vs_samsung_galaxy_s_iii-review-864`, `huawei_ascend_p7-review-1074`, `huawei_ascend_p6-review-967`, `motorola_moto_g-review-1021` | `https://www.gsmarena.com/<review>p<page>.php` | 2026-10-11 |
| `anandtech-nexus7` | AnandTech, "Nexus 7 (2013) - Mini Review", page 4, and its Octane v1 chart | `https://web.archive.org/web/20141227121351/http://www.anandtech.com/show/7176/nexus-7-2013-mini-review/4` | 2026-10-11; an archived copy |
| `rpi-pi2-bench` | Raspberry Pi news, "Benchmarking Raspberry Pi 2" (2015-02-05) | `https://www.raspberrypi.com/news/benchmarking-raspberry-pi-2/` | 2026-10-11 |
