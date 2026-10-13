# A browser engine on the card's ARM

Scope: what hosting a browser engine, or any large program, on the ZZ9000's ARM cores would take: what such a program needs that the firmware lacks, the cost of three ways to split an engine between the ARM and the 68k, what the TLS offload's shape would ask of an engine, what a third-party firmware line that loads whole ARM programs (XACP) shows, the layout engines one could build on, and what bounds a small engine by class of site.
Status: current

A citation with no source ID is `fw@cfbb910`; `os/` expands per `sources.md`.
The card's ARM services as built, with the call path and the per-call cost used here: `topics/arm-offload.md`.
How fast a script engine would run on these cores: `topics/native-engine-speed.md`.
No engine was built or run for this page: its costs are `[G]` with their arithmetic, and a measured figure is its source's own.

## What a large program would need that the firmware lacks

For a large third-party C library linked into `fw` ([G] unless marked; the facts behind each item: `topics/arm-offload.md`, "Mechanisms in the firmware", "Which core runs what", "ARM-side capacity"):

1. A way in: a handler linked into the firmware and an opcode range, since `fw` loads nothing at run time.
2. Bounded execution: an interrupt hook that the library polls, or scheduler time slices; [F] the only stop for a runaway task is a cold restart of core 1 (`os/core2.c:L182-246`).
3. A yield and resume path, or a second stack, if the library must wait for the 68k in mid-run: the worker has one stack and runs each task to completion.
4. Its own arena with a hard limit, reclaimable as a pool owner; [F] a new pool class or a raised limit is a firmware change (`os/card_pool.h:L29-43`).
5. An ARM-to-68k call path.
6. For an engine with a JIT or a C++ runtime: exceptions and unwind tables, threads, virtual memory and signals, none of which the build or the runtime provides; [F] the board support package does have instruction-cache invalidation for generated code (`ZZ9000_proto.sdk/zz9000_bsp_new/ps7_cortexa9_0/include/xil_cache.h:L109`).
7. File, time and network services: a handler gets only what it is passed in shared buffers.

## Splitting an engine across the bus

The inputs are from `topics/arm-offload.md`, "Per-call cost", on Zorro III with a 68060: 0.28 ms for the measured ping, 89 µs pipelined, 52-66 µs of bus time [G].
Unmeasured inputs: the 68k's write rate into a shared buffer on `fw`, and `k`, the ARM-to-68k speed ratio for interpreter code.

- [F] The SDK's own comparison has the same form: native cost against mailbox, transfer and ARM cost, with native winning when mailbox overhead dominates (`sdk/docs/zz9k-68k-offload.md:L50-61`; `sdk/tools/zz9k-m68k-offload-model.h:L30-68`).
- [G] The in-repository ARM-to-68060 ratios, mailbox included, are 53 for ChaCha20-Poly1305 at 16 KB (8,550 ÷ 162 KiB/s) and about 210 to 1,200 for the handshake operations (RSA-2048 verify 1,379 ÷ 6.51 ms; ECDSA-P256 verify 19,123 ÷ 15.90 ms) (`sdk/docs/zz9k-crypto-acceleration.md:L88-94, L128-140, L170-174`).
- [F] They compare a portable, correctness-first reference on the 68k with BearSSL on the ARM, and the 68060 lacks 64-bit multiply and divide in hardware (`sdk/docs/zz9k-crypto-acceleration.md:L168, L183-185, L255-257`).
- [G] So they do not transfer to an interpreter.

### Script engine on the ARM, document model on the 68k

- [G] Each DOM access is a call from the ARM to the 68k, which does not exist (`topics/arm-offload.md`, "Call path").
- [G] Built from what exists, each access is: the ARM task ends with a completion that asks for a host call, the 68k performs it and submits the answer; the calls depend on each other, so they cannot be pipelined.
- [G] On the existing mailbox the cost is N times the per-call time; the table gives two points on that path, and neither column is a bound.

