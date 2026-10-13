# ARM offload on the card

Scope: the ZZ9000's ARM services as the card is built: the mechanisms by which an Amiga program hands work to the ARM cores, the call path, how data moves, which core runs what, what a call costs, what the ARM side offers, and how the TLS offload is built.
Status: current

A citation with no source ID is `fw@cfbb910`; `drivers` citations are at `cb6a1c4`; `os/` expands per `sources.md`.
Every statement about what the firmware does or lacks is for `fw` at that commit.
What hosting a browser engine on these cores would take, and a third-party firmware line (XACP) that loads ARM programs: `topics/arm-hosted-engine.md`.
The firmware is bare metal, with no operating system: `sections/architecture.md`, "What each side runs".
Nothing was built or run for this page; a measured figure is its source's own.

## Mechanisms in the firmware

| Mechanism | State | Citation |
|---|---|---|
| SDK v2 mailbox, reached through `zz9k.library` | The call path for SDK services: one versioned, asynchronous interface | [F] `sdk/README.md:L20-24, L40` |
| Firmware-built services (core, memory, surface, image, codec, audio, crypto, diag, video) | Compiled into the firmware and dispatched by a fixed opcode switch; an unknown opcode returns `UNSUPPORTED` | [F] `os/sdk_service_catalog.h:L57-179`; `os/sdk_mailbox.c:L8317-8485` |
| Vendor and loadable services (`0x8000` and above) | An ID space and conventions only: no loader, no dynamic relocation, no plug-in ABI; no vendor opcode has a handler, and `0x8100` (JEDI) has no code under `os/` | [F] `sdk/docs/zz9k-modules.md:L7-9, L56-61`; `sdk/docs/zz9k-vendor-services.md:L3-8, L36-38`; `git grep` for `zz9k_service_registry`, `SERVICE_VENDOR` and `JEDI` over `os/` finds only `os/memorymap.h:L392-394` |
| Launcher that ran a raw ARM program on core 1 (`REG_ZZ_ARM_RUN`) | Removed by commit `350afc2`; the XACP line keeps it (`topics/arm-hosted-engine.md`) | [F] `os/core2.c:L412-418`; `os/main.c:L1704-1707`; `sdk/README.md:L22-24` |
| Hosted ARM applications | Named in a code comment; no code | [F] `os/core2.c:L412-418` |
| 68k code run on the ARM | A research track: a sandboxed function runner with a nine-instruction interpreter; AmigaOS traps, library calls and transparent process offload are outside it | [F] `sdk/docs/zz9k-68k-offload.md:L1-6, L15-36, L83-88` |

- [F] One SDK document says the JEDI renderer "ships as a loadable module" and another that packages "do not load modules dynamically"; the code matches the second (`sdk/docs/zz9k-vendor-services.md:L38`; `sdk/docs/zz9k-modules.md:L7-9`).
- [F] The firmware builds with `arm-none-eabi-gcc` and newlib, is packed by `bootgen` against the committed bitstream, and installs as `BOOT.bin` on the SD card (`BUILD.md:L11, L25, L182, L314-317`).
- [G] So a new service needs a firmware build, and no Vivado run.
- [F] A new opcode needs no `zz9k.library` change: `ZZ9KCall()` takes a request that the caller fills (`sdk/docs/zz9k-library.md:L257`).
- The firmware's licence: `sections/overview.md`, "Licences".

## Call path

