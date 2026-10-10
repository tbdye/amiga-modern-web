# Evidence: MYIR module pin maps

Scope: what each file in `evidence/` is, how it was produced, and from what.
Status: draft

| File | What it is |
|---|---|
| `pm.py` | Probe: prints each PDF line with its glyph box, the x positions of the "odd even" pin-number pairs and the `J1`/`J2` labels, to find the column centre `cx` for `pm2.py`. Usage: `python pm.py <pdf> <cx>` |
| `pm2.py` | Extractor: reads page 1, takes pin numbers within `TOL` (default 14 pt) of `cx`, binds each odd pin to the nearest name on its left and each even pin to the nearest name on its right; sections restart at pin 1. Usage: `python pm2.py <pdf> <cx> <out.json> [TOL]` |
| `z15.json` | MYC-C7Z015 module: `{section: {pin: net name}}`, two sections of 140 pins |
| `z20.json` | MYC-C7Z010/20 module, same shape |

Section keys `1`/`2` follow the 7020 connector numbering (J1/J2); the 7015 PDF calls the same connectors J2/J3.
The scripts need PyMuPDF (`import fitz`).
No licence has been chosen for this repository yet, so the scripts are readable but carry no reuse grant.

## Inputs and reproduction

Both inputs are public MYIR PDFs (`sources.md`, `myir-7015-pinmap` and `myir-7020-pinout`, with SHA-256).

| Output | Command | Reproduces? (re-run 2026-10-08) |
|---|---|---|
| `z20.json` | `python pm2.py MYC-C7Z010_20_PinOuts.pdf 608 z20.json` | Yes, every entry |
| `z15.json` | `python pm2.py MYC-C7Z015_PINMAP.pdf 300 z15.json` | Yes, except ten entries the script does not emit: section 2 pins 114, 116, 120, 122, 126, 128, 132, 134, 138 and 140 (GTP lanes 1 and 3 TX/RX, and MGTREFCLK1) |

- The ten entries were added by hand when the file was made.
- [F] Each was re-derived on 2026-10-08 from the PDF's page-1 glyph rows: the even pin number and the name to its right share a row (`myir-7015-pinmap` p1; pins 114/116 MGTPTXP1/N1, 120/122 MGTPRXP1/N1, 126/128 MGTPTXP3/N3, 132/134 MGTPRXP3/N3, 138/140 MGTREFCLKP1/N1).
- [F] `z15.json` section 1 pin 136 reads `VBAT_KEY_BACK_1.` because the PDF prints the name cut short in its cell (`myir-7015-pinmap` p1, verified 2026-10-10 from the glyph row); the 7020 map names the same pin `VBAT_KEY_BACK_1.8V` (`z20.json`).
- The JSON files are stored with LF line endings; `pm2.py` run on Windows writes CRLF.
  Compare parsed JSON, not bytes.

## What relies on them

- `topics/zynq-pin-budget.md`: PL pins per bank, the 12 added bank-13 pins, GTP pins and reference clocks, clock-capable changes, spare MIO, the reset-pin naming.
- `sections/gotchas.md`: the BCLK pin losing clock capability on a 7015.
