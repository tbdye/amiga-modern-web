# Knowledge base index

Scope: what the KB covers, which files to load for a task, and how pins are kept current.
Status: current

The KB holds the project's facts, decisions, open questions and rejected options for native modern web browsing on Zorro Amigas, each statement labelled and cited.
It describes the design under study; it does not argue for it.
Audio-path and power-domain depth, the Replica interconnect, prior-art depth and agent-tooling traps are deferred to a later KB version.

## Load by task

Load `AGENTS.md` and this file first, then only what the task needs.

| Task | Load |
|---|---|
| Understand the project | `sections/overview.md`, then `sections/architecture.md` |
| Which events resync the monitor (DEC-013 exemptions); lock times; when the window is black | `sections/display-coupling.md` |
| Run or report the monitor test (R-TRIM) | `sections/display-coupling.md`, "R-TRIM", then `topics/monitor-trim.md` |
| Latency definition and targets | `sections/architecture.md`, "Paths" |
| Pick or evaluate a Zynq part, package or module | `sections/zynq-and-board.md`, then `topics/zynq-pin-budget.md` |
| Pin or bank arithmetic; Replica board I/O and module footprint | `topics/zynq-pin-budget.md`, `evidence/README.md` |
| Pick or evaluate a browser chip; EDID and colour | `sections/browser-chip.md` |
| Chromium/CEF frames, dialogs, audio tap | `topics/cef-frame-path.md` |
| PCIe fetch or copy: link load, FIFO, pass thresholds | `topics/pcie-path.md` |
| Workbench look and feel: window, dialogs, downloads, clipboard, input, printing | `topics/look-and-feel.md`, then `decisions.md` (DEC-014) |
| Browsing on native (chipset) screens | `topics/native-screens.md` |
| Network: the browser chip's connection, the card's Ethernet, keeping the control link off the network | `topics/network.md`, then `sections/architecture.md`, "Control link (K8)" |
| Security of the browser chip: threat model, patching, clipboard and download defaults | `topics/security.md` |
| Firmware or RTL changes; toolchain | `sections/firmware-and-rtl.md`, `sections/gotchas.md`, `sections/architecture.md` ("AXI ports in use today") |
| Power | `sections/architecture.md` ("Blocks"), `decisions.md` (DEC-003), `unknowns.md` (K35-K38) |
| Audio | `unknowns.md` (K7, K32-K34), `topics/cef-frame-path.md` ("Audio") |
| PS DDR map, card pool and memory budgets | `sections/firmware-and-rtl.md`, "PS DDR map and card pool" |
| Safety of the browser plane | `topics/plane-safety.md` |
| Why an alternative was rejected or is not under study; prior approaches | `sections/options-rejected.md` |
| Why the browser chip does not drive the monitor | `sections/options-rejected.md` (P8), then `decisions.md` (DEC-013) |
| Sourcing channels and assembly | `sections/sourcing.md` |
| What is open, and what settles it | `unknowns.md` |
| Is something decided? Why a rule exists | `decisions.md`, then the DC table in `unknowns.md` |
| Who decides; licences; fault policy | `sections/overview.md` |
| A code or term | `glossary.md` |
| Build a link from a citation | `sources.md` |
| Change the KB: fixing errors, writing rules, size budgets, review and merge | `AGENTS.md` ("Precedence", "Rules for agents that write here", "Size budgets"), then `CONTRIBUTING.md` |
| Review or audit the whole KB | Each file in "Files" in turn, not all in one load |

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

## Keeping pins current

A citation is true at its pin forever; what can change is its truth at HEAD.
Re-pin a citation only when its fact changed at HEAD; a line shift alone is no reason to edit it.
To check a source that moved:

1. List KB citations to it, e.g. `rg -n "fw@" .kb/` (pass `.kb/` explicitly; it is hidden).
2. Run `git diff <pin>..<HEAD> --stat -- <cited paths>`; a claim whose cited paths did not change needs no further check.
3. For each changed path, re-read each claim that cites it at HEAD.
   Fact unchanged, even if its lines moved: leave the citation at its pin.
   Fact changed: re-derive the claim and cite it at the new commit; until then, the file is `stale`.
4. Record the commit checked and its `verified_on` date under `pins` in `_manifest.yaml`.

A public-repo pin must exist on the public remote.
For fw and drivers, run `git fetch` in a clone, then `git branch -r --contains <commit>`; no branch listed fails the pin.
For Linux and CEF, which have no local checkout here, confirm the commit exists at `https://github.com/<owner>/<repo>/commit/<sha>`; a 404 fails the pin.
Triggers: a firmware or driver release tag; a Replica revision the project relies on; any KB change that cites a source whose manifest pin is older than its HEAD.
