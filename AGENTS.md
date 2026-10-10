# Agent instructions

## What this is

A design-stage project for native modern web browsing on big-box Zorro Amigas.
Nothing is built, and there is no code; the repository holds documents and an agent knowledge base in `.kb/`.

## Read order

1. `README.md`.
2. `.kb/_index.md`, then only the files its loading table names for your task.

Do not load all of `.kb/`.

## Precedence

The KB is self-standing: a statement stands on its primary-source citation.
Where a KB statement and its cited source disagree, the source wins; report the KB defect in an issue or pull request rather than resolving it silently.

## Labels, status and citations

| Label | Meaning | Must carry |
|---|---|---|
| `[F]` | Fact | A citation |
| `[G]` | Guess, estimate or inference | Its basis, where one exists |
| `[R]` | Recalled or reported, not verified here | What would verify it |
| `[D]` | Requirement from a decision | The DEC ID (`.kb/decisions.md`) |

The label opens the sentence and the citation closes it; a table cell carries one label per claim.

Each KB file opens with `Scope:` and `Status:` lines matching `.kb/_manifest.yaml`:

- `current`: every input was reviewed, and so was the synthesis.
- `draft`: every `[F]` was re-verified against its primary source at its pin, but the file's selection and synthesis have not had a separate design review.
  Treat its `[F]` as checked and its framing as provisional.
- `stale`: a cited source moved and the file has not been re-verified.

Citation forms (IDs and link templates in `.kb/sources.md`):

| Kind | Form | Example |
|---|---|---|
| Public repo | `id@commit:path:Lstart-Lend` | `fw@8778ef3:video_source_sync.v:L122-128` |
| Private repo | Same form; `sources.md` marks it not public | `replica@96bdef0` (netlist) |
| Document | ID, revision, table or page | `ds187` Table 18, p15 |
| Web page | ID with access date in `sources.md` | `myir-order` |
| KB-internal | Relative path and heading | `sections/display-coupling.md`, "R-TRIM" |

Pins are as-of: a citation is true at its pin, not necessarily at HEAD.
Before acting on a pinned line, re-check it at HEAD (`.kb/_index.md`, "Keeping pins current").

## Rules for agents that write here

- Never state a fact without a citation; an uncited claim is `[G]` or `[R]`, or it is left out.
- One sentence per line; tables over prose (`CONTRIBUTING.md`).
- IDs (DEC, K, DC, SR, E, f) are stable and never reused; retire, don't renumber.
- Update `.kb/_manifest.yaml` for every file touched.
- Don't paste datasheet or source-code text; cite the page or line range.
- Don't characterise anyone's intent or plans; cite what they shipped.
- No personal information about anyone.
- Commits and pull requests follow `CONTRIBUTING.md`.

## Searching

`.kb/` is a hidden directory.
Many search tools (ripgrep and tools built on it) skip hidden directories unless given the path explicitly or `--hidden` [R].
Search with `.kb/` as the path argument, e.g. `rg -n "K49" .kb/`.

## Answering a reader

Cite the KB file and the primary source behind it.
Keep `[G]`, `[R]` and `Status: draft` visible in the answer; do not upgrade a guess to a fact by restating it.
