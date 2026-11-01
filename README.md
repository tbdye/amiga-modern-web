# amiga-modern-web

Modern web browsing on big-box Zorro Amigas, in a Workbench window or full screen.

In the design under study, a separate SoC runs Chromium and sends its finished frames, uncompressed, to a Zynq-7000.
The Zynq overlays them on the Amiga's RTG display and keeps every role a ZZ9000 with its audio add-on has today: RTG, native video capture and scan doubling, audio and Ethernet.

The design under study stays on the Zynq-7000 family used by the MNT ZZ9000, so the existing [firmware](https://github.com/BlitterStudio/zz9000-firmware), FPGA logic and AmigaOS drivers carry over with additions rather than a rewrite.
The ZZ9000 Replica (not yet public), the proposed feature-enhanced ZZ9000, is the starting point for the circuit blocks.
Whether this ends up as one card, a Zynq card plus an off-the-shelf SBC, or a reworked Replica is still open.

## Status

RFC 0001 is open for comment in [#8](https://github.com/tbdye/amiga-modern-web/pull/8).
RFC 0002 takes another point of view: software first, on hardware people already have, with an unmodified browser on a Linux computer and its page shown in a native Amiga window.
The project is design only, and nothing has been built.

| Document | Path | State |
|---|---|---|
| Agent instructions; `CLAUDE.md` imports them | `AGENTS.md` | Current |
| Agent knowledge base: facts, decisions, unknowns and options, each labelled and cited | `.kb/` | v1; some files are `Status: draft` |
| RFC 0001: Native modern web browsing on Zorro Amigas | [#8](https://github.com/tbdye/amiga-modern-web/pull/8) | Open for comment |
| RFC 0002: A remote browser in a native Amiga window | `rfc/0002-remote-browser.md` | Draft |

## Taking part

Comments on an RFC go in its pull request; for RFC 0001, [#8](https://github.com/tbdye/amiga-modern-web/pull/8).
For a specific point, comment on that line in the **Files changed** tab; for something broader, comment on the conversation.
Changes come as pull requests too.
See [CONTRIBUTING.md](CONTRIBUTING.md) for how review and merging work here.

Maintained by Thomas Dye (@tbdye).

## Licence

No licence has been chosen yet.
I will choose one before any hardware design or code lands in this repository.
