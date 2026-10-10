# Contributing

Everything here changes through pull requests, including the RFCs.

## Commenting on an RFC

An RFC arrives as an open pull request and stays open while it is discussed.

| To | Do this |
|---|---|
| Comment on one point | Open the PR's **Files changed** tab and comment on that line. Each sentence sits on its own line, so a comment attaches to one sentence. |
| Propose wording | Use a suggestion block in the line comment. Only users with write access can apply it, and applying it adds a commit that dismisses earlier approvals. |
| Raise something broader | Comment on the PR conversation, or start a review that covers several lines. |
| Agree or block | Submit a review: approve, comment or request changes. |

The RFC merges once its threads are resolved and someone other than the author has approved it.
Later changes to a merged RFC come as new pull requests.

## Proposing a change

1. Create a branch, or fork if you don't have write access.
2. Open a pull request against `main`.
3. Get one approving review from someone other than the author.
4. Any contributor with write access may then merge it.

`main` is protected, so nothing lands without a pull request.
Pull requests are squash-merged, and the branch is deleted on merge.
The squash commit uses the pull request title and description, so write both carefully, with the title in the style below.
As repository owner I can bypass the protection for repository housekeeping.

## Writing documents

| Convention | Why |
|---|---|
| One sentence per line in the Markdown source | Review comments and diffs land on a single sentence. |
| Tables over prose where the content allows | Easier to compare options. |
| Mermaid diagrams are fine | GitHub renders them, and they diff as text. |
| Plain language | Readers know the Amiga well, so skip the sales pitch and explain the design. |
| Mark estimates as estimates | Keep measured or cited facts apart from guesses. |
| Cite sources | Datasheet and page, or repository, path and commit. |
| Changes to `AGENTS.md` and `.kb/` follow these same rules | The knowledge base is reviewed like any document; its labelling, citation and manifest rules are in `AGENTS.md`, "Rules for agents that write here". |

## Commit messages

A plain imperative sentence with a capital first letter and no trailing period.
No type prefixes such as `feat:` or `fix:`.

| Good | Not this |
|---|---|
| `Add HDMI receiver pin budget to RFC 0001` | `feat: add hdmi receiver pin budget` |
| `Fix NTSC line count in the timing table` | `fix(rfc): ntsc line count` |

## Licence

No licence has been chosen yet.
Comments and small edits are welcome now.
Before sending substantial material such as schematics, layouts or code, open an issue first, until a licence is in place.