1. [F] The 68k finds the board by AutoConfig, reads the mailbox address from registers `0x104` and `0x106`, and maps it inside the board window (`sdk/host/src/zz9k_host.c:L977-1022`; `sdk/include/zz9k/abi.h:L63-75`).
2. [F] The mailbox is a 128-byte descriptor, a request ring and a completion ring; a ring entry is 64 bytes, big-endian, with 48 bytes of inline payload (`sdk/include/zz9k/abi.h:L21-22, L1984-2031`).
3. [F] A ring holds 64 entries on Zorro III and 22 on Zorro II (`os/sdk_mailbox.h:L25`; `os/memorymap.h:L289`).
4. [F] The mailbox lives in card DDR that the 68k reads and writes directly: the PL turns Zorro memory cycles into AXI on its `m00` port, with no ARM code in the path, and the ARM maps the region non-cacheable (`os/memorymap.h:L282-288, L467-482`; `os/sdk_mailbox.c:L8514-8540`; `fw` commit `a30214c`, message).
5. [F] To submit, the 68k writes the entry as 16-bit words and then advances `request_tail` (`sdk/host/src/zz9k_host.c:L735-781, L3382-3425`).
6. [F] Default builds have no doorbell: `SDK_ENABLE_HDL_DOORBELL` is 0 and nothing in the tree sets it, so the capability bit is not advertised and the library writes none (`os/sdk_mailbox.h:L93-95, L107-111`; `sdk/host/src/zz9k_host.c:L1084-1085, L3419-3421`).
7. [F] Core 0 notices a request by polling the descriptor on every 256th idle pass of its main loop (`os/main.c:L2076-2077, L2243-2246`).
8. [F] The mailbox task runs the handler inline on core 0, or queues it for core 1 and posts the completion on a later pass (`os/sdk_mailbox.c:L8707-8824`; `os/scheduler_arm.c:L392-417`).
9. [F] A completion is an entry in the completion ring, plus an Amiga interrupt (INT6 by default, INT2 optional) when the client enabled it (`os/sdk_mailbox.c:L8822-8823`; `sdk/docs/zz9k-library.md:L1640-1649`).
10. [F] The 68k waits by spin-polling the ring, 500 spins between polls for the first 16 polls and then doubling to 50,000, or sleeps on the interrupt when a task that owns the context armed it; a shared-library or provider context must not arm it (`sdk/host/src/zz9k_host.c:L434-449, L644-724`; `sdk/docs/zz9k-library.md:L1651-1658`).

- [F] The only ARM-to-68k signals are completion entries and that interrupt: the core-1 worker touches only the task queue and a task's buffers, never Zorro, the mailbox, the doorbell or the display (`os/scheduler_arm.c:L237-238`).
- [G] So no path lets ARM code call 68k code.

## How data moves

| Region | Size | Visible to the 68k | Citation |
|---|---|---|---|
| Inline payload | 48 B per entry | Yes | [F] `sdk/include/zz9k/abi.h:L2009` |
| Shared heap (Zorro III) | 3.94 MiB (4,128,768 bytes), at most 32 buffers (`topics/decode-rates.md`, "What the card's ARM decodes today") | Yes, with no copy: a buffer's `data` pointer points into the board window | [F] `sdk/docs/zz9k-library.md:L206-209` |
| Host-window heap (Zorro II) | 16 KiB on current profiles (64 KiB legacy), shared by every client | Yes | [F] `sdk/docs/zz9k-zorro2-services.md:L25-39`; `os/memorymap.h:L91-93` |
| `CARD_ONLY` buffers and ARM-local surfaces | A 32 MiB surface heap | No; passed by handle | [F] `sdk/docs/zz9k-library.md:L296-302, L362-368`; `os/memorymap.h:L120-121` |
| The RTG framebuffer as a surface | | Yes; the ARM also draws into it | `sections/firmware-and-rtl.md`, "What the card offers today" |

- [G] A larger shared region is a firmware and driver allocation change, not a bus limit: the Zorro III board window is 128 MB (`sections/firmware-and-rtl.md`, "PS DDR map and card pool").
- [F] The wire format is big-endian by rule, and the little-endian ARM converts every field (`sdk/include/zz9k/abi.h:L1998-2001`; `get_be32` and `put_be32` in `os/sdk_mailbox.c`).
- [G] Any structure that both CPUs read in place pays that conversion on one side.

## Which core runs what

- [F] Core 0 is one polled loop: it answers every Zorro register cycle that the ARM serves (the FPGA withholds DTACK until it does, with no timeout), kicks a watchdog that resets the whole PS after about 12.9 s, and services the mailbox, the Ethernet state machine (every 10 ms) and the audio pump only on passes with no register request pending (`os/main.c:L818-819, L887-906, L2076-2077, L2191-2204`; `os/scheduler_arm.c:L464-467`; `os/watchdog.c:L8-10`).
- [F] So core 0 never runs long work: with core 1 down, a long task is failed, not run inline (`os/scheduler_arm.c:L456-485`).
- [F] Core 1 is one run-to-completion worker over a 16-slot queue that only core 0 fills; it sleeps on WFE when idle, and its loop has no preemption, time slice or priority (`os/scheduler.h:L16`; `os/scheduler_arm.c:L240-264`).
- [F] That one worker serves TLS crypto, decompression, image scaling and decode, MP3, FLAC and Vorbis, video and WebM decode, overlay compose and the AX audio refill (`os/scheduler.h:L21-79`; `os/sdk_mailbox.c:L8244-8248`).
- [F] A scale job whose source or destination is the live framebuffer or an ARM-local surface is computed inline on core 0, not handed to the worker (`os/sdk_mailbox.c:L2824-2848`).
- [G] A script task that runs for seconds would delay every one of those, card-side audio refill included; an engine service needs bounded slices or a scheduler change.
- [F] RTG scanout and native-video capture are PL masters with no ARM code in their data path (`sections/architecture.md`, "AXI ports in use today").
- [G] ARM work reaches them only through DDR contention; no source read records a case.
- [F] Two PL masters do contend with each other: the overlay VDMA shares HP0 with the desktop scanout and falls behind on a 1080p frame at 60 Hz (`fw` commit `9cf58ee`, message).
- [F] A core-1 fault fails the task in flight and cold-restarts the core; three consecutive faults disable core 1 (`os/core2.c:L91-146, L182-246`; `os/scheduler_arm.c:L105, L419-454`).
- [F] An Amiga reset re-initialises the mailbox and drops shared buffers, surfaces and sessions (`os/sdk_mailbox.c:L8576-8677`); what it does to the card pool: `sections/firmware-and-rtl.md`, "PS DDR map and card pool".

