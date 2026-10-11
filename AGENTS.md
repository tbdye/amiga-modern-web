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
Where a KB statement and its cited source disagree, the source wins.
Until an RFC merges here, no RFC draft is a KB source.
If you find an error in the KB, verify it against the primary source as it stands now (HEAD, for a repository), then fix it in a pull request that carries the evidence.
Open an issue instead only when the sources available to you cannot verify the error, or when the fix would change a decision rather than a fact.
A `[G]` is an error when its stated basis is wrong, its reasoning does not follow from the basis, or a primary source now settles the point; a different estimate alone is not an error.
The KB is the canonical record of the project's settled technical knowledge: a pull request from anyone is reviewed like any other.
Edit it here; there is no other copy to update first.

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
- `stale`: a cited fact is known or suspected to differ at HEAD and has not been re-verified.
  A cited source moving is not by itself a reason to mark a file `stale`.

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
Re-pin a citation only when its fact changed at HEAD; a line shift alone is not an error and is no reason to edit the citation.

## Rules for agents that write here

- Never state a fact without a citation; an uncited claim is `[G]` or `[R]`, or it is left out.
- Record durable facts: datasheet limits, pinouts, decisions and their status, architecture, manufacturer lifecycle commitments, which channels sell a part.
- Leave out any fact that changes faster than it is worth keeping correct, such as prices, stock counts, availability snapshots and open/closed states of upstream issues; they change often, and agents would spend their time correcting details that do not matter.
  When you find one, remove it rather than update it, and state the durable form instead, e.g. "MYIR sells the module direct" or "at CEF commit X, cefclient has Y".
- One sentence per line; tables over prose (`CONTRIBUTING.md`).
- IDs (DEC, K, DC, SR, E, f) are stable and never reused; retire, don't renumber.
- Update `.kb/_manifest.yaml` for every file touched.
- A change that adds a new subject adds its row to the loading table in `.kb/_index.md` in the same pull request.
- Keep each file within its size budget ("Size budgets").
- Don't paste datasheet or source-code text; cite the page or line range.
- Don't characterise anyone's intent or plans; cite what they shipped.
- No personal information about anyone: no names, handles or descriptions of individuals, except the maintainer's credit in `README.md` and owner segments of source URLs in `.kb/sources.md`.
- Never publish who holds a tool licence or must be asked about something, to-dos, review rounds, draft revision numbers or approvals, project schedules or estimates of how long work will take, build budgets or per-card cost estimates, local filesystem paths, project-tracking IDs that resolve only outside this repository, or verbatim quotes from private sources.
- Commits and pull requests follow `CONTRIBUTING.md`; a KB change goes on a `kb/<topic>` branch (or a fork) and opens a pull request against `main`; open it as a draft only while it is incomplete.

## Size budgets

Tokens are estimated as words × 1.35.

| File | Maximum tokens |
|---|---|
| `AGENTS.md` | 1,500 |
| `.kb/_index.md` | 1,200 |
| Each `.kb/sections/*.md` | 3,000 |
| Each `.kb/topics/*.md` | 5,000 |
| `.kb/unknowns.md` | 8,000 |
| Each other registry (`decisions.md`, `glossary.md`, `sources.md`) | 3,000 |

There is no budget for `.kb/` as a whole.
A typical answer loads `AGENTS.md`, `.kb/_index.md` and one section, under 6,000 tokens.

## Searching

`.kb/` is a hidden directory.
Many search tools (ripgrep and tools built on it) skip hidden directories unless given the path explicitly or `--hidden` [R].
Search with `.kb/` as the path argument, e.g. `rg -n "K49" .kb/`.

## Answering a reader

Cite the KB file and the primary source behind it.
Keep `[G]`, `[R]` and `Status: draft` visible in the answer; do not upgrade a guess to a fact by restating it.