| DOM accesses N | At the measured ping, 0.28 ms | At the bus time of the existing entry, 66 µs |
|---|---|---|
| 10³ | 0.28 s | 0.07 s |
| 10⁴ | 2.8 s | 0.66 s |
| 10⁵ | 28 s | 6.6 s |
| 10⁶ | 280 s | 66 s |

- [G] The first column is not a best case: it is the armed, inline ping, and an engine call takes the core-1 route (0.39 ms for the smallest one measured) under the conditions that page lists.
- [G] The second column is not a floor: 66 µs is the bus time of the existing 64-byte entry, read byte by byte, at the top of its range and on a guessed cycle cost.
- [G] No floor for a purpose-built channel is established: a shared-memory slot needs a handful of bus cycles per access, which would put 10⁵ accesses well under 1 s of bus time, and what the rest of such a round trip costs is unmeasured.
- [G] At 0.28 ms a call, a script segment gains only when `t_68k × (1 − 1/k) > 0.28 ms`: more than about 0.28 ms of 68060 interpreter time per DOM access, for large `k`; the threshold moves with the per-access cost of the channel.
- [G] Code that touches the DOM often falls below that threshold and runs slower offloaded over the existing mailbox.
- [G] The run-to-completion worker either re-enters the engine on each access, which needs a yield and resume path, or spins on shared memory and blocks every other core-1 service.

### Script engine and document model on the ARM, layout and paint on the 68k

- [G] Each script turn costs one call plus the bytes the 68k must read, at least 0.28 ms + B ÷ 7.0 MB/s: 14.6 ms for 100 KB of changed tree and 143 ms for 1 MB (the read ceiling: `topics/bus-and-card-rates.md`, "Bus ceilings").
- [G] The shared heap is 3.94 MiB in at most 32 buffers (`topics/decode-rates.md`, "What the card's ARM decodes today"), so the model would live in ARM-only memory and the 68k would get serialised snapshots or deltas, unless the shared region is enlarged.
- [G] A script read that depends on layout (`offsetWidth`, `getComputedStyle`, `getBoundingClientRect`) forces an ARM-to-68k round trip and a 68k layout pass: the missing call of the first split, less often.
- [G] Layout, style and paint stay at 68k speed, so the gain is capped at 1 ÷ (1 − f), f being the share of page time spent in script and DOM.

### Whole engine on the ARM

- [F] Pixels need not cross the bus: ARM-side jobs draw into SDK surfaces and the RTG framebuffer (`sections/firmware-and-rtl.md`, "What the card offers today").
- [G] What crosses is input events (48 bytes inline, at most 3,342 a second synchronously), window geometry and clip lists, and page bytes.
- [G] Page bytes arrive through the Amiga's TCP/IP stack and its TLS library, then cross once more into a shared buffer; the receive rate that caps them, measured without TLS: `topics/target-config-rates.md`, "Network receive".
- [G] A card-side network path would avoid that crossing, but needs a TCP/IP and TLS stack on the ARM and a receive classifier on the port the Amiga already owns (`topics/network.md`, "The control link and the network").
- [G] No measured bus figure rules this split out on Zorro III, and none shows that the bus leaves it unbounded; the needs listed at the head of this page apply whatever the bus allows.
- [F] On Zorro II the aperture is 2 or 4 MiB (`sdk/docs/zz9k-zorro2-services.md:L25-28`), the host heap is 16 KiB and the rings hold 22 entries (`topics/arm-offload.md`, "How data moves", "Call path"), and offscreen bitmaps are disabled (`sections/firmware-and-rtl.md`, "What the card offers today").
- [G] Page bytes would stage through chunks of 8 KiB or less, as the archive tool's do (`sdk/docs/zz9k-zorro2-services.md:L51`); the rates are unmeasured.

## What the TLS offload's shape would ask of an engine