## Per-call cost

### Zorro III

- [F] The source of the round-trip rows names no bus, machine or CPU clock, only "the same 68060 hardware" (`sdk/docs/zz9k-crypto-acceleration.md:L83, L128`).
- [G] It was Zorro III: the same document carries `zz9k-cryptobench` results, and that tool cannot run its accelerated sections on Zorro II (`sdk/docs/zz9k-zorro2-services.md:L56-64`).

| Quantity | Value | Label and citation |
|---|---|---|
| Round-trip floor: submit and ring poll, the wait loop bypassed | 225-339 µs, average 279 µs | [F] `sdk/docs/zz9k-crypto-acceleration.md:L115-121` |
| `SDK ping`, synchronous, interrupt wait armed | 0.28 ms a call (3,342 calls a second) | [F] same file, `L128-132` |
| `SDK ping pipe`, 16 in flight, taken before the wait-loop fix | 11,193 calls a second; 1 ÷ 11,193 = 89 µs a call [G] | [F] same file, `L101-103`; `sdk/tools/zz9k-bench.c:L48` |
| Synchronous call with unarmed polling, which a shared-library context uses | Not reported; the polling is written to find a fast reply "within ~1 ms" | [F] same file, `L122-126`; `sdk/host/src/zz9k_host.c:L434-439` |
| Smallest-payload synchronous call that core 1 serves: 64 B of ChaCha20-Poly1305 | 64 B ÷ 162 KiB/s = 0.39 ms a call | [G] from [F] same file, `L144-145` |
| Bus cycles in one round trip with a 48-byte payload | 80 byte reads and 12-36 word writes, 92-116 cycles, plus 8 reads for each empty poll | [G] counted from `sdk/host/src/zz9k_host.c:L735-794, L3400-3421, L3501-3516`; `sdk/include/zz9k/abi.h:L1907-1912` |
| Bus time of one round trip | 92-116 × 0.569 µs = 52-66 µs, taking a byte read and a word write each to cost one longword read of card DDR | [G]; the 569 ns read: `topics/bus-and-card-rates.md`, "Bus ceilings" |
| 68k write rate into a shared buffer | Not recorded in `fw` or `drivers`; `zz9k-bench` has the probe ("CPU shared write", 16 KB and 256 KB) | [F] `sdk/tools/zz9k-bench.c:L43-47, L1028-1037`; a third-party figure on another firmware line: `topics/bus-and-card-rates.md`, "Bus ceilings" |
| USB mass storage, end to end, on "a Zorro III-capable Amiga", no CPU named | About 4 MB/s write and 3 MB/s read, given as a "historical baseline" | [F] `drivers@cb6a1c4:usb-poseidon/README.md:L25-27` |
| SD block I/O, polling, no machine named | A plateau around 1-2 MB/s: "most of the wall-clock time is polling" | [F] `drivers@cb6a1c4:sd-boot/README.md:L83-89` |

