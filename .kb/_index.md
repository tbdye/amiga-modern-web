# Knowledge base index

Scope: what the KB covers and which files to load for a task.
Status: current

The KB holds the project's facts, decisions, open questions and rejected options for modern web browsing on Zorro Amigas, each statement labelled and cited.
It covers the design under study, a Zorro card whose Zynq shows the output of a separate browser chip (the design `README.md` describes), and facts that hold whichever approach is taken.
That design is one proposal; no approach is chosen [D] DEC-020, DEC-022.
The KB describes; it does not argue for any approach.
Agent-tooling traps (PDF and KiCad parsing) are deferred to a later KB version.

## Load by task

Load `AGENTS.md` and this file first, then only what the task needs.

### The project, and facts for any approach

| Task | Load |
|---|---|
| Understand the project; the operating system on each side | `sections/overview.md`, then `sections/architecture.md` for the design under study |
| Workbench look and feel: window, dialogs, downloads, clipboard, input, printing | `topics/look-and-feel.md`, then `decisions.md` (DEC-014) |
| What native feel means; where the gain in feel comes from | `topics/look-and-feel.md`, "What native feel means", then `sections/options-rejected.md` |
| Prior approaches | `topics/prior-art.md` (Amiga browsers, remote engines, Chromium forks, Speedometer); `topics/prior-art-remote-clients.md` (Amiga clients) |
| Published rates | `topics/target-config-rates.md` (receive, copy, pixel); `topics/bus-and-card-rates.md` (Zorro ceilings, scrolls); `topics/decode-rates.md` (68k, ARM) |
| Owner groups; what reaches each | `topics/audience.md` (stock ZZ9000, RTG cards, emulators); `topics/audience-pistorm.md` (PiStorm) |
| Page-pixel compression: lossless, JPEG, soft text | `topics/page-pixels.md`, then `topics/page-pixels-lossless.md`, `topics/page-pixels-lossy.md` |
| What sites resend when scrolled; updates a second at 50 MHz | `topics/scroll-redraw.md` |
| Option families A-D, the quality ceiling, other names (genlocked or line-locked V) | `glossary.md`, "Option families and the quality ceiling", "Other names for the same thing" |
| What is open, and what settles it | `unknowns.md`; for a page under the first heading, its "Not established" list |
| Is something decided? Why a rule exists | `decisions.md`, then the DC table in `unknowns.md` |
| Who decides; licences; fault policy | `sections/overview.md` |
| A code or term | `glossary.md` |
| Build a link from a citation | The file's own `## Sources` or `sources.md`, whichever defines the ID (search for it) |
| Check a pinned citation against HEAD | `sources.md`, "Pin checks" |
| Change the KB: fixing errors, writing rules, size budgets, review and merge | `AGENTS.md` ("Precedence", "Rules for agents that write here", "Size budgets"), then `CONTRIBUTING.md` |
| Review or audit the whole KB | Each file in "Files" in turn, not all in one load |
| Not recorded here by policy: schedules, effort, spend and costs, prices and stock, to-dos, who to ask, review history, licence holders | `AGENTS.md`, "Rules for agents that write here" |

### The design under study (the card)

| Task | Load |
|---|---|
| Which events resync the monitor (DEC-013 exemptions); lock times; when the window is black | `sections/display-coupling.md` |
| Run or report the monitor test (R-TRIM) | `sections/display-coupling.md`, "R-TRIM", then `topics/monitor-trim.md` |
| Latency definition and targets | `sections/architecture.md`, "Paths" |
| Pick or evaluate a Zynq part, package or module | `sections/zynq-and-board.md`, then `topics/zynq-pin-budget.md` |
| Swapping the Zynq module: BCLK, PUDC_B, module-supplied rails | `sections/gotchas.md` ("Modules and pins"), `topics/power-domains.md` |
| Pin or bank arithmetic; module footprint | `topics/zynq-pin-budget.md`, `evidence/README.md` |
| Replica board I/O: translators, bus mastering, headers, PS MIO, video slot, the VGA-USB add-on | `topics/replica-interconnect.md` |
| Pick or evaluate a browser chip; EDID and colour | `sections/browser-chip.md` |
| Chromium/CEF frames, dialogs, audio tap | `topics/cef-frame-path.md` |
| PCIe fetch or copy: link load, FIFO, pass thresholds | `topics/pcie-path.md` |
| Browsing on native (chipset) screens | `topics/native-screens.md` |
| Network: the browser chip's connection, the card's Ethernet, keeping the control link off the network | `topics/network.md`, then `sections/architecture.md`, "Control link (K8)" |
| TLS crypto offload; the Ethernet receive backlog | `sections/firmware-and-rtl.md`, "What the card offers today" |
| Security of the browser chip: threat model, patching, browser-chip image builds and updates, clipboard and download defaults | `topics/security.md` |
| Firmware or RTL changes; toolchain | `sections/firmware-and-rtl.md`, `sections/gotchas.md`, `sections/architecture.md` ("AXI ports in use today") |
| Power: slot limits, the Replica power tree, PSU-lead inlets, per-chip budgets (K35-K38); thermals (K18) | `topics/power-domains.md` |
| Audio: ADAU1701 clocks, the audio fabric, browser audio routes, A/V sync (K7, K32-K34) | `topics/audio-path.md` |
| PS DDR map, card pool and memory budgets | `sections/firmware-and-rtl.md`, "PS DDR map and card pool" |
| Safety of the browser plane | `topics/plane-safety.md` |
| Why an alternative was rejected or is not under study | `sections/options-rejected.md` |
| Why the browser chip does not drive the monitor | `sections/options-rejected.md` (P8), then `decisions.md` (DEC-013) |
| Sourcing channels and assembly | `sections/sourcing.md` |

## Files

| File | Holds |
|---|---|
| `_manifest.yaml` | Per-file status, `reviewed_on` (date of the last reviewed change to the file) and cited sources; verified pins |
| `decisions.md` | DEC entries: rule, why, consequences, status |
| `unknowns.md` | K register, open design decisions (DC), freeze criteria, test methods, risks |
| `glossary.md` | Labels, terms, option codes, event codes E1-E22 |
| `sources.md` | Source IDs, visibility, link templates, pins, SHA-256 |
| `sections/` | Orientation; each read in one sitting |
| `topics/` | Depth; load only when the task needs it |
| `evidence/` | Pin-map data and the scripts that produced it |