How that offload is built: `topics/arm-offload.md`, "How the TLS offload is built".
The same structure, applied to a browser engine ([G] unless marked):

1. A seam where the work is coarse and self-contained, with a complete 68k implementation behind it; a script engine is such a seam only if the browser exposes it as one.
2. The engine on both sides, 68k and ARM, with the same semantics and matched versions; the firmware carries the ARM half, so browser and firmware releases couple, as [F] the Zorro II components already must come from one release set (`sdk/docs/zz9k-zorro2-services.md:L10`).
3. A choice per page or session, not per call: a script heap cannot fall back to the 68k in mid-run the way one TLS record can.
4. Either the DOM beside the engine, or a DOM binding that crosses the bus at the costs above.
5. Source access or a published plug-in interface on the browser side, and a licence compatible with the firmware's (`sections/overview.md`, "Licences").
6. Recovery of state: the card drops sessions on an Amiga reset and on a core-1 fault (`topics/arm-offload.md`, "Which core runs what").

## A firmware line that loads ARM programs (XACP)

[F] XACP is a third-party ZZ9000 firmware with Amiga programs, read at `xacp@cca1f3c`.
In this section a citation with no source ID is at that commit, and `xos/` is `firmware/source/XX19c/ZZ9000_proto.sdk/ZZ9000OS/src/` there.
Every figure in this section is that repository's own readme figure, taken on the XACP firmware and given as approximate.
[F] The bench readme names an A4000 with a 68060 at 50 MHz, and the Quake readme an A4000 with a 68060 and no clock (`xacp@cca1f3c:applications/benchmarks/ZZBenchGUI_readme_v1.3.md:L108`; `applications/games/ZZQuakeHighRes/README.md:L20-21`).
[F] The repository holds no RTL or bitstream source (file listing at `cca1f3c`).

| Question | Finding | Citation (`xacp@cca1f3c`) |
|---|---|---|
| What it is | Firmware `XX19c`, protocol "XACP v1.7": the card's ARM as a coprocessor, with services on core 0 and whole programs on core 1 | [F] `README.md:L1-16, L36-45` |
| Relation to `fw` | Its firmware source carries the ZZ9000 firmware's file headers and has no `sdk_mailbox`, scheduler or card-pool file, so `zz9k.library` services and the TLS offload are absent there | [F] `xos/main.c:L1-15`; file listing of `xos/` |
| Licences | Firmware sources GPL-3.0-or-later; `sdk/` headers Zero-Clause BSD; the Doom port's own source GPL-2.0-or-later; no licence file at the repository root | [F] `xos/main.c:L10`; `sdk/LICENSE`; `applications/games/ZZDoom/README.md:L225-231`; root listing |
| Buses | Commands go to "a dedicated Zorro III register", and the command structure and the core-1 program sit 64 MB into the board window; none of its Markdown files mentions Zorro II; the firmware source keeps inherited Zorro II register paths | [F] `docs/XACP_V1_NOTICE.md:L11, L30-38`; `xos/main.c:L125, L525-528`; `ZZDoomCAMD.c:L74`; `git grep` over its Markdown files |
| How ARM code reaches core 1 | At run time, from the Amiga side: the 68k program carries a flat ARM binary linked at a fixed address, copies it into card DDR and writes that address to registers `0x90` and `0x92`; core 0 holds core 1 in reset, publishes the address and releases it; core 1 calls it as a function | [F] `ZZDoomCAMD.c:L74-78, L609-633`; `xos/main.c:L1450-1457`; `xos/core2.c:L84-131, L169-218` |
| 68k to ARM | Register commands that core 0 serves inside the Zorro register cycle: an opcode written to register `0x64`, arguments in a 52-byte big-endian structure in shared DDR; a core-1 program reads a table of words in shared DDR | [F] `docs/XACP_V1_NOTICE.md:L11-22, L33-38, L45-47`; `xos/main.c:L192-207, L769-776`; `ZZDoomCAMD.c:L83-100, L526-531` |
| ARM to 68k | Polling only: core 1 writes status words and a PCM ring to shared DDR, and the 68k reads them; the firmware raises Amiga interrupts for audio, Ethernet and vertical blank only | [F] `ZZDoomCAMD.c:L636-639, L680-688`; `git grep amiga_interrupt_set` over `xos/` |
| Files | The 68k uploads them into card DDR before launch (Doom: one WAD under 16 MB) and writes saves back from DDR | [F] `ZZDoomCAMD.c:L370-385, L845-850`; `applications/games/ZZDoom/README.md:L102` |
| Display | Pixels do not cross the bus: the 68k opens a P96 screen and passes the ARM address of its buffers in shared DDR, core 1 draws there, and the 68k asks for a page flip that the firmware applies at vertical blank | [F] `ZZDoomCAMD.c:L52-71, L481-531, L896-942` |