- The bus's read ceiling: `topics/bus-and-card-rates.md`, "Bus ceilings"; the TCP receive rates through the card: `topics/target-config-rates.md`, "Network receive".
- [G] The 279 µs floor is not bus time: the bus accounts for 52-66 µs of it, and the pipelined 89 µs a call is close to that.
- [G] The other 210-230 µs is unsplit; its contributors, none measured, are the firmware's discovery poll (every 256th idle pass), ARM handler and cache-maintenance time, the 68k's marshalling instructions and its own poll gap, and the armed 0.28 ms figure adds the interrupt wake.
- [G] A doorbell (the code path exists, off by default, `os/main.c:L2229-2242`) or a tighter poll would move the synchronous floor toward the pipelined figure.
- [F] The KiB/s figures of `zz9k-cryptobench` time the calls only, with the data already in shared buffers; they are not bus throughput (`sdk/tools/zz9k-cryptobench.c:L916-926, L1084`).
- [F] A 68060 copying out of the card's window "spent as much on instructions as on the bus" (`drivers` commit `6f45554`, message).
- [G] So an application's copy rate sits below the bus ceiling.

What the measured figures assume:

- [F] The 0.28 ms call is a ping, which core 0 answers inline (`os/sdk_mailbox.c:L8321-8324`); a service that runs on core 1 is queued, and its completion is posted on a later core-0 pass (`os/sdk_mailbox.c:L7128-7144, L8788-8801`; `os/scheduler_arm.c:L392-417`; `os/main.c:L2319`).
- [F] It was taken with the interrupt wait armed, which only a task that owns the context may do, and its source states no display mode or load (`sdk/docs/zz9k-crypto-acceleration.md:L122-128`; `sdk/docs/zz9k-library.md:L1651-1656`).
- [F] The sources flag slower replies under display load three times: a reply late "because the board is busy driving the display", a timeout setting "for hardware diagnosis under display/bus contention", and round trips that "under display load (core-0's completion poll starved) balloon" (`sdk/docs/zz9k-amissl-provider.md:L317-319, L329-332`; `sdk/amiga/provider/zz9k_aead.c:L203-208`).
- [G] A program that draws through core 0 continuously has its round trips in that regime; the size of the effect is unmeasured.

### Zorro II

Not established: neither repository holds a round-trip, read or write timing for Zorro II at the commits read.

- [F] The Zorro II mailbox exists only after the generation-2 aperture handshake; its rings are 22 entries and its host heap 16 KiB; the SDK's document says the wider matrix "is not yet physically qualified" (`os/sdk_mailbox.c:L8506-8513`; `os/memorymap.h:L289`; `sdk/docs/zz9k-zorro2-services.md:L25-28, L81-85`).
- [F] Diagnostics that allocate with the default flags fail on Zorro II (`sdk/docs/zz9k-zorro2-services.md:L56-70`).
- [G] A ping needs no shared buffer, so those failures do not bear on it.
- [G] On a 68000 to 68030 the marshalling code, not the bus, would dominate a call; the bus's ceiling: `topics/bus-and-card-rates.md`, "Bus ceilings".

## ARM-side capacity

