# Security of the browser chip

Scope: the threat model for the browser chip, what bounds it by design, the proposed defaults for what crosses to the Amiga, patching and update channels, and network exposure.
Status: draft

## Status

No security decision exists.
Every default, rule and placement below is a proposal (`[G]`, "Proposed"); the open questions are K71-K77 in `unknowns.md`.

## Threat model

[G] Assumption: a web page eventually takes over the browser chip, so everything the chip sends is hostile, replies included; the design question is what it can reach.
[F] Chromium's Linux sandbox uses a setuid helper everywhere, and namespaces and seccomp-BPF where the kernel supports them (`chromium-linux-sandbox`).
[G] So taking over the chip most likely needs a renderer bug plus a sandbox escape.

| From a compromised chip, it reaches | Impact [G] | Bounded by design | Not yet designed |
|---|---|---|---|
| Amiga or Zynq memory | Total | [G] No path: the chip has no bus access | — |
| The picture (HDMI) | Garbage or fake UI inside the browser window | [G] SR13-SR15 bound the input writer and timing; the A9 and the 68k, not the chip, enable and place the plane (SR2) | [G] Receiver DDC serving only the fixed EDID; CEC off (K77) |
| The ARM firmware, over the control link | Firmware takeover is close to Amiga takeover, because the firmware serves RTG and the Zorro interface | [G] SR16 rate-limits the link (`topics/plane-safety.md`) | Message format and size caps (K76); over Ethernet SR16's real bound is the GEM receive ring [R] |
| The 68k client, over the control link | A client bug takes the whole Amiga, because AmigaOS has no memory protection [R: the Exec documentation would verify it] | — | Parser rules (K76) |
| Clipboard into the Amiga | Malformed data reaches every clipboard reader | — | Limits (K72) |
| Downloads onto Amiga volumes | Overwritten system drawers (`S:`, `LIBS:`); hostile `.info` icons | — | Default and confinement (K73) |
| From the Amiga into the chip | Keystrokes typed in other windows; Amiga clipboard contents leaked to pages | — | Input only while the browser window has focus (K75) |
| The home LAN | Scans of, or attacks on, the router, NAS and printers | — | Placement (K70; "Network placement") |
| The chip's own storage | Persistence across reboots | — | K74 |

## Proposed rules on the chip

- [G] Proposed: Chromium's sandbox always on (never `--no-sandbox`).
- [G] Proposed: the browser never runs as root.
- [G] Proposed: a read-only root file system, A/B images and a wipeable profile, against persistence (K74).

## Proposed parser rules

[G] Proposed, for both the ARM firmware and the 68k client:

1. Everything from the chip is untrusted, replies included.
2. Every message has a fixed header (type, length); over-length messages are rejected before the body is read, and unknown types are dropped.
3. The chip never supplies pointers, offsets, paths or Amiga names.
4. Data is copied into a bounded buffer and validated (encoding; rectangles clamped to the window) before anything acts on it.
5. Chip-supplied strings never reach ARexx, `Execute()` or format strings.
6. Both parsers are fuzzed before release.

## Proposed crossing defaults

| Crossing | Proposed default [G] | Proposed limit [G] |
|---|---|---|
| Web → Amiga clipboard | Plain text only; the client converts it to Latin-1 IFF FTXT; images off | 64 KB |
| Amiga → web clipboard | Text, only when the user pastes | 64 KB |
| Downloads | Off by default; when on, each one confirmed, saved to one fixed drawer under a sanitised name (no `:`, `/` or `.info`), never auto-extracted or run | A user-set size cap |
| Uploads | The user picks each file in an ASL requester | — |

[D] DEC-014 requires downloads to go natively to the Amiga's file system; how far the proposed defaults above restrict that, including confinement to one drawer, is open (K73).

## Patching

Release policies [F]:

| Source | Policy |
|---|---|
| Chrome | A new milestone reaches the stable channel every two weeks, and weekly stable refreshes deploy security fixes (`chromium-release-cycle`) |
| Chrome extended stable | Every fourth milestone is kept for six more weeks with backported security fixes; the channel itself ships to enterprises on Windows and Mac only, while security fixes relevant to any platform land on the branch for embedders (`chromium-release-cycle`) |
| CEF stable branches | Broad security fixes for about two weeks after entering stable (`cef-branches`) |
| CEF extended branches | Every fourth Chromium milestone branch; broad security fixes for about eight weeks in total (`cef-branches`) |
| CEF long-term (LTC) branches | Every 12th Chromium milestone branch; only platform-agnostic security fixes, for about nine months in total (`cef-branches`) |
| CEF updates | Branch updates are manual, so CEF builds can lag Chromium releases (`cef-branches`) |
| Prebuilt CEF | Spotify's automated builder publishes CEF builds for supported branches (`cef-branches`), Linux x64 and ARM64 among its platforms (`cef-builds`) |
| Debian 13 | Recommends Chromium for general browsing and keeps it current by rebuilding upstream releases (`debian-13-relnotes`, §5.2.3.1); `chromium` is in its security suite for amd64 and arm64 (`debian-chromium`); it packages no CEF (`debian-contents`) |

- [G] A fix that lands upstream is public before it ships, so an image that is not updated is exposed to published, exploitable bugs soon after each release.
- [G] Pinning the measured browser versions (`unknowns.md`, "Risks") and patching at Chrome's cadence pull in opposite directions; automated re-measurement in CI reconciles them.

| Update channel | Who patches | For [G] | Against [G] |
|---|---|---|---|
| A. Distribution Chromium with unattended upgrades | The distribution | Free and automatic | No CEF, so no Amiga-native dialogs and menus (`topics/look-and-feel.md`); versions not measured |
| B. A project image on a CEF long-term branch, with signed A/B updates from project CI | The project | Measured versions; in-branch updates can be automated | A rebase to each new long-term branch; platform-agnostic fixes only, so Linux-only bugs may stay open; builds lag Chrome; needs a maintainer and a signing key indefinitely; if the project stops, every chip stops receiving updates |
| C. User build scripts | Each user | No infrastructure | Most users never rebuild |

- [G] Proposed default: B, with CI re-measuring each update, and the browser window warning when the image has gone a set period (proposed: four weeks) without one.
- Which channel, and who builds the image, is open (K71).

## Network placement

| Placement | LAN exposure [G] |
|---|---|
| Own port or Wi-Fi on the home LAN | The whole LAN |
| The same, with a firewall in the chip's image allowing only the internet, gateway and DNS | Small, but a root compromise can remove it |
| The user's guest network or a VLAN | Small, and enforced outside the chip |
| Through an on-card switch on the card's Ethernet port, untagged | The Amiga's segment: the chip reaches the Amiga's TCP/IP stack unless filtered |
| Through the Amiga's TCP/IP stack | The Amiga becomes the chip's gateway (rejected, `topics/network.md`) |

- [G] Proposed: the chip's own internet path, a LAN block in its image, and a guest network or VLAN recommended.
- [G] Proposed: the control link kept physically separate from the internet path; over the card's Ethernet port only with port isolation or VLANs (`topics/network.md`).