`ZZDoomCAMD.c` is `applications/games/ZZDoom/source/amiga/ZZDoomCAMD.c`.

- [G] The protocol and the programs read need Zorro III: a 24-bit Zorro II address cannot reach 64 MB into a board window.
- [G] A card runs this line or `fw`, not both.
- [F] The launcher is the one `fw` removed: the same register names sit at `0x90` and `0x92` in `fw` (`fw@cfbb910:os/zz_regs.h:L107-108`).

What it shows:

- [F] The repository ships whole engines for core 1 on bare metal, and its readmes report that they run there: Doom (a 381 KB program), Quake, and Dark Forces on The Force Engine (1.47 MB) (`applications/games/ZZDoom/README.md:L5, L17-21`; `applications/games/ZZQuakeHighRes/README.md:L6-8`; `applications/games/ZZDarkForcesNEXT/README.md:L5`; `applications/games/ZZDarkForcesNEXT/BUILDING_BLOB.md:L58-63`).
- [F] The last is C++14 with hosted libstdc++, built without exceptions or RTTI, with SDL threads stubbed out and the GPU, UI, audio and scripting units excluded; firmware v1.7 gives core 1 a 248 MiB ARM-only arena (`applications/games/ZZDarkForcesNEXT/build_next.py:L50-55, L62-68, L561-570`; the root `README.md:L49-55`).
- [F] Quake's software renderer on core 1, `timedemo demo1`: 41.9 fps at 640×480, 29.6 at 800×600 and 20.0 at 1024×768 (`applications/games/ZZQuakeHighRes/README.md:L14-21`).
- [F] Dhrystone 2.1: about 1,059 VAX MIPS on core 1 against about 52 on the 68060, about 20 times; Whetstone about 19 times; no compiler is stated (`applications/benchmarks/ZZBenchGUI_readme_v1.3.md:L83-91, L108-113`).
- [G] That is a ratio for compiled C, well under the crypto ratios above, and not an interpreter figure.
- [F] The same readme times a 68k longword loop over card DDR through Zorro III (its read and write rates: `topics/bus-and-card-rates.md`, "Bus ceilings") and a copy into DDR before a command: about 9 µs for 64 B, 107 µs for 1 KB and 7.9 ms for 64 KB (same file, `L152-163`).
- [G] Its write rate is the only one found for the 68k writing card DDR; it is on another firmware line and a bitstream with no published source, so it does not settle the rate on `fw`.
- [F] A register command with no work: about 3 µs a call, about 10 µs through a guarded wrapper (same file, `L130-150`).
- [G] It is served inside the 68k's bus cycle on core 0, so it carries only work short enough to hold that cycle; [F] the line's own rule is to acknowledge fast and continue elsewhere (`docs/XACP_V1_6_DEVELOPER_DOCUMENTATION.md:L502-525`).
- [G] `fw` answers register cycles on core 0 in the same way (`topics/arm-offload.md`, "Which core runs what"), so a channel of this kind would be a firmware change there, not new hardware.

