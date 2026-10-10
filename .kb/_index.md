# Knowledge base index

Scope: what the KB covers, which files to load for a task, and how pins are kept current.
Status: current

The KB holds the project's facts, decisions, open questions and rejected options for native modern web browsing on Zorro Amigas, each statement labelled and cited.
It describes the design under study; it does not argue for it.
Audio-path and power-domain depth, the Replica interconnect, prior art and agent-tooling traps are deferred to a later KB version.

## Load by task

Load `AGENTS.md` and this file first, then only what the task needs.

| Task | Load |
|---|---|
| Understand the project | `sections/overview.md`, then `sections/architecture.md` |
| Why the monitor never resyncs; lock times; when the window is black | `sections/display-coupling.md` |
| Run or report the monitor test (R-TRIM) | `sections/display-coupling.md`, "R-TRIM" |
| Pick or evaluate a Zynq part, package or module | `sections/zynq-and-board.md`, then `topics/zynq-pin-budget.md` |
| Pin or bank arithmetic | `topics/zynq-pin-budget.md`, `evidence/README.md` |
| Pick or evaluate a browser chip; EDID and colour | `sections/browser-chip.md` |
| Chromium/CEF frames, dialogs, audio tap | `topics/cef-frame-path.md` |
| Firmware or RTL changes; toolchain | `sections/firmware-and-rtl.md`, `sections/gotchas.md` |
| Safety of the browser plane | `topics/plane-safety.md` |
| Why an alternative was rejected or is not under study | `sections/options-rejected.md` |
| Why the browser chip does not drive the monitor | `sections/options-rejected.md` (P8), then `decisions.md` (DEC-013) |
| Prices and stock | `sections/sourcing.md` |
| What is open, and what settles it | `unknowns.md` |
| Why a rule exists | `decisions.md` |
| A code or term | `glossary.md` |
| Build a link from a citation | `sources.md` |

## Files

| File | Holds |
|---|---|
| `_manifest.yaml` | Per-file status, review date and cited sources; verified pins |
| `decisions.md` | DEC entries: rule, why, consequences, status |
| `unknowns.md` | K register, open design decisions (DC), freeze criteria, test methods, risks |
| `glossary.md` | Labels, terms, option codes, event codes E1-E22 |
| `sources.md` | Source IDs, visibility, link templates, pins, SHA-256 |
| `sections/` | Orientation; each read in one sitting |
| `topics/` | Depth; load only when the task needs it |
| `evidence/` | Pin-map data and the scripts that produced it |

## Keeping pins current

A citation is true at its pin forever; what goes stale is its truth at HEAD.
Pins move only through a deliberate re-verification:

1. For a source that moved, list KB citations to it, e.g. `rg -n "fw@" .kb/` (pass `.kb/` explicitly; it is hidden).
2. Run `git diff <old>..<new> --stat -- <cited paths>`.
   Unchanged paths: bump the pin in the citations and the manifest.
   Changed paths: re-derive each affected claim, since line numbers shift.
3. Record `verified_on` in `_manifest.yaml`.

For Linux and CEF, which have no local checkout here, confirm the commit exists at `https://github.com/<owner>/<repo>/commit/<sha>`; a 404 fails the pin.
Triggers: a firmware or driver release tag; a Replica revision the project relies on; any KB change that cites a source whose manifest pin is older than its HEAD.