| Item | Value | Citation |
|---|---|---|
| Cores, clock, DDR size | Two Cortex-A9 at 666 MHz, 1 GB | `sections/firmware-and-rtl.md`, "Why the Zynq cannot host the browser" |
| DDR type | DDR3 at 533 MHz | [F] `zz9000_project.tcl:L1206, L1208` |
| Caches | 32 KB instruction and 32 KB data L1 per core, a shared 512 KB L2; all on for both cores | [F] `ds190` p1; `os/scheduler_arm.c:L187-195` |
| Cost of a missing instruction cache | Core 1 without it ran tight decode loops about 10-30 times slower | [F] `os/scheduler_arm.c:L189-193` (the code comment's own measurement) |
| Float | VFP and NEON, hard-float ABI; enabled on core 1 | [F] `ZZ9000_proto.sdk/ZZ9000OS/Makefile:L24`; `os/core2.c:L355-367` |
| C library and build | newlib (picolibc is rejected); `-O2`, no unwind tables; no C++ compiler or source in the Makefile | [F] `ZZ9000_proto.sdk/ZZ9000OS/Makefile:L8, L13-15, L19, L104-108, L120` |
| Heap | One newlib heap for both cores, behind a recursive spinlock that masks local IRQs | [F] `os/sdk_smp_lock.c:L3-19`; `os/sdk_smp_lock_arm.c:L64-67`; its size: `sections/firmware-and-rtl.md`, "PS DDR map and card pool" |
| Code headroom | The image is under 3 MB before the heap, with about 25 MB left to grow | [F] `os/lscript.ld:L14-16` |
| Card pool and its class limits | 64 KB pages to owners in three classes | `sections/firmware-and-rtl.md`, "PS DDR map and card pool" |
| Stacks | Core 0: 16 KB, plus 1-2 KB per exception mode; core 1: 1 MB, plus 8 KB per exception mode | [F] `os/lscript.ld:L13, L19-23`; `os/memorymap.h:L409-410`; `os/core2.c:L310-314` |
| Scheduling | None beyond "Which core runs what" | |
| MMU | A flat identity map in 1 MB sections; every DDR section shareable, AP=11, domain 15; core 1 sets all domains to manager; one 4 KB page table exists, for the Zorro II mailbox page | [F] `os/mmu_page.c:L21-28`; `os/scheduler_arm.c:L178-181`; `os/memorymap.h:L282-288`; `docs/memory-map.md:L3` |
| Memory protection | None: section value `0x15de6` has bit 4 (XN) clear, so all DDR is writable and executable by all code | [G] from `os/mmu_page.c:L35` |
| Dynamic loader | None | [F] `sdk/docs/zz9k-modules.md:L56-61` |
| Threads | None: `git grep pthread` over `os/` finds nothing | [F] |
| TCP/IP on the ARM | None | `sections/architecture.md`, "Control link (K8)" |

- [F] Stateful services already exist in this shape: a session table and a decoder heap owned by core 1, fed by one task per call, with at most 4 audio streams and 1 video session (`os/scheduler.h:L44-74`; `os/sdk_mailbox.h:L1060, L1075`); image-session and surface limits: `topics/decode-rates.md`, "What the card's ARM decodes today".
- [F] Their large working memory comes from pool arenas tracked by owner, which the firmware reclaims on a fault or an Amiga reset (`docs/memory-map.md:L22-24`).

## How the TLS offload is built

| Property | Citation |
|---|---|
| The seam is a shared library that many programs already open, `amissl.library`; the provider is compiled inside it, so applications are unchanged | [F] `sdk/integration/amissl/README.md:L3-6, L14-17, L23-31` |
| With no board, or no crypto service, the provider advertises nothing and the library behaves as stock AmiSSL | [F] `sdk/docs/zz9k-amissl-provider.md:L293-301`; `drivers@cb6a1c4:amissl/README.md:L9-13` |
| Each algorithm is gated on its own firmware service flag, read through `QUERY_SERVICE` | [F] `sdk/docs/zz9k-amissl-provider.md:L87-93`; `sdk/docs/zz9k-vendor-services.md:L42-48` |
| Each operation falls back to software on a miss or a late reply (default budget 250 ms); X25519 alone is offload-or-fail | [F] `sdk/docs/zz9k-amissl-provider.md:L307-332` |
| Small work stays on the 68k: records under 2,048 B are not offloaded | [F] `sdk/amiga/provider/zz9k_aead.c:L57-59, L203-225` |
| Each call is coarse and carries all its inputs; the card keeps only scratch buffers between calls | [F] `sdk/docs/zz9k-crypto-acceleration.md:L20-36`; `sdk/docs/zz9k-amissl-provider.md:L94-97` |
| The software path matches the stock library: one HTTPS page fetched by a browser on a 68060 took 15.36 s with offload off and 15.18 s with stock AmiSSL | [F] `sdk/docs/zz9k-crypto-acceleration.md:L223-249` |
| The same fetch took 12.95 s with offload on; 15.36 − 12.95 = 2.4 s, 16% | [F] same lines |
| An environment variable disables offload without a rebuild | [F] `sdk/docs/zz9k-amissl-provider.md:L325-328` |
| Two CPU builds; the installer picks one and backs up the stock library | [F] `drivers@cb6a1c4:amissl/README.md:L24-29, L39-43` |
| The same shape serves `mpega.library`, a drop-in of the same name, and `zz9k-picture.datatype` | [F] `sdk/README.md:L36-38, L82` |

## Not established

Each point names what would settle it; none is a condition of anything.

- A round trip, a read rate or a write rate on Zorro II: only a Zorro II machine shows it.
- A round trip on a 68030 or 68040, armed or unarmed: only such a machine shows it; the round-trip figures under "Per-call cost" are from a 68060.
- A synchronous call with unarmed polling, the kind a shared library makes: no source reports one.
- How the 210-230 µs of the round-trip floor beyond bus time divides: the firmware's timing diagnostic times the handler only, so nothing records the discovery poll (`os/sdk_mailbox.c:L8779-8786`).
- The 68k's write rate into a shared buffer on `fw`: its bench tool has the probe, and no result is recorded.
- Round trips while RTG draws continuously, and the delay a long core-1 task adds to TLS, audio refill and video decode: only the card under that load shows them; DDR headroom is `unknowns.md`, K25.
- USB throughput on the release the drivers pair with: the source gives its figure as a historical baseline, not a result for that release.