What it does not show:

- [F] No ARM-to-68k call: the 68k polls.
- [F] No recovery beyond resetting core 1: the abort handlers loop forever, and its documentation says each combination of services and core-1 programs must be validated explicitly (`xos/core2.c:L233-256`; `xos/main.c:L971-979`; `docs/XACP_V1_6_DEVELOPER_DOCUMENTATION.md:L529-551`).
- [G] One program at a time on core 1, with no scheduler (one entry address and one run flag, `xos/core2.c:L78-79`); the core-1 services of `fw` do not exist on that line, so nothing is learned about an engine sharing core 1 with TLS, decode and audio.
- [F] No windowed or clipped drawing in the sources read: the Doom port owns a whole screen and flips pages.
- [F] No network use and no script engine: inputs are local files staged before launch, the software its own overview lists holds no network program, and the Dark Forces port excludes its engine's scripting units (`docs/WHY_XACP.md:L278-305`; `applications/games/ZZDarkForcesNEXT/build_next.py:L62-67`).
- [F] No 68030 or 68040 figure.
- [G] The programs are frame loops over preloaded data; a browser's page bytes, DOM and event traffic have no counterpart there, so the split costs above are not measured by it.

## Layout engines small enough to consider

| Engine | Licence | What it is | Limit |
|---|---|---|---|
| libcss, libdom, libhubbub | [F] MIT-style (`libcss@499f1c4:COPYING`; `libdom@f69781e:COPYING`; `libhubbub@6651b8c:COPYING`) | [F] C libraries: a CSS parser and selection engine, an implementation of the W3C DOM, and an HTML parser that aims to comply with HTML5 (`libcss@499f1c4:README.md:L1-8`; `libdom@f69781e:README:L1-7`; `libhubbub@6651b8c:README:L1-8`) | [G] They parse and select; layout and painting are in the browser that uses them (`topics/prior-art.md`, "Native Amiga browsers", "Display lists and small renderers") |
| litehtml | [F] BSD-3-Clause (`litehtml@4a651c5:README.md:L32`) | [F] An HTML rendering engine with CSS2 and CSS3 support that parses HTML with gumbo and draws nothing itself: the host draws (`litehtml@4a651c5:README.md:L3, L11`) | [F] "using it as a full-featured HTML engine is not recommended"; "not fully compatible with HTML/CSS standards" (`litehtml@4a651c5:README.md:L7, L19`); [G] no script binding |

- [G] Not examined: LibWeb, Servo, WebKit and Blink, all of which assume a hosted operating system and far more memory than a 68k Amiga has.

## What bounds a small engine, by class of site

A script engine, or a script engine and document model, on one core of the card's ARM; each verdict is [G].
The speed figures are from `topics/native-engine-speed.md`.

| Class of site | Verdict | Basis |
|---|---|---|
| Documents, forums, wikis, shops, light script | Not ruled out on speed; unmeasured | [G] Compiled code runs about 20 times faster on the card's core than on a 68060 (`topics/native-engine-speed.md`, "68k CPUs"), and the ratio for an interpreter is unmeasured; how much page time that removes depends on the script share and on a document model that moves with the engine ("Splitting an engine across the bus") |
| Script-heavy pages near the median | Slow; reach unmeasured | [F] The median desktop home page of 2025 ships 697 KB of JavaScript in 2.86 MB (`almanac-2025`, page weight); [G] speed between a quarter of a first-generation Pi running Chromium and two-thirds of a Pi 2 (0.14 to 2.7 against 0.60 and 4.14: `topics/native-engine-speed.md`, "Estimate for one card core running an interpreter") |
| Heavy single-page applications: mail, maps, office suites, a video site's own player | Out of reach | Features first: what the native browsers' engines support is in `topics/prior-art.md`, "Native Amiga browsers"; memory second: one heap for both cores (`sections/firmware-and-rtl.md`, "PS DDR map and card pool"); speed third: [G] one to two orders of magnitude below the Pi 4 figures (same estimate) |
| Challenge and fingerprint gates | Uncertain to out of reach | [F] Cloudflare's challenges give "limited support" to "custom or heavily modified browser engines and embedded browsers" (`cf-challenges`); [G] compute-bound script is where an interpreter loses most (`topics/native-engine-speed.md`, "Interpreter against JIT") |
| WebAssembly | Out of reach without an added interpreter | Neither V8 with its JIT off, as first published, nor QuickJS runs it (`topics/native-engine-speed.md`, "Script engines one could build on", "Interpreter against JIT"); [F] modules were found on 0.35% of desktop sites and 2% of the top 1,000 (`almanac-2025`, WebAssembly) |
| Video | Within the envelope of the firmware's decoders; no H.264 decoder | [F] The firmware's decoders are those in `sections/firmware-and-rtl.md`, "What the card offers today", their real-time envelope on this processor is in `topics/decode-rates.md`, "What the card's ARM decodes today", and a search of `os/` and `sdk/docs` for an H.264 decoder finds none (`fw@cfbb910`, `git grep -i h264`); [G] software H.264 on this core is unmeasured |
| Video under DRM | Out of reach | [R] It needs a vendor's decryption module, which exists only for mainstream platforms; the module vendors' platform lists would verify |
| WebGL, WebGPU | Out of reach | [D] DEC-008: Amiga-side 3D is not a goal; [G] the Zynq has no GPU (`sections/firmware-and-rtl.md`, "Why the Zynq cannot host the browser") |

- [G] Engine completeness, not CPU speed, bounds the first rows: a build on an engine of QuickJS's class still needs a document model and a layout engine, and the candidates above are three parsing libraries and an engine that its own readme does not recommend as a full HTML engine ("Layout engines small enough to consider").

## Not established

Each point names what would settle it; none is a condition of anything.

- `k`, the ARM-to-68k speed ratio for interpreter code: only a measurement on the card and on a 68k shows it; the one ratio found is for compiled C on another firmware line ("A firmware line that loads ARM programs (XACP)").
- DOM accesses per page, and the share of page time spent in script and DOM: an instrumented engine build on a PC would give them, with no Amiga hardware.
- What a purpose-built ARM-to-68k channel costs beyond its bus cycles: none exists to time.
- The page-byte ceiling to an application with TLS, on a 68030 or a 68060: no source reports one.
- Whether the two XACP readmes describe one machine, and whether the XACP firmware runs on a Zorro II board: its sources state neither.
- Software H.264 decode on this core: no figure was found; published decode rates for a Cortex-A9 are in `topics/decode-rates.md`.
- The open points of the call path itself: `topics/arm-offload.md`, "Not established"; those of engine speed: `topics/native-engine-speed.md`, "Not established".

## Sources

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `xacp` | XACP-ZZ9000, a third-party ZZ9000 firmware line with its Amiga programs and documents | `github.com/Xanxi-Amiga/XACP-ZZ9000` | `cca1f3c`; read as data, nothing built or run |
| `almanac-2025` | HTTP Archive Web Almanac 2025, page weight and WebAssembly chapters | `https://almanac.httparchive.org/en/2025/page-weight`; `https://almanac.httparchive.org/en/2025/webassembly` | 2026-10-11 |
| `cf-challenges` | Cloudflare challenges, supported browsers | `https://developers.cloudflare.com/cloudflare-challenges/reference/supported-browsers/` | 2026-10-11 |
| `litehtml` | litehtml | `github.com/litehtml/litehtml` | `4a651c5` |
| `libcss`, `libdom`, `libhubbub` | CSS, DOM and HTML parsing libraries | `github.com/netsurf-browser/<name>` | `499f1c4`, `f69781e`, `6651b8c` |
